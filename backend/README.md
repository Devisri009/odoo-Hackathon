# Dayflow HRMS - FastAPI Backend Integration Layer

A clean, modular FastAPI backend that bridges frontend clients with the five standalone, specialized Dayflow HRMS AI agents.

## Architecture

```
Frontend (Next.js)
       ↓ HTTP (JSON)
FastAPI Backend (Port 8000)
       ↓
  Agent Routers
  ├── /api/v1/agents/leave/triage       → Leave Triage Agent (HITL)
  ├── /api/v1/agents/attendance/analyze → Attendance Anomaly Agent
  ├── /api/v1/agents/policy/ask         → Policy Q&A Agent (Read-Only)
  ├── /api/v1/agents/onboarding/inspect → Onboarding Agent (Supervised)
  └── /api/v1/agents/reports/generate   → Report & Payslip Agent (Authorized)
       ↓
  Structured Response (JSON)
```

## Features
- **Strict Separation of Concerns**: Contains no agent business logic; routes directly to standalone immutable agent modules.
- **Full OpenAPI / Swagger 3.0 Documentation**: Pre-configured tags, request/response models, and detailed summaries at `/docs`.
- **Package-Safe Agent Invocation**: Dedicated isolated harness (`agent_loader.py`) preventing internal namespace collisions.
- **Configurable CORS**: Supports Next.js localhost frontend communication out-of-the-box.

---

## Local Setup & Execution

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
```bash
cp .env.example .env
```

### 3. Start the API Server
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- **Interactive Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc UI**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **OpenAPI Schema**: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)
- **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **Agent Directory**: [http://127.0.0.1:8000/api/v1/agents](http://127.0.0.1:8000/api/v1/agents)

---

## Running Automated Backend Tests

```bash
pytest tests/test_api.py -v
```
