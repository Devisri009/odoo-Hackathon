from enum import Enum
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional, List, Literal
from datetime import datetime

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"
    BLOCKED = "BLOCKED"

class TaskPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class OnboardingSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class OnboardingTask(BaseModel):
    task_id: str
    employee_id: str
    task_name: str
    status: TaskStatus
    due_date: Optional[str] = None
    completed_at: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM

class OnboardingChecklist(BaseModel):
    onboarding_id: str
    employee_id: str
    start_date: str
    tasks: List[OnboardingTask]

class OnboardingRequest(BaseModel):
    request_id: str = Field(..., description="Unique request identifier")
    employee_id: str = Field(..., description="ID of the new employee")
    onboarding_id: str = Field(..., description="ID of the onboarding process")
    start_date: Optional[str] = Field(None, description="Employee joining date (YYYY-MM-DD)")
    as_of_date: Optional[str] = Field(None, description="Reference evaluation date (YYYY-MM-DD)")

    @field_validator('employee_id', 'onboarding_id')
    @classmethod
    def validate_non_empty_ids(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("ID field cannot be empty or whitespace only")
        return v.strip()

    @field_validator('start_date', 'as_of_date')
    @classmethod
    def validate_date_formats(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_clean = v.strip()
            if not v_clean:
                return None
            try:
                datetime.strptime(v_clean, "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Invalid date format '{v}'. Expected YYYY-MM-DD.")
            return v_clean
        return v

class ReminderRequest(BaseModel):
    employee_id: str
    task_name: str
    due_date: Optional[str] = None
    message: str

class EscalationRequest(BaseModel):
    employee_id: str
    onboarding_id: str
    reason: str
    details: str

class OnboardingResponse(BaseModel):
    request_id: str
    agent_name: str = "Onboarding Agent"
    success: bool
    employee_id: str
    onboarding_id: str
    completion_percentage: float
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    overdue_tasks: int
    recommendation: str
    severity: OnboardingSeverity
    reminder_sent: bool
    hr_escalation_sent: bool
    requires_hr_review: bool
    reasoning_summary: str
    warnings: List[str] = Field(default_factory=list)
    audit_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AuditEntry(BaseModel):
    audit_id: str
    request_id: str
    agent_name: str = "Onboarding Agent"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action_type: str
    tool_called: str
    tool_result: str
    details: str
