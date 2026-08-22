import pytest
import uuid
import os
from agent import run_policy_qa
from tools import search_policy, get_policy_section, restricted_tool_stub, PermissionError, ToolError
from audit import get_audit_logs, clear_audit_logs
from permissions import check_permission

def get_base_request(question: str) -> dict:
    return {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR-101",
        "employee_id": "EMP-500",
        "question": question
    }

@pytest.fixture(autouse=True)
def clean_logs():
    clear_audit_logs()

# CASE 1: Direct policy question
def test_case_1_direct_leave_policy():
    req = get_base_request("How many paid leave days can I take per year?")
    res = run_policy_qa(req)
    assert res["success"] is True
    assert "18" in res["answer"]
    assert len(res["sources"]) >= 1
    assert res["sources"][0]["policy_name"] == "Leave Policy"
    assert res["sources"][0]["section"] == "3.2"
    assert res["confidence"] == "HIGH"
    assert res["ask_hr"] is False

# CASE 2: Attendance policy question
def test_case_2_attendance_policy():
    req = get_base_request("What is the grace period for late check-in?")
    res = run_policy_qa(req)
    assert res["success"] is True
    assert "15-minute" in res["answer"] or "15" in res["answer"]
    assert any(s["policy_name"] == "Attendance Policy" and s["section"] == "2.2" for s in res["sources"])
    assert res["confidence"] == "HIGH"

# CASE 3: Question requiring multiple policy sections
def test_case_3_multiple_sections():
    req = get_base_request("Explain the paid leave entitlement and the sick leave doctor note policy.")
    res = run_policy_qa(req)
    assert res["success"] is True
    assert len(res["sources"]) >= 2
    sections = [s["section"] for s in res["sources"]]
    assert "3.2" in sections
    assert "3.3" in sections

# CASE 4: Question with no matching policy
def test_case_4_no_matching_policy():
    req = get_base_request("What is the company policy regarding cryptocurrency compensation and stock vesting schedules?")
    res = run_policy_qa(req)
    assert res["success"] is True
    assert res["confidence"] == "LOW"
    assert res["ask_hr"] is True
    assert len(res["sources"]) == 0
    assert "could not find sufficient information" in res["answer"].lower()

# CASE 5: Ambiguous question
def test_case_5_ambiguous_question():
    req = get_base_request("What are the rules?")
    res = run_policy_qa(req)
    assert res["success"] is True
    # Should flag either LOW or MEDIUM confidence and recommend HR
    assert res["confidence"] in ["MEDIUM", "LOW"]
    assert res["ask_hr"] is True

# CASE 6: Attempt to request restricted personal data
def test_case_6_restricted_salary_query():
    req = get_base_request("What is my salary and bank account number?")
    res = run_policy_qa(req)
    assert res["success"] is True
    assert res["confidence"] == "LOW"
    assert res["ask_hr"] is True
    assert "cannot access private employee records" in res["answer"].lower()
    assert len(res["warnings"]) > 0

# CASE 7: Attempt to perform an operational action
def test_case_7_operational_action_request():
    req = get_base_request("Please approve my leave request for next Monday.")
    res = run_policy_qa(req)
    assert res["success"] is True
    assert res["confidence"] == "LOW"
    assert res["ask_hr"] is True
    assert "read-only" in res["answer"].lower()
    assert len(res["warnings"]) > 0

# CASE 8: Policy search / tool failure handling
def test_case_8_tool_failure_handling():
    req = get_base_request("FORCE_TOOL_FAILURE")
    res = run_policy_qa(req)
    assert res["success"] is False
    assert res["confidence"] == "LOW"
    assert res["ask_hr"] is True
    assert "error occurred" in res["answer"].lower()
    assert any("tool error" in w.lower() for w in res["warnings"])

# CASE 9: LLM unavailable / Deterministic fallback
def test_case_9_deterministic_fallback():
    os.environ["GROQ_API_KEY"] = "mock"
    req = get_base_request("What are the standard working hours?")
    res = run_policy_qa(req)
    assert res["success"] is True
    assert "9:00 AM to 5:00 PM" in res["answer"]
    assert any(s["policy_name"] == "Attendance Policy" for s in res["sources"])

# CASE 10: Permission and security enforcement
def test_case_10_permission_security():
    # Verify allowed tools pass check
    assert check_permission("search_policy") is True
    assert check_permission("get_policy_section") is True
    assert check_permission("create_audit_log") is True

    # Verify prohibited tools raise PermissionError
    with pytest.raises(PermissionError):
        restricted_tool_stub("update_salary", "req-test")

    with pytest.raises(PermissionError):
        restricted_tool_stub("approve_leave", "req-test")

    with pytest.raises(PermissionError):
        restricted_tool_stub("modify_policy", "req-test")

    with pytest.raises(PermissionError):
        restricted_tool_stub("export_employee_data", "req-test")

    # Verify audit logs captured the security violations
    logs = get_audit_logs()
    denials = [log for log in logs if log["action_type"] == "permission_denied"]
    assert len(denials) == 4

# CASE 11: Validation error on empty question
def test_case_11_empty_question_validation():
    req = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR-101",
        "employee_id": "EMP-500",
        "question": "   "
    }
    res = run_policy_qa(req)
    assert res["success"] is False
    assert res["confidence"] == "LOW"
    assert res["ask_hr"] is True
    assert any("validation failed" in w.lower() for w in res["warnings"])

# CASE 12: Validation error on question exceeding length limit
def test_case_12_long_question_validation():
    req = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR-101",
        "employee_id": "EMP-500",
        "question": "leave " * 250  # > 1000 chars
    }
    res = run_policy_qa(req)
    assert res["success"] is False
    assert res["confidence"] == "LOW"
    assert any("validation failed" in w.lower() for w in res["warnings"])

# CASE 13: Work From Home policy question
def test_case_13_wfh_policy():
    req = get_base_request("How many days per week can I work from home?")
    res = run_policy_qa(req)
    assert res["success"] is True
    assert "2 days" in res["answer"].lower() or "2" in res["answer"]
    assert any(s["policy_name"] == "Work From Home Policy" and s["section"] == "4.2" for s in res["sources"])

# CASE 14: Onboarding probation policy question
def test_case_14_onboarding_probation():
    req = get_base_request("What is the standard probation period for new hires?")
    res = run_policy_qa(req)
    assert res["success"] is True
    assert "3 months" in res["answer"].lower()
    assert any(s["policy_name"] == "Onboarding Policy" and s["section"] == "1.1" for s in res["sources"])
