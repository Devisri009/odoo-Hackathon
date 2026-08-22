from typing import Optional, Dict, Any, List
from schemas import OnboardingChecklist, OnboardingTask, TaskStatus, TaskPriority
from mock_data import MOCK_ONBOARDING_DATABASE
from audit import log_action
from permissions import check_permission

class ToolError(Exception):
    """Raised when an onboarding tool encounters an operational failure."""
    pass

class PermissionError(Exception):
    """Raised when an unauthorized tool is invoked."""
    pass

def _verify_permission(tool_name: str, request_id: str):
    """Enforces least-privilege tool execution permissions."""
    if not check_permission(tool_name):
        log_action(
            request_id=request_id,
            agent_name="Onboarding Agent",
            action_type="permission_denied",
            tool_called=tool_name,
            tool_result="failed",
            details=f"Execution of prohibited tool '{tool_name}' was blocked by policy."
        )
        raise PermissionError(f"Access to '{tool_name}' is denied: prohibited for Onboarding Agent.")

def get_onboarding_checklist(onboarding_id: str, request_id: str) -> OnboardingChecklist:
    """Retrieve complete onboarding checklist and task details."""
    _verify_permission("get_onboarding_checklist", request_id)

    if onboarding_id in ["FAIL_SERVICE", "ONB_FAIL_SERVICE"]:
        log_action(request_id, "Onboarding Agent", "tool_call", "get_onboarding_checklist", "failure", "Simulated checklist service failure.")
        raise ToolError("Onboarding service is currently unavailable.")

    data = MOCK_ONBOARDING_DATABASE.get(onboarding_id)
    if not data:
        raise ToolError(f"Onboarding record '{onboarding_id}' not found.")

    tasks = [OnboardingTask(**t) for t in data.get("tasks", [])]
    checklist = OnboardingChecklist(
        onboarding_id=data["onboarding_id"],
        employee_id=data["employee_id"],
        start_date=data["start_date"],
        tasks=tasks
    )

    log_action(
        request_id=request_id,
        agent_name="Onboarding Agent",
        action_type="tool_call",
        tool_called="get_onboarding_checklist",
        tool_result="success",
        details=f"Retrieved checklist for onboarding_id '{onboarding_id}' with {len(tasks)} tasks."
    )
    return checklist

def get_task_status(onboarding_id: str, task_id: str, request_id: str) -> OnboardingTask:
    """Retrieve status and metadata of a specific onboarding task."""
    _verify_permission("get_task_status", request_id)

    checklist = get_onboarding_checklist(onboarding_id, request_id)
    for task in checklist.tasks:
        if task.task_id == task_id:
            log_action(
                request_id=request_id,
                agent_name="Onboarding Agent",
                action_type="tool_call",
                tool_called="get_task_status",
                tool_result="success",
                details=f"Retrieved task '{task_id}' ({task.task_name}): {task.status}."
            )
            return task

    raise ToolError(f"Task '{task_id}' not found in onboarding '{onboarding_id}'.")

def send_onboarding_reminder(
    employee_id: str,
    task_name: str,
    due_date: Optional[str],
    message: str,
    request_id: str
) -> Dict[str, Any]:
    """Send an approved onboarding reminder to an employee."""
    _verify_permission("send_onboarding_reminder", request_id)

    if employee_id == "FAIL_REMINDER":
        log_action(request_id, "Onboarding Agent", "tool_call", "send_onboarding_reminder", "failure", "Simulated notification gateway failure.")
        raise ToolError("Failed to deliver reminder notification.")

    full_message = f"Automated assistance: {message}\nWhy did I receive this? This is an automated onboarding progress reminder from Dayflow HRMS."

    log_action(
        request_id=request_id,
        agent_name="Onboarding Agent",
        action_type="tool_call",
        tool_called="send_onboarding_reminder",
        tool_result="success",
        details=f"Sent onboarding reminder to employee '{employee_id}' for task '{task_name}'."
    )

    return {
        "status": "sent",
        "employee_id": employee_id,
        "task_name": task_name,
        "due_date": due_date,
        "message_preview": full_message
    }

def notify_hr(
    employee_id: str,
    onboarding_id: str,
    reason: str,
    details: str,
    request_id: str
) -> Dict[str, Any]:
    """Create an HR escalation notification for blocked or critically overdue onboarding."""
    _verify_permission("notify_hr", request_id)

    if employee_id == "FAIL_ESCALATION":
        log_action(request_id, "Onboarding Agent", "tool_call", "notify_hr", "failure", "Simulated HR ticketing failure.")
        raise ToolError("Failed to deliver HR escalation.")

    escalation_ticket = f"HR-ESC-ONB-{onboarding_id}"

    log_action(
        request_id=request_id,
        agent_name="Onboarding Agent",
        action_type="tool_call",
        tool_called="notify_hr",
        tool_result="success",
        details=f"Created HR escalation ticket '{escalation_ticket}' for employee '{employee_id}': {reason}."
    )

    return {
        "status": "escalated",
        "ticket_id": escalation_ticket,
        "employee_id": employee_id,
        "onboarding_id": onboarding_id,
        "reason": reason,
        "details": details
    }

def create_audit_log(request_id: str, action_type: str, tool_called: str, tool_result: str, details: str) -> str:
    """Explicitly create an audit entry via tool registry."""
    _verify_permission("create_audit_log", request_id)
    return log_action(
        request_id=request_id,
        agent_name="Onboarding Agent",
        action_type=action_type,
        tool_called=tool_called,
        tool_result=tool_result,
        details=details
    )

def restricted_tool_stub(tool_name: str, request_id: str):
    """Helper method to test permission enforcement against prohibited tools."""
    _verify_permission(tool_name, request_id)
