// ==============================================================================
// Primo Service Solution Co., Ltd. - Full Hybrid LLM-Extracted Knowledge Graph Seeds
// Generated with qwen2.5:7b (Strict JSON Extraction Mode across 47 Pages)
// ==============================================================================

// --- Chapter 1: บททั่วไป (วัตถุประสงค์และสิทธิอำนาจการบริหารจัดการ - Pages 4-6) ---
MERGE (chap_1:Chapter {chapter_number: 1}) ON CREATE SET chap_1.title_th = 'บททั่วไป';
MERGE (a:Article {id: 'ART_1_1_1'}) ON CREATE SET a.number = 1, a.title = 'บททั่วไป', a.summary = 'หมวดนี้กำหนดวัตถุประสงค์ของข้อบังคับ การมีผลบังคับใช้ สิทธิอำนาจการบริหารจัดการ และการแก้ไขเพิ่มเติมข้อบังคับ' WITH a MATCH (c:Chapter {chapter_number: 1}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_1_1_1'}) ON CREATE SET m.name_th = 'ไม่ปฏิบัติตามข้อบังคับเกี่ยวกับการทำงาน', m.severity = 'ร้ายแรง', m.chapter = 1;
MATCH (c:Chapter {chapter_number: 1}), (m:Misconduct {id: 'MISC_1_1_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_1_1_1'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_1_1_2'}) ON CREATE SET m.name_th = 'ไม่ปฏิบัติตามคำสั่งของผู้บังคับบัญชา', m.severity = 'ร้ายแรง', m.chapter = 1;
MATCH (c:Chapter {chapter_number: 1}), (m:Misconduct {id: 'MISC_1_1_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_1_1_2'}), (p:DisciplinaryPenalty {level: 2}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_1_1_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'บริหารจัดการระเบียบวินัย ประสิทธิภาพ และประสิทธิผลในการทำงาน', pr.timeline_days = 30, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 1}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_1_1_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'กำหนดหรือเปลี่ยนแปลงวิธีการบริหารเพื่อความสำเร็จทางธุรกิจ', pr.timeline_days = 60, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 1}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_1_1_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'ออกกฎระเบียบข้อบังคับสำหรับควบคุมความประพฤติและหลักปฏิบัติงาน', pr.timeline_days = 90, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 1}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_1_1_1'}) ON CREATE SET ex.name = 'การแก้ไขเปลี่ยนแปลงหรือเพิ่มเติมข้อบังคับ', ex.description = 'บริษัทอาจแก้ไขเปลี่ยนแปลงหรือเพิ่มเติมข้อบังคับเกี่ยวกับการทำงานเพื่อให้เหมาะสมกับสภาวะเศรษฐกิจหรือการบริหารงานของบริษัท หรือเพื่อให้สอดคล้องกับบทบัญญัติของกฎหมาย' WITH ex MATCH (c:Chapter {chapter_number: 1}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 2: การว่าจ้าง (ประเภทพนักงานและการสมัครงาน - Pages 7-8) ---
MERGE (chap_2:Chapter {chapter_number: 2}) ON CREATE SET chap_2.title_th = 'การว่าจ้าง';
MERGE (a:Article {id: 'ART_2_2_1'}) ON CREATE SET a.number = 1, a.title = 'นโยบายการว่าจ้าง', a.summary = 'นโยบายในการสรรหา คัดเลือก บรรจุแต่งตั้งและโยกย้ายพนักงานเมื่อมีตำแหน่งว่าง โดยให้ความสำคัญกับบุคคลภายในที่มีคุณสมบัติเหมาะสมก่อน' WITH a MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_2_2_1'}) ON CREATE SET m.name_th = 'การกระทำความผิดทางอาญา', m.severity = 'ร้ายแรง', m.chapter = 2;
MATCH (c:Chapter {chapter_number: 2}), (m:Misconduct {id: 'MISC_2_2_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_2_2_1'}), (p:DisciplinaryPenalty {level: 4}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_2_2_2'}) ON CREATE SET m.name_th = 'การเป็นบุคคลไร้ความสามารถหรือเสมือนไร้ความสามารถ', m.severity = 'ร้ายแรง', m.chapter = 2;
MATCH (c:Chapter {chapter_number: 2}), (m:Misconduct {id: 'MISC_2_2_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_2_2_2'}), (p:DisciplinaryPenalty {level: 4}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_2_2_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'ยื่นหลักฐานการสมัครงาน', pr.timeline_days = null, pr.responsible = 'ผู้สมัครงาน' WITH pr MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_2_2_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'การสัมภาษณ์และคัดเลือก', pr.timeline_days = 7, pr.responsible = 'ประธานเจ้าหน้าที่บริหารหรือผู้ที่ได้รับมอบอำนาจ' WITH pr MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_2_2_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'การบรรจุแต่งตั้ง', pr.timeline_days = 14, pr.responsible = 'ประธานเจ้าหน้าที่บริหารหรือผู้ที่ไดรับมอบอำนาจ' WITH pr MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_2_2_4'}) ON CREATE SET pr.step_number = 4, pr.action = 'การรายงานตัว', pr.timeline_days = 7, pr.responsible = 'พนักงานใหม่' WITH pr MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_2_2_1'}) ON CREATE SET ex.name = 'การจ้างงานบุคคลภายนอก', ex.description = 'บริษัทฯ มีสิทธิ์ในการสรรหา คัดเลือก และบรรจุแต่งตั้งบุคคลในตำแหน่งต่าง ๆ จากบุคคลภายนอกตามที่เห็นสมควรและเหมาะสม' WITH ex MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_2_2_2'}) ON CREATE SET ex.name = 'การให้พนักงานไปทำงานนอกสถานที่', ex.description = 'บริษัทฯ มีสิทธิ์ในการให้พนักงานไปทำงานนอกสถานที่ โดยปฏิบัติตามเงื่อนไขของจำเป็น, ความเหมาะสม หรือการจ้างงานของแต่ละตำแหน่ง' WITH ex MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 2: การว่าจ้าง (การทดลองงานและการโยกย้ายแต่งตั้ง - Pages 9-11) ---
MERGE (chap_2:Chapter {chapter_number: 2}) ON CREATE SET chap_2.title_th = 'การว่าจ้าง';
MERGE (a:Article {id: 'ART_2_3_1'}) ON CREATE SET a.number = 1, a.title = 'การว่าจ้าง (การทดลองงานและการโยกย้ายแต่งตั้ง)', a.summary = 'หมวดที่ 2 ของข้อบังคับการทำงาน PRIMO กำหนดเกี่ยวกับการว่าจ้าง พนักงานต้องส่งเอกสารต่าง ๆ เช่น ทะเบียนบ้าน, สำเนาทะเบียนสมรส (หากมี), สำเนาเอกสารการศึกษาและการอบรมที่เกี่ยวข้อง และอื่น ๆ ภายในระยะเวลาที่กำหนด หากไม่แจ้งการเปลี่ยนแปลงสถานภาพส่วนบุคคลให้บริษัททราบภายใน 15 วัน อาจถูกลงโทษทางวินัย' WITH a MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_2_3_1'}) ON CREATE SET m.name_th = 'การไม่แจ้งการเปลี่ยนแปลงสถานภาพส่วนบุคคล', m.severity = 'ร้ายแรง', m.chapter = 2;
MATCH (c:Chapter {chapter_number: 2}), (m:Misconduct {id: 'MISC_2_3_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_2_3_1'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_2_3_2'}) ON CREATE SET m.name_th = 'การฝ่าฝืนข้อบังคับเกี่ยวกับการทำงาน', m.severity = 'ร้ายแรง', m.chapter = 2;
MATCH (c:Chapter {chapter_number: 2}), (m:Misconduct {id: 'MISC_2_3_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_2_3_2'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_2_3_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'แจ้งการลาออกล่วงหน้าอย่างน้อย 30 วัน', pr.timeline_days = 30, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_2_3_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'แจ้งต่อประธานเจ้าหน้าที่บริหารหรือตามที่บริษัทฯมอบอำนาจ', pr.timeline_days = 30, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_2_3_1'}) ON CREATE SET ex.name = 'การไม่เข้าไปมีส่วนร่วมในกิจการที่ไม่ใช่ธุรกิจของบริษัทฯ', ex.description = 'ห้ามพนักงานมีส่วนร่วมในกิจการของธุรกิจอื่น ๆ ในทำนองแข่งขันกับบริษัทฯ ภายในระยะเวลา 2 ปี นับแต่สัญญาจ้างสิ้นสุดลง' WITH ex MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 3: วันทำงาน เวลาทำงานปกติ และเวลาพัก (เวลาทำงานและวันหยุดประจำสัปดาห์ - Pages 12-13) ---
MERGE (chap_3:Chapter {chapter_number: 3}) ON CREATE SET chap_3.title_th = 'วันทำงาน เวลาทำงานปกติ และเวลาพัก';
MERGE (a:Article {id: 'ART_3_4_1'}) ON CREATE SET a.number = 1, a.title = 'หมวดที่ 3: วันทำงาน เวลาทำงานปกติ และเวลาพัก', a.summary = 'กำหนดวันทำงาน สัปดาห์ละไม่เกิน 48 ชม. และเวลาพักไม่น้อยกว่า 1 ชม.' WITH a MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_3_4_1'}) ON CREATE SET m.name_th = 'การมาสาย', m.severity = 'สถานเบา', m.chapter = 3;
MATCH (c:Chapter {chapter_number: 3}), (m:Misconduct {id: 'MISC_3_4_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_3_4_1'}), (p:DisciplinaryPenalty {level: 3}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_3_4_2'}) ON CREATE SET m.name_th = 'การละเลยไม่บันทึกเวลา', m.severity = 'สถานเบา', m.chapter = 3;
MATCH (c:Chapter {chapter_number: 3}), (m:Misconduct {id: 'MISC_3_4_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_3_4_2'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_3_4_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'ติดต่อผู้บังคับบัญชาทางโทรศัพท์ก่อนเข้างาน', pr.timeline_days = null, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_3_4_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'ยื่นจดหมายแสดงสาเหตุการมาสายให้ผู้บังคับบัญชาทราบทันที', pr.timeline_days = null, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_3_4_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'ได้รับอนุญาตจากผู้บังคับบัญชาล่วงหน้าก่อนเลิกงานก่อนเวลา', pr.timeline_days = null, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_3_4_4'}) ON CREATE SET pr.step_number = 4, pr.action = 'กรอกแบบฟอร์มขออนุญาตการเลิกงานก่อนเวลา', pr.timeline_days = null, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_3_4_1'}) ON CREATE SET ex.name = 'การเปลี่ยนแปลงกำหนดเวลาการทำงาน', ex.description = 'บริษัทฯสามารถจัดทำกำหนดเวลาการทำงานใหม่ได้หากมีความจำเป็น และจะแจ้งล่วงหน้าให้พนักงานทราบ' WITH ex MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_3_4_2'}) ON CREATE SET ex.name = 'การบันทึกเวลาการทำงาน', ex.description = 'พนักงานระดับ 4 [Manager, Senior Manager] ลงมาต้องบันทึกเวลาการเข้า-ออกงานด้วยการสแกนลายนิ้วมือ' WITH ex MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 4: วันลา และหลักเกณฑ์การลา (การลาป่วย ลากิจ ลาพักผ่อนประจำปี - Pages 14-15) ---
MERGE (chap_4:Chapter {chapter_number: 4}) ON CREATE SET chap_4.title_th = 'วันลา และหลักเกณฑ์การลา';
MERGE (a:Article {id: 'ART_4_5_1'}) ON CREATE SET a.number = 1, a.title = 'หมวดที่ 4: วันลา และหลักเกณฑ์การลา (การลาป่วย ลากิจ ลาพักผ่อนประจำปี)', a.summary = 'กำหนดประเภทและหลักเกณฑ์ในการลาของพนักงาน' WITH a MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_4_5_1'}) ON CREATE SET m.name_th = 'การลาป่วยที่เป็นเท็จ', m.severity = 'ร้ายแรง', m.chapter = 4;
MATCH (c:Chapter {chapter_number: 4}), (m:Misconduct {id: 'MISC_4_5_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_4_5_1'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_4_5_2'}) ON CREATE SET m.name_th = 'การลาป่วยบ่อยครั้งโดยไม่มีเหตุผลอันสมควร', m.severity = 'ร้ายแรง', m.chapter = 4;
MATCH (c:Chapter {chapter_number: 4}), (m:Misconduct {id: 'MISC_4_5_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_4_5_2'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_4_5_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'แจ้งการลาป่วยภายใน 2 ชั่วโมงแรกของเวลาทำงานปกติในวันแรกที่ต้องหยุดงาน', pr.timeline_days = null, pr.responsible = 'พนักงานหรือบุคคลอื่น' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_4_5_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'ยื่นใบลาตามแบบฟอร์มของบริษัทฯ ต่อผู้บังคับบัญชาภายใน 2 ชั่วโมงหลังจากเริ่มงานในวันแรกที่กลับเข้าทำงาน', pr.timeline_days = null, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_4_5_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'ขออนุมัติการลาต่อผู้บังคับบัญชาโดยตรงของตน', pr.timeline_days = null, pr.responsible = 'พนักงานที่ลาป่วย' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_4_5_4'}) ON CREATE SET pr.step_number = 4, pr.action = 'ยื่นหนังสือรับรองจากแพทย์แผนปัจจุบันชั้นหนึ่ง', pr.timeline_days = null, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_4_5_5'}) ON CREATE SET pr.step_number = 5, pr.action = 'แจ้งเหตุผลให้ผู้บังคับบัญชาทราบถ้าไม่สามารถแสดงใบรับรองแพทย์ได้', pr.timeline_days = null, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_4_5_6'}) ON CREATE SET pr.step_number = 6, pr.action = 'ขอเปลี่ยนงานในหน้าที่เป็นการชั่วคราวก่อนหรือหลังคลอดหากมีใบรับรองของแพทย์', pr.timeline_days = null, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_4_5_7'}) ON CREATE SET pr.step_number = 7, pr.action = 'แจ้งให้ผู้บังคับบัญชาทราบล่วงหน้าไม่น้อยกว่า 7 วัน', pr.timeline_days = null, pr.responsible = 'พนักงานที่จะลาเพื่อทำหมัน' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_4_5_8'}) ON CREATE SET pr.step_number = 8, pr.action = 'ยื่นหนังสือรับรองแพทย์ต่อผู้บังคับบัญชา', pr.timeline_days = null, pr.responsible = 'พนักงานที่จะลาเพื่อทำหมัน' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_4_5_1'}) ON CREATE SET ex.name = 'การลาคลอดบุตร', ex.description = 'พนักงานหญิงมีสิทธิลาเพื่อคลอดบุตรก่อนและหลังคลอดครรภ์หนึ่งไม่เกินเก้าสิบวัน (รวมวันหยุด) บริษัทฯ จ่ายค่าจ้างในวันทำงานให้แก่พนักงานซึ่งลาคลอดตลอดระยะเวลาที่ลาแต่ไม่เกินสี่สิบห้าวัน โดยลาล่วงหน้าอย่างน้อย 30 วัน' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_4_5_2'}) ON CREATE SET ex.name = 'การลาทำหมัน', ex.description = 'บริษัทฯ อนุญาตให้พนักงานลาเพื่อทำหมันได้ และมีสิทธิลาเนื่องจากการทำหมันโดยได้รับค่าจ้าง ทั้งนี้จำนวนวันลาให้เป็นไปตามระยะเวลาที่แพทย์แผนปัจจุบันชั้นหนึ่งเป็นผู้กำหนด' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 4: วันลา และหลักเกณฑ์การลา (การลาคลอด ทหาร ทำหมัน ฝึกอบรม ฌาปนกิจ - Pages 16-17) ---
MERGE (chap_4:Chapter {chapter_number: 4}) ON CREATE SET chap_4.title_th = 'วันลา และหลักเกณฑ์การลา';
MERGE (a:Article {id: 'ART_4_6_1'}) ON CREATE SET a.number = 1, a.title = 'หมวดที่ 4: วันลา และหลักเกณฑ์การลา (การลาคลอด ทหาร ทำหมัน ฝึกอบรม ฌาปนกิจ)', a.summary = 'กำหนดหลักเกณฑ์และขั้นตอนในการลาพนักงานในกรณีต่างๆ เช่น การลาเพื่อคลอดบุตร ทหาร ทำหมัน ฝึกอบรม และการลาพิธีฌาปนกิจศพ' WITH a MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (pr:ProcedureStep {id: 'PROC_4_6_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'แจ้งให้บริษัทฯ ทราบภายใน 7 วัน', pr.timeline_days = 7, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_4_6_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'ยื่นใบลาล่วงหน้าเพื่อให้ผู้บังคับบัญชาพิจารณาอนุมัติเป็นเวลาไม่น้อยกว่า 7 วัน', pr.timeline_days = 7, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_4_6_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'ยื่นใบลาล่วงหน้าไม่น้อยกว่า 15 วัน', pr.timeline_days = 15, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_4_6_1'}) ON CREATE SET ex.name = 'การลาเพื่อคลอดบุตร', ex.description = '98 วัน' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_4_6_2'}) ON CREATE SET ex.name = 'การลาทำหมัน', ex.description = 'ไม่มีข้อมูลเฉพาะ' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_4_6_3'}) ON CREATE SET ex.name = 'การลาเพื่อรับราชการทหาร', ex.description = '60 วัน (โดยนับต่อเนื่องและรวมทั้งวันหยุด)' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_4_6_4'}) ON CREATE SET ex.name = 'การลาฝึกอบรม', ex.description = '30 วันหรือ 3 ครั้ง' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_4_6_5'}) ON CREATE SET ex.name = 'การลาอุปสมบท', ex.description = '15 วัน (โดยได้รับค่าจ้าง)' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_4_6_6'}) ON CREATE SET ex.name = 'การลาพิธีฌาปนกิจศพ', ex.description = 'ไม่เกินครั้งละ 5 วัน' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_4_6_7'}) ON CREATE SET ex.name = 'การลาพิธีสมรส', ex.description = '3 วัน' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_4_6_8'}) ON CREATE SET ex.name = 'การลาในกรณีภัยพิบัติ', ex.description = 'ไม่เกิน 3 วัน' WITH ex MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 5: วันหยุดและหลักเกณฑ์การหยุด (วันหยุดประเพณีและวันหยุดพักผ่อน - Pages 18-18) ---
MERGE (chap_5:Chapter {chapter_number: 5}) ON CREATE SET chap_5.title_th = 'วันหยุดและหลักเกณฑ์การหยุด';
MERGE (a:Article {id: 'ART_5_7_1'}) ON CREATE SET a.number = 1, a.title = 'วันหยุดประจำสัปดาห์', a.summary = 'พนักงานทุกคนจะมีวันหยุดประจำสัปดาห์ละ 1 วัน บริษัทอาจให้สะสมและเลื่อนวันหยุดออกไปไม่เกิน 1 ปี และบริษัทสามารถจัดทำกำหนดเวลาการทำงานใหม่ได้หากมีความจำเป็น' WITH a MATCH (c:Chapter {chapter_number: 5}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (a:Article {id: 'ART_5_7_2'}) ON CREATE SET a.number = 2, a.title = 'วันหยุดตามประเพณี', a.summary = 'บริษัทกำหนดให้มีวันหยุดตามประเพณีปีละไม่น้อยกว่า 13 วัน และอาจมีการเปลี่ยนแปลงวันหยุดตามความเหมาะสม โดยพนักงานจะได้รับค่าจ้างเท่ากับวันทำงาน' WITH a MATCH (c:Chapter {chapter_number: 5}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (a:Article {id: 'ART_5_7_3'}) ON CREATE SET a.number = 3, a.title = 'วันหยุดพักผ่อนประจำปี', a.summary = 'พนักงานที่ทำงานครบ 1 ปีติดต่อกันมีสิทธิหยุดพักผ่อนตามระดับตำแหน่งงาน โดยมีจำนวนวันแตกต่างกัน' WITH a MATCH (c:Chapter {chapter_number: 5}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);

// --- Chapter 6: หลักเกณฑ์การทำงานล่วงเวลา และทำงานในวันหยุด (อัตราค่าตอบแทน OT และข้อยกเว้น - Pages 19-20) ---
MERGE (chap_6:Chapter {chapter_number: 6}) ON CREATE SET chap_6.title_th = 'หลักเกณฑ์การทำงานล่วงเวลา และทำงานในวันหยุด';
MERGE (a:Article {id: 'ART_6_8_1'}) ON CREATE SET a.number = 1, a.title = 'หลักเกณฑ์การทำงานล่วงเวลาและการทำงานในวันหยุด', a.summary = 'กำหนดอัตราค่าตอบแทนสำหรับการทำงานล่วงเวลาและทำงานในวันหยุด รวมถึงข้อยกเว้นสำหรับพนักงานระดับผู้จัดการ' WITH a MATCH (c:Chapter {chapter_number: 6}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_6_8_1'}) ON CREATE SET m.name_th = 'ขาดงานละทิ้งหน้าที่', m.severity = 'ไม่ร้ายแรง', m.chapter = 6;
MATCH (c:Chapter {chapter_number: 6}), (m:Misconduct {id: 'MISC_6_8_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_6_8_1'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_6_8_2'}) ON CREATE SET m.name_th = 'ไม่ยื่นใบลาล่วงหน้า', m.severity = 'ไม่ร้ายแรง', m.chapter = 6;
MATCH (c:Chapter {chapter_number: 6}), (m:Misconduct {id: 'MISC_6_8_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_6_8_2'}), (p:DisciplinaryPenalty {level: 2}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_6_8_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'ยื่นใบลาล่วงหน้า', pr.timeline_days = 7, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 6}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_6_8_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'รับอนุมัติจากผู้บังคับบัญชา', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 6}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_6_8_1'}) ON CREATE SET ex.name = 'ระดับผู้จัดการ', ex.description = 'ข้อยกเว้นสำหรับพนักงานระดับผู้จัดการในการทำงานล่วงเวลาและทำงานในวันหยุด' WITH ex MATCH (c:Chapter {chapter_number: 6}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 7: วันและสถานที่จ่ายค่าจ้าง ค่าล่วงเวลา (กำหนดการจ่ายและการหักเงิน - Pages 21-22) ---
MERGE (chap_7:Chapter {chapter_number: 7}) ON CREATE SET chap_7.title_th = 'วันและสถานที่จ่ายค่าจ้าง ค่าล่วงเวลา';
MERGE (a:Article {id: 'ART_7_9_1'}) ON CREATE SET a.number = 1, a.title = 'วันและสถานที่จ่ายค่าจ้าง', a.summary = 'บริษัทฯ กำหนดจ่ายค่าจ้างในวันทำงานปกติเดือนละ 1 ครั้งในวันสิ้นเดือน โดยจ่ายให้ ณ ที่ทำการของบริษัทฯ หรือจ่ายผ่านธนาคาร' WITH a MATCH (c:Chapter {chapter_number: 7}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (pr:ProcedureStep {id: 'PROC_7_9_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'กำหนดการจ่ายค่าจ้าง', pr.timeline_days = null, pr.responsible = 'บริษัทฯ' WITH pr MATCH (c:Chapter {chapter_number: 7}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_7_9_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'จ่ายค่าทำงานล่วงเวลาในวันหยุด', pr.timeline_days = null, pr.responsible = 'บริษัทฯ' WITH pr MATCH (c:Chapter {chapter_number: 7}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_7_9_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'จ่ายค่าทำงานในวันหยุด', pr.timeline_days = null, pr.responsible = 'บริษัทฯ' WITH pr MATCH (c:Chapter {chapter_number: 7}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_7_9_1'}) ON CREATE SET ex.name = 'พนักงานซึ่งมีอำนาจหน้าที่ทำการแทนบริษัทฯ', ex.description = 'ไม่มีสิทธิได้รับค่าทำงานล่วงเวลา ค่าทำงานในวันหยุด และค่าล่วงเวลาในวันหยุด' WITH ex MATCH (c:Chapter {chapter_number: 7}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_7_9_2'}) ON CREATE SET ex.name = 'พนักงานที่ทำงานล่วงเวลาและทำงานล่วงเวลาในวันหยุด', ex.description = 'มีสิทธิได้รับค่าตอบแทนเป็นเงินเท่ากับอัตราค่าจ้างต่อชั่วโมงในวันทำงานตามจำนวนชั่วโมงที่ทำ' WITH ex MATCH (c:Chapter {chapter_number: 7}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 8: วินัยและโทษทางวินัย (มาตรการและขั้นตอนการลงโทษทางวินัย 4 ขั้น - Pages 23-24) ---
MERGE (chap_8:Chapter {chapter_number: 8}) ON CREATE SET chap_8.title_th = 'วินัยและโทษทางวินัย';
MERGE (a:Article {id: 'ART_8_10_1'}) ON CREATE SET a.number = 1, a.title = 'หมวดที่ 8: วินัยและโทษทางวินัย (มาตรการและขั้นตอนการลงโทษทางวินัย 4 ขั้น)', a.summary = 'กำหนดมาตรการและขั้นตอนการลงโทษทางวินัย 4 ขั้น รวมถึงอำนาจลงโทษ' WITH a MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (a:Article {id: 'ART_8_10_2'}) ON CREATE SET a.number = 2, a.title = 'หมวดที่ 8: วินัยและโทษทางวินัย (นโยบาย)', a.summary = 'กำหนดนโยบายในการบริหารจัดการวินัยของพนักงาน' WITH a MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_8_10_1'}) ON CREATE SET m.name_th = 'ไม่ปฏิบัติตามระเบียบข้อบังคับและกฎเกณฑ์', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_10_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_10_1'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_8_10_2'}) ON CREATE SET m.name_th = 'ไม่แจ้งการเปลี่ยนแปลงสถานภาพ', m.severity = 'ไม่ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_10_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_10_2'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_8_10_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'ตักเตือนด้วยวาจา', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_10_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'ตักเตือนเป็นหนังสือ', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_10_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'พักงานไม่เกิน 7 วัน', pr.timeline_days = 7, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_10_4'}) ON CREATE SET pr.step_number = 4, pr.action = 'เลิกจ้างไม่จ่ายค่าชดเชย', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_8_10_1'}) ON CREATE SET ex.name = 'พนักงานซึ่งมีตำแหน่งระดับผู้จัดการแผนกขึ้นไป (หรือเทียบเท่า)', ex.description = 'ไม่มีสิทธิได้รับค่าล่วงเวลาและค่าทำงานในวันหยุด เว้นแต่จะเป็นดุลยพินิจของประธานเจ้าหน้าที่บริหาร' WITH ex MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_8_10_2'}) ON CREATE SET ex.name = 'พนักงานซึ่งบริษัทฯให้ทำงานขนส่งเฝ้าหรือดูแลสถานที่หรือทรัพย์สินงานนอกสถานที่', ex.description = 'โดยสภาพของงานไม่อาจกำหนดเวลาแน่นอนได้ หรือเป็นงานอื่นตามที่กระทรวงแรงงานและสวัสดิการสังคมกำหนด' WITH ex MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 8: วินัยและโทษทางวินัย (ความผิดวินัยทั่วไปและมาตรฐานการปฏิบัติงาน - Pages 25-27) ---
MERGE (chap_8:Chapter {chapter_number: 8}) ON CREATE SET chap_8.title_th = 'วินัยและโทษทางวินัย';
MERGE (a:Article {id: 'ART_8_11_1'}) ON CREATE SET a.number = 1, a.title = 'หมวดที่ 8: วินัยและโทษทางวินัย (ความผิดวินัยทั่วไปและมาตรฐานการปฏิบัติงาน)', a.summary = 'กำหนดข้อห้ามและความผิดวินัยทั่วไปของพนักงาน' WITH a MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_8_11_1'}) ON CREATE SET m.name_th = 'มาสาย', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_11_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_11_1'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_8_11_2'}) ON CREATE SET m.name_th = 'ขาดงาน', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_11_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_11_2'}), (p:DisciplinaryPenalty {level: 2}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_8_11_3'}) ON CREATE SET m.name_th = 'ละทิ้งหน้าที่', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_11_3'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_11_3'}), (p:DisciplinaryPenalty {level: 3}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_8_11_4'}) ON CREATE SET m.name_th = 'แต่งกายไม่สุภาพ', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_11_4'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_11_4'}), (p:DisciplinaryPenalty {level: 4}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_8_11_5'}) ON CREATE SET m.name_th = 'การไม่บันทึกเวลา', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_11_5'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_11_5'}), (p:DisciplinaryPenalty {level: 4}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_8_11_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'พนักงานต้องมาทำงานอย่างปกติและสม่ำเสมอตามวันเวลาทำงานที่บริษัทฯกำหนด', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_11_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'พนักงานต้องปฏิบัติตามระเบียบในเรื่องการลงเวลาเข้าและออกงานโดยเคร่งครัด', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_11_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'พนักงานต้องปฏิบัติตามระเบียบว่าด้วยการลาหรือการหยุดงานโดยเคร่งครัด', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_11_4'}) ON CREATE SET pr.step_number = 4, pr.action = 'พนักงานต้องปฏิบัติตามกำหนดการและเวลาในเรื่องการเข้าทำงาน การออกไปและการกลับเข้ามาในการปฏิบัติงานนอกบริษัทฯ และการเลิกงาน', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_11_5'}) ON CREATE SET pr.step_number = 5, pr.action = 'พนักงานห้ามทำบัตรบันทึกเวลาชำรุด สูญหาย หรือแก้ไขข้อความใด ๆ', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_8_11_1'}) ON CREATE SET ex.name = 'การกระทำที่ไม่เป็นไปตามระเบียบ', ex.description = 'หากพนักงานแสดงเจตนาที่จะทำงานล่วงเวลา หรือทำงานในวันหยุดแล้วแต่กรณีแต่ไม่มาปฏิบัติงานนั้นโดยไม่มีเหตุผลอันสมควร และส่งผลให้บริษัทฯ ได้รับความเสียหาย' WITH ex MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 8: วินัยและโทษทางวินัย (ความผิดวินัยร้ายแรงและการเลิกจ้าง - Pages 28-30) ---
MERGE (chap_8:Chapter {chapter_number: 8}) ON CREATE SET chap_8.title_th = 'วินัยและโทษทางวินัย';
MERGE (a:Article {id: 'ART_8_12_1'}) ON CREATE SET a.number = 1, a.title = 'ความประพฤติ', a.summary = 'พนักงานต้องไม่ทำการทะเลาะวิวาทหรือใช้กำลังประทุษร้ายซึ่งกันและกันในบริเวณบริษัทฯ รวมถึงสถานที่อื่น ๆ เมื่อบริษัทฯ จัดงานหรือมีงานนอกสถานที่บริษัทฯ หรือในขณะทำงานนอกสถานที่' WITH a MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (a:Article {id: 'ART_8_12_2'}) ON CREATE SET a.number = 2, a.title = 'ความซื่อสัตย์สุจริต', a.summary = 'พนักงานต้องไม่เปลี่ยนแปลง ปลอม แก้ไข ตัดทอน หรือทำลายเอกสารต่าง ๆ ของบริษัทฯ หรือเอกสารที่มีการเกี่ยวข้องระหว่างบริษัทฯ กับพนักงานโดยไม่มีอำนาจหน้าที่ที่จะกระทำการดังกล่าว' WITH a MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (a:Article {id: 'ART_8_12_3'}) ON CREATE SET a.number = 3, a.title = 'ความผิดวินัยร้ายแรงและการเลิกจ้าง', a.summary = 'การลงโทษทางวินัยของพนักงานตามที่ระบุมานี้พนักงานมีหน้าที่ต้องปฏิบัติตามอย่างเคร่งครัด และอนุโลมบังคับใช้ถึงบ้านพักหรือรถรับ - ส่งพนักงานด้วย บทลงโทษทางวินัยจะเป็นไปตามข้อหนึ่งข้อใดหรือหลายข้อรวมกันก็ได้' WITH a MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_8_12_1'}) ON CREATE SET m.name_th = 'ขาดงานติดต่อกัน 3 วัน', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_12_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_12_1'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_8_12_2'}) ON CREATE SET m.name_th = 'ทุจริต', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_12_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_12_2'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_8_12_3'}) ON CREATE SET m.name_th = 'เล่นการพนัน', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_12_3'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_12_3'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_8_12_4'}) ON CREATE SET m.name_th = 'เสพสุรา/ยาเสพติด', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_12_4'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_12_4'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_8_12_5'}) ON CREATE SET m.name_th = 'ทะเลาะวิวาท', m.severity = 'ร้ายแรง', m.chapter = 8;
MATCH (c:Chapter {chapter_number: 8}), (m:Misconduct {id: 'MISC_8_12_5'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_8_12_5'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_8_12_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'การตักเตือนด้วยวาจา โดยบันทึกเป็นหนังสือไว้เป็นหลักฐาน', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_12_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'การตักเตือนเป็นหนังสือ', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_12_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'พักงานโดยไม่จ่ายค่าจ้าง', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_8_12_4'}) ON CREATE SET pr.step_number = 4, pr.action = 'เลิกจ้าง', pr.timeline_days = null, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_8_12_1'}) ON CREATE SET ex.name = 'ม.119', ex.description = 'ไม่มีรายละเอียดเพิ่มเติมเกี่ยวกับข้อยกเว้น ม.119 ในเอกสาร' WITH ex MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 9: การร้องทุกข์ (กระบวนการและกรอบเวลาการยื่นคำร้องทุกข์ - Pages 31-32) ---
MERGE (chap_9:Chapter {chapter_number: 9}) ON CREATE SET chap_9.title_th = 'การร้องทุกข์';
MERGE (a:Article {id: 'ART_9_13_1'}) ON CREATE SET a.number = 1, a.title = 'การร้องทุกข์', a.summary = 'บริษัทฯ กำหนดหลักเกณฑ์การร้องทุกข์เพื่อเสริมสร้างความสัมพันธ์อันดีระหว่างบริษัทฯ กับพนักงาน และลดหรือขจัดปัญหาข้อข้องใจ' WITH a MATCH (c:Chapter {chapter_number: 9}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_9_13_1'}) ON CREATE SET m.name_th = 'จงใจทำให้บริษัทฯ ได้รับความเสียหาย', m.severity = 'ร้ายแรง', m.chapter = 9;
MATCH (c:Chapter {chapter_number: 9}), (m:Misconduct {id: 'MISC_9_13_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_9_13_1'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_9_13_2'}) ON CREATE SET m.name_th = 'ประมาทเลินเล่อเป็นเหตุให้บริษัทฯ ได้รับความเสียหายอย่างร้ายแรง', m.severity = 'ร้ายแรง', m.chapter = 9;
MATCH (c:Chapter {chapter_number: 9}), (m:Misconduct {id: 'MISC_9_13_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_9_13_2'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_9_13_3'}) ON CREATE SET m.name_th = 'ฝ่าฝืนข้อบังคับเกี่ยวกับการทำงาน หรือระเบียบ หรือคำสั่งของบริษัทฯ', m.severity = 'ไม่ร้ายแรง', m.chapter = 9;
MATCH (c:Chapter {chapter_number: 9}), (m:Misconduct {id: 'MISC_9_13_3'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_9_13_3'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_9_13_4'}) ON CREATE SET m.name_th = 'ละทิ้งหน้าที่เป็นเวลาสามวันทำงานติดต่อกัน', m.severity = 'ไม่ร้ายแรง', m.chapter = 9;
MATCH (c:Chapter {chapter_number: 9}), (m:Misconduct {id: 'MISC_9_13_4'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_9_13_4'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_9_13_5'}) ON CREATE SET m.name_th = 'ได้รับโทษจำคุกตามคำพิพากษาถึงที่สุดให้จำคุก', m.severity = 'ร้ายแรง', m.chapter = 9;
MATCH (c:Chapter {chapter_number: 9}), (m:Misconduct {id: 'MISC_9_13_5'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_9_13_5'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_9_13_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'ยื่นคำร้องทุกข์เป็นหนังสือ', pr.timeline_days = 7, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 9}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_9_13_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'สอบสวนและการพิจารณาข้อร้องทุกข์', pr.timeline_days = 14, pr.responsible = 'ผู้บังคับบัญชาระดับสูง' WITH pr MATCH (c:Chapter {chapter_number: 9}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_9_13_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'ยื่นอุทธรณ์ร้องทุกข์ต่อผู้บังคับบัญชาระดับบริหาร', pr.timeline_days = 7, pr.responsible = 'ผู้บังคับบัญชาระดับบริหาร' WITH pr MATCH (c:Chapter {chapter_number: 9}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_9_13_1'}) ON CREATE SET ex.name = 'การเปลี่ยนแปลงกฎระเบียบข้อบังคับในการทำงาน', ex.description = 'บริษัทฯ มีสิทธิที่จะเปลี่ยนแปลงหรือเพิ่มเติมกฎระเบียบข้อบังคับในการทำงานของบริษัทฯ เพื่อความเหมาะสมตามสภาพของสถานการณ์ภายหน้า' WITH ex MATCH (c:Chapter {chapter_number: 9}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 10: การเลิกจ้าง การพ้นสภาพ และการจ่ายค่าชดเชย (เหตุพ้นสภาพและการเกษียณอายุ - Pages 33-34) ---
MERGE (chap_10:Chapter {chapter_number: 10}) ON CREATE SET chap_10.title_th = 'การเลิกจ้าง การพ้นสภาพ และการจ่ายค่าชดเชย';
MERGE (a:Article {id: 'ART_10_14_1'}) ON CREATE SET a.number = 1, a.title = 'การเลิกจ้าง การพ้นสภาพ และการจ่ายค่าชดเชย (เหตุพ้นสภาพและการเกษียณอายุ)', a.summary = 'หมวดนี้กำหนดเกี่ยวกับกระบวนการเลิกจ้าง พ้นสภาพการเป็นพนักงาน รวมถึงการลาออกล่วงหน้า และการเกษียณอายุ พร้อมกับข้อกำหนดในการส่งมอบทรัพย์สินและค่าชดเชย' WITH a MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_10_14_1'}) ON CREATE SET m.name_th = 'เลิกจ้างเพราะเหตุผิดวินัย', m.severity = 'ร้ายแรง', m.chapter = 10;
MATCH (c:Chapter {chapter_number: 10}), (m:Misconduct {id: 'MISC_10_14_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_10_14_1'}), (p:DisciplinaryPenalty {level: 2}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_10_14_2'}) ON CREATE SET m.name_th = 'เลิกจ้างเนื่องจากผลงานไม่เป็นที่พอใจหรือไม่อยู่ในมาตรฐานของบริษัทฯ', m.severity = 'ร้ายแรง', m.chapter = 10;
MATCH (c:Chapter {chapter_number: 10}), (m:Misconduct {id: 'MISC_10_14_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_10_14_2'}), (p:DisciplinaryPenalty {level: 2}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_10_14_3'}) ON CREATE SET m.name_th = 'เลิกจ้างเนื่องจากมีพฤติกรรมไม่น่าไว้วางใจหรือขาดคุณสมบัติของพนักงาน', m.severity = 'ร้ายแรง', m.chapter = 10;
MATCH (c:Chapter {chapter_number: 10}), (m:Misconduct {id: 'MISC_10_14_3'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_10_14_3'}), (p:DisciplinaryPenalty {level: 2}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_10_14_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'การยุติข้อร้องทุกข์', pr.timeline_days = 30, pr.responsible = 'ผู้บังคับบัญชา' WITH pr MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_10_14_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'การวินิจฉัยและแก้ไขปัญหาด้วยความยุติธรรม', pr.timeline_days = 30, pr.responsible = 'ผู้มีอำนาจในการวินิจฉัย' WITH pr MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_10_14_1'}) ON CREATE SET ex.name = 'การลาออกล่วงหน้า', ex.description = 'พนักงานต้องแจ้งเป็นลายลักษณ์อักษรต่อผู้บังคับบัญชาโดยตรง ล่วงหน้าไม่น้อยกว่า 30 วัน' WITH ex MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_10_14_2'}) ON CREATE SET ex.name = 'การส่งมอบทรัพย์สิน', ex.description = 'พนักงานต้องส่งคืนทรัพย์สินของบริษัทฯ ที่ได้เบิกไปใช้ในการปฏิบัติหน้าที่ และชำระหนี้สินต่าง ๆ ต่อบริษัทฯ' WITH ex MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 10: การเลิกจ้าง การพ้นสภาพ และการจ่ายค่าชดเชย (เกณฑ์ค่าชดเชยและข้อยกเว้นตามกฎหมาย - Pages 35-36) ---
MERGE (chap_10:Chapter {chapter_number: 10}) ON CREATE SET chap_10.title_th = 'การเลิกจ้าง การพ้นสภาพ และการจ่ายค่าชดเชย';
MERGE (a:Article {id: 'ART_10_15_1'}) ON CREATE SET a.number = 1, a.title = 'การเลิกจ้างเนื่องจากพนักงานที่มีสุขภาพไม่สมบูรณ์ หรือหย่อนความสามารถ', a.summary = '' WITH a MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (a:Article {id: 'ART_10_15_2'}) ON CREATE SET a.number = 2, a.title = 'เกษียณอายุ 55 ปี (นับตามบัตรประชาชน)', a.summary = '' WITH a MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (a:Article {id: 'ART_10_15_3'}) ON CREATE SET a.number = 3, a.title = 'พนักงานที่เป็นโรคจิตหรือมีพฤติกรรมที่มีจิตบกพร่อง', a.summary = '' WITH a MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (m:Misconduct {id: 'MISC_10_15_1'}) ON CREATE SET m.name_th = 'การลงโทษทางวินัยตามความในข้อ 5 ของหมวด 8 ในข้อบังคับนี้', m.severity = 'ไม่ร้ายแรง', m.chapter = 10;
MATCH (c:Chapter {chapter_number: 10}), (m:Misconduct {id: 'MISC_10_15_1'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_10_15_1'}), (p:DisciplinaryPenalty {level: 1}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_10_15_2'}) ON CREATE SET m.name_th = 'การเลิกจ้างในระหว่างทดลองงาน', m.severity = 'ไม่ร้ายแรง', m.chapter = 10;
MATCH (c:Chapter {chapter_number: 10}), (m:Misconduct {id: 'MISC_10_15_2'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_10_15_2'}), (p:DisciplinaryPenalty {level: 2}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (m:Misconduct {id: 'MISC_10_15_3'}) ON CREATE SET m.name_th = 'การจ้างที่มีกำหนดระยะเวลาสำหรับโครงการเฉพาะที่มิใช่งานปกติของธุรกิจ', m.severity = 'ไม่ร้ายแรง', m.chapter = 10;
MATCH (c:Chapter {chapter_number: 10}), (m:Misconduct {id: 'MISC_10_15_3'}) MERGE (c)-[:DEFINES_MISCONDUCT]->(m);
MATCH (m:Misconduct {id: 'MISC_10_15_3'}), (p:DisciplinaryPenalty {level: 3}) MERGE (m)-[:SUBJECT_TO]->(p);
MERGE (pr:ProcedureStep {id: 'PROC_10_15_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'การเลิกจ้างพนักงานเนื่องจากเหตุผลที่ระบุ', pr.timeline_days = null, pr.responsible = 'บริษัทฯ' WITH pr MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_10_15_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'แจ้งวันที่จะเลิกจ้าง เหตุผล และรายชื่อพนักงานต่อพนักงานตรวจแรงงานและพนักงานที่จะเลิกจ้าง', pr.timeline_days = 60, pr.responsible = 'บริษัทฯ' WITH pr MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_10_15_3'}) ON CREATE SET pr.step_number = 3, pr.action = 'การแจ้งล่วงหน้าไม่ถูกต้องหรือไม่ครบตามระยะเวลาที่กำหนด', pr.timeline_days = null, pr.responsible = 'บริษัทฯ' WITH pr MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (ex:LegalException {id: 'EXC_10_15_1'}) ON CREATE SET ex.name = 'กรณีพนักงานทำงานติดต่อกันครบหกปีขึ้นไป', ex.description = 'ค่าชดเชยพิเศษเพิ่มขึ้นจากค่าชดเชยตามข้อ 3.2 สำหรับการทำงานที่เกินหกปี' WITH ex MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_10_15_2'}) ON CREATE SET ex.name = 'กรณีบริษัทฯ ย้ายสถานประกอบกิจการ', ex.description = 'แจ้งล่วงหน้าไม่น้อยกว่าสามสิบวัน และหากพนักงานไม่ประสงค์จะไปทำงานด้วยให้บอกเลิกสัญญาได้' WITH ex MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 11: ผลประโยชน์และสวัสดิการ (กองทุนสำรองเลี้ยงชีพและการประกันภัย - Pages 37-39) ---
MERGE (chap_11:Chapter {chapter_number: 11}) ON CREATE SET chap_11.title_th = 'ผลประโยชน์และสวัสดิการ';
MERGE (a:Article {id: 'ART_11_16_1'}) ON CREATE SET a.number = 1, a.title = 'หมวดที่ 11: ผลประโยชน์และสวัสดิการ (กองทุนสำรองเลี้ยงชีพและการประกันภัย)', a.summary = 'ระบุว่าบริษัทฯ มีนโยบายในการจัดสวัสดิการต่าง ๆ ให้แก่พนักงาน เช่น ประกันสุขภาพกลุ่ม, การตรวจสุขภาพประจำปี และกองทุนสำรองเลี้ยงชีพ' WITH a MATCH (c:Chapter {chapter_number: 11}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (pr:ProcedureStep {id: 'PROC_11_16_1'}) ON CREATE SET pr.step_number = 1, pr.action = 'ยื่นคำขอให้คณะกรรมการสวัสดิการแรงงานพิจารณา', pr.timeline_days = 30, pr.responsible = 'บริษัทฯ' WITH pr MATCH (c:Chapter {chapter_number: 11}) MERGE (c)-[:HAS_STEP]->(pr);
MERGE (pr:ProcedureStep {id: 'PROC_11_16_2'}) ON CREATE SET pr.step_number = 2, pr.action = 'ใช้สิทธิ์ในการบอกเลิกสัญญา', pr.timeline_days = 30, pr.responsible = 'พนักงาน' WITH pr MATCH (c:Chapter {chapter_number: 11}) MERGE (c)-[:HAS_STEP]->(pr);

// --- Chapter 11: ผลประโยชน์และสวัสดิการ (เงินช่วยเหลือและสวัสดิการพิเศษ - Pages 40-41) ---
MERGE (chap_11:Chapter {chapter_number: 11}) ON CREATE SET chap_11.title_th = 'ผลประโยชน์และสวัสดิการ';
MERGE (a:Article {id: 'ART_11_17_1'}) ON CREATE SET a.number = 1, a.title = 'เงินช่วยเหลือและสวัสดิการพิเศษ', a.summary = 'หมวดที่ 11 ของข้อบังคับการทำงาน PRIMO กำหนดเกี่ยวกับเงินช่วยเหลือและสวัสดิการพิเศษ เช่น เงินช่วยเหลืองานศพ, ของขวัญสมรส, และเครื่องแบบพนักงาน' WITH a MATCH (c:Chapter {chapter_number: 11}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
MERGE (ex:LegalException {id: 'EXC_11_17_1'}) ON CREATE SET ex.name = 'เงินช่วยเหลืองานศพ', ex.description = 'บริษัทฯ ช่วยเหลือค่าจัดการงานศพและพวงหรีดสำหรับพนักงานและครอบครัวในกรณีเสียชีวิต' WITH ex MATCH (c:Chapter {chapter_number: 11}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_11_17_2'}) ON CREATE SET ex.name = 'ของขวัญสมรส', ex.description = 'บริษัทฯ มอบของขวัญหรือเงินให้แก่พนักงานที่เป็นบิดาหรือมารดาที่ให้กำเนิดบุตร' WITH ex MATCH (c:Chapter {chapter_number: 11}) MERGE (c)-[:HAS_EXCEPTION]->(ex);
MERGE (ex:LegalException {id: 'EXC_11_17_3'}) ON CREATE SET ex.name = 'เครื่องแบบพนักงาน', ex.description = 'บริษัทฯ จัดสรรเครื่องแบบสำหรับพนักงาน' WITH ex MATCH (c:Chapter {chapter_number: 11}) MERGE (c)-[:HAS_EXCEPTION]->(ex);

// --- Chapter 12: สภาพการบังคับและการประกาศใช้ (ผลบังคับใช้และบทเฉพาะกาล - Pages 42-44) ---
MERGE (chap_12:Chapter {chapter_number: 12}) ON CREATE SET chap_12.title_th = 'สภาพการบังคับและการประกาศใช้';
MERGE (a:Article {id: 'ART_12_18_1'}) ON CREATE SET a.number = 1, a.title = 'บทเฉพาะกาล', a.summary = 'หมวดที่ 12 กำหนดวันเริ่มมีผลบังคับใช้ การยกเลิกประกาศหรือระเบียบเดิม และการตีความ' WITH a MATCH (c:Chapter {chapter_number: 12}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);

// --- Chapter 12: สภาพการบังคับและการประกาศใช้ (การลงนามประกาศใช้และบทส่งท้าย - Pages 45-47) ---
MERGE (chap_12:Chapter {chapter_number: 12}) ON CREATE SET chap_12.title_th = 'สภาพการบังคับและการประกาศใช้';
MERGE (a:Article {id: 'ART_12_19_1'}) ON CREATE SET a.number = 1, a.title = 'สภาพการบังคับและการประกาศใช้', a.summary = 'ระเบียบข้อบังคับนี้ใช้ต่อพนักงานทุกคน และข้อความที่มีผลบังคับใช้ในบริษัทฯ ก่อนหน้าวันที่ประกาศใช้นี้จะยกเลิกเฉพาะส่วนที่ขัดแย้งกับระเบียบข้อบังคับนี้' WITH a MATCH (c:Chapter {chapter_number: 12}) MERGE (c)-[:CONTAINS_ARTICLE]->(a);
