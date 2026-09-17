"""Vector Store and Retrieval Engine for HR Regulations.

Supports:
1. Hybrid Search: Dense FAISS (bge-m3) + Sparse BM25 (BM25Okapi)
2. Fusion Algorithms: Reciprocal Rank Fusion (RRF) & Relative Score Fusion (Convex Combination)
3. Small-to-Big Parent Document Retrieval
4. Structured Table Integration
5. Cross-Encoder / Relevance Re-ranking
"""

import json
import logging
import pickle
import re
from pathlib import Path
from typing import Any, Literal
import numpy as np

from src.config import settings
from src.vector.chunker import TextChunk, DocumentChunker
from src.vector.loader import PDFDocumentLoader
from src.vector.embeddings import OllamaEmbeddingClient
from src.vector.reranker import HRReranker

logger = logging.getLogger(__name__)


def thai_tokenize(text: str) -> list[str]:
    """Tokenizes Thai text into words and character 3-grams for high-recall BM25 matching."""
    text_lower = text.lower()
    # Word/alphanumeric tokens
    words = re.findall(r"[\w\u0E00-\u0E7F]+", text_lower)
    # Character 3-grams for Thai subword/compound matching
    ngrams = [
        text_lower[i : i + 3]
        for i in range(len(text_lower) - 2)
        if not re.search(r"\s", text_lower[i : i + 3])
    ]
    return words + ngrams[:60]


class HRVectorStore:
    """Vector storage, hybrid search, and parent-document retrieval engine."""

    def __init__(
        self,
        store_dir: Path | str | None = None,
        backend: Literal["faiss", "bm25", "hybrid"] | None = None,
        embedding_model: str | None = None,
        enable_hybrid: bool | None = None,
    ):
        if store_dir is None:
            self.store_dir = settings.DATA_DIR / "vector_store"
        else:
            self.store_dir = Path(store_dir)

        self.store_dir.mkdir(parents=True, exist_ok=True)
        self.backend: str = backend or getattr(settings, "VECTOR_INDEX_BACKEND", "faiss")
        self.model_name: str = embedding_model or settings.EMBEDDING_MODEL_NAME
        self.enable_hybrid = (
            enable_hybrid if enable_hybrid is not None
            else getattr(settings, "ENABLE_HYBRID_SEARCH", True)
        )

        self.model_slug = re.sub(r"[^\w\-]", "_", self.model_name)

        # File paths
        self.metadata_file = self.store_dir / "hr_chunks.json"
        self.parents_file = self.store_dir / "hr_parents.json"
        self.bm25_file = self.store_dir / "hr_bm25.pkl"
        self.faiss_file = self.store_dir / f"hr_faiss_{self.model_slug}.index"

        self.chunks: list[TextChunk] = []
        self.parents_map: dict[str, TextChunk] = {}

        # Search components
        self.bm25_index: Any = None
        self.faiss_index: Any = None
        self.embed_client = OllamaEmbeddingClient(model_name=self.model_name)
        self.reranker = HRReranker()

        if self.is_persisted():
            self.load()

    def is_persisted(self) -> bool:
        """Returns True if persisted vector index files exist on disk."""
        if not self.metadata_file.exists():
            return False
        if self.enable_hybrid:
            return self.faiss_file.exists() and self.bm25_file.exists()
        if self.backend == "faiss":
            return self.faiss_file.exists()
        return self.bm25_file.exists()

    def build_index_from_pdf(self) -> int:
        """Extracts PDF, performs Small-to-Big chunking, builds FAISS + BM25 indices, and saves."""
        logger.info("Extracting pages from PDF...")
        loader = PDFDocumentLoader()
        pages = loader.load_pages()

        logger.info("Chunking pages with Small-to-Big and Table structuring...")
        chunker = DocumentChunker()
        self.chunks, self.parents_map = chunker.chunk_pages(pages)

        corpus = [c.text for c in self.chunks]

        # Always build both for Hybrid capability
        self._build_faiss_index(corpus)
        self._build_bm25_index(corpus)

        self.save()
        logger.info(
            f"Successfully built and persisted index with {len(self.chunks)} chunks "
            f"and {len(self.parents_map)} parents."
        )
        return len(self.chunks)

    def _build_faiss_index(self, corpus: list[str]) -> None:
        """Builds dense FAISS IndexFlatIP (Cosine Similarity) with embeddings."""
        import faiss

        logger.info(f"Generating dense embeddings for {len(corpus)} chunks via {self.model_name}...")
        vectors = self.embed_client.embed_documents(corpus, batch_size=16, normalize=True)
        dim = vectors.shape[1]

        logger.info(f"Creating FAISS IndexFlatIP (dim={dim}, count={len(vectors)})...")
        self.faiss_index = faiss.IndexFlatIP(dim)
        self.faiss_index.add(vectors)

    def _build_bm25_index(self, corpus: list[str]) -> None:
        """Builds sparse BM25Okapi index with Thai tokenization."""
        from rank_bm25 import BM25Okapi

        logger.info(f"Building BM25Okapi index for {len(corpus)} chunks...")
        tokenized_corpus = [thai_tokenize(doc) for doc in corpus]
        self.bm25_index = BM25Okapi(tokenized_corpus)

    def save(self) -> None:
        """Saves indices and chunk metadata to disk."""
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.chunks], f, ensure_ascii=False, indent=2)

        with open(self.parents_file, "w", encoding="utf-8") as f:
            json.dump({k: v.to_dict() for k, v in self.parents_map.items()}, f, ensure_ascii=False, indent=2)

        import faiss
        if self.faiss_index is not None:
            faiss.write_index(self.faiss_index, str(self.faiss_file))
            logger.info(f"Saved FAISS index to {self.faiss_file}")

        if self.bm25_index is not None:
            with open(self.bm25_file, "wb") as f:
                pickle.dump(self.bm25_index, f)
            logger.info(f"Saved BM25 index to {self.bm25_file}")

    def load(self) -> None:
        """Loads indices and chunks metadata from disk."""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                raw_chunks = json.load(f)
                self.chunks = [TextChunk(**c) for c in raw_chunks]

        if self.parents_file.exists():
            with open(self.parents_file, "r", encoding="utf-8") as f:
                raw_parents = json.load(f)
                self.parents_map = {k: TextChunk(**v) for k, v in raw_parents.items()}

        import faiss
        if self.faiss_file.exists():
            self.faiss_index = faiss.read_index(str(self.faiss_file))
            logger.info(f"Loaded FAISS index ({self.faiss_index.ntotal} vectors) from {self.faiss_file}")

        if self.bm25_file.exists():
            with open(self.bm25_file, "rb") as f:
                self.bm25_index = pickle.load(f)
            logger.info(f"Loaded BM25 index from {self.bm25_file}")

    def search(
        self,
        query: str,
        top_k: int = 4,
        include_parents: bool | None = None,
        fusion_method: Literal["rrf", "convex"] = "rrf"
    ) -> list[dict[str, Any]]:
        """Searches vector index with Hybrid Search, Re-ranking, and Small-to-Big Retrieval."""
        if not self.chunks or (self.faiss_index is None and self.bm25_index is None):
            if self.is_persisted():
                self.load()
            else:
                self.build_index_from_pdf()

        # Decide search mode
        if self.enable_hybrid and self.faiss_index is not None and self.bm25_index is not None:
            candidates = self._search_hybrid(query, candidate_k=15, fusion_method=fusion_method)
        elif self.backend == "faiss" and self.faiss_index is not None:
            candidates = self._search_faiss_raw(query, candidate_k=15)
        else:
            candidates = self._search_bm25_raw(query, candidate_k=15)

        # Apply Re-ranking
        reranked = self.reranker.rerank(query, candidates, top_k=top_k)

        # Apply Small-to-Big Context Expansion if enabled
        expand_parents = (
            include_parents if include_parents is not None
            else getattr(settings, "ENABLE_PARENT_RETRIEVAL", True)
        )

        if expand_parents and self.parents_map:
            results = []
            seen_parents = set()
            for item in reranked:
                parent_id = item.get("parent_id")
                if parent_id and parent_id in self.parents_map and parent_id not in seen_parents:
                    parent = self.parents_map[parent_id]
                    seen_parents.add(parent_id)
                    results.append({
                        "score": item["score"],
                        "chunk_id": parent.chunk_id,
                        "child_chunk_id": item["chunk_id"],
                        "page_number": parent.page_number,
                        "chapter": parent.chapter,
                        "section_title": parent.section_title or item.get("section_title"),
                        "text": parent.text,
                        "is_table": parent.is_table or item.get("is_table", False)
                    })
                elif not parent_id or parent_id in seen_parents:
                    if item["chunk_id"] not in seen_parents:
                        results.append(item)
                        seen_parents.add(item["chunk_id"])
            return results[:top_k]

        return reranked

    def _search_faiss_raw(self, query: str, candidate_k: int = 15) -> list[dict[str, Any]]:
        """Direct FAISS search returning raw candidates."""
        query_vec = self.embed_client.embed_query(query, normalize=True)
        query_mat = query_vec.reshape(1, -1).astype(np.float32)
        k = min(candidate_k, self.faiss_index.ntotal)
        scores, indices = self.faiss_index.search(query_mat, k)

        candidates = []
        for score, idx in zip(scores[0], indices[0]):
            if 0 <= idx < len(self.chunks):
                chunk = self.chunks[idx]
                candidates.append({
                    "score": round(float(score), 4),
                    "chunk_id": chunk.chunk_id,
                    "page_number": chunk.page_number,
                    "chapter": chunk.chapter,
                    "section_title": chunk.section_title,
                    "parent_id": chunk.parent_id,
                    "is_table": chunk.is_table,
                    "text": chunk.text
                })
        return candidates

    def _search_bm25_raw(self, query: str, candidate_k: int = 15) -> list[dict[str, Any]]:
        """Direct BM25 search returning raw candidates."""
        tokenized_query = thai_tokenize(query)
        scores = self.bm25_index.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:candidate_k]

        candidates = []
        for idx in top_indices:
            score = float(scores[idx])
            chunk = self.chunks[idx]
            candidates.append({
                "score": round(score, 4),
                "chunk_id": chunk.chunk_id,
                "page_number": chunk.page_number,
                "chapter": chunk.chapter,
                "section_title": chunk.section_title,
                "parent_id": chunk.parent_id,
                "is_table": chunk.is_table,
                "text": chunk.text
            })
        return candidates

    def _search_hybrid(
        self,
        query: str,
        candidate_k: int = 15,
        fusion_method: Literal["rrf", "convex"] = "rrf",
        dense_weight: float = 0.65,
        sparse_weight: float = 0.35,
    ) -> list[dict[str, Any]]:
        """Executes Hybrid Search combining Dense (FAISS) and Sparse (BM25)."""
        dense_hits = self._search_faiss_raw(query, candidate_k=candidate_k)
        sparse_hits = self._search_bm25_raw(query, candidate_k=candidate_k)

        if fusion_method == "convex":
            # Relative Score Fusion / Convex Combination:
            # Score(d) = alpha * DenseNorm(d) + (1-alpha) * SparseNorm(d)
            dense_max = max((h["score"] for h in dense_hits), default=1.0) or 1.0
            dense_min = min((h["score"] for h in dense_hits), default=0.0)
            dense_range = max(dense_max - dense_min, 1e-6)

            sparse_max = max((h["score"] for h in sparse_hits), default=1.0) or 1.0
            sparse_min = min((h["score"] for h in sparse_hits), default=0.0)
            sparse_range = max(sparse_max - sparse_min, 1e-6)

            combined_scores: dict[str, float] = {}
            chunk_lookup: dict[str, dict[str, Any]] = {}

            for item in dense_hits:
                cid = item["chunk_id"]
                norm_score = (item["score"] - dense_min) / dense_range
                combined_scores[cid] = combined_scores.get(cid, 0.0) + (dense_weight * norm_score)
                chunk_lookup[cid] = item

            for item in sparse_hits:
                cid = item["chunk_id"]
                norm_score = (item["score"] - sparse_min) / sparse_range
                combined_scores[cid] = combined_scores.get(cid, 0.0) + (sparse_weight * norm_score)
                if cid not in chunk_lookup:
                    chunk_lookup[cid] = item

            sorted_cids = sorted(combined_scores.keys(), key=lambda k: combined_scores[k], reverse=True)
            fused_candidates = []
            for cid in sorted_cids[:candidate_k]:
                cand = dict(chunk_lookup[cid])
                cand["score"] = round(combined_scores[cid], 4)
                fused_candidates.append(cand)
            return fused_candidates

        # Default: Reciprocal Rank Fusion (RRF) with constant k=60
        rrf_constant = 60
        rrf_scores: dict[str, float] = {}
        chunk_lookup: dict[str, dict[str, Any]] = {}

        for rank, item in enumerate(dense_hits, start=1):
            cid = item["chunk_id"]
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (dense_weight / (rrf_constant + rank))
            chunk_lookup[cid] = item

        for rank, item in enumerate(sparse_hits, start=1):
            cid = item["chunk_id"]
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (sparse_weight / (rrf_constant + rank))
            if cid not in chunk_lookup:
                chunk_lookup[cid] = item

        sorted_cids = sorted(rrf_scores.keys(), key=lambda k: rrf_scores[k], reverse=True)
        fused_candidates = []
        for cid in sorted_cids[:candidate_k]:
            cand = dict(chunk_lookup[cid])
            cand["score"] = round(rrf_scores[cid] * 20.0, 4)
            fused_candidates.append(cand)

        return fused_candidates


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("[*] Re-building and testing HRVectorStore with FAISS + BM25 Hybrid Search...")
    store = HRVectorStore()
    count = store.build_index_from_pdf()
    print(f"[OK] Index built with {count} chunks.")

    test_q = "พนักงานระดับ 3 มีสิทธิ์ลาพักร้อนกี่วัน"
    print(f"\nSearching: '{test_q}'")
    hits = store.search(test_q, top_k=3)
    for h in hits:
        print(f"\n[Score: {h['score']}] หน้า {h['page_number']} ({h['chapter']}):")
        print(h['text'][:200] + "...")
