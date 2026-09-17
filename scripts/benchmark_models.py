"""Model Benchmarking Script for Knowledge Graph Feature & Entity Extraction.

Evaluates available Ollama models on RTX 3050 Laptop GPU (6GB VRAM):
- qwen2.5:3b
- llama3.2:3b
- smollm2:1.7b
- llama3.2:1b
- qwen2.5:0.5b

Metrics:
- Inference Speed (Tokens / Sec)
- Total Latency (Seconds)
- JSON Adherence & Validity
- Entity & Relation Extraction Quality (Thai Comprehension)
"""

import json
import logging
import re
import sys
import time
from typing import Any
import httpx
from tabulate import tabulate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("benchmark")

OLLAMA_URL = "http://localhost:11434"

MODELS_TO_TEST = [
    "qwen2.5:3b",
    "llama3.2:3b",
    "smollm2:1.7b",
    "llama3.2:1b",
    "qwen2.5:0.5b"
]

TEST_PASSAGE = """
หมวดที่ 8 วินัยและการลงโทษทางวินัย (หน้า 30-31)
ข้อ 28 พนักงานทุกคนต้องปฏิบัติตามวินัยและข้อห้ามอย่างเคร่งครัด ดังนี้:
1. การมาสายเกิน 10 นาที โดยไม่มีเหตุผลอันควร
2. ละทิ้งหน้าที่การงาน หรือขาดงานติดต่อกันเกิน 3 วันทำงานโดยไม่มีเหตุผลอันสมควร
3. ดื่มสุรา หรือเสพสิ่งเสพติดในขณะปฏิบัติงาน หรือเข้ามาในบริเวณบริษัทขณะมึนเมา
4. เล่นการพนันทุกชนิดในสถานที่ทำงานของบริษัท
5. ทุจริตต่อหน้าที่ หรือกระทำความผิดอาญาโดยเจตนาแก่นายจ้าง
6. ทะเลาะวิวาทหรือทำร้ายร่างกายเพื่อนร่วมงานในบริเวณบริษัท

ข้อ 29 ลำดับขั้นการลงโทษทางวินัย มี 4 ขั้น:
ขั้นที่ 1 ตักเตือนด้วยวาจา โดยบันทึกเป็นหนังสือไว้เป็นหลักฐาน
ขั้นที่ 2 ตักเตือนเป็นหนังสือ (มีผลบังคับไม่เกิน 1 ปี)
ขั้นที่ 3 พักงานโดยไม่จ่ายค่าจ้าง (ระหว่างสอบสวนไม่เกิน 7 วัน)
ขั้นที่ 4 เลิกจ้างโดยไม่จ่ายค่าชดเชย (กรณีความผิดร้ายแรง เช่น ทุจริต หรือ ขาดงาน 3 วัน)
"""

SYSTEM_PROMPT = """คุณคือ AI ผู้เชี่ยวชาญการสกัดข้อมูลเป็น Knowledge Graph
จงสกัด Entity และ Relationship จากข้อความกฎระเบียบบริษัทที่กำหนดให้
ต้องตอบกลับในรูปแบบ JSON เท่านั้น โดยมีโครงสร้างดังนี้:
{
  "entities": [
    {"id": "id_1", "name": "ชื่อภาษาไทย", "type": "Misconduct | DisciplinaryPenalty | Severity"}
  ],
  "relations": [
    {"source": "id_1", "target": "id_2", "type": "SUBJECT_TO | HAS_SEVERITY"}
  ]
}
ห้ามใส่คำเกริ่นนำหรือ markdown formatting อื่นใด ให้ตอบเฉพาะ JSON ล้วนๆ"""


def benchmark_single_model(model_name: str) -> dict[str, Any]:
    logger.info(f"--- Benchmarking Model: {model_name} ---")

    payload = {
        "model": model_name,
        "prompt": f"ข้อความสำหรับสกัด:\n{TEST_PASSAGE}\n\nจงสกัด Entity และ Relationship เป็น JSON:",
        "system": SYSTEM_PROMPT,
        "format": "json",
        "stream": False,
        "options": {
            "temperature": 0.1,
            "top_p": 0.9,
        }
    }

    start_time = time.time()
    try:
        with httpx.Client(timeout=90.0) as client:
            res = client.post(f"{OLLAMA_URL}/api/generate", json=payload)
            elapsed = time.time() - start_time

            if res.status_code != 200:
                return {
                    "model": model_name,
                    "status": f"HTTP {res.status_code}",
                    "elapsed_sec": round(elapsed, 2),
                    "tokens_per_sec": 0,
                    "json_valid": False,
                    "entity_count": 0,
                    "relation_count": 0,
                    "thai_quality": "Failed",
                    "raw_output": res.text[:200]
                }

            data = res.json()
            raw_text = data.get("response", "").strip()

            # Metrics from Ollama
            eval_count = data.get("eval_count", 0)
            eval_duration_ns = data.get("eval_duration", 1)
            tps = round((eval_count / (eval_duration_ns / 1e9)), 1) if eval_duration_ns > 0 else 0.0

            # Attempt JSON parse
            json_valid = False
            entity_count = 0
            relation_count = 0
            parsed = None

            # Clean markdown codeblocks if present
            cleaned_json = re.sub(r"^```json\s*", "", raw_text, flags=re.MULTILINE)
            cleaned_json = re.sub(r"```$", "", cleaned_json, flags=re.MULTILINE).strip()

            try:
                parsed = json.loads(cleaned_json)
                json_valid = True
                entity_count = len(parsed.get("entities", []))
                relation_count = len(parsed.get("relations", []))
            except Exception:
                # Try finding first { and last }
                match = re.search(r"(\{.*\})", raw_text, re.DOTALL)
                if match:
                    try:
                        parsed = json.loads(match.group(1))
                        json_valid = True
                        entity_count = len(parsed.get("entities", []))
                        relation_count = len(parsed.get("relations", []))
                    except Exception:
                        pass

            # Evaluate Thai quality and relevance
            thai_quality = "ต่ำ"
            if json_valid and entity_count >= 5:
                sample_names = " ".join([e.get("name", "") for e in parsed.get("entities", [])])
                if any(kw in sample_names for kw in ["สาย", "สุรา", "การพนัน", "ทุจริต", "ตักเตือน", "เลิกจ้าง"]):
                    if relation_count >= 3:
                        thai_quality = "ยอดเยี่ยม (High)"
                    else:
                        thai_quality = "ดี (Medium)"
                else:
                    thai_quality = "ปานกลาง (Fair)"
            elif json_valid:
                thai_quality = "ปานกลาง (Low Entities)"

            return {
                "model": model_name,
                "status": "Success",
                "elapsed_sec": round(elapsed, 2),
                "tokens_per_sec": tps,
                "json_valid": json_valid,
                "entity_count": entity_count,
                "relation_count": relation_count,
                "thai_quality": thai_quality,
                "raw_output": raw_text[:300]
            }

    except Exception as e:
        return {
            "model": model_name,
            "status": f"Error: {str(e)}",
            "elapsed_sec": round(time.time() - start_time, 2),
            "tokens_per_sec": 0,
            "json_valid": False,
            "entity_count": 0,
            "relation_count": 0,
            "thai_quality": "Error",
            "raw_output": ""
        }


def run_benchmark():
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("\n=======================================================")
    print("🚀 เริ่มต้นรัน Benchmark โมเดลสำหรับ Knowledge Graph Feature Extraction")
    print("🎯 ฮาร์ดแวร์: Intel i5-13420H | 16GB RAM | RTX 3050 6GB Laptop GPU")
    print("=======================================================\n")

    results = []
    for model in MODELS_TO_TEST:
        res = benchmark_single_model(model)
        results.append(res)
        print(f"[{model}] {res['status']} | {res['elapsed_sec']}s | {res['tokens_per_sec']} tps | Entities: {res['entity_count']} | Relations: {res['relation_count']} | Quality: {res['thai_quality']}")

    table_data = []
    for r in results:
        table_data.append([
            r["model"],
            f"{r['elapsed_sec']} วินาที",
            f"{r['tokens_per_sec']} t/s",
            "ผ่าน (Valid)" if r["json_valid"] else "ล้มเหลว (Invalid)",
            r["entity_count"],
            r["relation_count"],
            r["thai_quality"]
        ])

    print("\n" + tabulate(
        table_data,
        headers=["Model", "Latency", "Speed (t/s)", "JSON Output", "Entities", "Relations", "Thai KG Quality"],
        tablefmt="github"
    ))

    # Save results to json
    with open("scripts/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n[OK] บันทึกผล Benchmark ลงที่ 'scripts/benchmark_results.json' เรียบร้อยแล้ว")


if __name__ == "__main__":
    run_benchmark()
