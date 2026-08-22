ALLOWED_TOOLS = [
    "search_policy",
    "get_policy_section",
    "create_audit_log"
]

RESTRICTED_TOOLS = [
    "apply_leave",
    "approve_leave",
    "reject_leave",
    "update_attendance",
    "create_attendance",
    "update_salary",
    "get_salary_structure",
    "modify_employee",
    "change_role",
    "send_notification",
    "modify_policy",
    "export_employee_data"
]

def check_permission(tool_name: str) -> bool:
    """Explicitly verify tool permission against allow/restrict lists."""
    if tool_name in RESTRICTED_TOOLS:
        return False
    return tool_name in ALLOWED_TOOLS
