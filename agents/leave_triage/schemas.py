from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional, Literal, List
from datetime import date, datetime

class LeaveTriageRequest(BaseModel):
    request_id: str
    user_id: str
    employee_id: str
    leave_request_id: str
    leave_type: Literal["paid", "sick", "unpaid"]
    start_date: date
    end_date: date
    remarks: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('end_date')
    @classmethod
    def check_dates(cls, v: date, info: ValidationInfo) -> date:
        if 'start_date' in info.data and v < info.data['start_date']:
            raise ValueError("end_date cannot be before start_date")
        return v

class LeaveTriageResponse(BaseModel):
    request_id: str
    agent_name: str
    success: bool
    recommendation: Literal["approve", "reject", "review"]
    policy_compliant: bool
    balance_sufficient: bool
    validation_passed: bool
    reasoning_summary: str
    draft_note: str
    requires_human_approval: bool = True
    hitl_id: Optional[str]
    warnings: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class HITLRequest(BaseModel):
    hitl_id: str
    execution_id: str
    leave_request_id: str
    requested_by_agent: str
    recommendation: str
    status: str = "pending"
    draft_note: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AuditLog(BaseModel):
    audit_id: str
    execution_id: str
    agent_name: str
    actor_type: str
    actor_id: str
    action: str
    tool_name: str
    resource_type: str
    resource_id: str
    result: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
