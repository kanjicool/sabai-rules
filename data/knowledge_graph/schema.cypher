// ==========================================================
// Sabai-Rules Knowledge Graph Schema & Constraints
// Company: Primo Service Solution Co., Ltd. (Origin Property Group)
// Document: ข้อบังคับเกี่ยวกับการทำงาน (47 หน้า)
// ==========================================================

// --- Unique Constraints for Entity Integrity ---
CREATE CONSTRAINT unique_employee_level IF NOT EXISTS
FOR (e:EmployeeLevel) REQUIRE e.id IS UNIQUE;

CREATE CONSTRAINT unique_position IF NOT EXISTS
FOR (p:Position) REQUIRE p.title IS UNIQUE;

CREATE CONSTRAINT unique_benefit IF NOT EXISTS
FOR (b:Benefit) REQUIRE b.id IS UNIQUE;

CREATE CONSTRAINT unique_leave_type IF NOT EXISTS
FOR (l:LeaveType) REQUIRE l.id IS UNIQUE;

CREATE CONSTRAINT unique_document IF NOT EXISTS
FOR (d:DocumentRequired) REQUIRE d.name IS UNIQUE;

CREATE CONSTRAINT unique_pvd_rule IF NOT EXISTS
FOR (p:PVDRule) REQUIRE p.tenure_id IS UNIQUE;

CREATE CONSTRAINT unique_severance_rule IF NOT EXISTS
FOR (s:SeveranceRule) REQUIRE s.tier_id IS UNIQUE;

CREATE CONSTRAINT unique_policy_clause IF NOT EXISTS
FOR (c:PolicyClause) REQUIRE c.clause_id IS UNIQUE;

// --- Performance Indexes for Fast Multi-hop Lookup ---
CREATE INDEX idx_employee_level_num IF NOT EXISTS
FOR (e:EmployeeLevel) ON (e.level_number);

CREATE INDEX idx_benefit_category IF NOT EXISTS
FOR (b:Benefit) ON (b.category);

CREATE INDEX idx_leave_category IF NOT EXISTS
FOR (l:LeaveType) ON (l.category);
