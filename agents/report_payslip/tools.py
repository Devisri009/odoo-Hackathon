from typing import Dict, Any, List, Optional
from schemas import (
    PayrollData,
    Payslip,
    AttendanceReportData,
    LeaveBalanceItem,
    LeaveBalanceReportData,
    OnboardingReportData
)
from mock_data import (
    MOCK_EMPLOYEES,
    MOCK_PAYROLL_DATABASE,
    MOCK_ATTENDANCE_REPORT_DATABASE,
    MOCK_LEAVE_BALANCE_DATABASE,
    MOCK_ONBOARDING_REPORT_DATABASE
)
from audit import log_action
from permissions import check_permission

class ToolError(Exception):
    """Raised when a report generation tool encounters a data or operational error."""
    pass

class PermissionError(Exception):
    """Raised when an unauthorized tool or access is attempted."""
    pass

def _verify_permission(tool_name: str, request_id: str):
    """Enforces least-privilege tool execution permissions."""
    if not check_permission(tool_name):
        log_action(
            request_id=request_id,
            agent_name="Report & Payslip Agent",
            action_type="permission_denied",
            tool_called=tool_name,
            tool_result="failed",
            details=f"Execution of prohibited tool '{tool_name}' was blocked by policy."
        )
        raise PermissionError(f"Access to '{tool_name}' is denied: prohibited for Report & Payslip Agent.")

def get_authorized_payroll_data(employee_id: str, pay_period: str, request_id: str) -> PayrollData:
    """Retrieve authorized payroll data for a given employee and pay period."""
    _verify_permission("get_authorized_payroll_data", request_id)

    emp = MOCK_EMPLOYEES.get(employee_id)
    if not emp:
        log_action(request_id, "Report & Payslip Agent", "tool_call", "get_authorized_payroll_data", "failure", f"Employee '{employee_id}' not found.")
        raise ToolError(f"Employee '{employee_id}' does not exist.")

    if not emp.get("authorized_payroll", False):
        log_action(request_id, "Report & Payslip Agent", "permission_denied", "get_authorized_payroll_data", "failed", f"Unauthorized payroll access for '{employee_id}'.")
        raise PermissionError(f"Access denied: requester is not authorized to access payroll for '{employee_id}'.")

    key = f"{employee_id}_{pay_period}"
    data = MOCK_PAYROLL_DATABASE.get(key)
    if not data:
        log_action(request_id, "Report & Payslip Agent", "tool_call", "get_authorized_payroll_data", "failure", f"No payroll data for period '{pay_period}'.")
        raise ToolError(f"No payroll record found for employee '{employee_id}' in period '{pay_period}'.")

    log_action(
        request_id=request_id,
        agent_name="Report & Payslip Agent",
        action_type="tool_call",
        tool_called="get_authorized_payroll_data",
        tool_result="success",
        details=f"Retrieved authorized payroll metadata for '{employee_id}', period '{pay_period}'."
    )

    return PayrollData(
        employee_id=data["employee_id"],
        employee_name=data["employee_name"],
        pay_period=data["pay_period"],
        base_salary=data["base_salary"],
        allowances=data.get("allowances", {}),
        deductions=data.get("deductions", {})
    )

def generate_payslip(payroll_data: PayrollData, request_id: str) -> Payslip:
    """Generate structured payslip with deterministic salary and deduction arithmetic."""
    _verify_permission("generate_payslip", request_id)

    base = payroll_data.base_salary
    total_allowances = sum(payroll_data.allowances.values())
    gross_salary = round(base + total_allowances, 2)
    total_deductions = round(sum(payroll_data.deductions.values()), 2)
    net_salary = round(gross_salary - total_deductions, 2)

    allowance_lines = "\n".join([f"  - {k.replace('_', ' ').title()}: ${v:,.2f}" for k, v in payroll_data.allowances.items()])
    deduction_lines = "\n".join([f"  - {k.replace('_', ' ').title()}: ${v:,.2f}" for k, v in payroll_data.deductions.items()])

    doc_text = (
        f"====================================================\n"
        f"                 DAYFLOW HRMS PAYSLIP               \n"
        f"====================================================\n"
        f"Employee: {payroll_data.employee_name} ({payroll_data.employee_id})\n"
        f"Pay Period: {payroll_data.pay_period}\n"
        f"Disbursement Date: Last Working Day of {payroll_data.pay_period}\n"
        f"----------------------------------------------------\n"
        f"EARNINGS:\n"
        f"  - Base Salary: ${base:,.2f}\n"
        f"{allowance_lines}\n"
        f"TOTAL GROSS SALARY: ${gross_salary:,.2f}\n"
        f"----------------------------------------------------\n"
        f"DEDUCTIONS:\n"
        f"{deduction_lines}\n"
        f"TOTAL DEDUCTIONS: ${total_deductions:,.2f}\n"
        f"====================================================\n"
        f"NET TAKE-HOME PAY: ${net_salary:,.2f} USD\n"
        f"===================================================="
    )

    log_action(
        request_id=request_id,
        agent_name="Report & Payslip Agent",
        action_type="tool_call",
        tool_called="generate_payslip",
        tool_result="success",
        details=f"Generated payslip for employee '{payroll_data.employee_id}' for period '{payroll_data.pay_period}'."
    )

    return Payslip(
        employee_id=payroll_data.employee_id,
        employee_name=payroll_data.employee_name,
        pay_period=payroll_data.pay_period,
        base_salary=base,
        allowances=payroll_data.allowances,
        gross_salary=gross_salary,
        deductions=payroll_data.deductions,
        total_deductions=total_deductions,
        net_salary=net_salary,
        currency="USD",
        disbursement_date=f"{payroll_data.pay_period}-31",
        document_text=doc_text
    )

def get_attendance_report_data(employee_id: str, report_period: str, request_id: str) -> AttendanceReportData:
    """Retrieve and compute monthly attendance statistics for an employee."""
    _verify_permission("get_attendance_report_data", request_id)

    emp = MOCK_EMPLOYEES.get(employee_id)
    if not emp:
        raise ToolError(f"Employee '{employee_id}' not found.")

    key = f"{employee_id}_{report_period}"
    data = MOCK_ATTENDANCE_REPORT_DATABASE.get(key)
    if not data:
        raise ToolError(f"No attendance data found for employee '{employee_id}' in period '{report_period}'.")

    working_days = data["working_days"]
    present_days = data["present_days"]
    rate = round((present_days / working_days) * 100.0, 1) if working_days > 0 else 0.0

    doc_text = (
        f"DAYFLOW HRMS - MONTHLY ATTENDANCE REPORT\n"
        f"Employee: {data['employee_name']} ({employee_id})\n"
        f"Period: {report_period}\n"
        f"Total Working Days: {working_days}\n"
        f"Present Days: {present_days}\n"
        f"Absent Days: {data['absent_days']}\n"
        f"Late Check-ins: {data['late_days']}\n"
        f"Missing Punches: {data['missing_attendance_days']}\n"
        f"Attendance Rate: {rate}%"
    )

    log_action(
        request_id=request_id,
        agent_name="Report & Payslip Agent",
        action_type="tool_call",
        tool_called="get_attendance_report_data",
        tool_result="success",
        details=f"Retrieved attendance report for '{employee_id}', period '{report_period}'."
    )

    return AttendanceReportData(
        employee_id=employee_id,
        employee_name=data["employee_name"],
        report_period=report_period,
        working_days=working_days,
        present_days=present_days,
        absent_days=data["absent_days"],
        late_days=data["late_days"],
        missing_attendance_days=data["missing_attendance_days"],
        attendance_rate=rate,
        document_text=doc_text
    )

def get_leave_report_data(employee_id: str, request_id: str) -> LeaveBalanceReportData:
    """Retrieve leave balance summary for an employee."""
    _verify_permission("get_leave_report_data", request_id)

    emp = MOCK_EMPLOYEES.get(employee_id)
    if not emp:
        raise ToolError(f"Employee '{employee_id}' not found.")

    data = MOCK_LEAVE_BALANCE_DATABASE.get(employee_id)
    if not data:
        raise ToolError(f"No leave balance records found for employee '{employee_id}'.")

    items = [LeaveBalanceItem(**b) for b in data.get("balances", [])]
    lines = [f"  - {i.leave_type}: {i.allocated_days} allocated, {i.used_days} used, {i.remaining_days} remaining" for i in items]

    doc_text = (
        f"DAYFLOW HRMS - LEAVE BALANCE REPORT\n"
        f"Employee: {data['employee_name']} ({employee_id})\n"
        f"As of Date: {data['as_of_date']}\n"
        f"------------------------------------\n"
        f"BALANCES:\n" + "\n".join(lines)
    )

    log_action(
        request_id=request_id,
        agent_name="Report & Payslip Agent",
        action_type="tool_call",
        tool_called="get_leave_report_data",
        tool_result="success",
        details=f"Retrieved leave balance report for '{employee_id}'."
    )

    return LeaveBalanceReportData(
        employee_id=employee_id,
        employee_name=data["employee_name"],
        as_of_date=data["as_of_date"],
        balances=items,
        document_text=doc_text
    )

def get_onboarding_report_data(employee_id: str, request_id: str) -> OnboardingReportData:
    """Retrieve onboarding progress metrics for an employee."""
    _verify_permission("get_onboarding_report_data", request_id)

    emp = MOCK_EMPLOYEES.get(employee_id)
    if not emp:
        raise ToolError(f"Employee '{employee_id}' not found.")

    data = MOCK_ONBOARDING_REPORT_DATABASE.get(employee_id)
    if not data:
        raise ToolError(f"No onboarding report data found for employee '{employee_id}'.")

    total = data["total_tasks"]
    completed = data["completed_tasks"]
    pct = round((completed / total) * 100.0, 1) if total > 0 else 0.0

    doc_text = (
        f"DAYFLOW HRMS - ONBOARDING PROGRESS REPORT\n"
        f"Employee: {data['employee_name']} ({employee_id})\n"
        f"Onboarding ID: {data['onboarding_id']}\n"
        f"Total Tasks: {total}\n"
        f"Completed Tasks: {completed}\n"
        f"Pending Tasks: {data['pending_tasks']}\n"
        f"Overdue Tasks: {data['overdue_tasks']}\n"
        f"Completion: {pct}%"
    )

    log_action(
        request_id=request_id,
        agent_name="Report & Payslip Agent",
        action_type="tool_call",
        tool_called="get_onboarding_report_data",
        tool_result="success",
        details=f"Retrieved onboarding report for '{employee_id}'."
    )

    return OnboardingReportData(
        employee_id=employee_id,
        employee_name=data["employee_name"],
        onboarding_id=data["onboarding_id"],
        total_tasks=total,
        completed_tasks=completed,
        pending_tasks=data["pending_tasks"],
        overdue_tasks=data["overdue_tasks"],
        completion_percentage=pct,
        document_text=doc_text
    )

def generate_report(report_type: str, data: Dict[str, Any], request_id: str) -> Dict[str, Any]:
    """Generic tool stub for generating structured report outputs."""
    _verify_permission("generate_report", request_id)
    log_action(
        request_id=request_id,
        agent_name="Report & Payslip Agent",
        action_type="tool_call",
        tool_called="generate_report",
        tool_result="success",
        details=f"Generated report payload of type '{report_type}'."
    )
    return {"status": "success", "report_type": report_type, "payload": data}

def create_audit_log(request_id: str, action_type: str, tool_called: str, tool_result: str, details: str) -> str:
    """Explicitly create an audit entry via tool registry."""
    _verify_permission("create_audit_log", request_id)
    return log_action(
        request_id=request_id,
        agent_name="Report & Payslip Agent",
        action_type=action_type,
        tool_called=tool_called,
        tool_result=tool_result,
        details=details
    )

def restricted_tool_stub(tool_name: str, request_id: str):
    """Helper method to test permission enforcement against prohibited tools."""
    _verify_permission(tool_name, request_id)
