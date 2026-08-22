from enum import Enum
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
import re

class ReportType(str, Enum):
    PAYSLIP = "PAYSLIP"
    ATTENDANCE_REPORT = "ATTENDANCE_REPORT"
    LEAVE_BALANCE_REPORT = "LEAVE_BALANCE_REPORT"
    ONBOARDING_COMPLETION_REPORT = "ONBOARDING_COMPLETION_REPORT"

class ReportRequest(BaseModel):
    request_id: str = Field(..., description="Unique request identifier")
    user_id: str = Field(..., description="Requesting user identifier")
    employee_id: str = Field(..., description="Target employee identifier")
    report_type: ReportType = Field(..., description="Type of document/report to generate")
    report_period: Optional[str] = Field(None, description="Report or pay period (e.g. YYYY-MM)")

    @field_validator('employee_id', 'user_id')
    @classmethod
    def validate_non_empty_ids(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("ID fields cannot be empty or whitespace only")
        return v.strip()

    @field_validator('report_period')
    @classmethod
    def validate_period_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_clean = v.strip()
            if not v_clean:
                return None
            if not re.match(r"^\d{4}(-\d{2})?$", v_clean):
                raise ValueError(f"Invalid report_period format '{v}'. Expected YYYY or YYYY-MM.")
            return v_clean
        return v

class PayrollData(BaseModel):
    employee_id: str
    employee_name: str
    pay_period: str
    base_salary: float
    allowances: Dict[str, float] = Field(default_factory=dict)
    deductions: Dict[str, float] = Field(default_factory=dict)

class Payslip(BaseModel):
    employee_id: str
    employee_name: str
    pay_period: str
    base_salary: float
    allowances: Dict[str, float]
    gross_salary: float
    deductions: Dict[str, float]
    total_deductions: float
    net_salary: float
    currency: str = "USD"
    disbursement_date: str
    document_text: str

class AttendanceReportData(BaseModel):
    employee_id: str
    employee_name: str
    report_period: str
    working_days: int
    present_days: int
    absent_days: int
    late_days: int
    missing_attendance_days: int
    attendance_rate: float
    document_text: str

class LeaveBalanceItem(BaseModel):
    leave_type: str
    allocated_days: float
    used_days: float
    remaining_days: float

class LeaveBalanceReportData(BaseModel):
    employee_id: str
    employee_name: str
    as_of_date: str
    balances: List[LeaveBalanceItem]
    document_text: str

class OnboardingReportData(BaseModel):
    employee_id: str
    employee_name: str
    onboarding_id: str
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    completion_percentage: float
    document_text: str

class ReportResponse(BaseModel):
    request_id: str
    agent_name: str = "Report & Payslip Agent"
    success: bool
    report_type: ReportType
    employee_id: str
    report_period: Optional[str]
    generated: bool
    document_name: str
    content: Dict[str, Any]
    requires_hr_review: bool
    reasoning_summary: str
    warnings: List[str] = Field(default_factory=list)
    audit_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AuditEntry(BaseModel):
    audit_id: str
    request_id: str
    agent_name: str = "Report & Payslip Agent"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action_type: str
    tool_called: str
    tool_result: str
    details: str
