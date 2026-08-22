import pytest
import uuid
import os
from agent import run_attendance_anomaly
from tools import restricted_tool_stub, PermissionError

def get_base_request(date: str):
    return {
        "request_id": str(uuid.uuid4()),
        "target_date": date
    }

def test_case_1_normal_attendance():
    req = get_base_request("2024-01-10")
    req["employee_ids"] = ["EMP001"] # Alice is normal
    res = run_attendance_anomaly(req)
    assert res["success"] is True
    assert len(res["anomalies_detected"]) == 0
    assert res["systemic_issue"] is False

def test_case_2_missing_check_in():
    req = get_base_request("2024-01-10")
    req["employee_ids"] = ["EMP002"] # Bob missing check in
    res = run_attendance_anomaly(req)
    assert res["success"] is True
    assert len(res["anomalies_detected"]) == 1
    assert res["anomalies_detected"][0]["type"] == "MISSING_CHECK_IN"
    assert res["notification_sent"] is True

def test_case_3_missing_check_out():
    req = get_base_request("2024-01-10")
    req["employee_ids"] = ["EMP003"] # Charlie missing check out
    res = run_attendance_anomaly(req)
    assert res["success"] is True
    assert len(res["anomalies_detected"]) == 1
    assert res["anomalies_detected"][0]["type"] == "MISSING_CHECK_OUT"
    assert res["notification_sent"] is True

def test_case_4_late_check_in():
    req = get_base_request("2024-01-10")
    req["employee_ids"] = ["EMP004"] # Diana late check in
    res = run_attendance_anomaly(req)
    assert res["success"] is True
    assert len(res["anomalies_detected"]) == 1
    assert res["anomalies_detected"][0]["type"] == "LATE_CHECK_IN"
    assert res["notification_sent"] is True

def test_case_5_multiple_individual():
    req = get_base_request("2024-01-12")
    # 2 out of 4 anomalous (50%). Wait, threshold is 0.3!
    # If it's 50%, it WILL be systemic.
    # We must explicitly set SYSTEMIC_THRESHOLD_PERCENT for this test or alter mock data.
    # Let's mock the config or adjust threshold via env var to 0.6 so 2/4 is not systemic.
    os.environ["SYSTEMIC_THRESHOLD_PERCENT"] = "0.6"
    res = run_attendance_anomaly(req)
    assert res["success"] is True
    assert len(res["anomalies_detected"]) == 2
    assert res["systemic_issue"] is False
    assert res["notification_sent"] is True

def test_case_6_systemic_anomaly():
    os.environ["SYSTEMIC_THRESHOLD_PERCENT"] = "0.3" # Reset to default 30%
    req = get_base_request("2024-01-11") # 3 out of 4 missing checkin
    res = run_attendance_anomaly(req)
    assert res["success"] is True
    assert res["systemic_issue"] is True
    assert res["requires_hr_review"] is True
    assert res["notification_sent"] is False # Should stop automated reminders

def test_case_7_service_failure():
    req = get_base_request("FAIL_DATE")
    res = run_attendance_anomaly(req)
    assert res["success"] is False
    assert res["requires_hr_review"] is True
    assert "Attendance service failure" in res["recommendation"]

def test_case_8_permission_security():
    # Test that restricted tools raise PermissionError
    with pytest.raises(PermissionError):
        restricted_tool_stub("update_salary", "test-req")
    
    with pytest.raises(PermissionError):
        restricted_tool_stub("approve_leave", "test-req")
        
    with pytest.raises(PermissionError):
        restricted_tool_stub("delete_attendance", "test-req")
        
def test_invalid_input():
    # Missing required target_date
    res = run_attendance_anomaly({"request_id": "123"})
    assert res["success"] is False
    assert "Validation Error" in res["recommendation"]
