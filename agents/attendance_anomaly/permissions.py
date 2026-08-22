ALLOWED_TOOLS = [
    "get_attendance_records",
    "get_attendance_summary",
    "get_employee_notification_target",
    "send_attendance_reminder",
    "escalate_systemic_anomaly",
    "create_audit_log"
]

RESTRICTED_TOOLS = [
    "edit_attendance",
    "delete_attendance",
    "create_attendance",
    "update_profile",
    "read_salary",
    "update_salary",
    "modify_payroll",
    "approve_leave",
    "reject_leave",
    "change_roles",
    "bulk_export"
]

def check_permission(tool_name: str) -> bool:
    if tool_name in RESTRICTED_TOOLS:
        return False
    return tool_name in ALLOWED_TOOLS
