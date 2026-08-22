from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class AttendanceRecord(BaseModel):
    employee_id: str
    date: str
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    expected_check_in: str = "09:00:00"
    expected_check_out: str = "17:00:00"

class AttendanceAnomalyRequest(BaseModel):
    request_id: str
    target_date: str
    employee_ids: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AttendanceAnomalyResponse(BaseModel):
    request_id: str
    agent_name: str
    success: bool
    anomalies_detected: List[dict]
    systemic_issue: bool
    recommendation: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    notification_sent: bool
    requires_hr_review: bool
    reasoning_summary: str
    warnings: List[str]
    audit_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AuditEntry(BaseModel):
    audit_id: str
    request_id: str
    agent_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action_type: str
    tool_called: str
    tool_result: str
    details: str

class NotificationRequest(BaseModel):
    employee_id: str
    date: str
    issue_type: str
    message: str
