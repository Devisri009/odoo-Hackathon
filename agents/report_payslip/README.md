# Report & Payslip Agent

A supervised, read-only AI agent for the Dayflow HRMS project that generates authorized employee documents and operational reports.

## Supported Documents & Reports
- **Payslips**: Formats detailed salary statements with base pay, allowances, deductions, gross pay, and net pay.
- **Attendance Reports**: Monthly working days, present days, absent days, late arrivals, and attendance rate.
- **Leave Balance Reports**: Current leave allocations, consumed days, and remaining balances per category.
- **Onboarding Completion Reports**: Onboarding checklist progress, total tasks, completed, pending, and overdue counts.

## Security & Privacy Guardrails
- **Read-Only / Document Generation Only**: Cannot modify employee profiles, compensation, attendance, or leave balances.
- **Authorization Enforced**: Prohibits unauthorized users from accessing sensitive payroll records.
- **Audited Execution**: Every document creation and access denial is tracked without leaking raw salary data into audit logs.

## Setup & Testing
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment file (optional)
cp .env.example .env

# 3. Run the pytest suite
pytest tests/test_report_payslip.py -v
```

## Python Integration
```python
from agents.report_payslip.agent import run_report_payslip

response = run_report_payslip({
    "request_id": "req-rep-001",
    "user_id": "USR-101",
    "employee_id": "EMP001",
    "report_type": "PAYSLIP",
    "report_period": "2026-07"
})
print(response)
```
