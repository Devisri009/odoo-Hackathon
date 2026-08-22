import os
from typing import List
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from config import settings
from schemas.api import HealthResponse, AgentListResponse, AgentInfo
from routers.auth import router as auth_router
from routers.employees import router as employees_router
from routers.attendance_mgmt import router as attendance_mgmt_router
from routers.time_off import router as time_off_router
from routers.leave import router as leave_agent_router
from routers.attendance import router as attendance_agent_router
from routers.policy import router as policy_router
from routers.onboarding import router as onboarding_router
from routers.reports import router as reports_router

tags_metadata = [
    {
        "name": "System",
        "description": "System health and agent discovery metadata.",
    },
    {
        "name": "Authentication",
        "description": "Employee & Admin authentication, password management, and session verification.",
    },
    {
        "name": "Employee Management",
        "description": "Provisioning, directory search, profile viewing, updating, and deactivation.",
    },
    {
        "name": "Attendance Management",
        "description": "Employee check-in, check-out, working hour calculations, personal logs, company ledger, and daily overview.",
    },
    {
        "name": "Time Off Management",
        "description": "Employee leave submissions, dynamic quotas & balances, company-wide leave review, and approval/rejection workflows.",
    },
    {
        "name": "Leave Agent",
        "description": "Leave request triage, policy & balance verification, and HITL approval drafting.",
    },
    {
        "name": "Attendance Agent",
        "description": "Attendance log analysis, anomaly detection, individual reminders, and systemic outage escalation.",
    },
    {
        "name": "Policy Agent",
        "description": "Read-only HR policy question answering strictly with source citations and confidence metrics.",
    },
    {
        "name": "Onboarding Agent",
        "description": "Employee onboarding checklist tracking, overdue task reminders, and HR escalation.",
    },
    {
        "name": "Report Agent",
        "description": "Authorized document and report generation for payslips, attendance, leave, and onboarding.",
    },
]

app = FastAPI(
    title="Dayflow HRMS - Backend & AI Agent API",
    description=(
        "FastAPI backend integration layer connecting Dayflow HRMS frontend clients "
        "to core HR database services and specialized AI agents."
    ),
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS for Next.js frontend development (localhost and LAN access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+|172\.(1[6-9]|2[0-9]|3[0-1])\.\d+\.\d+)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Core Database Module Routers
app.include_router(auth_router)
app.include_router(employees_router)
app.include_router(attendance_mgmt_router)
app.include_router(time_off_router)

# Include Standalone AI Agent Routers
app.include_router(leave_agent_router)
app.include_router(attendance_agent_router)
app.include_router(policy_router)
app.include_router(onboarding_router)
app.include_router(reports_router)

# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(exc.errors()), "message": "Input validation failed for request payload."}
    )

@app.exception_handler(PermissionError)
async def permission_exception_handler(request: Request, exc: PermissionError):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc), "message": "Security policy violation: action prohibited."}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error occurred.", "message": "An unexpected error occurred while processing the request."}
    )

# System Endpoints
@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health Check Endpoint",
    description="Returns the operational status of the Dayflow HRMS backend service."
)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="Dayflow HRMS Backend")

@app.get(
    "/api/v1/agents",
    response_model=AgentListResponse,
    tags=["System"],
    summary="List Registered AI Agents",
    description="Returns a directory of all registered Dayflow HRMS AI agents and their designated API endpoints."
)
async def list_agents() -> AgentListResponse:
    return AgentListResponse(
        agents=[
            AgentInfo(
                name="Leave Triage Agent",
                endpoint="/api/v1/agents/leave/triage",
                description="Assists HR with leave validation, balance checks, policy compliance, and HITL recommendations."
            ),
            AgentInfo(
                name="Attendance Anomaly Agent",
                endpoint="/api/v1/agents/attendance/analyze",
                description="Identifies missing, late, or systemic attendance anomalies with automated reminders or escalations."
            ),
            AgentInfo(
                name="Policy Q&A Agent",
                endpoint="/api/v1/agents/policy/ask",
                description="Read-only assistant that answers HR policy inquiries strictly with citations and confidence metrics."
            ),
            AgentInfo(
                name="Onboarding Agent",
                endpoint="/api/v1/agents/onboarding/inspect",
                description="Supervises new employee onboarding tasks, sending reminders or triggering HR escalation."
            ),
            AgentInfo(
                name="Report & Payslip Agent",
                endpoint="/api/v1/agents/reports/generate",
                description="Generates authorized employee payslips, monthly attendance logs, leave balances, and onboarding reports."
            ),
        ]
    )
