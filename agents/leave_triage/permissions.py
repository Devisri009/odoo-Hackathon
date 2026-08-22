ALLOWED_TOOLS = [
    "get_leave_request",
    "get_leave_balance",
    "check_leave_policy",
    "get_employee_leave_history",
    "draft_approval_note"
]

RESTRICTED_TOOLS = [
    "approve_leave",
    "reject_leave",
    "update_leave_status",
    "update_employee",
    "update_profile",
    "update_salary",
    "update_payroll",
    "change_roles",
    "bulk_export"
]

def check_permission(tool_name: str) -> bool:
    if tool_name in RESTRICTED_TOOLS:
        return False
    return tool_name in ALLOWED_TOOLS
