import pytest
import uuid
import os
from agent import run_onboarding
from tools import (
    get_onboarding_checklist,
    get_task_status,
    send_onboarding_reminder,
    notify_hr,
    restricted_tool_stub,
    PermissionError,
    ToolError
)
from audit import get_audit_logs, clear_audit_logs
from permissions import check_permission

def get_base_request(employee_id: str, onboarding_id: str, as_of_date: str = "2026-08-22") -> dict:
    return {
        "request_id": str(uuid.uuid4()),
        "employee_id": employee_id,
        "onboarding_id": onboarding_id,
        "start_date": "2026-08-01",
        "as_of_date": as_of_date
    }

@pytest.fixture(autouse=True)
def clean_logs():
    clear_audit_logs()

# CASE 1: All onboarding tasks completed
def test_case_1_all_tasks_completed():
    req = get_base_request("EMP001", "ONB_COMPLETED")
    res = run_onboarding(req)
    assert res["success"] is True
    assert res["completion_percentage"] == 100.0
    assert res["total_tasks"] == 8
    assert res["completed_tasks"] == 8
    assert res["overdue_tasks"] == 0
    assert res["pending_tasks"] == 0
    assert res["recommendation"] == "Onboarding complete"
    assert res["severity"] == "LOW"
    assert res["reminder_sent"] is False
    assert res["hr_escalation_sent"] is False
    assert res["requires_hr_review"] is False

# CASE 2: Some tasks pending but none overdue
def test_case_2_tasks_pending_none_overdue():
    req = get_base_request("EMP002", "ONB_PENDING", as_of_date="2026-08-22")
    res = run_onboarding(req)
    assert res["success"] is True
    assert res["completion_percentage"] == 62.5
    assert res["completed_tasks"] == 5
    assert res["pending_tasks"] == 3
    assert res["overdue_tasks"] == 0
    assert res["recommendation"] == "Reminder recommended"
    assert res["severity"] == "MEDIUM"
    assert res["reminder_sent"] is True
    assert res["hr_escalation_sent"] is False
    assert res["requires_hr_review"] is False

# CASE 3: One non-critical task overdue
def test_case_3_single_overdue_task():
    req = get_base_request("EMP003", "ONB_OVERDUE_SINGLE", as_of_date="2026-08-22")
    res = run_onboarding(req)
    assert res["success"] is True
    assert res["overdue_tasks"] == 1
    assert res["recommendation"] == "Follow-up required"
    assert res["severity"] == "HIGH"
    assert res["reminder_sent"] is True
    assert res["hr_escalation_sent"] is False
    assert res["requires_hr_review"] is False

# CASE 4: Critical task overdue (triggers HR escalation)
def test_case_4_critical_task_overdue():
    req = get_base_request("EMP004", "ONB_CRITICAL_OVERDUE", as_of_date="2026-08-22")
    res = run_onboarding(req)
    assert res["success"] is True
    assert res["overdue_tasks"] >= 1
    assert res["recommendation"] == "HR escalation required"
    assert res["severity"] == "CRITICAL"
    assert res["hr_escalation_sent"] is True
    assert res["requires_hr_review"] is True

# CASE 5: Multiple overdue tasks
def test_case_5_multiple_overdue_tasks():
    req = get_base_request("EMP005", "ONB_MULTIPLE_OVERDUE", as_of_date="2026-08-22")
    res = run_onboarding(req)
    assert res["success"] is True
    assert res["overdue_tasks"] == 4
    assert res["recommendation"] == "HR escalation required"
    assert res["severity"] == "CRITICAL"
    assert res["hr_escalation_sent"] is True
    assert res["requires_hr_review"] is True

# CASE 6: Blocked task requires manual review
def test_case_6_blocked_task():
    req = get_base_request("EMP006", "ONB_BLOCKED", as_of_date="2026-08-22")
    res = run_onboarding(req)
    assert res["success"] is True
    assert res["recommendation"] == "Manual HR review required"
    assert res["severity"] == "HIGH"
    assert res["hr_escalation_sent"] is True
    assert res["requires_hr_review"] is True

# CASE 7: Service / Tool failure handling
def test_case_7_service_failure():
    req = get_base_request("EMP999", "FAIL_SERVICE")
    res = run_onboarding(req)
    assert res["success"] is False
    assert res["requires_hr_review"] is True
    assert "Onboarding service failure" in res["reasoning_summary"]
    assert len(res["warnings"]) > 0

# CASE 8: LLM unavailable / Deterministic fallback
def test_case_8_deterministic_fallback():
    os.environ["GROQ_API_KEY"] = "mock"
    req = get_base_request("EMP001", "ONB_COMPLETED")
    res = run_onboarding(req)
    assert res["success"] is True
    assert "100% completion" in res["reasoning_summary"]

# CASE 9: Invalid onboarding request data
def test_case_9_invalid_request_validation():
    # Empty employee ID
    req = {
        "request_id": str(uuid.uuid4()),
        "employee_id": "   ",
        "onboarding_id": "ONB_COMPLETED"
    }
    res = run_onboarding(req)
    assert res["success"] is False
    assert res["requires_hr_review"] is True
    assert any("validation failed" in w.lower() for w in res["warnings"])

    # Invalid date format
    req_date = {
        "request_id": str(uuid.uuid4()),
        "employee_id": "EMP001",
        "onboarding_id": "ONB_COMPLETED",
        "as_of_date": "22-08-2026"  # invalid format
    }
    res_date = run_onboarding(req_date)
    assert res_date["success"] is False
    assert res_date["requires_hr_review"] is True

# CASE 10: Permission and security enforcement
def test_case_10_permission_security():
    # Verify allowed tools
    assert check_permission("get_onboarding_checklist") is True
    assert check_permission("get_task_status") is True
    assert check_permission("send_onboarding_reminder") is True
    assert check_permission("notify_hr") is True
    assert check_permission("create_audit_log") is True

    # Verify prohibited tools raise PermissionError
    with pytest.raises(PermissionError):
        restricted_tool_stub("update_employee", "req-test")

    with pytest.raises(PermissionError):
        restricted_tool_stub("update_onboarding_task", "req-test")

    with pytest.raises(PermissionError):
        restricted_tool_stub("update_salary", "req-test")

    with pytest.raises(PermissionError):
        restricted_tool_stub("approve_leave", "req-test")

    # Verify audit log captures permission denials
    logs = get_audit_logs()
    denials = [log for log in logs if log["action_type"] == "permission_denied"]
    assert len(denials) == 4

# CASE 11: Duplicate task detection in checklist
def test_case_11_duplicate_task_detection():
    req = get_base_request("EMP007", "ONB_DUPLICATE_TASKS")
    res = run_onboarding(req)
    assert res["success"] is True
    assert any("duplicate task ids" in w.lower() for w in res["warnings"])

# CASE 12: Configurable escalation threshold
def test_case_12_escalation_threshold():
    # When threshold is set to 2 days, a task overdue by 7 days triggers escalation
    os.environ["ONBOARDING_ESCALATION_DAYS"] = "2"
    req = get_base_request("EMP003", "ONB_OVERDUE_SINGLE", as_of_date="2026-08-22")
    res = run_onboarding(req)
    assert res["success"] is True
    assert res["recommendation"] == "HR escalation required"
    assert res["severity"] == "CRITICAL"
    assert res["hr_escalation_sent"] is True
    # Reset back to default 7
    os.environ["ONBOARDING_ESCALATION_DAYS"] = "7"

# CASE 13: Reminder failure handling
def test_case_13_reminder_tool_failure():
    # Trigger simulated reminder failure
    req = get_base_request("FAIL_REMINDER", "ONB_PENDING")
    res = run_onboarding(req)
    assert res["success"] is True
    assert any("failed to deliver reminder" in w.lower() for w in res["warnings"])

# CASE 14: HR escalation failure handling
def test_case_14_hr_escalation_failure():
    # Trigger simulated escalation failure
    req = get_base_request("FAIL_ESCALATION", "ONB_BLOCKED")
    res = run_onboarding(req)
    assert res["success"] is True
    assert any("failed to deliver hr escalation" in w.lower() for w in res["warnings"])

# CASE 15: Single task status retrieval
def test_case_15_get_task_status_tool():
    task = get_task_status("ONB_COMPLETED", "TSK-01", "req-direct")
    assert task.task_id == "TSK-01"
    assert task.status == "COMPLETED"
    assert task.priority == "CRITICAL"
