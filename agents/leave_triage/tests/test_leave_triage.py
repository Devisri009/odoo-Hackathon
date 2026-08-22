import pytest
import os
import uuid
from datetime import date
from agent import run_leave_triage
from permissions import check_permission

def test_case_1_valid_approve():
    request_data = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR001",
        "employee_id": "EMP001",
        "leave_request_id": "REQ001",
        "leave_type": "paid",
        "start_date": "2024-01-10",
        "end_date": "2024-01-12",
        "remarks": "Vacation"
    }
    response = run_leave_triage(request_data)
    assert response["success"] is True
    assert response["recommendation"] == "approve"
    assert response["requires_human_approval"] is True
    assert "hitl_id" in response

def test_case_2_insufficient_balance():
    request_data = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR002",
        "employee_id": "EMP002", # EMP002 has 1 day left
        "leave_request_id": "REQ002",
        "leave_type": "paid",
        "start_date": "2024-01-10",
        "end_date": "2024-01-12", # 3 days requested
        "remarks": "Vacation"
    }
    response = run_leave_triage(request_data)
    assert response["success"] is True
    assert response["recommendation"] == "reject"
    assert response["balance_sufficient"] is False
    assert response["requires_human_approval"] is True

def test_case_3_policy_violation():
    # Paid leave max consecutive is 14
    request_data = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR001",
        "employee_id": "EMP001",
        "leave_request_id": "REQ001",
        "leave_type": "paid",
        "start_date": "2024-01-01",
        "end_date": "2024-01-20", # 20 days
        "remarks": "Long Vacation"
    }
    response = run_leave_triage(request_data)
    assert response["success"] is True
    assert response["recommendation"] == "reject"
    assert response["policy_compliant"] is False

def test_case_4_missing_invalid_info():
    request_data = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR001",
        "employee_id": "EMP001",
        "leave_request_id": "REQ004",
        "leave_type": "invalid", # Invalid type
        "start_date": "2024-01-10",
        "end_date": "2024-01-12",
        "remarks": ""
    }
    response = run_leave_triage(request_data)
    assert response["success"] is False
    assert response["recommendation"] == "review"
    assert response["validation_passed"] is False

def test_case_5_policy_service_failure():
    request_data = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR001",
        "employee_id": "EMP001",
        "leave_request_id": "REQ001",
        "leave_type": "paid",
        "start_date": "2024-01-10",
        "end_date": "2024-01-12",
        "remarks": ""
    }
    
    import agent
    import pytest
    from tools import ToolError
    
    # We patch the check_leave_policy function to raise a ToolError
    original_check = agent.check_leave_policy
    def mock_check(*args, **kwargs):
        raise ToolError("Policy service unavailable")
    
    agent.check_leave_policy = mock_check
    response = run_leave_triage(request_data)
    agent.check_leave_policy = original_check
    
    assert response["recommendation"] == "review"
    assert "Policy service unavailable" in response["warnings"]

def test_case_6_balance_service_failure():
    request_data = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR001",
        "employee_id": "EMP001",
        "leave_request_id": "REQ001",
        "leave_type": "paid",
        "start_date": "2024-01-10",
        "end_date": "2024-01-12",
        "remarks": ""
    }
    
    import agent
    from tools import ToolError
    
    original_get = agent.get_leave_balance
    def mock_get(*args, **kwargs):
        raise ToolError("Balance service unavailable")
    
    agent.get_leave_balance = mock_get
    response = run_leave_triage(request_data)
    agent.get_leave_balance = original_get
    
    assert response["recommendation"] == "review"
    assert "Balance service unavailable" in response["warnings"]

def test_dates_invalid():
    request_data = {
        "request_id": str(uuid.uuid4()),
        "user_id": "USR001",
        "employee_id": "EMP001",
        "leave_request_id": "REQ001",
        "leave_type": "paid",
        "start_date": "2024-01-12",
        "end_date": "2024-01-10", # End date before start date
        "remarks": "Vacation"
    }
    response = run_leave_triage(request_data)
    assert response["success"] is False
    assert response["validation_passed"] is False
    assert response["recommendation"] == "review"

def test_permissions():
    assert check_permission("get_leave_request") is True
    assert check_permission("approve_leave") is False
    assert check_permission("update_salary") is False
