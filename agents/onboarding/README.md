# Onboarding Agent

A supervised AI agent for Dayflow HRMS that tracks employee onboarding workflows, detects pending and overdue tasks, triggers automated employee reminders, and escalates critical or blocked onboarding items to HR.

## Features
- **Deterministic Evaluation**: Rules-based status evaluation, overdue detection, and completion calculations.
- **Automated Reminders**: Sends polite reminders with standard `"Automated assistance"` headers for pending or overdue tasks.
- **Configurable Escalation**: Automatically generates HR escalations for critical tasks or tasks overdue beyond the threshold.
- **Least-Privilege Security**: Strictly read-only on core employee data; cannot directly modify employee profiles, salaries, or onboarding databases.

## Local Setup & Testing
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment file (optional)
cp .env.example .env

# 3. Run the test suite
pytest tests/test_onboarding.py -v
```

## Python Integration
```python
from agents.onboarding.agent import run_onboarding

response = run_onboarding({
    "request_id": "req-onb-001",
    "employee_id": "EMP001",
    "onboarding_id": "ONB_COMPLETED",
    "start_date": "2026-08-01"
})
print(response)
```
