from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional, List, Literal
from datetime import datetime

class PolicyQuestionRequest(BaseModel):
    request_id: str = Field(..., description="Unique request identifier")
    user_id: str = Field(..., description="ID of the user making the request")
    employee_id: str = Field(..., description="ID of the employee")
    question: str = Field(..., description="Policy question asked by the employee")

    @field_validator('question')
    @classmethod
    def validate_question(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Question cannot be empty or whitespace only")
        if len(cleaned) > 1000:
            raise ValueError("Question exceeds maximum allowed length of 1000 characters")
        return cleaned

class PolicySearchRequest(BaseModel):
    query: str = Field(..., min_length=1)

class PolicySearchResult(BaseModel):
    policy_name: str
    section: str
    title: str
    snippet: str
    score: float

class PolicySection(BaseModel):
    policy_name: str
    section: str
    title: str
    content: str

class PolicySource(BaseModel):
    policy_name: str
    section: str
    title: str

class PolicyQAResponse(BaseModel):
    request_id: str
    agent_name: str = "Policy Q&A Agent"
    success: bool
    answer: str
    sources: List[PolicySource]
    confidence: Literal["HIGH", "MEDIUM", "LOW"]
    ask_hr: bool
    reasoning_summary: str
    warnings: List[str] = Field(default_factory=list)
    audit_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AuditEntry(BaseModel):
    audit_id: str
    request_id: str
    agent_name: str = "Policy Q&A Agent"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    action_type: str
    tool_called: str
    tool_result: str
    details: str
