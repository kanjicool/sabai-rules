"""Deterministic Cypher Query Service for HR Benefits & Regulations."""

import logging
from typing import Any
from src.graph.connection import Neo4jConnection

logger = logging.getLogger(__name__)


class Neo4jBenefitQuerier:
    """Service to execute structured, multi-hop Cypher queries against the HR graph."""

    def __init__(self, connection: Neo4jConnection | None = None):
        self.conn = connection or Neo4jConnection()

    def resolve_level(self, query_str: str) -> dict[str, Any] | None:
        """Resolves a query term (e.g. 'Senior', 'Manager', 'ช่าง', 'Level 3') to an EmployeeLevel."""
        clean_query = query_str.strip().lower()

        # 1. Check if user specified a level number directly (e.g. 'Level 3', 'ระดับ 4', '3')
        if any(kw in clean_query for kw in ["level", "lvl", "ระดับ"]):
            num_str = "".join(c for c in clean_query if c.isdigit())
            if num_str and 1 <= int(num_str) <= 9:
                q = """
                MATCH (l:EmployeeLevel {level_number: $lvl_num})
                OPTIONAL MATCH (l)-[:HAS_POSITION]->(p:Position)
                RETURN l.id AS id, l.level_number AS level_number, l.name AS name,
                       l.category AS category, collect(p.title) AS positions
                """
                res = self.conn.execute_query(q, {"lvl_num": int(num_str)})
                if res:
                    return res[0]

        # 2. Check exact position title match or stripped title match (e.g. 'Vice President' matching 'Vice President (VP)')
        q_exact = """
        MATCH (l:EmployeeLevel)-[:HAS_POSITION]->(p:Position)
        WHERE toLower(p.title) = $term 
           OR (p.name_th IS NOT NULL AND toLower(p.name_th) = $term)
           OR toLower(trim(split(p.title, '(')[0])) = $term
        WITH l
        OPTIONAL MATCH (l)-[:HAS_POSITION]->(p2:Position)
        RETURN l.id AS id, l.level_number AS level_number, l.name AS name,
               l.category AS category, collect(p2.title) AS positions
        ORDER BY l.level_number ASC
        LIMIT 1
        """
        res_exact = self.conn.execute_query(q_exact, {"term": clean_query})
        if res_exact:
            return res_exact[0]

        # 3. Check exact level name match (case-insensitive)
        q_lvl_exact = """
        MATCH (l:EmployeeLevel)
        WHERE toLower(l.name) = $term
           OR toLower(trim(split(l.name, '(')[0])) = $term
        OPTIONAL MATCH (l)-[:HAS_POSITION]->(p2:Position)
        RETURN l.id AS id, l.level_number AS level_number, l.name AS name,
               l.category AS category, collect(p2.title) AS positions
        LIMIT 1
        """
        res_lvl_exact = self.conn.execute_query(q_lvl_exact, {"term": clean_query})
        if res_lvl_exact:
            return res_lvl_exact[0]

        # 4. Check position contains query term
        q_pos_contains = """
        MATCH (l:EmployeeLevel)-[:HAS_POSITION]->(p:Position)
        WHERE toLower(p.title) CONTAINS $term OR (p.name_th IS NOT NULL AND p.name_th CONTAINS $term)
        WITH l
        ORDER BY l.level_number ASC
        OPTIONAL MATCH (l)-[:HAS_POSITION]->(p2:Position)
        RETURN l.id AS id, l.level_number AS level_number, l.name AS name,
               l.category AS category, collect(p2.title) AS positions
        LIMIT 1
        """
        res_pos = self.conn.execute_query(q_pos_contains, {"term": clean_query})
        if res_pos:
            return res_pos[0]

        # 5. Check level name contains query term
        q_lvl_contains = """
        MATCH (l:EmployeeLevel)
        WHERE toLower(l.name) CONTAINS $term
        OPTIONAL MATCH (l)-[:HAS_POSITION]->(p2:Position)
        RETURN l.id AS id, l.level_number AS level_number, l.name AS name,
               l.category AS category, collect(p2.title) AS positions
        ORDER BY l.level_number ASC
        LIMIT 1
        """
        res_lvl = self.conn.execute_query(q_lvl_contains, {"term": clean_query})
        return res_lvl[0] if res_lvl else None

    def get_benefits_summary_for_level(self, query_term: str) -> dict[str, Any]:
        """Returns comprehensive benefits overview for a specific role or level."""
        level_info = self.resolve_level(query_term)
        if not level_info:
            return {"error": f"Role or level '{query_term}' could not be resolved."}

        level_id = level_info["id"]

        query = """
        MATCH (l:EmployeeLevel {id: $level_id})
        // 1. Annual Leave
        OPTIONAL MATCH (l)-[rel_leave:ENTITLED_LEAVE]->(lv:LeaveType {id: 'ANNUAL_LEAVE'})
        // 2. Dental Condition
        OPTIONAL MATCH (l)-[:ELIGIBLE_FOR]->(c_den:BenefitCondition)<-[:HAS_POLICY]-(b_den:Benefit {id: 'DENTAL_BENEFIT'})
        // 3. Hospital Visit Condition
        OPTIONAL MATCH (l)-[:ELIGIBLE_FOR]->(c_vis:BenefitCondition)<-[:HAS_POLICY]-(b_vis:Benefit {id: 'HOSPITAL_VISIT_GIFT'})
        // 4. Executive Parking
        OPTIONAL MATCH (l)-[:ELIGIBLE_FOR_PARKING]->(b_park:Benefit)
        // 5. OT Exemption
        OPTIONAL MATCH (l)-[:EXEMPT_FROM_OT]->(ot:OvertimePolicy)
        // 6. Attendance Fingerprint Scan
        OPTIONAL MATCH (l)-[:SUBJECT_TO_ATTENDANCE]->(att:AttendanceRule)
        RETURN
            l.level_number AS level_number,
            l.name AS level_name,
            l.category AS category,
            rel_leave.days_per_year AS annual_leave_days,
            c_den.amount AS dental_benefit_thb,
            c_den.cycle AS dental_cycle,
            c_vis.amount AS hospital_visit_thb,
            (b_park IS NOT NULL) AS has_executive_parking,
            (ot IS NOT NULL) AS is_exempt_from_ot,
            (att IS NOT NULL) AS must_fingerprint_scan
        """
        records = self.conn.execute_query(query, {"level_id": level_id})
        if not records:
            return level_info

        res = records[0]
        res["resolved_positions"] = level_info.get("positions", [])
        return res

    def get_all_leave_types_and_rules(self) -> list[dict[str, Any]]:
        """Returns all recognized leave types, advance notice days, and required documents."""
        query = """
        MATCH (lv:LeaveType)
        OPTIONAL MATCH (lv)-[:REQUIRES_DOC]->(d:DocumentRequired)
        RETURN lv.id AS leave_id,
               lv.name_th AS leave_name,
               lv.chapter AS chapter,
               lv.pages AS pages,
               lv.max_paid_days AS max_paid_days,
               lv.advance_notice_days AS advance_notice_days,
               collect(d.name) AS required_documents
        ORDER BY lv.chapter, lv.name_th
        """
        return self.conn.execute_query(query)

    def get_leave_details(self, leave_keyword: str) -> list[dict[str, Any]]:
        """Finds details of a specific leave type (e.g. 'ลาป่วย', 'พักร้อน', 'ลาบวช')."""
        query = """
        MATCH (lv:LeaveType)
        WHERE toLower(lv.id) CONTAINS toLower($kw)
           OR lv.name_th CONTAINS $kw
        OPTIONAL MATCH (lv)-[:REQUIRES_DOC]->(d:DocumentRequired)
        RETURN lv.id AS id,
               lv.name_th AS name_th,
               lv.chapter AS chapter,
               lv.pages AS pages,
               lv.max_paid_days AS max_paid_days,
               lv.advance_notice_days AS advance_notice_days,
               lv.notice_timing AS notice_timing,
               lv.medical_cert_rule AS medical_cert_rule,
               lv.carry_over_rule AS carry_over_rule,
               collect(d.name) AS required_documents
        """
        return self.conn.execute_query(query, {"kw": leave_keyword.strip()})

    def get_pvd_rules(self, tenure_years: float | None = None) -> dict[str, Any]:
        """Calculates employee contribution options and employer vesting percentage based on tenure."""
        query = """
        MATCH (b:Benefit {id: 'PROVIDENT_FUND'})-[:HAS_PVD_TIER]->(r:PVDRule)
        RETURN r.tenure_id AS tenure_id,
               r.min_tenure_years AS min_years,
               r.max_tenure_years AS max_years,
               r.employee_rates AS allowed_employee_rates,
               r.employer_vesting_rate AS employer_vesting_rate
        ORDER BY r.min_tenure_years
        """
        tiers = self.conn.execute_query(query)
        result: dict[str, Any] = {
            "benefit_name": "กองทุนสำรองเลี้ยงชีพภาคสมัครใจ (Primo / Origin Property Group)",
            "all_tiers": tiers,
        }

        if tenure_years is not None:
            # Match specific tier
            matched_tier = None
            for t in tiers:
                if t["min_years"] <= tenure_years < t["max_years"]:
                    matched_tier = t
                    break
            if not matched_tier and tiers:
                matched_tier = tiers[-1]

            # Employer payout vesting rule
            vesting_pct = "100%"
            if tenure_years < 1.0:
                vesting_pct = "0% (อายุงานน้อยกว่า 1 ปี ไม่ได้รับส่วนเงินสมทบนายจ้าง)"
            elif 1.0 <= tenure_years <= 3.0:
                vesting_pct = "50% (อายุงาน 1-3 ปี ได้รับเงินสมทบนายจ้าง 50%)"
            else:
                vesting_pct = "100% (อายุงานมากกว่า 3 ปี ได้รับเงินสมทบนายจ้าง 100%)"

            result["tenure_inquired_years"] = tenure_years
            result["applicable_tier"] = matched_tier
            result["calculated_employer_vesting"] = vesting_pct
            result["employee_contribution_refund"] = "100% ของเงินสะสมส่วนพนักงานและผลประโยชน์สุทธิคืนแก่สมาชิกเสมอ"

        return result

    def get_severance_eligibility(self, tenure_months: int) -> dict[str, Any]:
        """Calculates legal severance pay entitlement days under Chapter 10 of Primo regulations."""
        tenure_days = tenure_months * 30
        tenure_years = tenure_months / 12.0

        query = """
        MATCH (s:SeveranceRule)
        WHERE s.short_notice_penalty_days IS NULL
        RETURN s.tier_id AS tier_id,
               s.min_days AS min_days,
               s.min_years AS min_years,
               s.max_years AS max_years,
               s.payout_days AS payout_days,
               s.desc AS description
        ORDER BY s.payout_days
        """
        rules = self.conn.execute_query(query)

        payout_days = 0
        matched_desc = "อายุงานน้อยกว่า 120 วัน ไม่ได้รับค่าชดเชยตามกฎหมาย"

        if tenure_days >= 120 and tenure_years < 1.0:
            payout_days = 30
            matched_desc = "ทำงานครบ 120 วันแต่ไม่ครบ 1 ปี ได้รับค่าชดเชย 30 วัน"
        elif 1.0 <= tenure_years < 3.0:
            payout_days = 90
            matched_desc = "ทำงานครบ 1 ปีแต่ไม่ครบ 3 ปี ได้รับค่าชดเชย 90 วัน"
        elif 3.0 <= tenure_years < 6.0:
            payout_days = 180
            matched_desc = "ทำงานครบ 3 ปีแต่ไม่ครบ 6 ปี ได้รับค่าชดเชย 180 วัน"
        elif 6.0 <= tenure_years < 10.0:
            payout_days = 240
            matched_desc = "ทำงานครบ 6 ปีแต่ไม่ครบ 10 ปี ได้รับค่าชดเชย 240 วัน"
        elif tenure_years >= 10.0:
            payout_days = 300
            matched_desc = "ทำงานครบ 10 ปีขึ้นไป ได้รับค่าชดเชย 300 วัน"

        return {
            "tenure_months": tenure_months,
            "tenure_years": round(tenure_years, 2),
            "entitled_severance_days": payout_days,
            "rule_description": matched_desc,
            "chapter_reference": "หมวด 10 การเลิกจ้างและค่าชดเชย (หน้า 35-37)"
        }

    def get_funeral_benefit(self, relationship_keyword: str) -> dict[str, Any]:
        """Retrieves funeral grant details based on relationship."""
        query = """
        MATCH (b:Benefit {id: 'FUNERAL_ASSISTANCE'})-[:HAS_POLICY]->(c:BenefitCondition)
        OPTIONAL MATCH (b)-[:REQUIRES_DOC]->(d:DocumentRequired)
        RETURN c.target AS target,
               c.amount AS cash_assistance_thb,
               c.host_nights AS host_nights,
               c.wreaths AS wreaths,
               collect(d.name) AS required_docs
        """
        all_policies = self.conn.execute_query(query)
        kw = relationship_keyword.strip().lower()

        matched = []
        for p in all_policies:
            if kw in p["target"].lower():
                matched.append(p)

        return {
            "query": relationship_keyword,
            "matched_policies": matched or all_policies,
            "reference": "หมวด 11 ผลประโยชน์และสวัสดิการ ข้อ 6 (หน้า 40-41)"
        }
