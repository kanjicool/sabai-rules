"""Interactive and Automated Verification of Primo Knowledge Graph."""

import sys
from tabulate import tabulate
from src.graph.connection import Neo4jConnection
from src.graph.queries import Neo4jBenefitQuerier

# Ensure UTF-8 output in Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def print_section(title: str) -> None:
    print("\n" + "=" * 75)
    print(f"  {title}")
    print("=" * 75)


def verify_database_stats(conn: Neo4jConnection) -> None:
    print_section("1. Graph Database Overview & Counts")
    node_query = """
    MATCH (n)
    RETURN labels(n)[0] AS Label, count(n) AS Count
    ORDER BY Count DESC
    """
    rel_query = """
    MATCH ()-[r]->()
    RETURN type(r) AS RelationshipType, count(r) AS Count
    ORDER BY Count DESC
    """
    labels_table = conn.execute_query(node_query)
    rels_table = conn.execute_query(rel_query)

    print("\n[Node Distribution]")
    print(tabulate(labels_table, headers="keys", tablefmt="fancy_grid"))

    print("\n[Relationship Distribution]")
    print(tabulate(rels_table, headers="keys", tablefmt="fancy_grid"))


def verify_scenario_role_entitlements(querier: Neo4jBenefitQuerier) -> None:
    print_section("2. Scenario 1: Multi-Role Entitlement Verification")
    test_roles = ["Operation", "Senior", "Manager", "Vice President", "CEO"]
    rows = []

    for role in test_roles:
        res = querier.get_benefits_summary_for_level(role)
        rows.append({
            "Query Role": role,
            "Level": f"L{res.get('level_number')}",
            "Category": res.get("category"),
            "Annual Leave": f"{res.get('annual_leave_days')} วัน",
            "Dental (THB/yr)": f"{res.get('dental_benefit_thb'):,} บ.",
            "Inpatient Visit": f"{res.get('hospital_visit_thb'):,} บ.",
            "OT Exempt?": "✅ ใช่ (งด OT)" if res.get("is_exempt_from_ot") else "❌ ไม่ (ได้ OT)",
            "Exec Parking?": "✅ มีสิทธิ์" if res.get("has_executive_parking") else "❌ ไม่มี",
            "Scan Fingerprint?": "✅ ต้องสแกน" if res.get("must_fingerprint_scan") else "❌ ไม่ต้อง"
        })

    print(tabulate(rows, headers="keys", tablefmt="fancy_grid"))


def verify_scenario_pvd(querier: Neo4jBenefitQuerier) -> None:
    print_section("3. Scenario 2: Provident Fund (PVD) Rule Calculations")
    tenure_cases = [0.5, 2.0, 4.0, 7.0]
    pvd_rows = []

    for years in tenure_cases:
        pvd_res = querier.get_pvd_rules(years)
        tier = pvd_res.get("applicable_tier") or {}
        pvd_rows.append({
            "Tenure Inquired": f"{years} ปี",
            "Allowed Savings %": str(tier.get("allowed_employee_rates", [])),
            "Employer Match Payout Vesting": pvd_res.get("calculated_employer_vesting"),
            "Employee Savings Refund": "100% เสมอ"
        })

    print(tabulate(pvd_rows, headers="keys", tablefmt="fancy_grid"))


def verify_scenario_severance(querier: Neo4jBenefitQuerier) -> None:
    print_section("4. Scenario 3: Legal Severance Pay Calculation (Chapter 10)")
    cases_months = [3, 8, 24, 48, 96, 150]
    sev_rows = []

    for m in cases_months:
        s = querier.get_severance_eligibility(m)
        sev_rows.append({
            "Tenure (Months)": f"{m} เดือน ({s['tenure_years']} ปี)",
            "Severance Days": f"{s['entitled_severance_days']} วัน",
            "Rule Summary": s["rule_description"]
        })

    print(tabulate(sev_rows, headers="keys", tablefmt="fancy_grid"))


def verify_scenario_leave_types(querier: Neo4jBenefitQuerier) -> None:
    print_section("5. Scenario 4: Leave Types, Advance Notice & Required Documents")
    leaves = querier.get_all_leave_types_and_rules()
    rows = []
    for lv in leaves:
        rows.append({
            "Leave ID": lv["leave_id"],
            "Leave Name": lv["leave_name"],
            "Paid Days": lv["max_paid_days"] if lv["max_paid_days"] is not None else "ตามเกณฑ์",
            "Advance Notice": f"{lv['advance_notice_days']} วัน" if lv["advance_notice_days"] is not None else "ตามเวลา",
            "Required Documents": "\n".join(lv["required_documents"]) if lv["required_documents"] else "-"
        })
    print(tabulate(rows, headers="keys", tablefmt="fancy_grid"))


def run_all_verifications() -> bool:
    conn = Neo4jConnection()
    if not conn.verify_connectivity():
        print("❌ Cannot connect to Neo4j database.")
        return False

    querier = Neo4jBenefitQuerier(conn)
    verify_database_stats(conn)
    verify_scenario_role_entitlements(querier)
    verify_scenario_pvd(querier)
    verify_scenario_severance(querier)
    verify_scenario_leave_types(querier)

    print("\n✅ ALL GRAPH VERIFICATIONS COMPLETED SUCCESSFULLY!\n")
    return True


if __name__ == "__main__":
    success = run_all_verifications()
    sys.exit(0 if success else 1)
