"""Query Processor for HR Regulations RAG.

Provides:
1. Thai Synonym and Acronym Expansion (Colloquial -> Official Terminology)
2. HyDE (Hypothetical Document Embeddings) Generator
"""

import logging
import re
from typing import Any
from src.config import settings

logger = logging.getLogger(__name__)

# Dictionary mapping informal/colloquial terms to official PRIMO regulations vocabulary
THAI_HR_SYNONYMS = {
    r"(พักร้อน|ลาพักร้อน)": "วันหยุดพักผ่อนประจำปี ลาพักร้อน",
    r"(ลาคลอด|มีครรภ์|ตั้งครรภ์|คลอดลูก|คลอดบุตร)": "การลาเพื่อคลอดบุตร สิทธิการลาคลอด",
    r"(โอที|ot|OT|ล่วงเวลา)": "การทำงานล่วงเวลา และทำงานในวันหยุด ค่าล่วงเวลา",
    r"(pvd|PVD|สำรองเลี้ยงชีพ)": "กองทุนสำรองเลี้ยงชีพ เงินสมทบนายจ้าง",
    r"(ไล่ออก|ให้ออก|ปลดออก)": "การเลิกจ้าง การพ้นสภาพการเป็นพนักงาน การจ่ายค่าชดเชย",
    r"(ชดเชย|เงินชดเชย)": "การจ่ายค่าชดเชยการเลิกจ้าง อัตราค่าชดเชยตามอายุงาน",
    r"(ทดลองงาน|ผ่านโปร)": "ระยะเวลาทดลองงาน การประเมินผลการทดลองงาน",
    r"(งานศพ|ฌาปนกิจ|เสียชีวิต)": "เงินช่วยเหลือกรณีพนักงานหรือครอบครัวเสียชีวิต สวัสดิการฌาปนกิจ",
    r"(ใบรับรองแพทย์|ลาป่วย)": "การลาป่วย ใบรับรองแพทย์แผนปัจจุบันชั้นหนึ่ง",
    r"(ร้องเรียน|ฟ้องร้อง|ร้องทุกข์)": "การร้องทุกข์ ขั้นตอนการยื่นคำร้องทุกข์",
    r"(ระดับ\s*3|l3|L3)": "พนักงานระดับ 3 ระดับชำนาญการ วันลาพักผ่อนประจำปี",
    r"(ระดับ\s*1|ระดับ\s*2|l1|l2|L1|L2)": "พนักงานระดับ 1-2 ระดับปฏิบัติการ",
    r"(ใบเตือน|หนังสือเตือน)": "หนังสือเตือน การลงโทษทางวินัย อายุหนังสือเตือน",
    r"(ประกันสังคม)": "กองทุนประกันสังคม สิทธิประโยชน์",
    r"(ขาดงาน|ละทิ้งหน้าที่)": "ละทิ้งหน้าที่ ขาดงาน ละทิ้งหน้าที่เป็นเวลาสามวันทำงานติดต่อกัน วินัยร้ายแรง เลิกจ้าง",
}


class HRQueryProcessor:
    """Processes, expands, and augments user questions for improved retrieval."""

    def __init__(self, enable_expansion: bool | None = None, enable_hyde: bool | None = None):
        self.enable_expansion = (
            enable_expansion if enable_expansion is not None
            else getattr(settings, "ENABLE_QUERY_EXPANSION", True)
        )
        self.enable_hyde = (
            enable_hyde if enable_hyde is not None
            else getattr(settings, "ENABLE_HYDE", False)
        )

    def process_query(self, user_query: str) -> str:
        """Applies synonym and acronym expansion to the input query."""
        if not self.enable_expansion or not user_query.strip():
            return user_query.strip()

        expanded_terms = []
        for pattern, official_synonym in THAI_HR_SYNONYMS.items():
            if re.search(pattern, user_query, flags=re.IGNORECASE):
                expanded_terms.append(official_synonym)

        if not expanded_terms:
            return user_query.strip()

        # Combine original query with unique official expanded terms
        unique_synonyms = " ".join(dict.fromkeys(expanded_terms))
        enriched_query = f"{user_query.strip()} ({unique_synonyms})"
        logger.info(f"Expanded Query: '{user_query}' -> '{enriched_query}'")
        return enriched_query

    def generate_hyde(self, query: str, llm_client: Any) -> str:
        """Generates a hypothetical Thai HR document snippet to aid semantic search."""
        if not self.enable_hyde or llm_client is None:
            return query

        prompt = (
            f"คำถามพนักงาน: {query}\n"
            f"จงเขียนข้อความสมมติ 1-2 บรรทัดที่เป็นเนื้อหาข้อบังคับการทำงานภาษาไทยที่เป็นทางการ "
            f"ที่คาดว่าจะพบในคู่มือพนักงานสำหรับตอบคำถามนี้ โดยไม่ต้องเกริ่นนำ:"
        )
        try:
            hypo_text = llm_client.generate(prompt)
            if hypo_text and "offline" not in hypo_text.lower():
                combined = f"{query} {hypo_text}".strip()
                logger.info(f"HyDE Augmented Query: {combined[:150]}...")
                return combined
        except Exception as e:
            logger.warning(f"HyDE generation skipped: {e}")

        return query


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    processor = HRQueryProcessor()
    test_queries = [
        "ท้อง ลาคลอดได้กี่วัน ได้รับค่าจ้างไหม",
        "พนักงานระดับ 3 มีสิทธิ์ลาพักร้อนกี่วัน",
        "โดนไล่ออกได้เงินชดเชยไหม",
        "ทำโอทีวันหยุดได้กี่เท่า",
        "เงินสมทบ pvd กี่เปอร์เซ็นต์"
    ]

    for q in test_queries:
        exp = processor.process_query(q)
        print(f"Original: {q}")
        print(f"Expanded: {exp}\n")
