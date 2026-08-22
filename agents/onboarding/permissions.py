ALLOWED_TOOLS = [
    "get_onboarding_checklist",
    "get_task_status",
    "send_onboarding_reminder",
    "notify_hr",
    "create_audit_log"
]

RESTRICTED_TOOLS = [
    "update_employee",
    "update_onboarding_task",
    "delete_onboarding_task",
    "update_salary",
    "get_salary_structure",
    "update_payroll",
    "approve_leave",
    "reject_leave",
    "update_attendance",
    "change_role",
    "export_employee_data"
]

def check_permission(tool_name: str) -> bool:
    """Enforces least-privilege tool execution permissions."""
    if tool_name in RESTRICTED_TOOLS:
        return False
    return tool_name in ALLOWED_TOOLS
