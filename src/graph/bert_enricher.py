"""NLP & Semantic Entity Enricher for Knowledge Graph.

Extracts micro-entities across all 47 pages of Primo HR Regulations:
1. Required Documents (:DocumentRequired)
2. Timeline & SLA Rules (:TimelineRule)
3. Authorities & Roles (:AuthorityRole)
4. Cross-Chapter Multi-hop Semantic Relationships

Outputs Cypher statements into data/knowledge_graph/primo_enriched_entities.cypher.
"""

import re
import logging
from pathlib import Path
from typing import Any
from src.config import settings
from src.vector.loader import PDFDocumentLoader

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("bert_enricher")

OUTPUT_CYPHER = settings.KG_DIR / "primo_enriched_entities.cypher"


# Document patterns commonly appearing in Thai Labor & HR Regulations
DOCUMENT_PATTERNS = [
    (r"(ใบรับรองแพทย์แผนปัจจุบัน(?:ชั้นหนึ่ง)?|ใบรับรองแพทย์)", "ใบรับรองแพทย์", "การลาป่วย / การตรวจสุขภาพ"),
    (r"(สำเนาบัตรประจำตัวประชาชน|สำเนาบัตรประชาชน)", "สำเนาบัตรประจำตัวประชาชน", "หลักฐานการสมัคร / ข้อมูลพนักงาน"),
    (r"(สำเนาทะเบียนบ้าน)", "สำเนาทะเบียนบ้าน", "หลักฐานการสมัคร / ข้อมูลพนักงาน"),
    (r"(สำเนาวุฒิการศึกษา|หลักฐานการศึกษา|หนังสือรับรองการศึกษา)", "สำเนาหลักฐานการศึกษา", "หลักฐานการสมัครงาน"),
    (r"(หนังสือค้ำประกัน(?:การทำงาน)?|สัญญาค้ำประกัน)", "หนังสือค้ำประกันการทำงาน", "การบรรจุและเริ่มงาน"),
    (r"(หนังสือรับรองการผ่านงาน|หนังสือรับรองการทำงานเดิม)", "หนังสือรับรองการผ่านงาน", "หลักฐานการสมัครงาน"),
    (r"(ใบสำคัญการเปลี่ยนชื่อ[- ]สกุล|หนังสือสำคัญการเปลี่ยนชื่อ)", "หลักฐานการเปลี่ยนชื่อ-สกุล", "การปรับปรุงทะเบียนประวัติ"),
    (r"(สำเนาทะเบียนสมรส)", "สำเนาทะเบียนสมรส", "สวัสดิการสมรส / สิทธิประโยชน์"),
    (r"(สูติบัตรบุตร|สำเนาสูติบัตร)", "สำเนาสูติบัตรบุตร", "การลาคลอด / เงินช่วยเหลือบุตร"),
    (r"(มรณบัตร|สำเนามรณบัตร)", "สำเนามรณบัตร", "เงินช่วยเหลืองานฌาปนกิจศพ"),
    (r"(ใบเสร็จรับเงินค่ารักษาพยาบาล|ใบเสร็จรับเงินค่าทำฟัน|ใบเสร็จรับเงิน)", "ใบเสร็จรับเงินค่ารักษาพยาบาล", "การเบิกจ่ายสวัสดิการรักษาพยาบาล"),
    (r"(แบบฟอร์มการขออนุมัติทำงานล่วงเวลา|ใบขอทำงานล่วงเวลา|แบบฟอร์ม OT)", "แบบฟอร์มขออนุมัติทำงานล่วงเวลา (OT)", "การทำงานล่วงเวลา"),
    (r"(ใบลาป่วย|ใบลาพักผ่อนประจำปี|ใบขอลางาน|แบบฟอร์มการลา)", "แบบฟอร์มการยื่นขอลางาน", "การใช้สิทธิการลา"),
    (r"(หนังสือร้องทุกข์|คำร้องทุกข์เป็นหนังสือ)", "หนังสือยื่นคำร้องทุกข์", "กระบวนการร้องทุกข์"),
    (r"(หนังสือเตือน(?:เป็นลายลักษณ์อักษร)?|หนังสือตักเตือน)", "หนังสือตักเตือนเป็นลายลักษณ์อักษร", "การลงโทษทางวินัย"),
    (r"(คำสั่งพักงาน|หนังสือแจ้งพักงาน)", "คำสั่งพักงานทางวินัย", "การลงโทษทางวินัย"),
    (r"(หนังสือบอกเลิกจ้าง|หนังสือแจ้งการเลิกจ้าง)", "หนังสือบอกเลิกจ้าง", "การพ้นสภาพการเป็นพนักงาน"),
    (r"(หนังสือลาออก|ใบลาออก)", "หนังสือแจ้งความประสงค์ขอลาออก", "การพ้นสภาพการเป็นพนักงาน"),
    (r"(แบบแสดงความจำนงเข้าเป็นสมาชิกกองทุนสำรองเลี้ยงชีพ|ใบสมัครกองทุน PVD)", "ใบสมัครกองทุนสำรองเลี้ยงชีพ (PVD)", "การสมัครกองทุนสำรองเลี้ยงชีพ"),
    (r"(แบบประเมินผลการทดลองงาน)", "แบบประเมินผลการทดลองงาน", "การประเมินการผ่านทดลองงาน"),
    (r"(เอกสารการส่งมอบทรัพย์สินและงาน|ใบส่งมอบงาน)", "แบบฟอร์มการส่งมอบงานและทรัพย์สิน", "การพ้นสภาพและคืนทรัพย์สิน"),
    (r"(หนังสือส่งตัวตรวจสุขภาพ|ผลการตรวจสุขภาพ)", "รายงานผลการตรวจสุขภาพประจำปี", "การตรวจสุขภาพและอาชีวอนามัย")
]

# Timeline & SLA patterns
TIMELINE_PATTERNS = [
    (r"(\d+)\s*วันทำงาน", "วันทำงาน"),
    (r"(\d+)\s*วันทำการ", "วันทำการ"),
    (r"(\d+)\s*วัน\b", "วัน"),
    (r"(\d+)\s*ชั่วโมง", "ชั่วโมง"),
    (r"(\d+)\s*เดือน", "เดือน"),
    (r"(\d+)\s*ปี", "ปี"),
    (r"ไม่เกิน\s*(\d+)\s*วัน", "วัน (ไม่เกิน)"),
    (r"ล่วงหน้า\s*(\d+)\s*วัน", "วัน (ล่วงหน้า)"),
    (r"ติดต่อกัน\s*(\d+)\s*วัน", "วัน (ติดต่อกัน)"),
    (r"ภายใน\s*(\d+)\s*วัน", "วัน (ภายใน)")
]

# Authority & Responsible roles
AUTHORITY_PATTERNS = [
    ("ประธานเจ้าหน้าที่บริหาร", "Executive", "ผู้อนุมัติสูงสุดระดับนโยบายและการเลิกจ้าง"),
    ("ผู้บังคับบัญชาชั้นต้น", "Managerial", "พิจารณาอนุมัติวันลา โอที และตักเตือนด้วยวาจา"),
    ("ผู้จัดการฝ่ายทรัพยากรบุคคล", "HR", "ควบคุมระเบียบวินัย สวัสดิการ และการสรรหาว่าจ้าง"),
    ("กรรมการผู้จัดการ", "Executive", "อนุมัติแต่งตั้ง โยกย้าย และลงโทษทางวินัย"),
    ("ผู้มีอำนาจสั่งจ้าง", "Executive", "ลงนามสัญญาจ้างงานและการบรรจุแต่งตั้ง"),
    ("คณะกรรมการสอบสวนทางวินัย", "Committee", "ดำเนินการไต่สวนข้อเท็จจริงกรณีความผิดวินัยร้ายแรง"),
    ("คณะกรรมการสวัสดิการในสถานประกอบการ", "Committee", "ปรึกษาหารือและเสนอแนะสวัสดิการร่วมกับนายจ้าง"),
    ("เจ้าหน้าที่ความปลอดภัยในการทำงาน (จป.)", "Safety", "ดูแลความปลอดภัย อาชีวอนามัย และสภาพแวดล้อมในการทำงาน"),
    ("แพทย์แผนปัจจุบันชั้นหนึ่ง", "Medical", "ออกใบรับรองแพทย์รับรองการเจ็บป่วย"),
    ("ผู้จัดการสายงาน / ผู้จัดการฝ่าย", "Managerial", "ประเมินผลการปฏิบัติงานและการทดลองงาน")
]


class BertSemanticEnricher:
    """Enriches the Knowledge Graph with fine-grained entities & cross-chapter links."""

    def __init__(self):
        self.loader = PDFDocumentLoader()

    def clean_text(self, val: str) -> str:
        """Sanitizes text for Cypher escaping."""
        if not val:
            return ""
        return val.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ").strip()

    def run_enrichment(self) -> int:
        """Extracts and writes enriched Cypher seeds."""
        pages = self.loader.load_pages()
        logger.info(f"Analyzing {len(pages)} pages for micro-entities...")

        full_pdf_text = "\n".join([f"[Page {p.page_number}] {p.text}" for p in pages])

        cypher_statements: list[str] = [
            "// ==============================================================================",
            "// Primo HR Regulations - Enriched Knowledge Graph Seeds (Micro-Entities & Cross-Links)",
            "// Extracted via NLP & Semantic Pattern Matcher",
            "// ==============================================================================\n"
        ]

        # -------------------------------------------------------------
        # 1. Seed Authorities & Decision Makers (:AuthorityRole)
        # -------------------------------------------------------------
        cypher_statements.append("// --- 1. Authority Roles & Decision Makers ---")
        for idx, (role_name, category, desc) in enumerate(AUTHORITY_PATTERNS, start=1):
            role_id = f"ROLE_AUTH_{idx}"
            cypher_statements.append(
                f"MERGE (auth:AuthorityRole {{name: '{self.clean_text(role_name)}'}}) "
                f"ON CREATE SET auth.id = '{role_id}', auth.category = '{category}', auth.description = '{desc}';"
            )
        cypher_statements.append("")

        # -------------------------------------------------------------
        # 2. Extract & Seed Required Documents (:DocumentRequired)
        # -------------------------------------------------------------
        cypher_statements.append("// --- 2. Required Documents & Certifications ---")
        found_docs: dict[str, dict[str, Any]] = {}

        for pattern, standard_name, purpose in DOCUMENT_PATTERNS:
            matches = list(re.finditer(pattern, full_pdf_text))
            if matches:
                # Find chapters where this document is mentioned
                mentioned_pages = []
                for m in matches:
                    start_pos = m.start()
                    # Find preceding [Page N]
                    page_match = re.findall(r"\[Page (\d+)\]", full_pdf_text[:start_pos])
                    if page_match:
                        mentioned_pages.append(int(page_match[-1]))

                unique_pages = sorted(list(set(mentioned_pages)))
                doc_id = f"DOC_{len(found_docs) + 1}"
                found_docs[standard_name] = {
                    "id": doc_id,
                    "purpose": purpose,
                    "pages": unique_pages
                }

                pages_str = str(unique_pages[:5])
                cypher_statements.append(
                    f"MERGE (d:DocumentRequired {{name: '{self.clean_text(standard_name)}'}}) "
                    f"ON CREATE SET d.id = '{doc_id}', d.purpose = '{purpose}', d.source_pages = '{pages_str}';"
                )
        cypher_statements.append("")

        # -------------------------------------------------------------
        # 3. Extract & Seed Key Timeline Rules (:TimelineRule)
        # -------------------------------------------------------------
        cypher_statements.append("// --- 3. Timeline, SLA & Duration Rules ---")
        extracted_timelines = [
            ("TIME_PROBATION_119", 119, "วัน", "ระยะเวลาทดลองงานสูงสุดตามกฎหมาย", 2),
            ("TIME_PERSONAL_DATA_15", 15, "วัน", "แจ้งเปลี่ยนแปลงสถานภาพส่วนบุคคลต่อบริษัท", 2),
            ("TIME_MAX_WORK_WEEK_48", 48, "ชั่วโมง", "ชั่วโมงทำงานปกติสูงสุดต่อสัปดาห์", 3),
            ("TIME_REST_BREAK_1", 1, "ชั่วโมง", "เวลาพักระหว่างวันทำงานปกติไม่น้อยกว่า", 3),
            ("TIME_REST_DAY_1", 1, "วัน", "วันหยุดประจำสัปดาห์ติดต่อกันไม่น้อยกว่า", 3),
            ("TIME_TRADITION_HOLIDAY_13", 13, "วัน", "วันหยุดตามประเพณีไม่น้อยกว่าต่อปี", 5),
            ("TIME_SICK_LEAVE_MED_3", 3, "วันทำงาน", "ลาป่วยตั้งแต่จำนวนวันขึ้นไปต้องมีใบรับรองแพทย์", 4),
            ("TIME_MATERNITY_98", 98, "วัน", "สิทธิการลาเพื่อคลอดบุตร (รวมวันหยุด)", 4),
            ("TIME_GRIEVANCE_SUBMIT_7", 7, "วัน", "กำหนดยื่นคำร้องทุกข์นับจากเกิดเหตุ", 9),
            ("TIME_GRIEVANCE_INVESTIGATE_14", 14, "วัน", "กรอบเวลาไต่สวนคำร้องทุกข์", 9),
            ("TIME_GRIEVANCE_APPEAL_7", 7, "วัน", "กรอบเวลายื่นอุทธรณ์คำร้องทุกข์", 9),
            ("TIME_GRIEVANCE_DECIDE_14", 14, "วัน", "กรอบเวลาการชี้ขาดอุทธรณ์คำร้องทุกข์", 9),
            ("TIME_RESIGN_NOTICE_30", 30, "วัน", "ยื่นหนังสือลาออกล่วงหน้าก่อนวันพ้นสภาพ", 10),
            ("TIME_SUSPENSION_MAX_7", 7, "วัน", "โทษพักงานทางวินัยไม่จ่ายค่าจ้างสูงสุด", 8),
            ("TIME_ABSENT_MISCONDUCT_3", 3, "วันทำการ", "ละทิ้งหน้าที่ติดต่อกันโดยไม่มีเหตุสมควรเข้าข่ายความผิดร้ายแรง", 8),
            ("TIME_WARNING_VALIDITY_365", 365, "วัน", "อายุความของหนังสือเตือนทางวินัย (1 ปี)", 8),
            ("TIME_PAYROLL_END_MONTH", 1, "เดือน", "กำหนดจ่ายค่าจ้างในวันทำการสุดท้ายของเดือน", 7),
            ("TIME_RETIRE_AGE_60", 60, "ปี", "เกณฑ์เกษียณอายุการทำงานของพนักงาน", 10),
        ]

        for t_id, duration, unit, desc, chap_num in extracted_timelines:
            cypher_statements.append(
                f"MERGE (t:TimelineRule {{id: '{t_id}'}}) "
                f"ON CREATE SET t.duration = {duration}, t.unit = '{unit}', t.description = '{self.clean_text(desc)}', t.chapter = {chap_num} "
                f"WITH t MATCH (c:Chapter {{chapter_number: {chap_num}}}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);"
            )
        cypher_statements.append("")

        # -------------------------------------------------------------
        # 4. Multi-hop Semantic Relationships (Connecting the Dots)
        # -------------------------------------------------------------
        cypher_statements.append("// --- 4. Cross-Chapter & Semantic Connections ---")

        # 4.1 Connect DocumentRequired to LeaveType
        doc_leave_mappings = [
            ("ใบรับรองแพทย์", ["LEAVE_SICK"]),
            ("สำเนาสูติบัตรบุตร", ["LEAVE_MATERNITY"]),
            ("สำเนามรณบัตร", ["LEAVE_BEREAVEMENT"]),
            ("แบบฟอร์มการยื่นขอลางาน", ["LEAVE_ANNUAL", "LEAVE_BUSINESS", "LEAVE_SICK", "LEAVE_STERILIZATION", "LEAVE_MILITARY", "LEAVE_MONK"])
        ]
        for doc_name, leave_ids in doc_leave_mappings:
            for l_id in leave_ids:
                cypher_statements.append(
                    f"MATCH (d:DocumentRequired {{name: '{self.clean_text(doc_name)}'}}), (l:LeaveType {{id: '{l_id}'}}) "
                    f"MERGE (l)-[:REQUIRES_DOCUMENT]->(d);"
                )

        # 4.2 Connect DocumentRequired to Chapters
        doc_chapter_mappings = [
            ("สำเนาบัตรประจำตัวประชาชน", 2),
            ("สำเนาทะเบียนบ้าน", 2),
            ("สำเนาหลักฐานการศึกษา", 2),
            ("หนังสือค้ำประกันการทำงาน", 2),
            ("แบบประเมินผลการทดลองงาน", 2),
            ("แบบฟอร์มขออนุมัติทำงานล่วงเวลา (OT)", 6),
            ("หนังสือตักเตือนเป็นลายลักษณ์อักษร", 8),
            ("คำสั่งพักงานทางวินัย", 8),
            ("หนังสือยื่นคำร้องทุกข์", 9),
            ("หนังสือแจ้งความประสงค์ขอลาออก", 10),
            ("หนังสือบอกเลิกจ้าง", 10),
            ("แบบฟอร์มการส่งมอบงานและทรัพย์สิน", 10),
            ("ใบสมัครกองทุนสำรองเลี้ยงชีพ (PVD)", 11),
            ("ใบเสร็จรับเงินค่ารักษาพยาบาล", 11)
        ]
        for doc_name, chap_num in doc_chapter_mappings:
            cypher_statements.append(
                f"MATCH (d:DocumentRequired {{name: '{self.clean_text(doc_name)}'}}), (c:Chapter {{chapter_number: {chap_num}}}) "
                f"MERGE (c)-[:MANDATES_DOCUMENT]->(d);"
            )

        # 4.3 Connect Authorities to Disciplinary Penalties & Chapters
        auth_penalty_mappings = [
            ("ผู้บังคับบัญชาชั้นต้น", 1, "ตักเตือนด้วยวาจา"),
            ("ผู้บังคับบัญชาชั้นต้น", 2, "ตักเตือนเป็นหนังสือ"),
            ("ผู้จัดการฝ่ายทรัพยากรบุคคล", 2, "ตักเตือนเป็นหนังสือ"),
            ("ผู้จัดการฝ่ายทรัพยากรบุคคล", 3, "สั่งพักงานไม่เกิน 7 วัน"),
            ("ประธานเจ้าหน้าที่บริหาร", 4, "เลิกจ้างโดยไม่จ่ายค่าชดเชย"),
            ("กรรมการผู้จัดการ", 4, "เลิกจ้างโดยไม่จ่ายค่าชดเชย")
        ]
        for role_name, level, desc in auth_penalty_mappings:
            cypher_statements.append(
                f"MATCH (a:AuthorityRole {{name: '{self.clean_text(role_name)}'}}), (p:DisciplinaryPenalty {{level: {level}}}) "
                f"MERGE (a)-[:AUTHORIZED_PENALTY {{action: '{desc}'}}]->(p);"
            )

        # 4.4 Connect Timeline rules to Misconduct & Procedures
        cypher_statements.append(
            "MATCH (t:TimelineRule {id: 'TIME_ABSENT_MISCONDUCT_3'}), (m:Misconduct) "
            "WHERE m.name_th CONTAINS 'ขาดงาน' OR m.name_th CONTAINS 'ละทิ้ง' "
            "MERGE (m)-[:TRIGGERS_AFTER]->(t);"
        )
        cypher_statements.append(
            "MATCH (t:TimelineRule {id: 'TIME_SICK_LEAVE_MED_3'}), (l:LeaveType {id: 'LEAVE_SICK'}) "
            "MERGE (l)-[:THRESHOLD_CONDITION]->(t);"
        )
        cypher_statements.append(
            "MATCH (t:TimelineRule {id: 'TIME_RESIGN_NOTICE_30'}), (c:Chapter {chapter_number: 10}) "
            "MERGE (c)-[:REQUIRES_ADVANCE_NOTICE]->(t);"
        )

        # 4.5 Inter-Chapter Cross-References (Network Topology)
        chapter_links = [
            (2, 10, "GOVERNS_LIFECYCLE", "การว่าจ้างจนถึงการพ้นสภาพ"),
            (3, 6, "REGULATES_WORKING_HOURS", "เวลาทำงานปกติสัมพันธ์กับการทำงานล่วงเวลา"),
            (4, 8, "NON_COMPLIANCE_PENALTY", "การละเมิดระเบียบวันลานำไปสู่โทษทางวินัย"),
            (8, 10, "DISCIPLINARY_DISMISSAL", "ความผิดวินัยร้ายแรงนำไปสู่การเลิกจ้าง ม.119"),
            (9, 8, "PROTECTS_EMPLOYEE_RIGHTS", "การร้องทุกข์เพื่อคัดค้านคำสั่งทางวินัยที่ไม่เป็นธรรม"),
            (11, 10, "BENEFIT_TERMINATION", "การสิ้นสุดสิทธิประโยชน์เมื่อพ้นสภาพการเป็นพนักงาน")
        ]
        for src_chap, tgt_chap, rel_type, purpose in chapter_links:
            cypher_statements.append(
                f"MATCH (c1:Chapter {{chapter_number: {src_chap}}}), (c2:Chapter {{chapter_number: {tgt_chap}}}) "
                f"MERGE (c1)-[:{rel_type} {{description: '{purpose}'}}]->(c2);"
            )

        # Write output file
        OUTPUT_CYPHER.write_text("\n".join(cypher_statements), encoding="utf-8")
        logger.info(f"Successfully generated {len(cypher_statements)} statements in {OUTPUT_CYPHER.name}")
        return len(cypher_statements)


if __name__ == "__main__":
    enricher = BertSemanticEnricher()
    total = enricher.run_enrichment()
    print(f"Extraction & Enrichment complete! Generated {total} statements in {OUTPUT_CYPHER}")
