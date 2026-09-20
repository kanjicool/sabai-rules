// ==============================================================================
// Primo HR Regulations - Enriched Knowledge Graph Seeds (Micro-Entities & Cross-Links)
// Extracted via NLP & Semantic Pattern Matcher
// ==============================================================================

// --- 1. Authority Roles & Decision Makers ---
MERGE (auth:AuthorityRole {name: 'ประธานเจ้าหน้าที่บริหาร'}) ON CREATE SET auth.id = 'ROLE_AUTH_1', auth.category = 'Executive', auth.description = 'ผู้อนุมัติสูงสุดระดับนโยบายและการเลิกจ้าง';
MERGE (auth:AuthorityRole {name: 'ผู้บังคับบัญชาชั้นต้น'}) ON CREATE SET auth.id = 'ROLE_AUTH_2', auth.category = 'Managerial', auth.description = 'พิจารณาอนุมัติวันลา โอที และตักเตือนด้วยวาจา';
MERGE (auth:AuthorityRole {name: 'ผู้จัดการฝ่ายทรัพยากรบุคคล'}) ON CREATE SET auth.id = 'ROLE_AUTH_3', auth.category = 'HR', auth.description = 'ควบคุมระเบียบวินัย สวัสดิการ และการสรรหาว่าจ้าง';
MERGE (auth:AuthorityRole {name: 'กรรมการผู้จัดการ'}) ON CREATE SET auth.id = 'ROLE_AUTH_4', auth.category = 'Executive', auth.description = 'อนุมัติแต่งตั้ง โยกย้าย และลงโทษทางวินัย';
MERGE (auth:AuthorityRole {name: 'ผู้มีอำนาจสั่งจ้าง'}) ON CREATE SET auth.id = 'ROLE_AUTH_5', auth.category = 'Executive', auth.description = 'ลงนามสัญญาจ้างงานและการบรรจุแต่งตั้ง';
MERGE (auth:AuthorityRole {name: 'คณะกรรมการสอบสวนทางวินัย'}) ON CREATE SET auth.id = 'ROLE_AUTH_6', auth.category = 'Committee', auth.description = 'ดำเนินการไต่สวนข้อเท็จจริงกรณีความผิดวินัยร้ายแรง';
MERGE (auth:AuthorityRole {name: 'คณะกรรมการสวัสดิการในสถานประกอบการ'}) ON CREATE SET auth.id = 'ROLE_AUTH_7', auth.category = 'Committee', auth.description = 'ปรึกษาหารือและเสนอแนะสวัสดิการร่วมกับนายจ้าง';
MERGE (auth:AuthorityRole {name: 'เจ้าหน้าที่ความปลอดภัยในการทำงาน (จป.)'}) ON CREATE SET auth.id = 'ROLE_AUTH_8', auth.category = 'Safety', auth.description = 'ดูแลความปลอดภัย อาชีวอนามัย และสภาพแวดล้อมในการทำงาน';
MERGE (auth:AuthorityRole {name: 'แพทย์แผนปัจจุบันชั้นหนึ่ง'}) ON CREATE SET auth.id = 'ROLE_AUTH_9', auth.category = 'Medical', auth.description = 'ออกใบรับรองแพทย์รับรองการเจ็บป่วย';
MERGE (auth:AuthorityRole {name: 'ผู้จัดการสายงาน / ผู้จัดการฝ่าย'}) ON CREATE SET auth.id = 'ROLE_AUTH_10', auth.category = 'Managerial', auth.description = 'ประเมินผลการปฏิบัติงานและการทดลองงาน';

// --- 2. Required Documents & Certifications ---
MERGE (d:DocumentRequired {name: 'ใบรับรองแพทย์'}) ON CREATE SET d.id = 'DOC_1', d.purpose = 'การลาป่วย / การตรวจสุขภาพ', d.source_pages = '[8, 9, 14, 39]';
MERGE (d:DocumentRequired {name: 'สำเนาบัตรประจำตัวประชาชน'}) ON CREATE SET d.id = 'DOC_2', d.purpose = 'หลักฐานการสมัคร / ข้อมูลพนักงาน', d.source_pages = '[8]';
MERGE (d:DocumentRequired {name: 'สำเนาทะเบียนบ้าน'}) ON CREATE SET d.id = 'DOC_3', d.purpose = 'หลักฐานการสมัคร / ข้อมูลพนักงาน', d.source_pages = '[8, 9]';
MERGE (d:DocumentRequired {name: 'สำเนาหลักฐานการศึกษา'}) ON CREATE SET d.id = 'DOC_4', d.purpose = 'หลักฐานการสมัครงาน', d.source_pages = '[8, 23]';
MERGE (d:DocumentRequired {name: 'สำเนาทะเบียนสมรส'}) ON CREATE SET d.id = 'DOC_5', d.purpose = 'สวัสดิการสมรส / สิทธิประโยชน์', d.source_pages = '[9]';
MERGE (d:DocumentRequired {name: 'ใบเสร็จรับเงินค่ารักษาพยาบาล'}) ON CREATE SET d.id = 'DOC_6', d.purpose = 'การเบิกจ่ายสวัสดิการรักษาพยาบาล', d.source_pages = '[39]';
MERGE (d:DocumentRequired {name: 'หนังสือยื่นคำร้องทุกข์'}) ON CREATE SET d.id = 'DOC_7', d.purpose = 'กระบวนการร้องทุกข์', d.source_pages = '[32]';
MERGE (d:DocumentRequired {name: 'หนังสือตักเตือนเป็นลายลักษณ์อักษร'}) ON CREATE SET d.id = 'DOC_8', d.purpose = 'การลงโทษทางวินัย', d.source_pages = '[31]';
MERGE (d:DocumentRequired {name: 'คำสั่งพักงานทางวินัย'}) ON CREATE SET d.id = 'DOC_9', d.purpose = 'การลงโทษทางวินัย', d.source_pages = '[31]';
MERGE (d:DocumentRequired {name: 'หนังสือแจ้งความประสงค์ขอลาออก'}) ON CREATE SET d.id = 'DOC_10', d.purpose = 'การพ้นสภาพการเป็นพนักงาน', d.source_pages = '[10]';

// --- 3. Timeline, SLA & Duration Rules ---
MERGE (t:TimelineRule {id: 'TIME_PROBATION_119'}) ON CREATE SET t.duration = 119, t.unit = 'วัน', t.description = 'ระยะเวลาทดลองงานสูงสุดตามกฎหมาย', t.chapter = 2 WITH t MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_PERSONAL_DATA_15'}) ON CREATE SET t.duration = 15, t.unit = 'วัน', t.description = 'แจ้งเปลี่ยนแปลงสถานภาพส่วนบุคคลต่อบริษัท', t.chapter = 2 WITH t MATCH (c:Chapter {chapter_number: 2}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_MAX_WORK_WEEK_48'}) ON CREATE SET t.duration = 48, t.unit = 'ชั่วโมง', t.description = 'ชั่วโมงทำงานปกติสูงสุดต่อสัปดาห์', t.chapter = 3 WITH t MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_REST_BREAK_1'}) ON CREATE SET t.duration = 1, t.unit = 'ชั่วโมง', t.description = 'เวลาพักระหว่างวันทำงานปกติไม่น้อยกว่า', t.chapter = 3 WITH t MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_REST_DAY_1'}) ON CREATE SET t.duration = 1, t.unit = 'วัน', t.description = 'วันหยุดประจำสัปดาห์ติดต่อกันไม่น้อยกว่า', t.chapter = 3 WITH t MATCH (c:Chapter {chapter_number: 3}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_TRADITION_HOLIDAY_13'}) ON CREATE SET t.duration = 13, t.unit = 'วัน', t.description = 'วันหยุดตามประเพณีไม่น้อยกว่าต่อปี', t.chapter = 5 WITH t MATCH (c:Chapter {chapter_number: 5}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_SICK_LEAVE_MED_3'}) ON CREATE SET t.duration = 3, t.unit = 'วันทำงาน', t.description = 'ลาป่วยตั้งแต่จำนวนวันขึ้นไปต้องมีใบรับรองแพทย์', t.chapter = 4 WITH t MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_MATERNITY_98'}) ON CREATE SET t.duration = 98, t.unit = 'วัน', t.description = 'สิทธิการลาเพื่อคลอดบุตร (รวมวันหยุด)', t.chapter = 4 WITH t MATCH (c:Chapter {chapter_number: 4}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_GRIEVANCE_SUBMIT_7'}) ON CREATE SET t.duration = 7, t.unit = 'วัน', t.description = 'กำหนดยื่นคำร้องทุกข์นับจากเกิดเหตุ', t.chapter = 9 WITH t MATCH (c:Chapter {chapter_number: 9}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_GRIEVANCE_INVESTIGATE_14'}) ON CREATE SET t.duration = 14, t.unit = 'วัน', t.description = 'กรอบเวลาไต่สวนคำร้องทุกข์', t.chapter = 9 WITH t MATCH (c:Chapter {chapter_number: 9}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_GRIEVANCE_APPEAL_7'}) ON CREATE SET t.duration = 7, t.unit = 'วัน', t.description = 'กรอบเวลายื่นอุทธรณ์คำร้องทุกข์', t.chapter = 9 WITH t MATCH (c:Chapter {chapter_number: 9}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_GRIEVANCE_DECIDE_14'}) ON CREATE SET t.duration = 14, t.unit = 'วัน', t.description = 'กรอบเวลาการชี้ขาดอุทธรณ์คำร้องทุกข์', t.chapter = 9 WITH t MATCH (c:Chapter {chapter_number: 9}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_RESIGN_NOTICE_30'}) ON CREATE SET t.duration = 30, t.unit = 'วัน', t.description = 'ยื่นหนังสือลาออกล่วงหน้าก่อนวันพ้นสภาพ', t.chapter = 10 WITH t MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_SUSPENSION_MAX_7'}) ON CREATE SET t.duration = 7, t.unit = 'วัน', t.description = 'โทษพักงานทางวินัยไม่จ่ายค่าจ้างสูงสุด', t.chapter = 8 WITH t MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_ABSENT_MISCONDUCT_3'}) ON CREATE SET t.duration = 3, t.unit = 'วันทำการ', t.description = 'ละทิ้งหน้าที่ติดต่อกันโดยไม่มีเหตุสมควรเข้าข่ายความผิดร้ายแรง', t.chapter = 8 WITH t MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_WARNING_VALIDITY_365'}) ON CREATE SET t.duration = 365, t.unit = 'วัน', t.description = 'อายุความของหนังสือเตือนทางวินัย (1 ปี)', t.chapter = 8 WITH t MATCH (c:Chapter {chapter_number: 8}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_PAYROLL_END_MONTH'}) ON CREATE SET t.duration = 1, t.unit = 'เดือน', t.description = 'กำหนดจ่ายค่าจ้างในวันทำการสุดท้ายของเดือน', t.chapter = 7 WITH t MATCH (c:Chapter {chapter_number: 7}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);
MERGE (t:TimelineRule {id: 'TIME_RETIRE_AGE_60'}) ON CREATE SET t.duration = 60, t.unit = 'ปี', t.description = 'เกณฑ์เกษียณอายุการทำงานของพนักงาน', t.chapter = 10 WITH t MATCH (c:Chapter {chapter_number: 10}) MERGE (c)-[:ENFORCES_TIMELINE]->(t);

// --- 4. Cross-Chapter & Semantic Connections ---
MATCH (d:DocumentRequired {name: 'ใบรับรองแพทย์'}), (l:LeaveType {id: 'LEAVE_SICK'}) MERGE (l)-[:REQUIRES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'สำเนาสูติบัตรบุตร'}), (l:LeaveType {id: 'LEAVE_MATERNITY'}) MERGE (l)-[:REQUIRES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'สำเนามรณบัตร'}), (l:LeaveType {id: 'LEAVE_BEREAVEMENT'}) MERGE (l)-[:REQUIRES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'แบบฟอร์มการยื่นขอลางาน'}), (l:LeaveType {id: 'LEAVE_ANNUAL'}) MERGE (l)-[:REQUIRES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'แบบฟอร์มการยื่นขอลางาน'}), (l:LeaveType {id: 'LEAVE_BUSINESS'}) MERGE (l)-[:REQUIRES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'แบบฟอร์มการยื่นขอลางาน'}), (l:LeaveType {id: 'LEAVE_SICK'}) MERGE (l)-[:REQUIRES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'แบบฟอร์มการยื่นขอลางาน'}), (l:LeaveType {id: 'LEAVE_STERILIZATION'}) MERGE (l)-[:REQUIRES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'แบบฟอร์มการยื่นขอลางาน'}), (l:LeaveType {id: 'LEAVE_MILITARY'}) MERGE (l)-[:REQUIRES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'แบบฟอร์มการยื่นขอลางาน'}), (l:LeaveType {id: 'LEAVE_MONK'}) MERGE (l)-[:REQUIRES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'สำเนาบัตรประจำตัวประชาชน'}), (c:Chapter {chapter_number: 2}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'สำเนาทะเบียนบ้าน'}), (c:Chapter {chapter_number: 2}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'สำเนาหลักฐานการศึกษา'}), (c:Chapter {chapter_number: 2}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'หนังสือค้ำประกันการทำงาน'}), (c:Chapter {chapter_number: 2}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'แบบประเมินผลการทดลองงาน'}), (c:Chapter {chapter_number: 2}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'แบบฟอร์มขออนุมัติทำงานล่วงเวลา (OT)'}), (c:Chapter {chapter_number: 6}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'หนังสือตักเตือนเป็นลายลักษณ์อักษร'}), (c:Chapter {chapter_number: 8}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'คำสั่งพักงานทางวินัย'}), (c:Chapter {chapter_number: 8}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'หนังสือยื่นคำร้องทุกข์'}), (c:Chapter {chapter_number: 9}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'หนังสือแจ้งความประสงค์ขอลาออก'}), (c:Chapter {chapter_number: 10}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'หนังสือบอกเลิกจ้าง'}), (c:Chapter {chapter_number: 10}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'แบบฟอร์มการส่งมอบงานและทรัพย์สิน'}), (c:Chapter {chapter_number: 10}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'ใบสมัครกองทุนสำรองเลี้ยงชีพ (PVD)'}), (c:Chapter {chapter_number: 11}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (d:DocumentRequired {name: 'ใบเสร็จรับเงินค่ารักษาพยาบาล'}), (c:Chapter {chapter_number: 11}) MERGE (c)-[:MANDATES_DOCUMENT]->(d);
MATCH (a:AuthorityRole {name: 'ผู้บังคับบัญชาชั้นต้น'}), (p:DisciplinaryPenalty {level: 1}) MERGE (a)-[:AUTHORIZED_PENALTY {action: 'ตักเตือนด้วยวาจา'}]->(p);
MATCH (a:AuthorityRole {name: 'ผู้บังคับบัญชาชั้นต้น'}), (p:DisciplinaryPenalty {level: 2}) MERGE (a)-[:AUTHORIZED_PENALTY {action: 'ตักเตือนเป็นหนังสือ'}]->(p);
MATCH (a:AuthorityRole {name: 'ผู้จัดการฝ่ายทรัพยากรบุคคล'}), (p:DisciplinaryPenalty {level: 2}) MERGE (a)-[:AUTHORIZED_PENALTY {action: 'ตักเตือนเป็นหนังสือ'}]->(p);
MATCH (a:AuthorityRole {name: 'ผู้จัดการฝ่ายทรัพยากรบุคคล'}), (p:DisciplinaryPenalty {level: 3}) MERGE (a)-[:AUTHORIZED_PENALTY {action: 'สั่งพักงานไม่เกิน 7 วัน'}]->(p);
MATCH (a:AuthorityRole {name: 'ประธานเจ้าหน้าที่บริหาร'}), (p:DisciplinaryPenalty {level: 4}) MERGE (a)-[:AUTHORIZED_PENALTY {action: 'เลิกจ้างโดยไม่จ่ายค่าชดเชย'}]->(p);
MATCH (a:AuthorityRole {name: 'กรรมการผู้จัดการ'}), (p:DisciplinaryPenalty {level: 4}) MERGE (a)-[:AUTHORIZED_PENALTY {action: 'เลิกจ้างโดยไม่จ่ายค่าชดเชย'}]->(p);
MATCH (t:TimelineRule {id: 'TIME_ABSENT_MISCONDUCT_3'}), (m:Misconduct) WHERE m.name_th CONTAINS 'ขาดงาน' OR m.name_th CONTAINS 'ละทิ้ง' MERGE (m)-[:TRIGGERS_AFTER]->(t);
MATCH (t:TimelineRule {id: 'TIME_SICK_LEAVE_MED_3'}), (l:LeaveType {id: 'LEAVE_SICK'}) MERGE (l)-[:THRESHOLD_CONDITION]->(t);
MATCH (t:TimelineRule {id: 'TIME_RESIGN_NOTICE_30'}), (c:Chapter {chapter_number: 10}) MERGE (c)-[:REQUIRES_ADVANCE_NOTICE]->(t);
MATCH (c1:Chapter {chapter_number: 2}), (c2:Chapter {chapter_number: 10}) MERGE (c1)-[:GOVERNS_LIFECYCLE {description: 'การว่าจ้างจนถึงการพ้นสภาพ'}]->(c2);
MATCH (c1:Chapter {chapter_number: 3}), (c2:Chapter {chapter_number: 6}) MERGE (c1)-[:REGULATES_WORKING_HOURS {description: 'เวลาทำงานปกติสัมพันธ์กับการทำงานล่วงเวลา'}]->(c2);
MATCH (c1:Chapter {chapter_number: 4}), (c2:Chapter {chapter_number: 8}) MERGE (c1)-[:NON_COMPLIANCE_PENALTY {description: 'การละเมิดระเบียบวันลานำไปสู่โทษทางวินัย'}]->(c2);
MATCH (c1:Chapter {chapter_number: 8}), (c2:Chapter {chapter_number: 10}) MERGE (c1)-[:DISCIPLINARY_DISMISSAL {description: 'ความผิดวินัยร้ายแรงนำไปสู่การเลิกจ้าง ม.119'}]->(c2);
MATCH (c1:Chapter {chapter_number: 9}), (c2:Chapter {chapter_number: 8}) MERGE (c1)-[:PROTECTS_EMPLOYEE_RIGHTS {description: 'การร้องทุกข์เพื่อคัดค้านคำสั่งทางวินัยที่ไม่เป็นธรรม'}]->(c2);
MATCH (c1:Chapter {chapter_number: 11}), (c2:Chapter {chapter_number: 10}) MERGE (c1)-[:BENEFIT_TERMINATION {description: 'การสิ้นสุดสิทธิประโยชน์เมื่อพ้นสภาพการเป็นพนักงาน'}]->(c2);