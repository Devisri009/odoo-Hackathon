# Odoo-Hackathon
# HRMS — Human Resource Management System

A modern, role-based Human Resource Management System that centralizes employee management, attendance, time off, salary, and payroll operations in a single platform.

## 🚀 Features

### 👨‍💼 Admin / HR Dashboard

The Admin/HR dashboard provides centralized control over the organization's HR operations.

- View HR overview and key statistics
- Manage employees
- Add, edit, and view employee profiles
- View organization-wide attendance
- Monitor employee check-in / check-out
- Manage time-off requests
- Approve or reject leave requests
- Manage leave allocations
- Configure employee salaries
- Manage salary components and deductions
- View payroll information
- Access authorized employee and HR data

### 👤 Employee Portal

Employees have access to their own HR information and activities.

- View personal profile
- View employee information
- Check in / check out
- View attendance history
- Apply for time off
- Upload supporting documents
- View leave balance
- Track time-off request status
- Access permitted salary information


## 🔄 Core HR Workflow

```text
                    ┌──────────────┐
                    │    ADMIN     │
                    │   / HR       │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ HRMS SYSTEM  │
                    └──────┬───────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
     Employees         Attendance        Time Off
          │                │                │
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                    Salary / Payroll
