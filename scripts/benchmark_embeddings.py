"""Empirical Benchmark Script for Embedding Models on Thai HR Regulations.

Compares:
1. TF-IDF (Baseline char_wb 3-5)
2. all-minilm (384d)
3. nomic-embed-text (768d)
4. bge-m3 (1024d)

Metrics:
- Top-1 Hit Rate (%)
- Top-3 Hit Rate (%)
- Mean Reciprocal Rank (MRR)
- Average Query Latency (ms)
- Indexing Time (sec)
"""

import json
import logging
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("benchmark")

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.vector.loader import PDFDocumentLoader
from src.vector.chunker import DocumentChunker
from src.vector.store import HRVectorStore

# 10 Representative Ground-Truth Queries across the 12 Chapters
BENCHMARK_DATASET = [
    {
        "id": "Q1",
        "query": "พนักงานระดับ 3 มีสิทธิ์ลาพักร้อนกี่วัน",
        "category": "สิทธิวันลา (ภาษาพูด)",
        "target_pages": {17, 18},
        "target_chapter": "วันลา",
    },
    {
        "id": "Q2",
        "query": "การจ่ายเงินชดเชยการเลิกจ้าง",
        "category": "การเลิกจ้าง (คีย์เวิร์ดตรง)",
        "target_pages": {33, 34, 35, 36},
        "target_chapter": "เลิกจ้าง",
    },
    {
        "id": "Q3",
        "query": "กองทุนสำรองเลี้ยงชีพ",
        "category": "สวัสดิการ (คำเฉพาะ/ย่อ)",
        "target_pages": {37, 38, 39, 40, 41},
        "target_chapter": "ผลประโยชน์และสวัสดิการ",
    },
    {
        "id": "Q4",
        "query": "ท้อง ลาคลอดได้กี่วัน ได้รับค่าจ้างไหม",
        "category": "วันลาคลอด (ภาษาพูด/เงื่อนไข)",
        "target_pages": {15, 16},
        "target_chapter": "วันลา",
    },
    {
        "id": "Q5",
        "query": "ขาดงานติดต่อกัน 3 วัน ถือเป็นความผิดร้ายแรงหรือไม่ เลิกจ้างได้ไหม",
        "category": "วินัยและการเลิกจ้าง (ประโยคยาว/เงื่อนไข)",
        "target_pages": {27, 28, 29, 30, 34, 35},
        "target_chapter": "วินัย",
    },
    {
        "id": "Q6",
        "query": "ทำงานล่วงเวลา โอที วันหยุด ได้ค่าตอบแทนอย่างไร",
        "category": "ค่าล่วงเวลา (ภาษาพูด/คำย่อ)",
        "target_pages": {19, 20},
        "target_chapter": "ล่วงเวลา",
    },
    {
        "id": "Q7",
        "query": "ระยะเวลาทดลองงานกี่วัน",
        "category": "การจ้างงาน (คำถามสั้น)",
        "target_pages": {7, 8, 9, 10},
        "target_chapter": "การว่าจ้าง",
    },
    {
        "id": "Q8",
        "query": "หนังสือเตือนมีอายุกี่ปี เมื่อไหร่ถึงหมดผล",
        "category": "โทษทางวินัย (ระเบียบเวลา)",
        "target_pages": {24, 25, 26},
        "target_chapter": "วินัย",
    },
    {
        "id": "Q9",
        "query": "เงินช่วยเหลืองานศพ ครอบครัวพนักงานเสียชีวิต เบิกได้เท่าไหร่",
        "category": "สวัสดิการ (กรณีเฉพาะ)",
        "target_pages": {38, 39, 40},
        "target_chapter": "ผลประโยชน์และสวัสดิการ",
    },
    {
        "id": "Q10",
        "query": "ขั้นตอนการร้องทุกข์ของพนักงาน",
        "category": "กระบวนการร้องทุกข์ (โครงสร้างขั้นตอน)",
        "target_pages": {31, 32},
        "target_chapter": "การร้องทุกข์",
    },
]


@dataclass
class BenchmarkResult:
    model_name: str
    backend: str
    dimension: int
    indexing_time_sec: float
    avg_latency_ms: float
    top1_hit_rate: float
    top3_hit_rate: float
    mrr: float
    query_details: list[dict[str, Any]]


def run_benchmark_for_model(name: str, backend: str, embedding_model: str | None = None) -> BenchmarkResult:
    logger.info(f"\n{'='*60}\nRunning Benchmark: {name} (Backend: {backend})\n{'='*60}")
    
    # Dedicated benchmark store dir to avoid cache conflict
    bench_dir = Path("data/benchmark_stores") / name.replace(":", "_").replace("-", "_")
    bench_dir.mkdir(parents=True, exist_ok=True)

    store = HRVectorStore(
        store_dir=bench_dir,
        backend=backend,
        embedding_model=embedding_model or "bge-m3",
    )

    # 1. Measure Indexing Time
    t0 = time.perf_counter()
    num_chunks = store.build_index_from_pdf()
    indexing_time = time.perf_counter() - t0
    logger.info(f"[{name}] Index built with {num_chunks} chunks in {indexing_time:.2f}s")

    # Detect dimension
    if backend == "faiss" and store.faiss_index is not None:
        dim = store.faiss_index.d
    elif backend == "tfidf" and store.matrix is not None:
        dim = store.matrix.shape[1]
    else:
        dim = 0

    # 2. Warm up
    _ = store.search("ทดสอบ", top_k=2)

    # 3. Evaluate Queries
    top1_hits = 0
    top3_hits = 0
    reciprocal_ranks = []
    latencies = []
    query_details = []

    for item in BENCHMARK_DATASET:
        q = item["query"]
        target_pages = item["target_pages"]
        target_chapter = item["target_chapter"]

        t_start = time.perf_counter()
        hits = store.search(q, top_k=5)
        latency_ms = (time.perf_counter() - t_start) * 1000.0
        latencies.append(latency_ms)

        # Check ranks
        rank_found = 0
        hit_details = []
        for i, h in enumerate(hits, start=1):
            is_match = (h["page_number"] in target_pages) or (target_chapter in h["chapter"])
            hit_details.append({
                "rank": i,
                "score": h["score"],
                "page": h["page_number"],
                "chapter": h["chapter"],
                "is_match": is_match,
                "snippet": h["text"][:80].replace("\n", " ")
            })
            if is_match and rank_found == 0:
                rank_found = i

        if rank_found == 1:
            top1_hits += 1
        if 1 <= rank_found <= 3:
            top3_hits += 1

        rr = 1.0 / rank_found if rank_found > 0 else 0.0
        reciprocal_ranks.append(rr)

        query_details.append({
            "id": item["id"],
            "query": q,
            "category": item["category"],
            "rank_found": rank_found if rank_found > 0 else None,
            "latency_ms": round(latency_ms, 2),
            "hits": hit_details[:3]
        })

    n = len(BENCHMARK_DATASET)
    avg_latency = sum(latencies) / n
    top1_rate = (top1_hits / n) * 100.0
    top3_rate = (top3_hits / n) * 100.0
    mrr = sum(reciprocal_ranks) / n

    result = BenchmarkResult(
        model_name=name,
        backend=backend,
        dimension=dim,
        indexing_time_sec=round(indexing_time, 2),
        avg_latency_ms=round(avg_latency, 2),
        top1_hit_rate=round(top1_rate, 1),
        top3_hit_rate=round(top3_rate, 1),
        mrr=round(mrr, 4),
        query_details=query_details
    )

    logger.info(
        f"[{name}] Results: Top-1={result.top1_hit_rate}%, Top-3={result.top3_hit_rate}%, "
        f"MRR={result.mrr}, Avg Latency={result.avg_latency_ms}ms"
    )
    return result


def main():
    print("🚀 Starting Embedding Model & FAISS Benchmark on Thai HR Regulations...\n")

    models_to_test = [
        ("TF-IDF (Baseline)", "tfidf", None),
        ("all-minilm (FAISS)", "faiss", "all-minilm"),
        ("nomic-embed-text (FAISS)", "faiss", "nomic-embed-text"),
        ("bge-m3 (FAISS)", "faiss", "bge-m3"),
    ]

    all_results: list[BenchmarkResult] = []

    for label, backend, embed_model in models_to_test:
        try:
            res = run_benchmark_for_model(label, backend, embed_model)
            all_results.append(res)
        except Exception as e:
            logger.error(f"Error evaluating {label}: {e}", exc_info=True)

    # Save results as JSON
    output_json = Path("docs") / "embedding_benchmark_results.json"
    output_json.parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump([r.__dict__ for r in all_results], f, ensure_ascii=False, indent=2)

    print(f"\n✅ Benchmark completed! Results saved to {output_json}\n")

    # Print markdown summary table to stdout
    print("| โมเดล / Backend | มิติ (Dim) | Indexing Time (s) | Latency (ms) | Top-1 Hit (%) | Top-3 Hit (%) | MRR |")
    print("|---|---|---|---|---|---|---|")
    for r in all_results:
        print(f"| **{r.model_name}** | {r.dimension} | {r.indexing_time_sec}s | {r.avg_latency_ms} ms | **{r.top1_hit_rate}%** | **{r.top3_hit_rate}%** | **{r.mrr}** |")


if __name__ == "__main__":
    main()
