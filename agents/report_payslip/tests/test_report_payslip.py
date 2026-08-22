import pytest
import uuid
import os
from agent import run_report_payslip
from schemas import ReportType
from tools import (
    get_authorized_payroll_data,
    generate_payslip,
    restricted_tool_stub,
    PermissionError,
    ToolError
)
from audit import get_audit_logs, clear_audit_logs
from permissions import check_permission

def get_base_request(report_type: str, employee_id: str = "EMP001", period: str = "2026-07") -> dict:
    return {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR-101",
        "employee_id": employee_id,
        "report_type": report_type,
        "report_period": period
    }

@pytest.fixture(autouse=True)
def clean_logs():
    clear_audit_logs()

# CASE 1: Valid payslip request
def test_case_1_valid_payslip_generation():
    req = get_base_request("PAYSLIP", "EMP001", "2026-07")
    res = run_report_payslip(req)
    assert res["success"] is True
    assert res["generated"] is True
    assert res["report_type"] == ReportType.PAYSLIP
    assert res["employee_id"] == "EMP001"
    assert "PAYSLIP_EMP001_2026-07.txt" in res["document_name"]
    
    content = res["content"]
    assert content["base_salary"] == 5000.0
    assert content["gross_salary"] == 6150.0  # 5000 + 800 + 200 + 150
    assert content["total_deductions"] == 1000.0  # 600 + 150 + 250
    assert content["net_salary"] == 5150.0  # 6150 - 1000
    assert "DAYFLOW HRMS PAYSLIP" in content["document_text"]

# CASE 2: Valid attendance report
def test_case_2_valid_attendance_report():
    req = get_base_request("ATTENDANCE_REPORT", "EMP001", "2026-07")
    res = run_report_payslip(req)
    assert res["success"] is True
    assert res["generated"] is True
    assert res["report_type"] == ReportType.ATTENDANCE_REPORT
    
    content = res["content"]
    assert content["working_days"] == 22
    assert content["present_days"] == 21
    assert content["attendance_rate"] == 95.5
    assert "MONTHLY ATTENDANCE REPORT" in content["document_text"]

# CASE 3: Valid leave balance report
def test_case_3_valid_leave_report():
    req = get_base_request("LEAVE_BALANCE_REPORT", "EMP001")
    res = run_report_payslip(req)
    assert res["success"] is True
    assert res["generated"] is True
    assert res["report_type"] == ReportType.LEAVE_BALANCE_REPORT
    
    content = res["content"]
    assert len(content["balances"]) == 3
    paid_leave = next(b for b in content["balances"] if b["leave_type"] == "Paid Leave")
    assert paid_leave["allocated_days"] == 18.0
    assert paid_leave["used_days"] == 5.0
    assert paid_leave["remaining_days"] == 13.0

# CASE 4: Valid onboarding completion report
def test_case_4_valid_onboarding_report():
    req = get_base_request("ONBOARDING_COMPLETION_REPORT", "EMP001")
    res = run_report_payslip(req)
    assert res["success"] is True
    assert res["generated"] is True
    assert res["report_type"] == ReportType.ONBOARDING_COMPLETION_REPORT
    
    content = res["content"]
    assert content["total_tasks"] == 8
    assert content["completed_tasks"] == 8
    assert content["completion_percentage"] == 100.0

# CASE 5: Invalid / Non-existent employee ID
def test_case_5_invalid_employee():
    req = get_base_request("PAYSLIP", "EMP_NON_EXISTENT", "2026-07")
    res = run_report_payslip(req)
    assert res["success"] is False
    assert res["generated"] is False
    assert res["requires_hr_review"] is True
    assert any("does not exist" in w.lower() or "not found" in w.lower() for w in res["warnings"])

# CASE 6: Unauthorized payroll access attempt
def test_case_6_unauthorized_payroll_access():
    req = get_base_request("PAYSLIP", "EMP_UNAUTHORIZED", "2026-07")
    res = run_report_payslip(req)
    assert res["success"] is False
    assert res["generated"] is False
    assert res["requires_hr_review"] is True
    assert any("not authorized" in w.lower() or "access denied" in w.lower() for w in res["warnings"])

# CASE 7: Attempt to modify salary or payroll (PermissionError)
def test_case_7_salary_modification_denial():
    with pytest.raises(PermissionError):
        restricted_tool_stub("update_salary", "req-sec-01")

    with pytest.raises(PermissionError):
        restricted_tool_stub("update_payroll", "req-sec-02")

    with pytest.raises(PermissionError):
        restricted_tool_stub("modify_salary_structure", "req-sec-03")

    with pytest.raises(PermissionError):
        restricted_tool_stub("delete_payroll", "req-sec-04")

# CASE 8: Invalid report period format
def test_case_8_invalid_period_format():
    req = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR-101",
        "employee_id": "EMP001",
        "report_type": "PAYSLIP",
        "report_period": "July-2026"  # Invalid format
    }
    res = run_report_payslip(req)
    assert res["success"] is False
    assert res["generated"] is False
    assert res["requires_hr_review"] is True
    assert any("validation failed" in w.lower() for w in res["warnings"])

# CASE 9: Deterministic payroll calculations (Bob Jones)
def test_case_9_payroll_arithmetic_verification():
    req = get_base_request("PAYSLIP", "EMP002", "2026-07")
    res = run_report_payslip(req)
    assert res["success"] is True
    content = res["content"]
    assert content["base_salary"] == 4200.0
    assert content["gross_salary"] == 4850.0  # 4200 + 500 + 150
    assert content["total_deductions"] == 570.0  # 450 + 120
    assert content["net_salary"] == 4280.0  # 4850 - 570

# CASE 10: Missing period / unindexed report data failure
def test_case_10_missing_period_record():
    req = get_base_request("PAYSLIP", "EMP001", "2025-01")  # No records for 2025-01
    res = run_report_payslip(req)
    assert res["success"] is False
    assert res["generated"] is False
    assert res["requires_hr_review"] is True
    assert any("no payroll record found" in w.lower() for w in res["warnings"])

# CASE 11: LLM unavailable / Deterministic fallback
def test_case_11_deterministic_fallback():
    os.environ["GROQ_API_KEY"] = "mock"
    req = get_base_request("PAYSLIP", "EMP001", "2026-07")
    res = run_report_payslip(req)
    assert res["success"] is True
    assert "Generated authorized payslip" in res["reasoning_summary"]

# CASE 12: Audit logging compliance
def test_case_12_audit_logging():
    req = get_base_request("PAYSLIP", "EMP001", "2026-07")
    res = run_report_payslip(req)
    assert res["success"] is True
    
    logs = get_audit_logs()
    assert len(logs) >= 2
    # Verify salary numbers are NOT stored in audit logs
    for log in logs:
        assert "$5,000.00" not in log["details"]
        assert "$5,150.00" not in log["details"]

# CASE 13: Permission registry check
def test_case_13_permissions_registry():
    assert check_permission("get_authorized_payroll_data") is True
    assert check_permission("generate_payslip") is True
    assert check_permission("get_attendance_report_data") is True
    assert check_permission("get_leave_report_data") is True
    assert check_permission("get_onboarding_report_data") is True
    assert check_permission("create_audit_log") is True

    assert check_permission("update_salary") is False
    assert check_permission("approve_leave") is False
    assert check_permission("modify_attendance") is False
    assert check_permission("export_bulk_employee_data") is False

# CASE 14: Onboarding report for in-progress employee
def test_case_14_in_progress_onboarding_report():
    req = get_base_request("ONBOARDING_COMPLETION_REPORT", "EMP002")
    res = run_report_payslip(req)
    assert res["success"] is True
    content = res["content"]
    assert content["total_tasks"] == 8
    assert content["completed_tasks"] == 5
    assert content["pending_tasks"] == 3
    assert content["completion_percentage"] == 62.5
