import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import ValidationError
from groq import Groq

from schemas import (
    ReportRequest,
    ReportResponse,
    ReportType,
    PayrollData,
    Payslip,
    AttendanceReportData,
    LeaveBalanceReportData,
    OnboardingReportData
)
from tools import (
    get_authorized_payroll_data,
    generate_payslip,
    get_attendance_report_data,
    get_leave_report_data,
    get_onboarding_report_data,
    ToolError,
    PermissionError
)
from audit import log_action
from config import get_groq_api_key, get_model_name, get_default_report_period

def run_report_payslip(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entrypoint for the Report & Payslip Agent.
    Accepts a dictionary or ReportRequest and returns a validated ReportResponse dictionary.
    """
    execution_id = str(uuid.uuid4())
    warnings: List[str] = []

    # 1. Validate Input Request
    try:
        if isinstance(request_data, ReportRequest):
            req = request_data
        else:
            req = ReportRequest(**request_data)
    except ValidationError as e:
        err_msg = f"Request validation failed: {str(e)}"
        log_action(
            request_id=request_data.get("request_id", execution_id) if isinstance(request_data, dict) else execution_id,
            agent_name="Report & Payslip Agent",
            action_type="validation_error",
            tool_called="N/A",
            tool_result="failed",
            details=err_msg
        )
        return _build_error_response(
            request_id=request_data.get("request_id", execution_id) if isinstance(request_data, dict) else execution_id,
            execution_id=execution_id,
            employee_id=request_data.get("employee_id", "UNKNOWN") if isinstance(request_data, dict) else "UNKNOWN",
            report_type=ReportType.PAYSLIP,
            report_period=request_data.get("report_period") if isinstance(request_data, dict) else None,
            reason=err_msg,
            warnings=[err_msg]
        )

    log_action(
        request_id=req.request_id,
        agent_name="Report & Payslip Agent",
        action_type="start_report_generation",
        tool_called="N/A",
        tool_result="success",
        details=f"Starting generation of '{req.report_type}' for employee '{req.employee_id}'."
    )

    # 2. Dispatch Report Generation by Type
    try:
        if req.report_type == ReportType.PAYSLIP:
            period = req.report_period or get_default_report_period()
            payroll_data = get_authorized_payroll_data(req.employee_id, period, req.request_id)
            payslip = generate_payslip(payroll_data, req.request_id)
            
            document_name = f"PAYSLIP_{req.employee_id}_{period}.txt"
            content = payslip.model_dump(mode='json')
            reasoning = f"Generated authorized payslip for {payslip.employee_name} ({req.employee_id}) for period {period}. Gross: ${payslip.gross_salary:,.2f}, Deductions: ${payslip.total_deductions:,.2f}, Net: ${payslip.net_salary:,.2f} USD."

        elif req.report_type == ReportType.ATTENDANCE_REPORT:
            period = req.report_period or get_default_report_period()
            attendance_data = get_attendance_report_data(req.employee_id, period, req.request_id)
            
            document_name = f"ATTENDANCE_REPORT_{req.employee_id}_{period}.txt"
            content = attendance_data.model_dump(mode='json')
            reasoning = f"Generated monthly attendance report for {attendance_data.employee_name} ({req.employee_id}) for period {period}. Working days: {attendance_data.working_days}, Present: {attendance_data.present_days}, Attendance Rate: {attendance_data.attendance_rate}%."

        elif req.report_type == ReportType.LEAVE_BALANCE_REPORT:
            leave_data = get_leave_report_data(req.employee_id, req.request_id)
            
            document_name = f"LEAVE_BALANCE_REPORT_{req.employee_id}.txt"
            content = leave_data.model_dump(mode='json')
            reasoning = f"Generated leave balance report for {leave_data.employee_name} ({req.employee_id}) as of {leave_data.as_of_date} with {len(leave_data.balances)} leave categories."

        elif req.report_type == ReportType.ONBOARDING_COMPLETION_REPORT:
            onb_data = get_onboarding_report_data(req.employee_id, req.request_id)
            
            document_name = f"ONBOARDING_REPORT_{req.employee_id}.txt"
            content = onb_data.model_dump(mode='json')
            reasoning = f"Generated onboarding progress report for {onb_data.employee_name} ({req.employee_id}). Progress: {onb_data.completion_percentage}% ({onb_data.completed_tasks}/{onb_data.total_tasks} completed)."

        else:
            raise ToolError(f"Unsupported report type '{req.report_type}'.")

    except PermissionError as e:
        warnings.append(f"Security Alert: {str(e)}")
        return _build_error_response(
            request_id=req.request_id,
            execution_id=execution_id,
            employee_id=req.employee_id,
            report_type=req.report_type,
            report_period=req.report_period,
            reason=f"Access denied: {str(e)}",
            warnings=warnings
        )
    except ToolError as e:
        warnings.append(f"Report generation tool error: {str(e)}")
        return _build_error_response(
            request_id=req.request_id,
            execution_id=execution_id,
            employee_id=req.employee_id,
            report_type=req.report_type,
            report_period=req.report_period,
            reason=f"Report generation failed: {str(e)}",
            warnings=warnings
        )
    except Exception as e:
        warnings.append(f"Unexpected system error: {str(e)}")
        return _build_error_response(
            request_id=req.request_id,
            execution_id=execution_id,
            employee_id=req.employee_id,
            report_type=req.report_type,
            report_period=req.report_period,
            reason="An unexpected system error occurred during document generation.",
            warnings=warnings
        )

    # 3. Formulate Summary using LLM (if configured) or Deterministic Template
    summary = _synthesize_summary(req.report_type.value, req.employee_id, reasoning)

    log_action(
        request_id=req.request_id,
        agent_name="Report & Payslip Agent",
        action_type="report_completed",
        tool_called="generate_report",
        tool_result="success",
        details=f"Successfully generated document '{document_name}' of type '{req.report_type}'."
    )

    res = ReportResponse(
        request_id=req.request_id,
        agent_name="Report & Payslip Agent",
        success=True,
        report_type=req.report_type,
        employee_id=req.employee_id,
        report_period=req.report_period or get_default_report_period(),
        generated=True,
        document_name=document_name,
        content=content,
        requires_hr_review=False,
        reasoning_summary=summary,
        warnings=warnings,
        audit_id=execution_id
    )
    return res.model_dump(mode='json')

def _synthesize_summary(report_type: str, employee_id: str, deterministic_text: str) -> str:
    """Generate natural language summary using Groq if available or fallback."""
    api_key = get_groq_api_key()
    if api_key and api_key != "mock":
        try:
            client = Groq(api_key=api_key)
            prompt = (
                f"You are the Dayflow HRMS Report & Payslip Agent. Write a 1-sentence concise notification "
                f"confirming the generation of a '{report_type}' for employee '{employee_id}'.\n"
                f"Context: {deterministic_text}\n\nSummary:"
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

    return deterministic_text

def _build_error_response(
    request_id: str,
    execution_id: str,
    employee_id: str,
    report_type: ReportType,
    report_period: Optional[str],
    reason: str,
    warnings: List[str]
) -> Dict[str, Any]:
    res = ReportResponse(
        request_id=request_id,
        agent_name="Report & Payslip Agent",
        success=False,
        report_type=report_type,
        employee_id=employee_id,
        report_period=report_period,
        generated=False,
        document_name="N/A",
        content={},
        requires_hr_review=True,
        reasoning_summary=reason,
        warnings=warnings,
        audit_id=execution_id
    )
    return res.model_dump(mode='json')
