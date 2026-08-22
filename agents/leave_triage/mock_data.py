MOCK_EMPLOYEES = {
    "EMP001": {"name": "Alice", "status": "active"},
    "EMP002": {"name": "Bob", "status": "active"},
    "EMP003": {"name": "Charlie", "status": "active"},
    "EMP999": {"name": "Ghost", "status": "inactive"}
}

MOCK_LEAVE_REQUESTS = {
    "REQ001": {"employee_id": "EMP001", "leave_type": "paid", "start_date": "2024-01-10", "end_date": "2024-01-12", "remarks": "Vacation", "current_status": "pending"},
    "REQ002": {"employee_id": "EMP002", "leave_type": "paid", "start_date": "2024-01-10", "end_date": "2024-01-12", "remarks": "Vacation", "current_status": "pending"},
    "REQ003": {"employee_id": "EMP003", "leave_type": "sick", "start_date": "2024-01-10", "end_date": "2024-01-20", "remarks": "Surgery", "current_status": "pending"},
    "REQ004": {"employee_id": "EMP001", "leave_type": "paid", "start_date": "2024-01-10", "end_date": "2024-01-12", "remarks": "", "current_status": "pending"},
    "REQ_BAL_FAIL": {"employee_id": "FAIL_BALANCE", "leave_type": "paid", "start_date": "2024-01-10", "end_date": "2024-01-12", "remarks": "", "current_status": "pending"},
    "REQ_POL_FAIL": {"employee_id": "EMP001", "leave_type": "FAIL_POLICY", "start_date": "2024-01-10", "end_date": "2024-01-12", "remarks": "", "current_status": "pending"}
}

MOCK_LEAVE_BALANCES = {
    "EMP001": {"paid": {"allocated_days": 20, "used_days": 5, "available_days": 15}, "sick": {"allocated_days": 10, "used_days": 0, "available_days": 10}},
    "EMP002": {"paid": {"allocated_days": 20, "used_days": 19, "available_days": 1}, "sick": {"allocated_days": 10, "used_days": 0, "available_days": 10}},
    "EMP003": {"sick": {"allocated_days": 10, "used_days": 2, "available_days": 8}, "paid": {"allocated_days": 20, "used_days": 2, "available_days": 18}},
}

MOCK_LEAVE_POLICIES = {
    "paid": {"max_consecutive_days": 14, "requires_notice_days": 7},
    "sick": {"max_consecutive_days": 5, "requires_medical_certificate_above_days": 3}
}

MOCK_LEAVE_HISTORY = {
    "EMP001": [{"leave_type": "paid", "status": "approved", "days": 5}],
    "EMP002": [{"leave_type": "paid", "status": "approved", "days": 19}],
    "EMP003": [{"leave_type": "sick", "status": "approved", "days": 2}],
}
