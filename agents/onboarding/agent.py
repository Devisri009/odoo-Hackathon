import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import ValidationError
from groq import Groq

from schemas import (
    OnboardingRequest,
    OnboardingResponse,
    OnboardingChecklist,
    OnboardingTask,
    TaskStatus,
    TaskPriority,
    OnboardingSeverity
)
from tools import (
    get_onboarding_checklist,
    send_onboarding_reminder,
    notify_hr,
    ToolError,
    PermissionError
)
from audit import log_action
from config import get_groq_api_key, get_model_name, get_escalation_days, get_current_mock_date

def run_onboarding(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entrypoint for the Onboarding Agent.
    Accepts a dictionary or OnboardingRequest and returns a validated OnboardingResponse dictionary.
    """
    execution_id = str(uuid.uuid4())
    warnings: List[str] = []

    # 1. Validate Input Request
    try:
        if isinstance(request_data, OnboardingRequest):
            req = request_data
        else:
            req = OnboardingRequest(**request_data)
    except ValidationError as e:
        err_msg = f"Request validation failed: {str(e)}"
        log_action(
            request_id=request_data.get("request_id", execution_id) if isinstance(request_data, dict) else execution_id,
            agent_name="Onboarding Agent",
            action_type="validation_error",
            tool_called="N/A",
            tool_result="failed",
            details=err_msg
        )
        return _build_error_response(
            request_id=request_data.get("request_id", execution_id) if isinstance(request_data, dict) else execution_id,
            execution_id=execution_id,
            employee_id=request_data.get("employee_id", "UNKNOWN") if isinstance(request_data, dict) else "UNKNOWN",
            onboarding_id=request_data.get("onboarding_id", "UNKNOWN") if isinstance(request_data, dict) else "UNKNOWN",
            reason=err_msg,
            warnings=[err_msg]
        )

    log_action(
        request_id=req.request_id,
        agent_name="Onboarding Agent",
        action_type="start_inspection",
        tool_called="N/A",
        tool_result="success",
        details=f"Inspecting onboarding for employee '{req.employee_id}', onboarding_id '{req.onboarding_id}'."
    )

    # 2. Retrieve Checklist via Scoped Tool
    try:
        checklist: OnboardingChecklist = get_onboarding_checklist(req.onboarding_id, req.request_id)
    except ToolError as e:
        warnings.append(f"Tool error fetching checklist: {str(e)}")
        return _build_error_response(
            request_id=req.request_id,
            execution_id=execution_id,
            employee_id=req.employee_id,
            onboarding_id=req.onboarding_id,
            reason="Onboarding service failure. Manual HR review required.",
            warnings=warnings
        )
    except Exception as e:
        warnings.append(f"Unexpected error: {str(e)}")
        return _build_error_response(
            request_id=req.request_id,
            execution_id=execution_id,
            employee_id=req.employee_id,
            onboarding_id=req.onboarding_id,
            reason="System exception occurred during checklist retrieval.",
            warnings=warnings
        )

    # 3. Data Integrity & Duplicate Checks
    tasks = checklist.tasks
    task_ids = [t.task_id for t in tasks]
    if len(task_ids) != len(set(task_ids)):
        warnings.append("Duplicate task IDs detected in onboarding checklist.")

    # 4. Task Metrics & Overdue Calculations
    ref_date_str = req.as_of_date or get_current_mock_date()
    try:
        ref_date = datetime.strptime(ref_date_str, "%Y-%m-%d")
    except ValueError:
        ref_date = datetime.utcnow()

    total_tasks = len(tasks)
    completed_tasks_list = [t for t in tasks if t.status == TaskStatus.COMPLETED]
    blocked_tasks_list = [t for t in tasks if t.status == TaskStatus.BLOCKED]
    
    overdue_tasks_list: List[OnboardingTask] = []
    pending_tasks_list: List[OnboardingTask] = []

    escalation_threshold_days = get_escalation_days()
    has_critical_overdue = False
    has_escalated_overdue = False

    for t in tasks:
        if t.status == TaskStatus.COMPLETED or t.status == TaskStatus.BLOCKED:
            continue

        is_overdue = False
        if t.status == TaskStatus.OVERDUE:
            is_overdue = True

        if t.due_date:
            try:
                task_due = datetime.strptime(t.due_date, "%Y-%m-%d")
                if task_due < ref_date:
                    is_overdue = True
                    days_overdue = (ref_date - task_due).days
                    if days_overdue >= escalation_threshold_days:
                        has_escalated_overdue = True
            except ValueError:
                pass

        if is_overdue:
            overdue_tasks_list.append(t)
            if t.priority == TaskPriority.CRITICAL:
                has_critical_overdue = True
        else:
            pending_tasks_list.append(t)

    completed_count = len(completed_tasks_list)
    overdue_count = len(overdue_tasks_list)
    pending_count = total_tasks - completed_count
    completion_pct = round((completed_count / total_tasks) * 100.0, 1) if total_tasks > 0 else 0.0

    # 5. Deterministic Decision Engine
    reminder_sent = False
    hr_escalation_sent = False
    requires_hr_review = False
    severity = OnboardingSeverity.LOW
    recommendation = ""
    reasoning_summary = ""

    if blocked_tasks_list:
        severity = OnboardingSeverity.HIGH
        recommendation = "Manual HR review required"
        requires_hr_review = True
        blocked_names = ", ".join([t.task_name for t in blocked_tasks_list])
        reasoning_summary = f"Onboarding is blocked on: {blocked_names}. Immediate HR intervention required."
        try:
            notify_hr(
                employee_id=req.employee_id,
                onboarding_id=req.onboarding_id,
                reason="Onboarding task blocked",
                details=reasoning_summary,
                request_id=req.request_id
            )
            hr_escalation_sent = True
        except ToolError as e:
            warnings.append(f"Failed to deliver HR escalation: {str(e)}")

    elif has_critical_overdue or has_escalated_overdue or overdue_count >= 3:
        severity = OnboardingSeverity.CRITICAL
        recommendation = "HR escalation required"
        requires_hr_review = True
        overdue_names = ", ".join([t.task_name for t in overdue_tasks_list])
        reasoning_summary = f"Critical/escalated overdue tasks detected: {overdue_names}. Escalating to HR."
        try:
            notify_hr(
                employee_id=req.employee_id,
                onboarding_id=req.onboarding_id,
                reason="Critical onboarding task(s) overdue",
                details=reasoning_summary,
                request_id=req.request_id
            )
            hr_escalation_sent = True
        except ToolError as e:
            warnings.append(f"Failed to deliver HR escalation: {str(e)}")

    elif overdue_count > 0:
        severity = OnboardingSeverity.HIGH
        recommendation = "Follow-up required"
        requires_hr_review = False
        overdue_names = ", ".join([t.task_name for t in overdue_tasks_list])
        reasoning_summary = f"{overdue_count} task(s) are overdue ({overdue_names}). Sent follow-up reminder to employee."
        # Send reminder for top overdue task
        top_overdue = overdue_tasks_list[0]
        try:
            msg = f"Your onboarding task '{top_overdue.task_name}' was due on {top_overdue.due_date}. Please complete it as soon as possible."
            send_onboarding_reminder(
                employee_id=req.employee_id,
                task_name=top_overdue.task_name,
                due_date=top_overdue.due_date,
                message=msg,
                request_id=req.request_id
            )
            reminder_sent = True
        except ToolError as e:
            warnings.append(f"Failed to deliver reminder: {str(e)}")

    elif pending_count > 0:
        severity = OnboardingSeverity.MEDIUM
        recommendation = "Reminder recommended"
        requires_hr_review = False
        pending_names = ", ".join([t.task_name for t in pending_tasks_list])
        reasoning_summary = f"Onboarding is in progress ({completion_pct}% complete). {pending_count} pending task(s): {pending_names}."
        if pending_tasks_list:
            next_task = pending_tasks_list[0]
            try:
                msg = f"Your onboarding checklist still has pending tasks, including '{next_task.task_name}', due on {next_task.due_date}. Please complete it when convenient."
                send_onboarding_reminder(
                    employee_id=req.employee_id,
                    task_name=next_task.task_name,
                    due_date=next_task.due_date,
                    message=msg,
                    request_id=req.request_id
                )
                reminder_sent = True
            except ToolError as e:
                warnings.append(f"Failed to deliver reminder: {str(e)}")

    else:
        severity = OnboardingSeverity.LOW
        recommendation = "Onboarding complete"
        requires_hr_review = False
        reasoning_summary = f"All {total_tasks} onboarding tasks have been successfully completed (100% completion)."

    # 6. Synthesize Natural Language Summary using LLM (if configured) or Deterministic Engine
    reasoning_summary = _synthesize_summary(
        employee_id=req.employee_id,
        completion_pct=completion_pct,
        total_tasks=total_tasks,
        completed_count=completed_count,
        overdue_count=overdue_count,
        pending_count=pending_count,
        recommendation=recommendation,
        reasoning_summary=reasoning_summary
    )

    log_action(
        request_id=req.request_id,
        agent_name="Onboarding Agent",
        action_type="decision_evaluated",
        tool_called="N/A",
        tool_result="success",
        details=f"Onboarding decision: {recommendation}, Severity: {severity}, Completion: {completion_pct}%."
    )

    return _build_response(
        request_id=req.request_id,
        execution_id=execution_id,
        success=True,
        employee_id=req.employee_id,
        onboarding_id=req.onboarding_id,
        completion_percentage=completion_pct,
        total_tasks=total_tasks,
        completed_tasks=completed_count,
        pending_tasks=pending_count,
        overdue_tasks=overdue_count,
        recommendation=recommendation,
        severity=severity,
        reminder_sent=reminder_sent,
        hr_escalation_sent=hr_escalation_sent,
        requires_hr_review=requires_hr_review,
        reasoning_summary=reasoning_summary,
        warnings=warnings
    )

def _synthesize_summary(
    employee_id: str,
    completion_pct: float,
    total_tasks: int,
    completed_count: int,
    overdue_count: int,
    pending_count: int,
    recommendation: str,
    reasoning_summary: str
) -> str:
    """Generate professional summary using Groq LLM if active, or deterministic text."""
    api_key = get_groq_api_key()
    if api_key and api_key != "mock":
        try:
            client = Groq(api_key=api_key)
            prompt = (
                f"You are the Dayflow HRMS Onboarding Agent. Write a concise 1-2 sentence professional "
                f"status update for Employee '{employee_id}'.\n"
                f"Completion: {completion_pct}% ({completed_count}/{total_tasks} completed).\n"
                f"Pending: {pending_count}, Overdue: {overdue_count}.\n"
                f"Recommendation: {recommendation}.\n"
                f"Context: {reasoning_summary}\n\nSummary:"
            )
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=get_model_name(),
                temperature=0.0
            )
            llm_text = completion.choices[0].message.content.strip()
            if llm_text:
                return llm_text
        except Exception:
            pass

    return reasoning_summary

def _build_response(
    request_id: str,
    execution_id: str,
    success: bool,
    employee_id: str,
    onboarding_id: str,
    completion_percentage: float,
    total_tasks: int,
    completed_tasks: int,
    pending_tasks: int,
    overdue_tasks: int,
    recommendation: str,
    severity: OnboardingSeverity,
    reminder_sent: bool,
    hr_escalation_sent: bool,
    requires_hr_review: bool,
    reasoning_summary: str,
    warnings: List[str]
) -> Dict[str, Any]:
    res = OnboardingResponse(
        request_id=request_id,
        agent_name="Onboarding Agent",
        success=success,
        employee_id=employee_id,
        onboarding_id=onboarding_id,
        completion_percentage=completion_percentage,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks,
        overdue_tasks=overdue_tasks,
        recommendation=recommendation,
        severity=severity,
        reminder_sent=reminder_sent,
        hr_escalation_sent=hr_escalation_sent,
        requires_hr_review=requires_hr_review,
        reasoning_summary=reasoning_summary,
        warnings=warnings,
        audit_id=execution_id
    )
    return res.model_dump(mode='json')

def _build_error_response(
    request_id: str,
    execution_id: str,
    employee_id: str,
    onboarding_id: str,
    reason: str,
    warnings: List[str]
) -> Dict[str, Any]:
    res = OnboardingResponse(
        request_id=request_id,
        agent_name="Onboarding Agent",
        success=False,
        employee_id=employee_id,
        onboarding_id=onboarding_id,
        completion_percentage=0.0,
        total_tasks=0,
        completed_tasks=0,
        pending_tasks=0,
        overdue_tasks=0,
        recommendation="Manual HR review required",
        severity=OnboardingSeverity.HIGH,
        reminder_sent=False,
        hr_escalation_sent=False,
        requires_hr_review=True,
        reasoning_summary=reason,
        warnings=warnings,
        audit_id=execution_id
    )
    return res.model_dump(mode='json')
