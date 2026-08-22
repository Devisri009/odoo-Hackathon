MOCK_ATTENDANCE_DB = {
    "2024-01-10": [
        # Normal
        {"employee_id": "EMP001", "date": "2024-01-10", "check_in": "08:50:00", "check_out": "17:10:00"},
        # Missing check-in
        {"employee_id": "EMP002", "date": "2024-01-10", "check_in": None, "check_out": "17:00:00"},
        # Missing check-out
        {"employee_id": "EMP003", "date": "2024-01-10", "check_in": "09:00:00", "check_out": None},
        # Late check-in
        {"employee_id": "EMP004", "date": "2024-01-10", "check_in": "10:30:00", "check_out": "17:00:00"},
    ],
    "2024-01-11": [
        # Systemic failure: large number of employees missing check-in
        {"employee_id": "EMP001", "date": "2024-01-11", "check_in": None, "check_out": None},
        {"employee_id": "EMP002", "date": "2024-01-11", "check_in": None, "check_out": None},
        {"employee_id": "EMP003", "date": "2024-01-11", "check_in": None, "check_out": None},
        {"employee_id": "EMP004", "date": "2024-01-11", "check_in": "08:55:00", "check_out": "17:05:00"},
    ],
    "2024-01-12": [
        # Multiple employees affected independently (Late and Missing out)
        {"employee_id": "EMP001", "date": "2024-01-12", "check_in": "09:45:00", "check_out": "17:00:00"},
        {"employee_id": "EMP002", "date": "2024-01-12", "check_in": "08:50:00", "check_out": None},
        {"employee_id": "EMP003", "date": "2024-01-12", "check_in": "08:50:00", "check_out": "17:10:00"},
        {"employee_id": "EMP004", "date": "2024-01-12", "check_in": "08:55:00", "check_out": "17:05:00"},
    ],
    "FAIL_DATE": "ERROR" # For service failure testing
}

MOCK_EMPLOYEES = {
    "EMP001": {"name": "Alice", "email": "alice@example.com"},
    "EMP002": {"name": "Bob", "email": "bob@example.com"},
    "EMP003": {"name": "Charlie", "email": "charlie@example.com"},
    "EMP004": {"name": "Diana", "email": "diana@example.com"},
}
