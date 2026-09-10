// ==============================================================================
// Primo Service Solution Co., Ltd. (Origin Property Group)
// Complete Knowledge Graph Seed File (47-Page HR Regulations & Benefits)
// ==============================================================================

// --- Step 0: Clean existing Primo HR nodes to prevent orphaned duplicates ---
MATCH (n)
WHERE n:EmployeeLevel
   OR n:Position
   OR n:Benefit
   OR n:LeaveType
   OR n:DocumentRequired
   OR n:PVDRule
   OR n:SeveranceRule
   OR n:PolicyClause
   OR n:Company
   OR n:BenefitCondition
   OR n:OvertimePolicy
   OR n:AttendanceRule
   OR n:DisciplinaryPenalty
   OR n:GrievanceProcedure
DETACH DELETE n;

// --- Step 1: Company Profile ---
MERGE (c:Company {id: 'PRIMO_SERVICE_SOLUTION'})
ON CREATE SET
    c.name_th = 'บริษัท พรีโม เซอร์วิส โซลูชั่น จำกัด',
    c.name_en = 'Primo Service Solution Co., Ltd.',
    c.parent_company = 'บริษัท ออริจิ้น พร็อพเพอร์ตี้ จำกัด (มหาชน)',
    c.address = '496 หมู่ 9 ตำบลสำโรงเหนือ อำเภอเมืองสมุทรปราการ จังหวัดสมุทรปราการ 10270',
    c.business_type = 'Service',
    c.effective_date = '2018-07-01';

// --- Step 2: Employee Levels (1-9) ---
MERGE (:EmployeeLevel {id: 'LEVEL_1', level_number: 1, name: 'Operation', category: 'Operational'});
MERGE (:EmployeeLevel {id: 'LEVEL_2', level_number: 2, name: 'Officer / Executive', category: 'Staff'});
MERGE (:EmployeeLevel {id: 'LEVEL_3', level_number: 3, name: 'Senior / Assistant Manager / Supervisor', category: 'Senior Staff'});
MERGE (:EmployeeLevel {id: 'LEVEL_4', level_number: 4, name: 'Manager / Senior Manager', category: 'Management'});
MERGE (:EmployeeLevel {id: 'LEVEL_5', level_number: 5, name: 'Assistant Vice President (AVP) / AM / GM', category: 'Management'});
MERGE (:EmployeeLevel {id: 'LEVEL_6', level_number: 6, name: 'Vice President (VP)', category: 'Executive'});
MERGE (:EmployeeLevel {id: 'LEVEL_7', level_number: 7, name: 'Senior Vice President (SVP) / MD BU', category: 'Executive'});
MERGE (:EmployeeLevel {id: 'LEVEL_8', level_number: 8, name: 'Executive Vice President (EVP) / Group MD', category: 'Executive'});
MERGE (:EmployeeLevel {id: 'LEVEL_9', level_number: 9, name: 'Chief Executive Officer (CEO)', category: 'Top Executive'});

// --- Step 3: Positions & Map to Levels ---
MERGE (l:EmployeeLevel {id: 'LEVEL_1'}) MERGE (p:Position {title: 'Technician'}) ON CREATE SET p.name_th = 'ช่างซ่อมบำรุง' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_1'}) MERGE (p:Position {title: 'Maid'}) ON CREATE SET p.name_th = 'แม่บ้าน' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_1'}) MERGE (p:Position {title: 'Driver'}) ON CREATE SET p.name_th = 'พนักงานขับรถ' MERGE (l)-[:HAS_POSITION]->(p);

MERGE (l:EmployeeLevel {id: 'LEVEL_2'}) MERGE (p:Position {title: 'Officer'}) ON CREATE SET p.name_th = 'เจ้าหน้าที่' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_2'}) MERGE (p:Position {title: 'Executive (Sales)'}) ON CREATE SET p.name_th = 'เจ้าหน้าที่ฝ่ายขาย' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_2'}) MERGE (p:Position {title: 'Building Officer'}) ON CREATE SET p.name_th = 'เจ้าหน้าที่บริหารอาคาร' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_2'}) MERGE (p:Position {title: 'Operation Supervisor'}) ON CREATE SET p.name_th = 'หัวหน้างานปฏิบัติการ' MERGE (l)-[:HAS_POSITION]->(p);

MERGE (l:EmployeeLevel {id: 'LEVEL_3'}) MERGE (p:Position {title: 'Senior'}) ON CREATE SET p.name_th = 'เจ้าหน้าที่อาวุโส' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_3'}) MERGE (p:Position {title: 'Assistant Manager'}) ON CREATE SET p.name_th = 'ผู้ช่วยผู้จัดการ' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_3'}) MERGE (p:Position {title: 'Supervisor'}) ON CREATE SET p.name_th = 'หัวหน้างาน' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_3'}) MERGE (p:Position {title: 'Building Manager'}) ON CREATE SET p.name_th = 'ผู้จัดการอาคาร' MERGE (l)-[:HAS_POSITION]->(p);

MERGE (l:EmployeeLevel {id: 'LEVEL_4'}) MERGE (p:Position {title: 'Manager'}) ON CREATE SET p.name_th = 'ผู้จัดการ' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_4'}) MERGE (p:Position {title: 'Senior Manager'}) ON CREATE SET p.name_th = 'ผู้จัดการอาวุโส' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_4'}) MERGE (p:Position {title: 'Senior Building Manager'}) ON CREATE SET p.name_th = 'ผู้จัดการอาคารอาวุโส' MERGE (l)-[:HAS_POSITION]->(p);

MERGE (l:EmployeeLevel {id: 'LEVEL_5'}) MERGE (p:Position {title: 'Assistant Vice President (AVP)'}) ON CREATE SET p.name_th = 'ผู้ช่วยรองกรรมการผู้จัดการ' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_5'}) MERGE (p:Position {title: 'Area Manager (AM)'}) ON CREATE SET p.name_th = 'ผู้จัดการเขต' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_5'}) MERGE (p:Position {title: 'Senior Area Manager (SAM)'}) ON CREATE SET p.name_th = 'ผู้จัดการเขตอาวุโส' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_5'}) MERGE (p:Position {title: 'GM Business Unit'}) ON CREATE SET p.name_th = 'ผู้จัดการทั่วไปหน่วยธุรกิจ' MERGE (l)-[:HAS_POSITION]->(p);

MERGE (l:EmployeeLevel {id: 'LEVEL_6'}) MERGE (p:Position {title: 'Vice President (VP)'}) ON CREATE SET p.name_th = 'รองกรรมการผู้จัดการ' MERGE (l)-[:HAS_POSITION]->(p);

MERGE (l:EmployeeLevel {id: 'LEVEL_7'}) MERGE (p:Position {title: 'Senior Vice President (SVP)'}) ON CREATE SET p.name_th = 'รองกรรมการผู้จัดการอาวุโส' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_7'}) MERGE (p:Position {title: 'MD Business Unit'}) ON CREATE SET p.name_th = 'กรรมการผู้จัดการหน่วยธุรกิจ' MERGE (l)-[:HAS_POSITION]->(p);

MERGE (l:EmployeeLevel {id: 'LEVEL_8'}) MERGE (p:Position {title: 'Group Managing Director (MD)'}) ON CREATE SET p.name_th = 'กรรมการผู้จัดการกลุ่มบริษัท' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_8'}) MERGE (p:Position {title: 'Executive Vice President (EVP)'}) ON CREATE SET p.name_th = 'รองประธานเจ้าหน้าที่บริหาร' MERGE (l)-[:HAS_POSITION]->(p);
MERGE (l:EmployeeLevel {id: 'LEVEL_8'}) MERGE (p:Position {title: 'Senior Executive Vice President (SEVP)'}) ON CREATE SET p.name_th = 'รองประธานเจ้าหน้าที่บริหารอาวุโส' MERGE (l)-[:HAS_POSITION]->(p);

MERGE (l:EmployeeLevel {id: 'LEVEL_9'}) MERGE (p:Position {title: 'Chief Executive Officer (CEO)'}) ON CREATE SET p.name_th = 'ประธานเจ้าหน้าที่บริหาร' MERGE (l)-[:HAS_POSITION]->(p);

// --- Step 4: Documents Required ---
MERGE (:DocumentRequired {name: 'ใบรับรองแพทย์แผนปัจจุบันชั้นหนึ่ง (ต้นฉบับ)', timing: 'ยื่นเมื่อกลับเข้าทำงานวันแรก หรือตามที่บริษัทกำหนด'});
MERGE (:DocumentRequired {name: 'แบบฟอร์มใบลาตามแบบของบริษัท', timing: 'ยื่นล่วงหน้าตามเกณฑ์ หรือภายใน 2 ชั่วโมงหลังเริ่มงานวันแรกที่กลับมา'});
MERGE (:DocumentRequired {name: 'หนังสือรับรองการอุปสมบท (ใบสุทธิ)', timing: 'ยื่นต่อเจ้าหน้าที่ฝ่ายบุคคลในวันที่กลับมาปฏิบัติงาน'});
MERGE (:DocumentRequired {name: 'หนังสือตอบรับการเข้าฝึกอบรมและรายละเอียดหลักสูตร', timing: 'ยื่นล่วงหน้าไม่น้อยกว่า 7 วัน'});
MERGE (:DocumentRequired {name: 'หมายเรียกตัวเข้ารับราชการทหาร', timing: 'แจ้งบริษัทภายใน 7 วันนับจากวันที่ได้รับหมายเรียก'});
MERGE (:DocumentRequired {name: 'ใบเสร็จรับเงินและใบรับรองแพทย์จากสถานพยาบาล', timing: 'ยื่นต่อฝ่ายทรัพยากรบุคคลเพื่อเบิกเงินคืนกรณีรักษานอกเครือข่าย'});
MERGE (:DocumentRequired {name: 'มรณบัตรและเอกสารพิสูจน์ความสัมพันธ์', timing: 'ยื่นต่อฝ่ายทรัพยากรบุคคลเพื่อขอรับเงินช่วยเหลือ'});

// --- Step 5: Leave Types & Linking ---
// 5.1 Annual Leave (วันหยุดพักผ่อนประจำปี)
MERGE (lv_annual:LeaveType {id: 'ANNUAL_LEAVE'})
ON CREATE SET
    lv_annual.name_th = 'วันหยุดพักผ่อนประจำปี',
    lv_annual.chapter = 5,
    lv_annual.pages = '18-19',
    lv_annual.min_tenure_years = 1,
    lv_annual.advance_notice_days = 7,
    lv_annual.min_days_per_request = 1,
    lv_annual.carry_over_rule = 'สะสมวันลาที่ไม่ได้ใช้ได้ 1 รอบปีปฏิทินถัดไป',
    lv_annual.approval_required = 'ต้องได้รับอนุมัติเป็นลายลักษณ์อักษรจากผู้บังคับบัญชาก่อน มิฉะนั้นถือว่าขาดงานละทิ้งหน้าที่';

MERGE (lv_annual:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (d_form:DocumentRequired {name: 'แบบฟอร์มใบลาตามแบบของบริษัท'}) MERGE (lv_annual)-[:REQUIRES_DOC]->(d_form);

// Link Annual Leave Entitlements
MERGE (l1:EmployeeLevel {id: 'LEVEL_1'}) MERGE (lv:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (l1)-[:ENTITLED_LEAVE {days_per_year: 6}]->(lv);
MERGE (l2:EmployeeLevel {id: 'LEVEL_2'}) MERGE (lv:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (l2)-[:ENTITLED_LEAVE {days_per_year: 6}]->(lv);
MERGE (l3:EmployeeLevel {id: 'LEVEL_3'}) MERGE (lv:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (l3)-[:ENTITLED_LEAVE {days_per_year: 7}]->(lv);
MERGE (l4:EmployeeLevel {id: 'LEVEL_4'}) MERGE (lv:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (l4)-[:ENTITLED_LEAVE {days_per_year: 7}]->(lv);
MERGE (l5:EmployeeLevel {id: 'LEVEL_5'}) MERGE (lv:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (l5)-[:ENTITLED_LEAVE {days_per_year: 7}]->(lv);
MERGE (l6:EmployeeLevel {id: 'LEVEL_6'}) MERGE (lv:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (l6)-[:ENTITLED_LEAVE {days_per_year: 8}]->(lv);
MERGE (l7:EmployeeLevel {id: 'LEVEL_7'}) MERGE (lv:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (l7)-[:ENTITLED_LEAVE {days_per_year: 8}]->(lv);
MERGE (l8:EmployeeLevel {id: 'LEVEL_8'}) MERGE (lv:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (l8)-[:ENTITLED_LEAVE {days_per_year: 8}]->(lv);
MERGE (l9:EmployeeLevel {id: 'LEVEL_9'}) MERGE (lv:LeaveType {id: 'ANNUAL_LEAVE'}) MERGE (l9)-[:ENTITLED_LEAVE {days_per_year: 10}]->(lv);

// 5.2 Sick Leave (ลาป่วย)
MERGE (lv_sick:LeaveType {id: 'SICK_LEAVE'})
ON CREATE SET
    lv_sick.name_th = 'ลาป่วย',
    lv_sick.chapter = 4,
    lv_sick.pages = '14-15',
    lv_sick.max_paid_days = 30,
    lv_sick.min_hours_per_request = 4,
    lv_sick.notice_timing = 'แจ้งภายใน 2 ชั่วโมงแรกของเวลาทำงานปกติในวันแรกที่หยุด',
    lv_sick.submission_timing = 'ยื่นใบลาภายใน 2 ชั่วโมงหลังจากเริ่มงานในวันแรกที่กลับเข้าทำงาน',
    lv_sick.medical_cert_rule = 'ลาป่วยตั้งแต่ 3 วันทำงานขึ้นไป (มีวันหยุดคั่นหรือไม่ก็ตาม) ต้องมีใบรับรองแพทย์แผนปัจจุบันชั้นหนึ่งฉบับจริง',
    lv_sick.penalty = 'การลาป่วยเท็จถือเป็นความผิดร้ายแรงฐานทุจริต ลงโทษทางวินัยขั้นร้ายแรงหรือเลิกจ้างไม่จ่ายค่าชดเชย';

MERGE (lv:LeaveType {id: 'SICK_LEAVE'}) MERGE (d:DocumentRequired {name: 'ใบรับรองแพทย์แผนปัจจุบันชั้นหนึ่ง (ต้นฉบับ)'}) MERGE (lv)-[:REQUIRES_DOC]->(d);
MERGE (lv:LeaveType {id: 'SICK_LEAVE'}) MERGE (d:DocumentRequired {name: 'แบบฟอร์มใบลาตามแบบของบริษัท'}) MERGE (lv)-[:REQUIRES_DOC]->(d);

// 5.3 Maternity Leave (ลาเพื่อคลอดบุตร)
MERGE (lv_mat:LeaveType {id: 'MATERNITY_LEAVE'})
ON CREATE SET
    lv_mat.name_th = 'ลาเพื่อคลอดบุตร',
    lv_mat.chapter = 4,
    lv_mat.pages = '15',
    lv_mat.max_total_days = 90,
    lv_mat.paid_days = 45,
    lv_mat.unpaid_additional_days = 30,
    lv_mat.advance_notice_days = 30,
    lv_mat.special_rights = 'พนักงานหญิงมีครรภ์มีสิทธิขอเปลี่ยนงานในหน้าที่ชั่วคราวก่อนหรือหลังคลอดได้ตามความเห็นแพทย์';

MERGE (lv:LeaveType {id: 'MATERNITY_LEAVE'}) MERGE (d:DocumentRequired {name: 'แบบฟอร์มใบลาตามแบบของบริษัท'}) MERGE (lv)-[:REQUIRES_DOC]->(d);

// 5.4 Sterilization Leave (ลาเพื่อทำหมัน)
MERGE (lv_steril:LeaveType {id: 'STERILIZATION_LEAVE'})
ON CREATE SET
    lv_steril.name_th = 'ลาเพื่อทำหมัน',
    lv_steril.chapter = 4,
    lv_steril.pages = '15',
    lv_steril.is_paid = true,
    lv_steril.advance_notice_days = 7,
    lv_steril.duration_rule = 'ตามระยะเวลาที่แพทย์แผนปัจจุบันชั้นหนึ่งกำหนด';

MERGE (lv:LeaveType {id: 'STERILIZATION_LEAVE'}) MERGE (d:DocumentRequired {name: 'ใบรับรองแพทย์แผนปัจจุบันชั้นหนึ่ง (ต้นฉบับ)'}) MERGE (lv)-[:REQUIRES_DOC]->(d);

// 5.5 Military Leave (ลารับราชการทหาร)
MERGE (lv_mil:LeaveType {id: 'MILITARY_LEAVE'})
ON CREATE SET
    lv_mil.name_th = 'ลาเพื่อรับราชการทหาร (เรียกพล ฝึกวิชาทหาร หรือทดสอบความพรั่งพร้อม)',
    lv_mil.chapter = 4,
    lv_mil.pages = '16',
    lv_mil.max_paid_days = 60,
    lv_mil.advance_notice_days = 30,
    lv_mil.notice_within_days = 7,
    lv_mil.return_within_days = 3,
    lv_mil.drafted_rule = 'กรณีถูกเกณฑ์ทหารจะต้องลาออกจากการเป็นพนักงาน';

MERGE (lv:LeaveType {id: 'MILITARY_LEAVE'}) MERGE (d:DocumentRequired {name: 'หมายเรียกตัวเข้ารับราชการทหาร'}) MERGE (lv)-[:REQUIRES_DOC]->(d);

// 5.6 Training Leave (ลาเพื่อฝึกอบรม)
MERGE (lv_train:LeaveType {id: 'TRAINING_LEAVE'})
ON CREATE SET
    lv_train.name_th = 'ลาเพื่อการฝึกอบรมหรือพัฒนาความรู้ความสามารถ',
    lv_train.chapter = 4,
    lv_train.pages = '16',
    lv_train.is_paid = false,
    lv_train.max_days = 30,
    lv_train.max_times = 3,
    lv_train.advance_notice_days = 7,
    lv_train.probation_required = true;

MERGE (lv:LeaveType {id: 'TRAINING_LEAVE'}) MERGE (d:DocumentRequired {name: 'หนังสือตอบรับการเข้าฝึกอบรมและรายละเอียดหลักสูตร'}) MERGE (lv)-[:REQUIRES_DOC]->(d);

// 5.7 Ordination Leave (ลาเพื่ออุปสมบท)
MERGE (lv_ord:LeaveType {id: 'ORDINATION_LEAVE'})
ON CREATE SET
    lv_ord.name_th = 'ลาเพื่ออุปสมบท',
    lv_ord.chapter = 4,
    lv_ord.pages = '17',
    lv_ord.max_days = 15,
    lv_ord.is_paid = true,
    lv_ord.lifetime_limit = 'สามารถลาได้เพียงครั้งเดียวตลอดอายุการทำงาน',
    lv_ord.probation_required = true,
    lv_ord.condition = 'ต้องใช้สิทธิลาหยุดพักผ่อนประจำปีก่อน ส่วนที่เหลือเป็นลากิจที่บริษัทพิจารณาอนุมัติ';

MERGE (lv:LeaveType {id: 'ORDINATION_LEAVE'}) MERGE (d:DocumentRequired {name: 'หนังสือรับรองการอุปสมบท (ใบสุทธิ)'}) MERGE (lv)-[:REQUIRES_DOC]->(d);

// 5.8 Special Compassionate Leaves
MERGE (:LeaveType {id: 'COMPASSIONATE_FUNERAL_LEAVE', name_th: 'ลาเพื่อจัดพิธีฌาปนกิจศพ (บิดา มารดา คู่สมรส พี่น้อง บุตร)', chapter: 4, pages: '17', max_paid_days: 5, advance_notice_days: 1});
MERGE (:LeaveType {id: 'MARRIAGE_LEAVE', name_th: 'ลาเพื่อประกอบพิธีสมรสของพนักงาน', chapter: 4, pages: '17', max_paid_days: 3, advance_notice_days: 15});
MERGE (:LeaveType {id: 'DISASTER_LEAVE', name_th: 'ลาเนื่องจากภัยพิบัติทางธรรมชาติ (อัคคีภัย อุทกภัย บ้านเสียหายเกินครึ่ง)', chapter: 4, pages: '17', max_paid_days: 3});

// --- Step 6: Benefits & Conditions ---
// 6.1 Dental Benefit (ค่าทันตกรรม - หน้า 45)
MERGE (b_den:Benefit {id: 'DENTAL_BENEFIT'})
ON CREATE SET
    b_den.name_th = 'สวัสดิการค่าทันตกรรม',
    b_den.chapter = 11,
    b_den.pages = '45',
    b_den.probation_required = true,
    b_den.covered_items = 'ขูดหินปูน, อุดฟัน, ถอนฟัน, ผ่าฟันคุด, รักษารากฟัน, เอ็กซเรย์ฟัน, ครอบฟัน, เคลือบฟลูออไรด์, ทำฟันปลอม',
    b_den.excluded_items = 'การจัดฟัน, การขัดหรือฟอกสีฟัน';

MERGE (c_den_1_3:BenefitCondition {id: 'DENTAL_TIER_L1_3', amount: 3000, currency: 'THB', cycle: 'year', desc: 'Operation - Senior, Supervisor, Assistant Manager (ระดับ 1-3)'});
MERGE (c_den_4_7:BenefitCondition {id: 'DENTAL_TIER_L4_7', amount: 4000, currency: 'THB', cycle: 'year', desc: 'Manager - SVP (ระดับ 4-7)'});
MERGE (c_den_8_9:BenefitCondition {id: 'DENTAL_TIER_L8_9', amount: 6000, currency: 'THB', cycle: 'year', desc: 'EVP up - CEO (ระดับ 8-9)'});

MERGE (b_den:Benefit {id: 'DENTAL_BENEFIT'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L1_3'}) MERGE (b_den)-[:HAS_POLICY]->(c);
MERGE (b_den:Benefit {id: 'DENTAL_BENEFIT'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L4_7'}) MERGE (b_den)-[:HAS_POLICY]->(c);
MERGE (b_den:Benefit {id: 'DENTAL_BENEFIT'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L8_9'}) MERGE (b_den)-[:HAS_POLICY]->(c);

MERGE (l:EmployeeLevel {id: 'LEVEL_1'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L1_3'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_2'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L1_3'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_3'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L1_3'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_4'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L4_7'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_5'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L4_7'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_6'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L4_7'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_7'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L4_7'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_8'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L8_9'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_9'}) MERGE (c:BenefitCondition {id: 'DENTAL_TIER_L8_9'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);

// 6.2 Hospital Visit Gift (ของเยี่ยมผู้ป่วย - หน้า 40)
MERGE (b_vis:Benefit {id: 'HOSPITAL_VISIT_GIFT'})
ON CREATE SET
    b_vis.name_th = 'ของเยี่ยมผู้ป่วยใน (IPD พัก 1 คืนขึ้นไป)',
    b_vis.chapter = 11,
    b_vis.pages = '40',
    b_vis.condition = 'เจ็บป่วยและเข้ารับการรักษาตัวในโรงพยาบาลเป็นผู้ป่วยใน 1 คืนขึ้นไป';

MERGE (c_vis_1_5:BenefitCondition {id: 'VISIT_TIER_L1_5', amount: 700, currency: 'THB', cycle: 'per_event', desc: 'Operation - AVP (ระดับ 1-5)'});
MERGE (c_vis_6_9:BenefitCondition {id: 'VISIT_TIER_L6_9', amount: 1000, currency: 'THB', cycle: 'per_event', desc: 'VP UP (ระดับ 6-9)'});

MERGE (b_vis:Benefit {id: 'HOSPITAL_VISIT_GIFT'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L1_5'}) MERGE (b_vis)-[:HAS_POLICY]->(c);
MERGE (b_vis:Benefit {id: 'HOSPITAL_VISIT_GIFT'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L6_9'}) MERGE (b_vis)-[:HAS_POLICY]->(c);

MERGE (l:EmployeeLevel {id: 'LEVEL_1'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L1_5'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_2'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L1_5'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_3'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L1_5'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_4'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L1_5'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_5'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L1_5'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_6'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L6_9'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_7'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L6_9'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_8'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L6_9'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);
MERGE (l:EmployeeLevel {id: 'LEVEL_9'}) MERGE (c:BenefitCondition {id: 'VISIT_TIER_L6_9'}) MERGE (l)-[:ELIGIBLE_FOR]->(c);

// 6.3 Funeral Assistance (เงินช่วยเหลืองานศพ - หน้า 40-41)
MERGE (b_fun:Benefit {id: 'FUNERAL_ASSISTANCE'})
ON CREATE SET
    b_fun.name_th = 'เงินช่วยเหลืองานศพและสวัสดิการเจ้าภาพ',
    b_fun.chapter = 11,
    b_fun.pages = '40-41';

MERGE (c_fun_emp:BenefitCondition {id: 'FUNERAL_EMPLOYEE', amount: 10000, host_nights: 1, wreaths: 1, target: 'กรณีพนักงานเสียชีวิต'});
MERGE (c_fun_fam:BenefitCondition {id: 'FUNERAL_DIRECT_FAMILY', amount: 5000, host_nights: 1, wreaths: 1, target: 'กรณีบิดา มารดา บุตร สามี ภรรยา ของพนักงานเสียชีวิต'});
MERGE (c_fun_gr:BenefitCondition {id: 'FUNERAL_GRANDPARENTS', amount: 3000, host_nights: 0, wreaths: 1, target: 'กรณีปู่ย่าและตายายของพนักงานเสียชีวิต'});

MERGE (b_fun:Benefit {id: 'FUNERAL_ASSISTANCE'}) MERGE (c:BenefitCondition {id: 'FUNERAL_EMPLOYEE'}) MERGE (b_fun)-[:HAS_POLICY]->(c);
MERGE (b_fun:Benefit {id: 'FUNERAL_ASSISTANCE'}) MERGE (c:BenefitCondition {id: 'FUNERAL_DIRECT_FAMILY'}) MERGE (b_fun)-[:HAS_POLICY]->(c);
MERGE (b_fun:Benefit {id: 'FUNERAL_ASSISTANCE'}) MERGE (c:BenefitCondition {id: 'FUNERAL_GRANDPARENTS'}) MERGE (b_fun)-[:HAS_POLICY]->(c);

MERGE (d_death:DocumentRequired {name: 'มรณบัตรและเอกสารพิสูจน์ความสัมพันธ์'})
MERGE (b_fun:Benefit {id: 'FUNERAL_ASSISTANCE'}) MERGE (b_fun)-[:REQUIRES_DOC]->(d_death);

// 6.4 Group Health Insurance (ประกันสุขภาพกลุ่ม - หน้า 38-39)
MERGE (b_hlth:Benefit {id: 'GROUP_HEALTH_INSURANCE'})
ON CREATE SET
    b_hlth.name_th = 'ประกันสุขภาพกลุ่ม (ผู้ป่วยใน IPD และ ผู้ป่วยนอก OPD)',
    b_hlth.chapter = 11,
    b_hlth.pages = '38-39',
    b_hlth.probation_required = true,
    b_hlth.ipd_network_rule = 'โรงพยาบาลในเครือข่าย: ยื่นบัตรประกันสุขภาพ ไม่ต้องสำรองจ่าย จ่ายเฉพาะส่วนเกิน',
    b_hlth.ipd_non_network_rule = 'นอกเครือข่าย: สำรองจ่ายก่อน แล้วนำใบเสร็จรับเงินและใบรับรองแพทย์มาเบิกคืนที่ HR',
    b_hlth.opd_network_rule = 'ในเครือข่าย: ไม่เสียค่าใช้จ่ายตามวงเงินประกันตามตำแหน่งงาน',
    b_hlth.post_employment_rule = 'คุ้มครองเฉพาะขณะมีสภาพพนักงาน ลาออกต้องคืนบัตรทันที หากนำไปใช้จะเรียกเก็บเงินคืนทุกกรณี';

MERGE (d_rec:DocumentRequired {name: 'ใบเสร็จรับเงินและใบรับรองแพทย์จากสถานพยาบาล'})
MERGE (b_hlth:Benefit {id: 'GROUP_HEALTH_INSURANCE'}) MERGE (b_hlth)-[:REQUIRES_DOC]->(d_rec);

// 6.5 Childbirth Gift (ของขวัญการมีบุตร - หน้า 40)
MERGE (:Benefit {id: 'CHILDBIRTH_GIFT', name_th: 'ของขวัญการมีบุตรของพนักงาน', chapter: 11, pages: '40', gift_value: 1500, cash_amount: 1500, total_value: 3000, condition: 'พนักงานที่เป็นบิดาหรือมารดาที่ให้กำเนิดบุตรโดยชอบด้วยกฎหมาย'});

// 6.6 Birthday Gift (วันเกิด - หน้า 40)
MERGE (:Benefit {id: 'BIRTHDAY_GIFT', name_th: 'สวัสดิการวันเกิดพนักงาน', chapter: 11, pages: '40', desc: 'จัดหาของขวัญเนื่องในวันเกิดและกิจกรรมอวยพรวันเกิดตามความเหมาะสม'});

// 6.7 Annual Health Checkup (ตรวจสุขภาพประจำปี - หน้า 39-40)
MERGE (:Benefit {id: 'ANNUAL_HEALTH_CHECKUP', name_th: 'การตรวจสุขภาพประจำปี', chapter: 11, pages: '39-40', frequency: 'ปีละ 1 ครั้ง โดยโรงพยาบาลที่บริษัทประสานงาน', exemption: 'พนักงานที่ตรวจสุขภาพก่อนเริ่มงานหรือตรวจเองนับถึงวันตรวจน้อยกว่า 3 เดือน ไม่จำเป็นต้องตรวจ'});

// 6.8 Provident Fund (กองทุนสำรองเลี้ยงชีพ PVD - หน้า 41-43)
MERGE (b_pvd:Benefit {id: 'PROVIDENT_FUND'})
ON CREATE SET
    b_pvd.name_th = 'กองทุนสำรองเลี้ยงชีพภาคสมัครใจ',
    b_pvd.chapter = 11,
    b_pvd.pages = '41-43',
    b_pvd.eligibility = 'พนักงานประจำที่ได้รับการบรรจุ หรือกรณีพิเศษที่คณะกรรมการอนุมัติ',
    b_pvd.resignation_reapply_wait_years = 1,
    b_pvd.transferable = true,
    b_pvd.employee_refund_rate = '100% ของเงินสะสมและผลประโยชน์สุทธิคืนแก่พนักงานเมื่อสิ้นสุดสมาชิกภาพ';

MERGE (pvd1:PVDRule {tenure_id: 'PVD_TENURE_UNDER_3Y', min_tenure_years: 0.0, max_tenure_years: 3.0, employee_rates: [2, 3], employer_vesting_rate: '50% (หากอายุงาน 1-3 ปี), 0% (หากอายุงาน < 1 ปี)'});
MERGE (pvd2:PVDRule {tenure_id: 'PVD_TENURE_3_TO_5Y', min_tenure_years: 3.0, max_tenure_years: 5.0, employee_rates: [2, 3, 5], employer_vesting_rate: '100%'});
MERGE (pvd3:PVDRule {tenure_id: 'PVD_TENURE_5Y_UP', min_tenure_years: 5.0, max_tenure_years: 99.0, employee_rates: [2, 3, 5, 7], employer_vesting_rate: '100%'});

MERGE (b_pvd:Benefit {id: 'PROVIDENT_FUND'}) MERGE (p:PVDRule {tenure_id: 'PVD_TENURE_UNDER_3Y'}) MERGE (b_pvd)-[:HAS_PVD_TIER]->(p);
MERGE (b_pvd:Benefit {id: 'PROVIDENT_FUND'}) MERGE (p:PVDRule {tenure_id: 'PVD_TENURE_3_TO_5Y'}) MERGE (b_pvd)-[:HAS_PVD_TIER]->(p);
MERGE (b_pvd:Benefit {id: 'PROVIDENT_FUND'}) MERGE (p:PVDRule {tenure_id: 'PVD_TENURE_5Y_UP'}) MERGE (b_pvd)-[:HAS_PVD_TIER]->(p);

// 6.9 Real Estate Discount (ส่วนลดซื้ออสังหาริมทรัพย์ - หน้า 45-46)
MERGE (:Benefit {
    id: 'REAL_ESTATE_DISCOUNT',
    name_th: 'ส่วนลดของพนักงานในการซื้ออสังหาริมทรัพย์ในเครือออริจิ้น',
    chapter: 11,
    pages: '45-46',
    quota_units_per_project: 2,
    presale_booking_contract_discount: '1.5%',
    presale_transfer_discount: '1.5%',
    presale_total_discount: '3.0%',
    ready_to_move_in_discount: '3.0%',
    presale_refund_condition: 'จ่ายเงินงวดดาวน์ครบ 12 เดือน สามารถขอคืนห้องให้แก่บริษัทได้',
    default_penalty: 'ค้างงวดดาวน์ 3 งวดติดต่อกัน บริษัทขอสงวนสิทธิ์ยกเลิกสัญญาและริบเงินที่ชำระมาแล้วทั้งหมด'
});

// 6.10 Telephone SIM Card (ค่าโทรศัพท์ - หน้า 46)
MERGE (:Benefit {id: 'TELEPHONE_SIM', name_th: 'สวัสดิการค่าโทรศัพท์ (SIM การ์ด)', chapter: 11, pages: '46', desc: 'มอบ SIM สำหรับพนักงานเพื่อความสะดวกรวดเร็วในการประสานงาน'});

// 6.11 Executive Parking (ที่จอดรถสำหรับผู้บริหาร - หน้า 46)
MERGE (b_park:Benefit {id: 'EXECUTIVE_PARKING', name_th: 'ที่จอดรถสำหรับผู้บริหาร', chapter: 11, pages: '46', min_level: 6, location: 'สำนักงานใหญ่ (มอบบัตรที่จอดรถหรือบัตรคูปอง)'});

MERGE (l:EmployeeLevel {id: 'LEVEL_6'}) MERGE (b:Benefit {id: 'EXECUTIVE_PARKING'}) MERGE (l)-[:ELIGIBLE_FOR_PARKING]->(b);
MERGE (l:EmployeeLevel {id: 'LEVEL_7'}) MERGE (b:Benefit {id: 'EXECUTIVE_PARKING'}) MERGE (l)-[:ELIGIBLE_FOR_PARKING]->(b);
MERGE (l:EmployeeLevel {id: 'LEVEL_8'}) MERGE (b:Benefit {id: 'EXECUTIVE_PARKING'}) MERGE (l)-[:ELIGIBLE_FOR_PARKING]->(b);
MERGE (l:EmployeeLevel {id: 'LEVEL_9'}) MERGE (b:Benefit {id: 'EXECUTIVE_PARKING'}) MERGE (l)-[:ELIGIBLE_FOR_PARKING]->(b);

// 6.12 Uniforms (ชุดฟอร์มพนักงาน - หน้า 44)
MERGE (:Benefit {id: 'UNIFORM', name_th: 'ชุดฟอร์มพนักงาน', chapter: 11, pages: '44', office_service_rule: 'แม่บ้านและพนักงานรับส่งเอกสาร สวมใส่ขณะปฏิบัติงานทุกวัน', maintenance_rule: 'เจ้าหน้าที่ซ่อมบำรุง สวมใส่ขณะปฏิบัติงานทุกวัน'});

// 6.13 Office Refreshments & First Aid (อาหารเครื่องดื่มและเวชภัณฑ์ - หน้า 44)
MERGE (:Benefit {id: 'REFRESHMENT_FIRST_AID', name_th: 'สวัสดิการอาหาร เครื่องดื่ม ขนม และเวชภัณฑ์ยารักษาโรค', chapter: 11, pages: '44'});

// --- Step 7: Overtime & Attendance Rules (หมวด 3, 6, 7) ---
MERGE (ot:OvertimePolicy {
    id: 'OT_HOLIDAY_RULES',
    normal_ot_multiplier: 1.5,
    holiday_work_monthly_multiplier: 1.0,
    holiday_work_daily_multiplier: 2.0,
    holiday_ot_multiplier: 3.0,
    hourly_rate_formula: 'เงินเดือนหารด้วยผลคูณของสามสิบและจำนวนชั่วโมงทำงานต่อวันโดยเฉลี่ย (Salary / (30 * NormalHours))',
    exempt_roles: 'พนักงานซึ่งมีตำแหน่งระดับผู้จัดการแผนกขึ้นไป (ระดับ 4 ขึ้นไป) ไม่มีสิทธิได้รับค่าล่วงเวลาและค่าทำงานในวันหยุด เว้นแต่ดุลยพินิจ CEO เป็นกรณีพิเศษ'
});

MERGE (l:EmployeeLevel {id: 'LEVEL_4'}) MERGE (ot:OvertimePolicy {id: 'OT_HOLIDAY_RULES'}) MERGE (l)-[:EXEMPT_FROM_OT]->(ot);
MERGE (l:EmployeeLevel {id: 'LEVEL_5'}) MERGE (ot:OvertimePolicy {id: 'OT_HOLIDAY_RULES'}) MERGE (l)-[:EXEMPT_FROM_OT]->(ot);
MERGE (l:EmployeeLevel {id: 'LEVEL_6'}) MERGE (ot:OvertimePolicy {id: 'OT_HOLIDAY_RULES'}) MERGE (l)-[:EXEMPT_FROM_OT]->(ot);
MERGE (l:EmployeeLevel {id: 'LEVEL_7'}) MERGE (ot:OvertimePolicy {id: 'OT_HOLIDAY_RULES'}) MERGE (l)-[:EXEMPT_FROM_OT]->(ot);
MERGE (l:EmployeeLevel {id: 'LEVEL_8'}) MERGE (ot:OvertimePolicy {id: 'OT_HOLIDAY_RULES'}) MERGE (l)-[:EXEMPT_FROM_OT]->(ot);
MERGE (l:EmployeeLevel {id: 'LEVEL_9'}) MERGE (ot:OvertimePolicy {id: 'OT_HOLIDAY_RULES'}) MERGE (l)-[:EXEMPT_FROM_OT]->(ot);

MERGE (att:AttendanceRule {
    id: 'FINGERPRINT_SCAN_RULE',
    scope: 'พนักงานตั้งแต่ระดับ 4 (Manager, Senior Manager) ลงมา มีหน้าที่ต้องสแกนลายนิ้วมือเข้า-ออก',
    late_threshold_minutes: 10,
    grace_period_desc: 'บันทึกเวลาเข้างานภายในไม่เกิน 10 นาทีของเวลาเข้างาน หากเกิน 10 นาทีถือว่ามาสาย'
});

MERGE (l:EmployeeLevel {id: 'LEVEL_1'}) MERGE (att:AttendanceRule {id: 'FINGERPRINT_SCAN_RULE'}) MERGE (l)-[:SUBJECT_TO_ATTENDANCE]->(att);
MERGE (l:EmployeeLevel {id: 'LEVEL_2'}) MERGE (att:AttendanceRule {id: 'FINGERPRINT_SCAN_RULE'}) MERGE (l)-[:SUBJECT_TO_ATTENDANCE]->(att);
MERGE (l:EmployeeLevel {id: 'LEVEL_3'}) MERGE (att:AttendanceRule {id: 'FINGERPRINT_SCAN_RULE'}) MERGE (l)-[:SUBJECT_TO_ATTENDANCE]->(att);
MERGE (l:EmployeeLevel {id: 'LEVEL_4'}) MERGE (att:AttendanceRule {id: 'FINGERPRINT_SCAN_RULE'}) MERGE (l)-[:SUBJECT_TO_ATTENDANCE]->(att);

// --- Step 8: Severance Pay Rules (หมวด 10 หน้า 35-37) ---
MERGE (:SeveranceRule {tier_id: 'SEV_120D_TO_1Y', min_days: 120, max_years: 1.0, payout_days: 30, desc: 'ทำงานครบ 120 วัน แต่ไม่ครบ 1 ปี ได้รับค่าชดเชยไม่น้อยกว่าค่าจ้าง 30 วัน'});
MERGE (:SeveranceRule {tier_id: 'SEV_1Y_TO_3Y', min_years: 1.0, max_years: 3.0, payout_days: 90, desc: 'ทำงานครบ 1 ปี แต่ไม่ครบ 3 ปี ได้รับค่าชดเชยไม่น้อยกว่าค่าจ้าง 90 วัน'});
MERGE (:SeveranceRule {tier_id: 'SEV_3Y_TO_6Y', min_years: 3.0, max_years: 6.0, payout_days: 180, desc: 'ทำงานครบ 3 ปี แต่ไม่ครบ 6 ปี ได้รับค่าชดเชยไม่น้อยกว่าค่าจ้าง 180 วัน'});
MERGE (:SeveranceRule {tier_id: 'SEV_6Y_TO_10Y', min_years: 6.0, max_years: 10.0, payout_days: 240, desc: 'ทำงานครบ 6 ปี แต่ไม่ครบ 10 ปี ได้รับค่าชดเชยไม่น้อยกว่าค่าจ้าง 240 วัน'});
MERGE (:SeveranceRule {tier_id: 'SEV_10Y_UP', min_years: 10.0, max_years: 99.0, payout_days: 300, desc: 'ทำงานครบ 10 ปีขึ้นไป ได้รับค่าชดเชยไม่น้อยกว่าค่าจ้าง 300 วัน'});
MERGE (:SeveranceRule {tier_id: 'SEV_TECH_AUTOMATION_SPECIAL', advance_notice_days: 60, short_notice_penalty_days: 60, tenure_6y_plus_bonus: 'ทำงานเกิน 6 ปี จ่ายค่าชดเชยพิเศษเพิ่ม 15 วันต่อปีที่เกิน 6 ปี รวมสูงสุดไม่เกิน 360 วัน'});

// --- Step 9: Disciplinary Penalties (หมวด 8 หน้า 30) ---
MERGE (:DisciplinaryPenalty {level: 1, name: 'การตักเตือนด้วยวาจา โดยบันทึกเป็นหนังสือไว้เป็นหลักฐาน'});
MERGE (:DisciplinaryPenalty {level: 2, name: 'การตักเตือนเป็นหนังสือ (มีผลบังคับไม่เกิน 1 ปี)'});
MERGE (:DisciplinaryPenalty {level: 3, name: 'พักงานโดยไม่จ่ายค่าจ้าง (ระหว่างสอบสวนไม่เกิน 7 วัน)'});
MERGE (:DisciplinaryPenalty {level: 4, name: 'เลิกจ้างโดยไม่จ่ายค่าชดเชย'});

// --- Step 10: Grievance Procedure (หมวด 9 หน้า 32-33) ---
MERGE (:GrievanceProcedure {
    id: 'GRIEVANCE_TIMELINE',
    initial_filing_days: 7,
    supervisor_resolution_days: 14,
    appeal_filing_days: 7,
    executive_resolution_days: 14,
    ruling_nature: 'คำวินิจฉัยของผู้บังคับบัญชาระดับบริหารถือเป็นอันสิ้นสุด'
});
