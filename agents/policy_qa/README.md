# Policy Q&A Agent

A read-only, supervised AI assistant for the Dayflow HRMS project that answers employee policy inquiries strictly based on authoritative HR policy documents.

## Features
- **Least-Privilege / Read-Only**: Enforces strict read-only tool registry. Prohibits operational actions (e.g. applying/approving leave, updating salaries).
- **Source Citations**: Every substantive answer includes authoritative policy names, section numbers, and titles.
- **Deterministic & Safe**: Contains fallback answer synthesis when LLM is unavailable or offline, preventing hallucinations.
- **Audited Execution**: Every query, tool call, refusal, and prohibited action is logged into an immutable audit trail.

## Local Setup & Testing
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment file (optional)
cp .env.example .env

# 3. Run the pytest suite
pytest tests/test_policy_qa.py -v
```

## Python Integration
```python
from agents.policy_qa.agent import run_policy_qa

response = run_policy_qa({
    "request_id": "req-001",
    "user_id": "USR-101",
    "employee_id": "EMP-500",
    "question": "How many paid leave days do I get?"
})
print(response)
```
