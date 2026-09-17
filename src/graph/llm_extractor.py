"""Knowledge Graph Hybrid LLM-Assisted Entity Extractor for Primo HR Regulations.

Uses Local Ollama (default: Qwen2.5:7b) in strict JSON format mode to extract
structured entities (Articles, Misconducts, Procedures, Legal Exceptions) across
all 12 chapters (Pages 4-47) of the PDF and converts them directly into Neo4j Cypher.
"""

import sys
import json
import logging
from pathlib import Path
from typing import Any
import httpx
from src.config import settings
from src.vector.loader import PDFDocumentLoader

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("llm_extractor")

OLLAMA_URL = settings.OLLAMA_BASE_URL
DEFAULT_MODEL = "qwen2.5:7b"
FALLBACK_MODEL = "qwen2.5:3b"
OUTPUT_CYPHER = settings.KG_DIR / "primo_hybrid_extracted.cypher"


# Comprehensive coverage of all 12 Chapters across pages 4-47
CHAPTER_SECTIONS = [
    {
        "chapter_num": 1,
        "title": "บททั่วไป",
        "sub_name": "วัตถุประสงค์และสิทธิอำนาจการบริหารจัดการ",
        "pages": (4, 6),
        "focus": "วัตถุประสงค์ การมีผลบังคับใช้ สิทธิอำนาจการบริหารจัดการ การแก้ไขเพิ่มเติมข้อบังคับ อำนาจการสั่งการ"
    },
    {
        "chapter_num": 2,
        "title": "การว่าจ้าง",
        "sub_name": "ประเภทพนักงานและการสมัครงาน",
        "pages": (7, 8),
        "focus": "ประเภทพนักงาน หลักฐานการสมัคร การจัดทำประวัติพนักงาน การรายงานตัว ข้อห้ามการจ้าง"
    },
    {
        "chapter_num": 2,
        "title": "การว่าจ้าง",
        "sub_name": "การทดลองงานและการโยกย้ายแต่งตั้ง",
        "pages": (9, 11),
        "focus": "ระยะเวลาทดลองงาน 119 วัน การประเมินผล การค้ำประกัน ผลงานหรือสิ่งประดิษฐ์ การโยกย้ายแต่งตั้งถอดถอน"
    },
    {
        "chapter_num": 3,
        "title": "วันทำงาน เวลาทำงานปกติ และเวลาพัก",
        "sub_name": "เวลาทำงานและวันหยุดประจำสัปดาห์",
        "pages": (12, 13),
        "focus": "วันทำงานปกติ สัปดาห์ละไม่เกิน 48 ชม. เวลาทำงานปกติ เวลาพักไม่น้อยกว่า 1 ชม. วันหยุดประจำสัปดาห์ไม่น้อยกว่า 1 วัน"
    },
    {
        "chapter_num": 4,
        "title": "วันลา และหลักเกณฑ์การลา",
        "sub_name": "การลาป่วย ลากิจ ลาพักผ่อนประจำปี",
        "pages": (14, 15),
        "focus": "การลาป่วย ใบรับรองแพทย์ตั้งแต่ 3 วันขึ้นไป ลากิจธุระอันจำเป็น ลาหยุดพักผ่อนประจำปีตามระดับตำแหน่ง"
    },
    {
        "chapter_num": 4,
        "title": "วันลา และหลักเกณฑ์การลา",
        "sub_name": "การลาคลอด ทหาร ทำหมัน ฝึกอบรม ฌาปนกิจ",
        "pages": (16, 17),
        "focus": "การลาเพื่อคลอดบุตร 98 วัน ลาทำหมัน ลารับราชการทหาร ลาฝึกอบรม ลาอุปสมบท ลาเพื่อพิธีฌาปนกิจศพครอบครัว"
    },
    {
        "chapter_num": 5,
        "title": "วันหยุดและหลักเกณฑ์การหยุด",
        "sub_name": "วันหยุดประเพณีและวันหยุดพักผ่อน",
        "pages": (18, 18),
        "focus": "วันหยุดประจำสัปดาห์ วันหยุดตามประเพณีไม่น้อยกว่า 13 วันต่อปี การประกาศวันหยุดล่วงหน้า การเลื่อนวันหยุด"
    },
    {
        "chapter_num": 6,
        "title": "หลักเกณฑ์การทำงานล่วงเวลา และทำงานในวันหยุด",
        "sub_name": "อัตราค่าตอบแทน OT และข้อยกเว้น",
        "pages": (19, 20),
        "focus": "การทำงานล่วงเวลา อัตรา 1.5 เท่า, 2 เท่า, 3 เท่า การขออนุมัติล่วงหน้า ข้อยกเว้นระดับ 4 ขึ้นไป (ระดับผู้จัดการ)"
    },
    {
        "chapter_num": 7,
        "title": "วันและสถานที่จ่ายค่าจ้าง ค่าล่วงเวลา",
        "sub_name": "กำหนดการจ่ายและการหักเงิน",
        "pages": (21, 22),
        "focus": "กำหนดวันจ่ายค่าจ้างสิ้นเดือน การโอนผ่านธนาคาร การหักภาษี ณ ที่จ่าย เงินสมทบประกันสังคม กองทุน PVD"
    },
    {
        "chapter_num": 8,
        "title": "วินัยและโทษทางวินัย",
        "sub_name": "มาตรการและขั้นตอนการลงโทษทางวินัย 4 ขั้น",
        "pages": (23, 24),
        "focus": "ลำดับโทษ 4 ขั้น: ตักเตือนด้วยวาจา, ตักเตือนเป็นหนังสือ, พักงานไม่เกิน 7 วัน, เลิกจ้างไม่จ่ายค่าชดเชย อำนาจลงโทษ"
    },
    {
        "chapter_num": 8,
        "title": "วินัยและโทษทางวินัย",
        "sub_name": "ความผิดวินัยทั่วไปและมาตรฐานการปฏิบัติงาน",
        "pages": (25, 27),
        "focus": "ความผิดวินัยทั่วไป: มาสาย, ขาดงาน, ละทิ้งหน้าที่, แต่งกายไม่สุภาพ, การไม่บันทึกเวลา, การไม่เชื่อฟังผู้บังคับบัญชา"
    },
    {
        "chapter_num": 8,
        "title": "วินัยและโทษทางวินัย",
        "sub_name": "ความผิดวินัยร้ายแรงและการเลิกจ้าง",
        "pages": (28, 30),
        "focus": "ความผิดร้ายแรง: ขาดงานติดต่อกัน 3 วัน, ทุจริต, เล่นการพนัน, เสพสุรา/ยาเสพติด, ทะเลาะวิวาท, โทษจำคุก, ข้อยกเว้น ม.119"
    },
    {
        "chapter_num": 9,
        "title": "การร้องทุกข์",
        "sub_name": "กระบวนการและกรอบเวลาการยื่นคำร้องทุกข์",
        "pages": (31, 32),
        "focus": "ขั้นตอนการยื่นคำร้องทุกข์เป็นหนังสือ กรอบเวลา 7 วัน, การไต่สวน 14 วัน, สิทธิอุทธรณ์ 7 วัน, การวินิจฉัย 14 วัน"
    },
    {
        "chapter_num": 10,
        "title": "การเลิกจ้าง การพ้นสภาพ และการจ่ายค่าชดเชย",
        "sub_name": "เหตุพ้นสภาพและการเกษียณอายุ",
        "pages": (33, 34),
        "focus": "เหตุพ้นสภาพการเป็นพนักงาน การลาออกล่วงหน้า 30 วัน การเกษียณอายุ 60 ปีบริบูรณ์ การส่งมอบงานและทรัพย์สิน"
    },
    {
        "chapter_num": 10,
        "title": "การเลิกจ้าง การพ้นสภาพ และการจ่ายค่าชดเชย",
        "sub_name": "เกณฑ์ค่าชดเชยและข้อยกเว้นตามกฎหมาย",
        "pages": (35, 36),
        "focus": "ตารางอัตราค่าชดเชยตามอายุงาน 30 วันถึง 400 วัน ข้อยกเว้นไม่จ่ายค่าชดเชยตามมาตรา 119 ค่าชดเชยพิเศษ"
    },
    {
        "chapter_num": 11,
        "title": "ผลประโยชน์และสวัสดิการ",
        "sub_name": "กองทุนสำรองเลี้ยงชีพและการประกันภัย",
        "pages": (37, 39),
        "focus": "กองทุนสำรองเลี้ยงชีพ PVD อัตราสะสมและสมทบ 3-15% ประกันสุขภาพกลุ่ม ประกันอุบัติเหตุ ประกันชีวิตกลุ่ม"
    },
    {
        "chapter_num": 11,
        "title": "ผลประโยชน์และสวัสดิการ",
        "sub_name": "เงินช่วยเหลือและสวัสดิการพิเศษ",
        "pages": (40, 41),
        "focus": "เงินช่วยเหลือมรณกรรม (พนักงาน/ครอบครัว) ค่าพวงหรีด เงินของขวัญสมรส ของขวัญคลอดบุตร เครื่องแบบพนักงาน"
    },
    {
        "chapter_num": 12,
        "title": "สภาพการบังคับและการประกาศใช้",
        "sub_name": "ผลบังคับใช้และบทเฉพาะกาล",
        "pages": (42, 44),
        "focus": "วันเริ่มมีผลบังคับใช้ การยกเลิกประกาศหรือระเบียบเดิม การตีความ การอนุโลมตามกฎหมายคุ้มครองแรงงาน"
    },
    {
        "chapter_num": 12,
        "title": "สภาพการบังคับและการประกาศใช้",
        "sub_name": "การลงนามประกาศใช้และบทส่งท้าย",
        "pages": (45, 47),
        "focus": "การลงนามประกาศใช้โดยกรรมการผู้มีอำนาจ เอกสารแนบท้าย การเผยแพร่ให้พนักงานรับทราบโดยทั่วกัน"
    }
]


class HybridGraphExtractor:
    """Extracts relational entities from text sections using Qwen2.5 (default: 7b)."""

    def __init__(self, model_name: str | None = None):
        self.loader = PDFDocumentLoader()
        self.model_name = self._resolve_model(model_name)

    def _resolve_model(self, requested_model: str | None) -> str:
        """Checks if requested model exists in Ollama; falls back if necessary."""
        target = requested_model or DEFAULT_MODEL
        try:
            with httpx.Client(timeout=10.0) as client:
                res = client.get(f"{OLLAMA_URL}/api/tags")
                if res.status_code == 200:
                    installed = [m.get("name", "") for m in res.json().get("models", [])]
                    # Direct match or prefix match (e.g. qwen2.5:7b matches qwen2.5:7b-instruct-q4)
                    if any(target in m for m in installed):
                        logger.info(f"Using model '{target}' for extraction.")
                        return target
                    logger.warning(
                        f"Model '{target}' not currently downloaded in Ollama. "
                        f"Installed models: {installed}. Falling back to '{FALLBACK_MODEL}' if available."
                    )
                    if any(FALLBACK_MODEL in m for m in installed):
                        return FALLBACK_MODEL
        except Exception as e:
            logger.warning(f"Could not connect to Ollama to verify model list: {e}")
        return target

    def query_llm_json(self, prompt: str, system_prompt: str) -> dict[str, Any] | None:
        """Queries local Ollama with strict JSON mode."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt,
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
            }
        }
        try:
            with httpx.Client(timeout=180.0) as client:
                res = client.post(f"{OLLAMA_URL}/api/generate", json=payload)
                if res.status_code == 200:
                    raw_text = res.json().get("response", "").strip()
                    return json.loads(raw_text)
                logger.error(f"Ollama error {res.status_code}: {res.text}")
        except Exception as e:
            logger.error(f"Failed LLM extraction call ({self.model_name}): {e}")
        return None

    def extract_section_entities(self, sec: dict[str, Any], text: str, sec_idx: int) -> list[str]:
        """Prompts LLM to extract structured Article, Misconduct, Step, and Exception nodes."""
        chap_num = sec["chapter_num"]
        chap_title = sec["title"]
        sub_name = sec.get("sub_name", chap_title)
        focus = sec["focus"]

        system_prompt = (
            "คุณคือ Senior Knowledge Graph Engineer ผู้เชี่ยวชาญการแปลงเอกสารกฎหมายแรงงานและข้อบังคับการทำงานเป็น Graph Database\n"
            "จงสกัด Entities และ Relationships จากข้อความที่กำหนดให้อย่างละเอียด ละเว้นการแต่งเติมข้อมูล และรักษาความถูกต้อง 100%\n"
            "ต้องตอบกลับเป็น JSON เท่านั้นตามโครงสร้างนี้:\n"
            "{\n"
            '  "articles": [{"num": 1, "title": "...", "summary": "..."}],\n'
            '  "misconducts": [{"name": "ชื่อการกระทำความผิด", "penalty_step": 1..4, "severity": "ร้ายแรง | ไม่ร้ายแรง"}],\n'
            '  "procedures": [{"step_no": 1, "action": "...", "timeline_days": 7, "responsible": "ผู้บังคับบัญชา | พนักงาน"}],\n'
            '  "exceptions": [{"name": "...", "description": "..."}]\n'
            "}"
        )

        prompt = (
            f"ข้อความจากเอกสารข้อบังคับการทำงาน PRIMO:\n"
            f"หมวดที่ {chap_num}: {chap_title} ({sub_name})\n"
            f"จุดเน้นที่ต้องสกัด: {focus}\n\n"
            f"เนื้อหาเอกสาร (หน้า {sec['pages'][0]}-{sec['pages'][1]}):\n{text[:7000]}\n\n"
            f"กรุณาสกัด Articles, Misconducts, Procedures, และ Exceptions เป็น JSON:"
        )

        logger.info(f"[{sec_idx}/{len(CHAPTER_SECTIONS)}] Extracting Chapter {chap_num} ({sub_name}) using {self.model_name}...")
        data = self.query_llm_json(prompt, system_prompt)

        cypher_lines = []
        if not data:
            logger.warning(f"No JSON returned for Chapter {chap_num} ({sub_name})")
            return cypher_lines

        # Helper functions for safe Cypher formatting
        def safe_str(val: Any, default: str = "") -> str:
            if val is None:
                return default
            return str(val).replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ").strip()

        def safe_int(val: Any, default: int = 1, min_val: int = 1, max_val: int = 20) -> int:
            try:
                n = int(val)
                return max(min_val, min(max_val, n))
            except (ValueError, TypeError):
                return default

        # 1. Merge Chapter Node
        chap_var = f"chap_{chap_num}"
        cypher_lines.append(
            f"MERGE ({chap_var}:Chapter {{chapter_number: {chap_num}}}) "
            f"ON CREATE SET {chap_var}.title_th = '{chap_title}';"
        )

        # 2. Merge Articles
        for a_idx, a in enumerate(data.get("articles", []), start=1):
            raw_num = a.get("num")
            num_int = safe_int(raw_num, default=a_idx, min_val=1, max_val=200)
            title = safe_str(a.get("title"), default=f"มาตรา {num_int}")
            summary = safe_str(a.get("summary"), default="")
            art_id = f"ART_{chap_num}_{sec_idx}_{num_int}"
            cypher_lines.append(
                f"MERGE (a:Article {{id: '{art_id}'}}) "
                f"ON CREATE SET a.number = {num_int}, a.title = '{title}', a.summary = '{summary}' "
                f"WITH a MATCH (c:Chapter {{chapter_number: {chap_num}}}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);"
            )

        # 3. Merge Misconducts (Disciplinary breaches)
        for m_idx, m in enumerate(data.get("misconducts", []), start=1):
            name = safe_str(m.get("name"))
            penalty_step = safe_int(m.get("penalty_step"), default=1, min_val=1, max_val=4)
            severity = safe_str(m.get("severity"), default="ทั่วไป")
            if name:
                misc_id = f"MISC_{chap_num}_{sec_idx}_{m_idx}"
                cypher_lines.append(
                    f"MERGE (m:Misconduct {{id: '{misc_id}'}}) "
                    f"ON CREATE SET m.name_th = '{name}', m.severity = '{severity}', m.chapter = {chap_num};"
                )
                cypher_lines.append(
                    f"MATCH (c:Chapter {{chapter_number: {chap_num}}}), (m:Misconduct {{id: '{misc_id}'}}) "
                    f"MERGE (c)-[:DEFINES_MISCONDUCT]->(m);"
                )
                cypher_lines.append(
                    f"MATCH (m:Misconduct {{id: '{misc_id}'}}), (p:DisciplinaryPenalty {{level: {penalty_step}}}) "
                    f"MERGE (m)-[:SUBJECT_TO]->(p);"
                )

        # 4. Merge Procedures (Workflow steps)
        for p_idx, p in enumerate(data.get("procedures", []), start=1):
            step_no = safe_int(p.get("step_no"), default=p_idx, min_val=1, max_val=20)
            action = safe_str(p.get("action"))
            raw_days = p.get("timeline_days")
            days_str = str(int(raw_days)) if isinstance(raw_days, (int, float)) and raw_days > 0 else "null"
            resp = safe_str(p.get("responsible"), default="ผู้บังคับบัญชา")
            if action:
                proc_id = f"PROC_{chap_num}_{sec_idx}_{step_no}"
                cypher_lines.append(
                    f"MERGE (pr:ProcedureStep {{id: '{proc_id}'}}) "
                    f"ON CREATE SET pr.step_number = {step_no}, pr.action = '{action}', "
                    f"pr.timeline_days = {days_str}, pr.responsible = '{resp}' "
                    f"WITH pr MATCH (c:Chapter {{chapter_number: {chap_num}}}) MERGE (c)-[:HAS_STEP]->(pr);"
                )

        # 5. Merge Legal Exceptions / Clauses
        for e_idx, e in enumerate(data.get("exceptions", []), start=1):
            name = safe_str(e.get("name"))
            desc = safe_str(e.get("description"))
            if name:
                exc_id = f"EXC_{chap_num}_{sec_idx}_{e_idx}"
                cypher_lines.append(
                    f"MERGE (ex:LegalException {{id: '{exc_id}'}}) "
                    f"ON CREATE SET ex.name = '{name}', ex.description = '{desc}' "
                    f"WITH ex MATCH (c:Chapter {{chapter_number: {chap_num}}}) MERGE (c)-[:HAS_EXCEPTION]->(ex);"
                )

        return cypher_lines

    def run_full_extraction(self) -> int:
        """Iterates through all designated sections across pages 4-47 and saves Cypher file."""
        pages = self.loader.load_pages()
        all_cypher: list[str] = [
            "// ==============================================================================",
            "// Primo Service Solution Co., Ltd. - Full Hybrid LLM-Extracted Knowledge Graph Seeds",
            f"// Generated with {self.model_name} (Strict JSON Extraction Mode across 47 Pages)",
            "// ==============================================================================\n"
        ]

        total_statements = 0
        total_sections = len(CHAPTER_SECTIONS)

        for sec_idx, sec in enumerate(CHAPTER_SECTIONS, start=1):
            p_start, p_end = sec["pages"]
            section_pages = [p.text for p in pages if p_start <= p.page_number <= p_end]
            section_text = "\n\n".join(section_pages)

            logger.info(f"Processing pages {p_start}-{p_end} ({sec['title']} - {sec['sub_name']})...")
            statements = self.extract_section_entities(sec, section_text, sec_idx=sec_idx)

            if statements:
                all_cypher.append(f"// --- Chapter {sec['chapter_num']}: {sec['title']} ({sec['sub_name']} - Pages {p_start}-{p_end}) ---")
                all_cypher.extend(statements)
                all_cypher.append("")
                total_statements += len(statements)

        # Ensure directory exists and write cleanly in UTF-8
        OUTPUT_CYPHER.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_CYPHER.write_text("\n".join(all_cypher), encoding="utf-8")
        logger.info(f"Successfully generated {total_statements} Cypher statements in {OUTPUT_CYPHER.name}")
        return total_statements


def extract_and_seed_cli():
    """CLI execution entrypoint."""
    import sys
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    # Parse optional --model argument
    chosen_model = DEFAULT_MODEL
    for arg in sys.argv[1:]:
        if arg.startswith("--model="):
            chosen_model = arg.split("=", 1)[1]
        elif arg == "--fallback":
            chosen_model = FALLBACK_MODEL

    print(f"\n🚀 เริ่มต้นการสกัด Entities และ Relationships ทั้งหมด 47 หน้า ด้วยโมเดล: {chosen_model}")
    print(f"📄 ครอบคลุมทั้ง 12 หมวด (หมวดที่ 1 - 12: หน้า 4 ถึง 47)")
    print(f"💾 ไฟล์ปลายทาง: {OUTPUT_CYPHER}\n")

    extractor = HybridGraphExtractor(model_name=chosen_model)
    stmt_count = extractor.run_full_extraction()

    print(f"\n✅ สกัดเสร็จสิ้นสมบูรณ์!")
    print(f"📊 สร้างคำสั่ง Cypher รวมทั้งหมด {stmt_count} คำสั่ง ที่ '{OUTPUT_CYPHER}'")
    print(f"\n💡 คำสั่งถัดไปเพื่อนำเข้า Neo4j:")
    print(f"   python -m src.graph.seeder --reset")
    print(f"   python -m src.graph.analytics\n")


if __name__ == "__main__":
    extract_and_seed_cli()
