ALLOWED_TOOLS = [
    "get_authorized_payroll_data",
    "get_attendance_report_data",
    "get_leave_report_data",
    "get_onboarding_report_data",
    "generate_payslip",
    "generate_report",
    "create_audit_log"
]

RESTRICTED_TOOLS = [
    "update_salary",
    "update_payroll",
    "delete_payroll",
    "modify_salary_structure",
    "modify_attendance",
    "modify_leave",
    "approve_leave",
    "reject_leave",
    "update_employee",
    "change_user_role",
    "export_bulk_employee_data"
]

def check_permission(tool_name: str) -> bool:
    """Enforces least-privilege tool execution permissions for report generation."""
    if tool_name in RESTRICTED_TOOLS:
        return False
    return tool_name in ALLOWED_TOOLS
