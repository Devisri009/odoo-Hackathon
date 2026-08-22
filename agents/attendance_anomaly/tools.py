from mock_data import MOCK_ATTENDANCE_DB, MOCK_EMPLOYEES
from audit import log_action
from permissions import check_permission

class ToolError(Exception):
    pass

class PermissionError(Exception):
    pass

def _verify_permission(tool_name: str, request_id: str):
    if not check_permission(tool_name):
        log_action(request_id, "Attendance Anomaly Agent", "permission_denied", tool_name, "failed", f"Access to {tool_name} denied")
        raise PermissionError(f"Access to {tool_name} is denied by security policy.")

def get_attendance_records(date: str, request_id: str, employee_ids: list = None) -> list:
    _verify_permission("get_attendance_records", request_id)
    log_action(request_id, "Attendance Anomaly Agent", "read", "get_attendance_records", "success", f"Read records for {date}")
    
    if date == "FAIL_DATE":
        raise ToolError("Attendance service is unavailable")
        
    records = MOCK_ATTENDANCE_DB.get(date, [])
    if employee_ids:
        records = [r for r in records if r["employee_id"] in employee_ids]
    return records

def get_attendance_summary(date: str, request_id: str) -> dict:
    _verify_permission("get_attendance_summary", request_id)
    records = get_attendance_records(date, request_id)
    total = len(MOCK_EMPLOYEES) # Expected headcount
    log_action(request_id, "Attendance Anomaly Agent", "read", "get_attendance_summary", "success", f"Read summary for {date}")
    return {
        "expected_headcount": total,
        "actual_records": len(records)
    }

def get_employee_notification_target(employee_id: str, request_id: str) -> dict:
    _verify_permission("get_employee_notification_target", request_id)
    log_action(request_id, "Attendance Anomaly Agent", "read", "get_employee_notification_target", "success", f"Read target for {employee_id}")
    emp = MOCK_EMPLOYEES.get(employee_id)
    if not emp:
        raise ToolError(f"Employee {employee_id} not found")
    return {"name": emp["name"], "email": emp["email"]}

def send_attendance_reminder(employee_id: str, date: str, issue_type: str, message: str, request_id: str) -> dict:
    _verify_permission("send_attendance_reminder", request_id)
    target = get_employee_notification_target(employee_id, request_id)
    
    full_message = f"Automated assistance: {message}\nWhy did I receive this? This is an automated reminder regarding your attendance."
    log_action(request_id, "Attendance Anomaly Agent", "write", "send_attendance_reminder", "success", f"Sent reminder to {employee_id} for {issue_type}")
    
    return {"status": "sent", "employee_id": employee_id, "message_preview": full_message}

def escalate_systemic_anomaly(date: str, description: str, request_id: str) -> dict:
    _verify_permission("escalate_systemic_anomaly", request_id)
    log_action(request_id, "Attendance Anomaly Agent", "write", "escalate_systemic_anomaly", "success", f"Escalated systemic anomaly for {date}")
    return {"status": "escalated", "ticket_id": f"HR-TKT-{date}", "description": description}

def restricted_tool_stub(tool_name: str, request_id: str):
    # Helper to test permission denial
    _verify_permission(tool_name, request_id)
