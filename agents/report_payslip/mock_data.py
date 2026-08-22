from typing import Dict, Any

MOCK_EMPLOYEES: Dict[str, Dict[str, Any]] = {
    "EMP001": {"name": "Alice Smith", "department": "Engineering", "authorized_payroll": True},
    "EMP002": {"name": "Bob Jones", "department": "Product", "authorized_payroll": True},
    "EMP003": {"name": "Charlie Brown", "department": "Marketing", "authorized_payroll": True},
    "EMP_UNAUTHORIZED": {"name": "Eve Secret", "department": "Executive", "authorized_payroll": False}
}

MOCK_PAYROLL_DATABASE: Dict[str, Dict[str, Any]] = {
    "EMP001_2026-07": {
        "employee_id": "EMP001",
        "employee_name": "Alice Smith",
        "pay_period": "2026-07",
        "base_salary": 5000.0,
        "allowances": {
            "housing_allowance": 800.0,
            "transport_allowance": 200.0,
            "meal_allowance": 150.0
        },
        "deductions": {
            "income_tax": 600.0,
            "health_insurance": 150.0,
            "retirement_fund": 250.0
        }
    },
    "EMP002_2026-07": {
        "employee_id": "EMP002",
        "employee_name": "Bob Jones",
        "pay_period": "2026-07",
        "base_salary": 4200.0,
        "allowances": {
            "housing_allowance": 500.0,
            "transport_allowance": 150.0
        },
        "deductions": {
            "income_tax": 450.0,
            "health_insurance": 120.0
        }
    }
}

MOCK_ATTENDANCE_REPORT_DATABASE: Dict[str, Dict[str, Any]] = {
    "EMP001_2026-07": {
        "employee_id": "EMP001",
        "employee_name": "Alice Smith",
        "report_period": "2026-07",
        "working_days": 22,
        "present_days": 21,
        "absent_days": 0,
        "late_days": 1,
        "missing_attendance_days": 0
    },
    "EMP002_2026-07": {
        "employee_id": "EMP002",
        "employee_name": "Bob Jones",
        "report_period": "2026-07",
        "working_days": 22,
        "present_days": 18,
        "absent_days": 3,
        "late_days": 2,
        "missing_attendance_days": 1
    }
}

MOCK_LEAVE_BALANCE_DATABASE: Dict[str, Dict[str, Any]] = {
    "EMP001": {
        "employee_id": "EMP001",
        "employee_name": "Alice Smith",
        "as_of_date": "2026-08-22",
        "balances": [
            {"leave_type": "Paid Leave", "allocated_days": 18.0, "used_days": 5.0, "remaining_days": 13.0},
            {"leave_type": "Sick Leave", "allocated_days": 10.0, "used_days": 2.0, "remaining_days": 8.0},
            {"leave_type": "Unpaid Sabbatical", "allocated_days": 30.0, "used_days": 0.0, "remaining_days": 30.0}
        ]
    },
    "EMP002": {
        "employee_id": "EMP002",
        "employee_name": "Bob Jones",
        "as_of_date": "2026-08-22",
        "balances": [
            {"leave_type": "Paid Leave", "allocated_days": 18.0, "used_days": 17.0, "remaining_days": 1.0},
            {"leave_type": "Sick Leave", "allocated_days": 10.0, "used_days": 0.0, "remaining_days": 10.0}
        ]
    }
}

MOCK_ONBOARDING_REPORT_DATABASE: Dict[str, Dict[str, Any]] = {
    "EMP001": {
        "employee_id": "EMP001",
        "employee_name": "Alice Smith",
        "onboarding_id": "ONB_EMP001",
        "total_tasks": 8,
        "completed_tasks": 8,
        "pending_tasks": 0,
        "overdue_tasks": 0
    },
    "EMP002": {
        "employee_id": "EMP002",
        "employee_name": "Bob Jones",
        "onboarding_id": "ONB_EMP002",
        "total_tasks": 8,
        "completed_tasks": 5,
        "pending_tasks": 3,
        "overdue_tasks": 0
    }
}
