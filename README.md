# Odoo-Hackathon
# Dayflow HRMS

## Agentic AI–Integrated Human Resource Management System

> **Every workday, perfectly aligned — safe, human-supervised AI agents for HR operations.**

Dayflow HRMS is a modern, role-based Human Resource Management System designed to centralize employee management, attendance, leave, payroll visibility, onboarding, notifications, and HR analytics.

The platform extends traditional HRMS functionality with **supervised AI agents** that automate routine HR workflows while maintaining strict security, least-privilege access, auditability, and Human-in-the-Loop (HITL) approval for sensitive operations.

---

## 🚀 Overview

Dayflow HRMS supports two primary user roles:

- **Admin / HR Officer**
- **Employee**

The system also contains a supervised **Agentic AI layer** consisting of specialized agents for attendance anomalies, leave triage, policy questions, onboarding coordination, and report/payslip generation.

AI agents are intentionally restricted from directly modifying sensitive employee records.

All high-impact changes pass through a **Human-in-the-Loop approval gate**.

---

## 👥 User Roles

### 👨‍💼 Admin / HR Officer

Admins and HR officers can:

- Manage employees
- View attendance records
- Review leave requests
- Approve or reject leave
- Manage payroll information
- View salary structures
- Monitor attendance anomalies
- Review AI-generated leave recommendations
- Generate HR reports
- Generate payslips
- Monitor agent activity
- View audit logs

### 👩‍💻 Employee

Employees can:

- View and update permitted profile information
- Check in / check out
- View attendance
- Apply for leave
- View leave status and balance
- View salary information
- Download payslips
- Complete onboarding tasks
- Ask HR policy questions
- Receive attendance and onboarding reminders

---

# 🤖 Agentic AI Layer

Dayflow introduces specialized AI agents designed to assist HR operations.

### 1. Attendance Anomaly Agent

Detects:

- Missing attendance
- Late entries
- Unusual attendance patterns

Actions:

- Flags anomalies
- Sends polite reminders
- Escalates systemic issues to HR

The agent does not directly modify attendance records.

---

### 2. Leave Triage Agent

The Leave Triage Agent:

1. Receives a leave request
2. Validates request completeness
3. Checks leave balance
4. Checks applicable policy rules
5. Drafts an approval/rejection note
6. Places the recommendation in the HR Leave Triage Queue

### Human-in-the-Loop

The HR officer can:

- Accept the draft
- Edit the draft
- Ignore the draft
- Manually approve/reject

**The AI agent never directly finalizes the leave decision.**

---

### 3. Policy Q&A Agent

Provides read-only answers to questions about:

- Leave policies
- Attendance rules
- Profile editing rules
- HR procedures

The agent retrieves information from the curated policy knowledge base and provides policy citations.

If the question is outside its permitted scope, the employee can escalate it to HR.

---

### 4. Onboarding Agent

Coordinates new employee onboarding through:

- Document checklist
- Tax/ID form tracking
- Policy acknowledgments
- Training links
- Reminder notifications
- Deadline escalation

The agent has read-only access to new-hire information and cannot modify employee profiles.

---

### 5. Report & Payslip Agent

Provides:

- Instant payslip PDF generation
- Attendance reports
- Leave balance reports
- Onboarding completion reports
- Scheduled report generation
- Authorized report delivery

The agent cannot modify salary structures or payroll data.

---

# 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                         │
│                                                             │
│   Employee Web/App          Admin / HR Web Console          │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              API GATEWAY + AUTHN / AUTHZ                    │
│                                                             │
│       Authentication • RBAC • Role Validation               │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│              AGENT ORCHESTRATION LAYER                      │
│                                                             │
│                    Agent Controller                         │
│       Routing • Stop Conditions • HITL Enforcement           │
└──────────────┬──────────┬──────────┬──────────┬─────────────┘
               │          │          │          │
               ▼          ▼          ▼          ▼
       Attendance      Leave      Policy     Onboarding
        Anomaly       Triage       Q&A        Agent
          Agent        Agent       Agent
               │          │          │          │
               └──────────┴──────┬───┴──────────┘
                                  │
                                  ▼
                       Report & Payslip Agent
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    TOOL REGISTRY                            │
│                                                             │
│ get_leave_balance        check_policy_rules                 │
│ draft_approval_note      send_notification                  │
│ generate_payslip_pdf     generate_attendance_report         │
│ search_policy_kb                                             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATA SERVICES                          │
│                                                             │
│ HRMS Database     Vector Store       Immutable Audit Store  │
│                                                             │
│ Employees         Policy KB          Agent Actions          │
│ Attendance        Policy Docs        Tool Calls             │
│ Leave             Permitted Cases    Data Access            │
│ Payroll                              HITL Decisions         │
│ Onboarding                            Workflow Results       │
└─────────────────────────────────────────────────────────────┘

              ┌────────────────────────────────┐
              │      CONTROL PLANE             │
              │                                │
              │ Least Privilege                │
              │ Data Classification             │
              │ PII Masking                    │
              │ Permission Checks               │
              │ HITL Gates                      │
              │ Rate Limiting                   │
              │ Cost Monitoring                 │
              │ Audit Logging                   │
              └────────────────────────────────┘───────────────┘
                           ▼
                    Salary / Payroll
