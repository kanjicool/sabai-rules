"""Re-ranker for HR Regulations RAG Candidates.

Re-scores and filters Top-N candidates from Hybrid Retrieval based on:
1. RRF / Base Similarity Score
2. Lexical Entity Overlap (job levels, numbers, disciplinary terms)
3. Table priority boost for numerical policy inquiries
4. Table of Contents (TOC) noise penalty
"""

import logging
import re
from typing import Any
from src.config import settings

logger = logging.getLogger(__name__)


class HRReranker:
    """Re-ranks retrieved chunk candidates to ensure highest factual precision."""

    def __init__(self, enabled: bool | None = None):
        self.enabled = (
            enabled if enabled is not None
            else getattr(settings, "ENABLE_RERANKING", True)
        )

    def rerank(
        self,
        query: str,
        candidates: list[dict[str, Any]],
        top_k: int = 4
    ) -> list[dict[str, Any]]:
        """Re-ranks candidates and returns the top_k most relevant chunks."""
        if not self.enabled or not candidates:
            return candidates[:top_k]

        scored_candidates: list[tuple[float, dict[str, Any]]] = []

        # Extract salient entities/numbers from query (e.g. 'ระดับ 3', '3 วัน', 'pvd', 'ลาคลอด')
        query_lower = query.lower()
        query_words = set(re.findall(r"[\w\u0E00-\u0E7F]+", query_lower))

        for cand in candidates:
            base_score = float(cand.get("score", 0.5))
            text = cand.get("text", "")
            text_lower = text.lower()
            page_num = cand.get("page_number", 0)
            is_table = cand.get("is_table", False)

            relevance_boost = 0.0

            # 1. Penalize Table of Contents (Pages 2-3 or snippets with high page number dots)
            if page_num == 3 or "สารบัญ" in text or "หมวดที่ เรื่อง หน้า" in text:
                relevance_boost -= 0.35

            # 2. Boost Structured Tables for policy/numerical queries
            if is_table:
                # If query asks about levels, severance, leave, or pvd
                if any(w in query_lower for w in ["ระดับ", "กี่วัน", "พักร้อน", "ชดเชย", "อายุงาน", "pvd", "สมทบ", "วินัย", "โทษ"]):
                    relevance_boost += 0.25

            # 3. Match Salient Numbers and Terms
            # Check for specific numbers mentioned in the query
            numbers_in_query = re.findall(r"\d+", query)
            for num in numbers_in_query:
                if num in text:
                    relevance_boost += 0.08

            # Check keyword presence in chunk
            matching_words = [w for w in query_words if len(w) > 2 and w in text_lower]
            keyword_ratio = len(matching_words) / max(len(query_words), 1)
            relevance_boost += (keyword_ratio * 0.15)

            final_score = round(base_score + relevance_boost, 4)
            scored_candidates.append((final_score, cand))

        # Sort descending by re-ranked score
        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        reranked_results = []
        for final_score, cand in scored_candidates[:top_k]:
            updated_cand = dict(cand)
            updated_cand["score"] = final_score
            reranked_results.append(updated_cand)

        return reranked_results


if __name__ == "__main__":
    reranker = HRReranker()
    sample_candidates = [
        {"score": 0.55, "page_number": 3, "text": "สารบัญ หมวด 10 การจ่ายเงินชดเชย หน้า 33", "is_table": False},
        {"score": 0.52, "page_number": 35, "text": "ตารางอัตราค่าชดเชยตามอายุงาน 120 วัน ได้ 30 วัน", "is_table": True},
        {"score": 0.48, "page_number": 22, "text": "การทำงานในวันหยุด ได้ค่าทำงานหนึ่งเท่า", "is_table": False},
    ]

    reranked = reranker.rerank("การจ่ายเงินชดเชยการเลิกจ้าง", sample_candidates, top_k=2)
    print("Top 1 after rerank:", reranked[0]["page_number"], reranked[0]["score"])
