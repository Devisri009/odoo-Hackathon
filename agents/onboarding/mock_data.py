from typing import Dict, Any

MOCK_ONBOARDING_DATABASE: Dict[str, Dict[str, Any]] = {
    "ONB_COMPLETED": {
        "onboarding_id": "ONB_COMPLETED",
        "employee_id": "EMP001",
        "start_date": "2026-08-01",
        "tasks": [
            {"task_id": "TSK-01", "employee_id": "EMP001", "task_name": "Identity Document Submission", "status": "COMPLETED", "due_date": "2026-08-05", "completed_at": "2026-08-03", "priority": "CRITICAL"},
            {"task_id": "TSK-02", "employee_id": "EMP001", "task_name": "Tax Document Submission", "status": "COMPLETED", "due_date": "2026-08-07", "completed_at": "2026-08-04", "priority": "HIGH"},
            {"task_id": "TSK-03", "employee_id": "EMP001", "task_name": "Bank Details Submission", "status": "COMPLETED", "due_date": "2026-08-07", "completed_at": "2026-08-05", "priority": "HIGH"},
            {"task_id": "TSK-04", "employee_id": "EMP001", "task_name": "Policy Acknowledgement", "status": "COMPLETED", "due_date": "2026-08-10", "completed_at": "2026-08-08", "priority": "MEDIUM"},
            {"task_id": "TSK-05", "employee_id": "EMP001", "task_name": "Employment Agreement Signing", "status": "COMPLETED", "due_date": "2026-08-03", "completed_at": "2026-08-01", "priority": "CRITICAL"},
            {"task_id": "TSK-06", "employee_id": "EMP001", "task_name": "HR Orientation Session", "status": "COMPLETED", "due_date": "2026-08-08", "completed_at": "2026-08-08", "priority": "MEDIUM"},
            {"task_id": "TSK-07", "employee_id": "EMP001", "task_name": "Security & Compliance Training", "status": "COMPLETED", "due_date": "2026-08-15", "completed_at": "2026-08-12", "priority": "HIGH"},
            {"task_id": "TSK-08", "employee_id": "EMP001", "task_name": "Equipment Assignment & Verification", "status": "COMPLETED", "due_date": "2026-08-05", "completed_at": "2026-08-02", "priority": "MEDIUM"}
        ]
    },
    "ONB_PENDING": {
        "onboarding_id": "ONB_PENDING",
        "employee_id": "EMP002",
        "start_date": "2026-08-18",
        "tasks": [
            {"task_id": "TSK-11", "employee_id": "EMP002", "task_name": "Identity Document Submission", "status": "COMPLETED", "due_date": "2026-08-20", "completed_at": "2026-08-19", "priority": "CRITICAL"},
            {"task_id": "TSK-12", "employee_id": "EMP002", "task_name": "Tax Document Submission", "status": "COMPLETED", "due_date": "2026-08-22", "completed_at": "2026-08-21", "priority": "HIGH"},
            {"task_id": "TSK-13", "employee_id": "EMP002", "task_name": "Bank Details Submission", "status": "COMPLETED", "due_date": "2026-08-22", "completed_at": "2026-08-21", "priority": "HIGH"},
            {"task_id": "TSK-14", "employee_id": "EMP002", "task_name": "Policy Acknowledgement", "status": "PENDING", "due_date": "2026-08-28", "completed_at": None, "priority": "MEDIUM"},
            {"task_id": "TSK-15", "employee_id": "EMP002", "task_name": "Employment Agreement Signing", "status": "COMPLETED", "due_date": "2026-08-19", "completed_at": "2026-08-18", "priority": "CRITICAL"},
            {"task_id": "TSK-16", "employee_id": "EMP002", "task_name": "HR Orientation Session", "status": "COMPLETED", "due_date": "2026-08-21", "completed_at": "2026-08-21", "priority": "MEDIUM"},
            {"task_id": "TSK-17", "employee_id": "EMP002", "task_name": "Security & Compliance Training", "status": "IN_PROGRESS", "due_date": "2026-08-30", "completed_at": None, "priority": "HIGH"},
            {"task_id": "TSK-18", "employee_id": "EMP002", "task_name": "Account Setup Verification", "status": "PENDING", "due_date": "2026-08-29", "completed_at": None, "priority": "LOW"}
        ]
    },
    "ONB_OVERDUE_SINGLE": {
        "onboarding_id": "ONB_OVERDUE_SINGLE",
        "employee_id": "EMP003",
        "start_date": "2026-08-01",
        "tasks": [
            {"task_id": "TSK-21", "employee_id": "EMP003", "task_name": "Identity Document Submission", "status": "COMPLETED", "due_date": "2026-08-05", "completed_at": "2026-08-04", "priority": "CRITICAL"},
            {"task_id": "TSK-22", "employee_id": "EMP003", "task_name": "Tax Document Submission", "status": "COMPLETED", "due_date": "2026-08-07", "completed_at": "2026-08-06", "priority": "HIGH"},
            {"task_id": "TSK-23", "employee_id": "EMP003", "task_name": "Bank Details Submission", "status": "COMPLETED", "due_date": "2026-08-07", "completed_at": "2026-08-06", "priority": "HIGH"},
            {"task_id": "TSK-24", "employee_id": "EMP003", "task_name": "Policy Acknowledgement", "status": "COMPLETED", "due_date": "2026-08-10", "completed_at": "2026-08-09", "priority": "MEDIUM"},
            {"task_id": "TSK-25", "employee_id": "EMP003", "task_name": "Employment Agreement Signing", "status": "COMPLETED", "due_date": "2026-08-03", "completed_at": "2026-08-02", "priority": "CRITICAL"},
            {"task_id": "TSK-26", "employee_id": "EMP003", "task_name": "HR Orientation Session", "status": "COMPLETED", "due_date": "2026-08-08", "completed_at": "2026-08-08", "priority": "MEDIUM"},
            {"task_id": "TSK-27", "employee_id": "EMP003", "task_name": "Security & Compliance Training", "status": "OVERDUE", "due_date": "2026-08-19", "completed_at": None, "priority": "MEDIUM"},
            {"task_id": "TSK-28", "employee_id": "EMP003", "task_name": "Account Setup Verification", "status": "PENDING", "due_date": "2026-08-25", "completed_at": None, "priority": "LOW"}
        ]
    },
    "ONB_CRITICAL_OVERDUE": {
        "onboarding_id": "ONB_CRITICAL_OVERDUE",
        "employee_id": "EMP004",
        "start_date": "2026-08-01",
        "tasks": [
            {"task_id": "TSK-31", "employee_id": "EMP004", "task_name": "Identity Document Submission", "status": "OVERDUE", "due_date": "2026-08-08", "completed_at": None, "priority": "CRITICAL"},
            {"task_id": "TSK-32", "employee_id": "EMP004", "task_name": "Tax Document Submission", "status": "COMPLETED", "due_date": "2026-08-07", "completed_at": "2026-08-06", "priority": "HIGH"},
            {"task_id": "TSK-33", "employee_id": "EMP004", "task_name": "Bank Details Submission", "status": "COMPLETED", "due_date": "2026-08-07", "completed_at": "2026-08-06", "priority": "HIGH"},
            {"task_id": "TSK-34", "employee_id": "EMP004", "task_name": "Policy Acknowledgement", "status": "PENDING", "due_date": "2026-08-25", "completed_at": None, "priority": "MEDIUM"},
            {"task_id": "TSK-35", "employee_id": "EMP004", "task_name": "Employment Agreement Signing", "status": "COMPLETED", "due_date": "2026-08-03", "completed_at": "2026-08-02", "priority": "CRITICAL"}
        ]
    },
    "ONB_MULTIPLE_OVERDUE": {
        "onboarding_id": "ONB_MULTIPLE_OVERDUE",
        "employee_id": "EMP005",
        "start_date": "2026-07-25",
        "tasks": [
            {"task_id": "TSK-41", "employee_id": "EMP005", "task_name": "Identity Document Submission", "status": "OVERDUE", "due_date": "2026-08-01", "completed_at": None, "priority": "CRITICAL"},
            {"task_id": "TSK-42", "employee_id": "EMP005", "task_name": "Tax Document Submission", "status": "OVERDUE", "due_date": "2026-08-05", "completed_at": None, "priority": "HIGH"},
            {"task_id": "TSK-43", "employee_id": "EMP005", "task_name": "Bank Details Submission", "status": "OVERDUE", "due_date": "2026-08-05", "completed_at": None, "priority": "HIGH"},
            {"task_id": "TSK-44", "employee_id": "EMP005", "task_name": "Policy Acknowledgement", "status": "OVERDUE", "due_date": "2026-08-10", "completed_at": None, "priority": "MEDIUM"},
            {"task_id": "TSK-45", "employee_id": "EMP005", "task_name": "Employment Agreement Signing", "status": "COMPLETED", "due_date": "2026-07-28", "completed_at": "2026-07-27", "priority": "CRITICAL"}
        ]
    },
    "ONB_BLOCKED": {
        "onboarding_id": "ONB_BLOCKED",
        "employee_id": "EMP006",
        "start_date": "2026-08-10",
        "tasks": [
            {"task_id": "TSK-51", "employee_id": "EMP006", "task_name": "Identity Document Submission", "status": "COMPLETED", "due_date": "2026-08-15", "completed_at": "2026-08-14", "priority": "CRITICAL"},
            {"task_id": "TSK-52", "employee_id": "EMP006", "task_name": "Equipment Assignment & Workstation Setup", "status": "BLOCKED", "due_date": "2026-08-16", "completed_at": None, "priority": "HIGH"},
            {"task_id": "TSK-53", "employee_id": "EMP006", "task_name": "Security & Compliance Training", "status": "PENDING", "due_date": "2026-08-25", "completed_at": None, "priority": "MEDIUM"}
        ]
    },
    "ONB_DUPLICATE_TASKS": {
        "onboarding_id": "ONB_DUPLICATE_TASKS",
        "employee_id": "EMP007",
        "start_date": "2026-08-10",
        "tasks": [
            {"task_id": "TSK-99", "employee_id": "EMP007", "task_name": "Identity Document Submission", "status": "COMPLETED", "due_date": "2026-08-15", "completed_at": "2026-08-14", "priority": "CRITICAL"},
            {"task_id": "TSK-99", "employee_id": "EMP007", "task_name": "Identity Document Submission Duplicate", "status": "PENDING", "due_date": "2026-08-20", "completed_at": None, "priority": "HIGH"}
        ]
    }
}
