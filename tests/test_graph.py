"""Pytest test suite for Knowledge Graph connectivity, seeding, and deterministic queries."""

import pytest
from src.graph.connection import Neo4jConnection
from src.graph.queries import Neo4jBenefitQuerier


@pytest.fixture(scope="module")
def neo4j_conn():
    conn = Neo4jConnection()
    assert conn.verify_connectivity() is True, "Neo4j must be reachable for tests."
    yield conn


@pytest.fixture(scope="module")
def querier(neo4j_conn):
    return Neo4jBenefitQuerier(neo4j_conn)


def test_neo4j_connectivity(neo4j_conn):
    """Test connection alive."""
    assert neo4j_conn.verify_connectivity() is True


def test_senior_entitlements(querier):
    """Test Level 3 (Senior) benefits."""
    senior_info = querier.get_benefits_summary_for_level("Senior")
    assert senior_info["level_number"] == 3
    assert senior_info["annual_leave_days"] == 7
    assert senior_info["dental_benefit_thb"] == 3000
    assert senior_info["hospital_visit_thb"] == 700
    assert senior_info["is_exempt_from_ot"] is False
    assert senior_info["has_executive_parking"] is False


def test_manager_entitlements(querier):
    """Test Level 4 (Manager) benefits & OT exemption."""
    mgr_info = querier.get_benefits_summary_for_level("Manager")
    assert mgr_info["level_number"] == 4
    assert mgr_info["annual_leave_days"] == 7
    assert mgr_info["dental_benefit_thb"] == 4000
    assert mgr_info["is_exempt_from_ot"] is True
    assert mgr_info["must_fingerprint_scan"] is True


def test_vp_entitlements(querier):
    """Test Level 6 (VP) benefits including Executive Parking."""
    vp_info = querier.get_benefits_summary_for_level("Vice President")
    assert vp_info["level_number"] == 6
    assert vp_info["annual_leave_days"] == 8
    assert vp_info["dental_benefit_thb"] == 4000
    assert vp_info["hospital_visit_thb"] == 1000
    assert vp_info["has_executive_parking"] is True


def test_pvd_rules_calculations(querier):
    """Test Provident Fund calculations across tenures."""
    res_half_year = querier.get_pvd_rules(0.5)
    assert "0%" in res_half_year["calculated_employer_vesting"]

    res_2_years = querier.get_pvd_rules(2.0)
    assert "50%" in res_2_years["calculated_employer_vesting"]

    res_4_years = querier.get_pvd_rules(4.0)
    assert "100%" in res_4_years["calculated_employer_vesting"]


def test_severance_eligibility(querier):
    """Test statutory severance days by tenure."""
    assert querier.get_severance_eligibility(2)["entitled_severance_days"] == 0
    assert querier.get_severance_eligibility(8)["entitled_severance_days"] == 30
    assert querier.get_severance_eligibility(24)["entitled_severance_days"] == 90
    assert querier.get_severance_eligibility(48)["entitled_severance_days"] == 180
    assert querier.get_severance_eligibility(96)["entitled_severance_days"] == 240
    assert querier.get_severance_eligibility(150)["entitled_severance_days"] == 300


def test_sick_leave_medical_cert(querier):
    """Test sick leave details and required documents."""
    sick_leaves = querier.get_leave_details("ลาป่วย")
    assert len(sick_leaves) > 0
    sick = sick_leaves[0]
    assert sick["max_paid_days"] == 30
    assert any("ใบรับรองแพทย์" in doc for doc in sick["required_documents"])


def test_funeral_benefit(querier):
    """Test funeral grant for parents and direct family."""
    res_parent = querier.get_funeral_benefit("บิดา")
    assert len(res_parent["matched_policies"]) > 0
    policy = res_parent["matched_policies"][0]
    assert policy["cash_assistance_thb"] == 5000
    assert policy["wreaths"] == 1
    assert policy["host_nights"] == 1


def test_ceo_entitlements(querier):
    """Test Top Executive (CEO Level 9) entitlements."""
    ceo = querier.get_benefits_summary_for_level("CEO")
    assert ceo["level_number"] == 9
    assert ceo["annual_leave_days"] == 10
    assert ceo["dental_benefit_thb"] == 6000
    assert ceo["hospital_visit_thb"] == 1000
    assert ceo["has_executive_parking"] is True
    assert ceo["is_exempt_from_ot"] is True
    assert ceo["must_fingerprint_scan"] is False
