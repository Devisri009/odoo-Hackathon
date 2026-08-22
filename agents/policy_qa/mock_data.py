from typing import Dict, List, Any

MOCK_POLICY_DATABASE: Dict[str, Dict[str, Any]] = {
    "Leave Policy": {
        "policy_id": "POL_LEAVE",
        "description": "Comprehensive rules governing paid, sick, parental, and unpaid leaves.",
        "sections": {
            "3.1": {
                "title": "Annual Leave Types",
                "content": "Dayflow provides several categories of leave: paid annual leave, sick leave, maternity/paternity leave, bereavement leave, and unpaid sabbatical leave. All leaves must be submitted through the Dayflow portal.",
                "keywords": ["leave types", "categories", "annual leave", "types of leave", "paid leave", "sick leave", "sabbatical"]
            },
            "3.2": {
                "title": "Paid Leave Entitlement",
                "content": "Employees are entitled to 18 paid leave days per calendar year, accrued proportionally at 1.5 days per month. Paid leave requests exceeding 3 consecutive days require at least 7 days advance notice and manager approval.",
                "keywords": ["paid leave", "entitlement", "how many days", "paid vacation", "vacation days", "advance notice", "18 days", "accrual"]
            },
            "3.3": {
                "title": "Sick Leave Policy",
                "content": "Employees receive 10 paid sick leave days per calendar year. A certified medical practitioner note is mandatory for consecutive sick leave absences exceeding 2 working days.",
                "keywords": ["sick leave", "medical certificate", "doctor note", "illness", "sick days", "10 days", "medical"]
            },
            "3.4": {
                "title": "Unpaid Leave & Sabbaticals",
                "content": "Unpaid leave of up to 30 calendar days may be approved by department heads for personal or educational reasons after all accrued paid leave has been exhausted.",
                "keywords": ["unpaid leave", "sabbatical", "leave without pay", "extended leave", "30 days"]
            }
        }
    },
    "Attendance Policy": {
        "policy_id": "POL_ATTENDANCE",
        "description": "Guidelines on standard work hours, check-in rules, and attendance regularization.",
        "sections": {
            "2.1": {
                "title": "Working Hours and Core Hours",
                "content": "Standard company working hours are 9:00 AM to 5:00 PM Monday through Friday. Core hours where all employees must be available for meetings and collaboration are 10:00 AM to 4:00 PM.",
                "keywords": ["working hours", "work hours", "shift", "core hours", "timing", "schedule", "office hours", "9:00", "5:00"]
            },
            "2.2": {
                "title": "Late Check-in & Grace Period",
                "content": "Employees are granted a 15-minute grace period each morning until 9:15 AM. Check-ins after 9:15 AM without prior notification are logged as late check-in anomalies. More than 3 late check-ins in a month may trigger an HR review.",
                "keywords": ["late check-in", "grace period", "late arrival", "9:15", "late policy", "tardy", "15 minutes"]
            },
            "2.3": {
                "title": "Missing Attendance Regularization",
                "content": "If an employee forgets to check in or check out, an attendance regularization request must be submitted within 3 working days via the Dayflow portal.",
                "keywords": ["missing check-in", "missing check-out", "forgot check in", "regularization", "attendance regularisation", "missed punch"]
            }
        }
    },
    "Work From Home Policy": {
        "policy_id": "POL_WFH",
        "description": "Rules for remote work, hybrid arrangements, and remote equipment.",
        "sections": {
            "4.1": {
                "title": "WFH Eligibility",
                "content": "Full-time employees who have successfully completed their 3-month probation period are eligible to apply for regular Work From Home (WFH) arrangements.",
                "keywords": ["wfh eligibility", "remote work", "work from home", "who can work from home", "eligibility", "probation"]
            },
            "4.2": {
                "title": "Weekly WFH Allowance",
                "content": "Eligible employees may work from home up to 2 days per work week, subject to team coverage and line manager approval.",
                "keywords": ["wfh allowance", "how many days wfh", "remote days", "2 days", "work from home limit", "weekly wfh"]
            },
            "4.3": {
                "title": "Remote Work Equipment",
                "content": "The company provides a standard issue laptop and a one-time ergonomic allowance of $200 for home office setup upon transition to hybrid work.",
                "keywords": ["wfh equipment", "ergonomic allowance", "laptop", "home office", "monitor", "allowance", "200"]
            }
        }
    },
    "Onboarding Policy": {
        "policy_id": "POL_ONBOARDING",
        "description": "Procedures for new hires, probation timeline, and documentation.",
        "sections": {
            "1.1": {
                "title": "Probation Period",
                "content": "The standard probationary period for all new hires is 3 months from the employment start date. This may be extended up to a maximum of 6 months based on performance assessment.",
                "keywords": ["probation period", "probation", "new hire", "trial period", "3 months", "probation duration"]
            },
            "1.2": {
                "title": "Documentation Submission",
                "content": "New hires are required to submit government ID proofs, tax identification forms, educational credentials, and previous employment relieving letters within 14 calendar days of joining.",
                "keywords": ["documentation", "documents required", "onboarding docs", "tax forms", "id proof", "14 days", "joining documents"]
            }
        }
    },
    "Payroll Policy": {
        "policy_id": "POL_PAYROLL",
        "description": "General rules regarding salary processing schedules, payslip delivery, and reimbursement guidelines.",
        "sections": {
            "5.1": {
                "title": "Salary Disbursement Schedule",
                "content": "Salaries are processed and disbursed on the last working day of each calendar month directly into the employee's registered bank account. If the last day falls on a public holiday or weekend, disbursement occurs on the preceding business day.",
                "keywords": ["salary disbursement", "pay day", "salary date", "when do we get paid", "payment schedule", "last working day", "payroll date"]
            },
            "5.2": {
                "title": "Payslip Access",
                "content": "Monthly digital payslips are generated and accessible securely via the Dayflow employee self-service portal within 2 business days following salary disbursement.",
                "keywords": ["payslip", "access payslip", "download payslip", "salary slip", "view payslip", "portal"]
            },
            "5.3": {
                "title": "Reimbursements & Expense Claims",
                "content": "Official business expense and travel reimbursement claims submitted with valid receipts by the 15th of the month will be reimbursed in the same month's payroll cycle. Claims after the 15th roll over to the following month.",
                "keywords": ["reimbursement", "expense claim", "travel expenses", "receipts", "15th of the month", "claims"]
            }
        }
    },
    "General Employee Policy": {
        "policy_id": "POL_GENERAL",
        "description": "Company-wide behavioral expectations, ethics, and workplace standards.",
        "sections": {
            "6.1": {
                "title": "Code of Conduct & Ethics",
                "content": "All employees are expected to maintain the highest standards of professional integrity, respect workplace diversity, strictly adhere to zero-tolerance anti-harassment rules, and safeguard company confidentiality.",
                "keywords": ["code of conduct", "ethics", "behavior", "harassment", "anti-harassment", "integrity", "confidentiality"]
            },
            "6.2": {
                "title": "Office Dress Code",
                "content": "Dayflow observes a business casual dress code from Monday through Thursday. Casual attire, including clean jeans and casual shirts, is permitted on Fridays.",
                "keywords": ["dress code", "what to wear", "attire", "business casual", "friday casual", "clothing"]
            }
        }
    }
}
