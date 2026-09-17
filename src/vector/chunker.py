"""Text Chunker and Table Structurer for HR Regulations PDF.

Supports Small-to-Big (Parent-Child) chunking, preserving Thai context,
hierarchical metadata, and structured Markdown tables for legal rules.
"""

import logging
import re
from dataclasses import dataclass, asdict
from typing import Any
from src.vector.loader import DocumentPage, PDFDocumentLoader

logger = logging.getLogger(__name__)


@dataclass
class TextChunk:
    """Represents an embedded text chunk with metadata and parent linkage."""
    chunk_id: str
    text: str
    page_number: int
    chapter: str
    section_title: str | None = None
    parent_id: str | None = None
    is_table: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Predefined high-fidelity Markdown tables extracted from PRIMO Regulations
PRIMO_STRUCTURED_TABLES = [
    {
        "table_id": "tbl_leave_entitlement",
        "page_number": 18,
        "chapter": "หมวด 4 วันลา และหลักเกณฑ์การลา",
        "section_title": "สิทธิวันลาพักผ่อนประจำปีตามระดับตำแหน่ง (L1-L9)",
        "markdown": (
            "### ตารางสิทธิวันลาพักผ่อนประจำปีตามระดับตำแหน่ง (PRIMO)\n"
            "| ระดับตำแหน่ง (Job Level) | กลุ่มตำแหน่งตัวอย่าง | สิทธิ์วันลาพักผ่อนประจำปี (วัน/ปี) |\n"
            "|---|---|---|\n"
            "| **ระดับ 1–2 (L1-L2)** | เจ้าหน้าที่ปฏิบัติการ, ธุรการ, พนักงานทั่วไป | **6 วันทำงาน** |\n"
            "| **ระดับ 3–5 (L3-L5)** | เจ้าหน้าที่อาวุโส, วิศวกร, หัวหน้างาน, ผู้จัดการระดับต้น | **7 วันทำงาน** |\n"
            "| **ระดับ 6–8 (L6-L8)** | ผู้จัดการฝ่าย, ผู้อำนวยการส่วน (AVP, VP) | **8 วันทำงาน** |\n"
            "| **ระดับ 9 (L9)** | ผู้บริหารระดับสูง (C-Level / MD / CEO) | **10 วันทำงาน** |\n"
            "*เงื่อนไข: พนักงานมีสิทธิ์เมื่อผ่านการทดลองงานและทำงานครบ 1 ปีขึ้นไป การสะสมวันลาทำได้ตามระเบียบบริษัท*"
        )
    },
    {
        "table_id": "tbl_severance_pay",
        "page_number": 35,
        "chapter": "หมวด 10 การเลิกจ้าง การพ้นสภาพการเป็นพนักงานและการจ่ายค่าชดเชย",
        "section_title": "อัตราค่าชดเชยการเลิกจ้างตามอายุงาน (ตามกฎหมายแรงงาน)",
        "markdown": (
            "### ตารางอัตราค่าชดเชยการเลิกจ้างตามอายุงาน (PRIMO)\n"
            "| ระยะเวลาการทำงาน (อายุงาน) | อัตราค่าชดเชยที่ได้รับ (ไม่น้อยกว่าค่าจ้างอัตราสุดท้าย) |\n"
            "|---|---|\n"
            "| ครบ 120 วัน แต่ไม่ถึง 1 ปี | **30 วัน** (1 เดือน) |\n"
            "| ครบ 1 ปี แต่ไม่ถึง 3 ปี | **90 วัน** (3 เดือน) |\n"
            "| ครบ 3 ปี แต่ไม่ถึง 6 ปี | **180 วัน** (6 เดือน) |\n"
            "| ครบ 6 ปี แต่ไม่ถึง 10 ปี | **240 วัน** (8 เดือน) |\n"
            "| ครบ 10 ปีขึ้นไป | **300 วัน** (10 เดือน) |\n"
            "*ข้อยกเว้น: การเลิกจ้างเพราะทุจริต หรือกระทำความผิดร้ายแรงตามมาตรา 119 ไม่ได้รับค่าชดเชย*"
        )
    },
    {
        "table_id": "tbl_pvd_contributions",
        "page_number": 43,
        "chapter": "หมวด 11 ผลประโยชน์และสวัสดิการ",
        "section_title": "อัตราเงินสะสมและเงินสมทบกองทุนสำรองเลี้ยงชีพ (PVD) ตามอายุงาน",
        "markdown": (
            "### ตารางเงินสะสมและเงินสมทบ กองทุนสำรองเลี้ยงชีพ (PVD) PRIMO\n"
            "| อายุงานของพนักงาน | อัตราเงินสะสมของสมาชิก (ร้อยละของค่าจ้าง) | อัตราเงินสมทบของนายจ้าง (บริษัท) |\n"
            "|---|---|---|\n"
            "| **น้อยกว่า 3 ปี** | 2% หรือ 3% | จ่ายสมทบในอัตราเดียวกับเงินสะสม (2% หรือ 3%) |\n"
            "| **ตั้งแต่ 3 ปี แต่ไม่ถึง 5 ปี** | 2% หรือ 3% หรือ 5% | จ่ายสมทบในอัตราเดียวกับเงินสะสม (2%, 3% หรือ 5%) |\n"
            "| **ตั้งแต่ 5 ปี ขึ้นไป** | 2% หรือ 3% หรือ 5% หรือ 7% | จ่ายสมทบในอัตราเดียวกับเงินสะสม (สูงสุด 7%) |\n\n"
            "**เกณฑ์การรับเงินสมทบส่วนของนายจ้างเมื่อสิ้นสุดสมาชิกภาพ:**\n"
            "- อายุงานน้อยกว่า 1 ปี: ได้รับเงินสมทบนายจ้าง **0%**\n"
            "- อายุงาน 1 ถึง 3 ปี: ได้รับเงินสมทบนายจ้าง **50%**\n"
            "- อายุงานมากกว่า 3 ปีขึ้นไป: ได้รับเงินสมทบนายจ้าง **100%**"
        )
    },
    {
        "table_id": "tbl_leave_types_rules",
        "page_number": 15,
        "chapter": "หมวด 4 วันลา และหลักเกณฑ์การลา",
        "section_title": "ประเภทวันลาและหลักเกณฑ์การจ่ายค่าจ้าง",
        "markdown": (
            "### ตารางสรุปประเภทวันลาและสิทธิ์การรับค่าจ้าง (PRIMO)\n"
            "| ประเภทการลา | สิทธิ์จำนวนวันลาสูงสุด | สิทธิ์การรับค่าจ้าง | เอกสาร/เงื่อนไข |\n"
            "|---|---|---|---|\n"
            "| **ลาป่วย** | ตามที่ป่วยจริง | จ่ายค่าจ้างไม่เกิน **30 วันทำงาน/ปี** | ป่วย 3 วันขึ้นไปต้องมีใบรับรองแพทย์ |\n"
            "| **ลาเพื่อคลอดบุตร** | ไม่เกิน **98 วัน** (รวมวันหยุด) | จ่ายค่าจ้างไม่เกิน **45 วันทำงาน** | นับรวมการตรวจครรภ์ก่อนคลอด |\n"
            "| **ลาทำหมัน** | ตามแพทย์กำหนดและออกใบรับรอง | ได้รับค่าจ้างตลอดระยะเวลาที่ลา | ใบรับรองแพทย์ระบุการทำหมัน |\n"
            "| **ลากิจธุระอันจำเป็น** | ตามระเบียบบริษัทกำหนด | ได้รับค่าจ้างตามที่บริษัทอนุมัติ | ต้องยื่นขอล่วงหน้าต่อผู้บังคับบัญชา |\n"
            "| **ลารับราชการทหาร** | ตามหมายเรียกพลเพื่อฝึกวิชา | ได้รับค่าจ้างไม่เกิน **60 วัน/ปี** | แนบหมายเรียกพลเข้ารับราชการ |"
        )
    },
    {
        "table_id": "tbl_disciplinary_steps",
        "page_number": 24,
        "chapter": "หมวด 8 วินัยและโทษทางวินัย",
        "section_title": "ขั้นตอนและลำดับขั้นบทลงโทษทางวินัย 4 ขั้น",
        "markdown": (
            "### ตารางลำดับขั้นบทลงโทษทางวินัย (PRIMO)\n"
            "| ลำดับขั้น | มาตรการลงโทษทางวินัย | รายละเอียดและผลบังคับ |\n"
            "|---|---|---|\n"
            "| **ขั้นที่ 1** | **ตักเตือนด้วยวาจา** | บันทึกเป็นลายลักษณ์อักษรเป็นหลักฐาน |\n"
            "| **ขั้นที่ 2** | **ตักเตือนเป็นหนังสือ** | หนังสือเตือนมีอายุ **1 ปี** นับแต่วันกระทำความผิด |\n"
            "| **ขั้นที่ 3** | **พักงานโดยไม่จ่ายค่าจ้าง** | พักงานครั้งละไม่เกิน **7 วันทำงาน** |\n"
            "| **ขั้นที่ 4** | **เลิกจ้างโดยไม่จ่ายค่าชดเชย** | ความผิดวินัยร้ายแรง หรือทำผิดซ้ำคำเตือนเป็นหนังสือภายใน 1 ปี |"
        )
    }
]


class DocumentChunker:
    """Splits pages into semantic chunks suitable for Vector Search and Small-to-Big Retrieval."""

    def __init__(
        self,
        chunk_size: int = 450,
        chunk_overlap: int = 80,
        small_chunk_size: int = 250,
        small_chunk_overlap: int = 50,
        enable_small_to_big: bool = True
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.small_chunk_size = small_chunk_size
        self.small_chunk_overlap = small_chunk_overlap
        self.enable_small_to_big = enable_small_to_big

    def chunk_pages(
        self,
        pages: list[DocumentPage]
    ) -> tuple[list[TextChunk], dict[str, TextChunk]]:
        """Processes document pages into indexable chunks and parent documents.
        
        Returns:
            tuple of (search_chunks, parent_chunks_map)
        """
        search_chunks: list[TextChunk] = []
        parents_map: dict[str, TextChunk] = {}

        section_pattern = re.compile(r"(ข้อที่\s*\d+[^\n]*|หมวดที่\s*\d+[^\n]*|บทที่\s*\d+[^\n]*)")

        # 1. Process regular pages
        for page in pages:
            text = page.text
            if not text.strip():
                continue

            current_section = None
            found_section = section_pattern.search(text)
            if found_section:
                current_section = found_section.group(1).strip()

            # Create Parent Chunk (representing full page / section)
            parent_id = f"parent_p{page.page_number}"
            parent_chunk = TextChunk(
                chunk_id=parent_id,
                text=text,
                page_number=page.page_number,
                chapter=page.detected_chapter or "บททั่วไป",
                section_title=current_section,
                parent_id=None
            )
            parents_map[parent_id] = parent_chunk

            # If small-to-big is disabled, use standard chunking
            target_size = self.small_chunk_size if self.enable_small_to_big else self.chunk_size
            target_overlap = self.small_chunk_overlap if self.enable_small_to_big else self.chunk_overlap

            # Split into child search chunks
            if len(text) <= target_size:
                child_id = f"c_p{page.page_number}_0"
                search_chunks.append(
                    TextChunk(
                        chunk_id=child_id,
                        text=text,
                        page_number=page.page_number,
                        chapter=page.detected_chapter or "บททั่วไป",
                        section_title=current_section,
                        parent_id=parent_id
                    )
                )
            else:
                paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
                current_chunk_text = ""
                sub_idx = 0

                for para in paragraphs:
                    if len(current_chunk_text) + len(para) + 1 <= target_size:
                        current_chunk_text = f"{current_chunk_text}\n{para}".strip()
                    else:
                        if current_chunk_text:
                            child_id = f"c_p{page.page_number}_{sub_idx}"
                            search_chunks.append(
                                TextChunk(
                                    chunk_id=child_id,
                                    text=current_chunk_text,
                                    page_number=page.page_number,
                                    chapter=page.detected_chapter or "บททั่วไป",
                                    section_title=current_section,
                                    parent_id=parent_id
                                )
                            )
                            sub_idx += 1
                            if target_overlap > 0 and len(current_chunk_text) > target_overlap:
                                overlap_prefix = current_chunk_text[-target_overlap:]
                                current_chunk_text = f"{overlap_prefix}\n{para}".strip()
                            else:
                                current_chunk_text = para
                        else:
                            # Slide through long paragraph
                            start = 0
                            while start < len(para):
                                end = start + target_size
                                part = para[start:end]
                                child_id = f"c_p{page.page_number}_{sub_idx}"
                                search_chunks.append(
                                    TextChunk(
                                        chunk_id=child_id,
                                        text=part,
                                        page_number=page.page_number,
                                        chapter=page.detected_chapter or "บททั่วไป",
                                        section_title=current_section,
                                        parent_id=parent_id
                                    )
                                )
                                sub_idx += 1
                                start += (target_size - target_overlap)
                            current_chunk_text = ""

                if current_chunk_text:
                    child_id = f"c_p{page.page_number}_{sub_idx}"
                    search_chunks.append(
                        TextChunk(
                            chunk_id=child_id,
                            text=current_chunk_text,
                            page_number=page.page_number,
                            chapter=page.detected_chapter or "บททั่วไป",
                            section_title=current_section,
                            parent_id=parent_id
                        )
                    )

        # 2. Inject Structured Markdown Tables
        for tbl in PRIMO_STRUCTURED_TABLES:
            parent_id = f"parent_{tbl['table_id']}"
            parent_chunk = TextChunk(
                chunk_id=parent_id,
                text=tbl["markdown"],
                page_number=tbl["page_number"],
                chapter=tbl["chapter"],
                section_title=tbl["section_title"],
                is_table=True
            )
            parents_map[parent_id] = parent_chunk

            # Add table as search chunk directly
            search_chunks.append(
                TextChunk(
                    chunk_id=f"c_{tbl['table_id']}",
                    text=tbl["markdown"],
                    page_number=tbl["page_number"],
                    chapter=tbl["chapter"],
                    section_title=tbl["section_title"],
                    parent_id=parent_id,
                    is_table=True
                )
            )

        logger.info(
            f"Chunking complete: {len(search_chunks)} child search chunks, "
            f"{len(parents_map)} parent contexts (including {len(PRIMO_STRUCTURED_TABLES)} structured tables)."
        )
        return search_chunks, parents_map


if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    loader = PDFDocumentLoader()
    pages = loader.load_pages()
    chunker = DocumentChunker()
    chunks, parents = chunker.chunk_pages(pages)

    print(f"[OK] Generated {len(chunks)} search chunks and {len(parents)} parent contexts.")
    table_chunks = [c for c in chunks if c.is_table]
    print(f"[OK] Injected {len(table_chunks)} structured table chunks.")
    if table_chunks:
        print("\n--- Sample Structured Table ---")
        print(table_chunks[0].text)
