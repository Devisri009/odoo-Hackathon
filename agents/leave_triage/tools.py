from mock_data import MOCK_LEAVE_REQUESTS, MOCK_LEAVE_BALANCES, MOCK_LEAVE_POLICIES, MOCK_LEAVE_HISTORY
from audit import log_action

class ToolError(Exception):
    pass

def get_leave_request(leave_request_id: str, execution_id: str) -> dict:
    log_action(execution_id, "Leave Triage Agent", "system", "system", "read", "get_leave_request", "leave_request", leave_request_id, "success")
    if leave_request_id not in MOCK_LEAVE_REQUESTS:
        raise ToolError(f"Leave request {leave_request_id} not found")
    return MOCK_LEAVE_REQUESTS[leave_request_id]

def get_leave_balance(employee_id: str, leave_type: str, execution_id: str) -> dict:
    log_action(execution_id, "Leave Triage Agent", "system", "system", "read", "get_leave_balance", "leave_balance", employee_id, "success")
    if employee_id == "FAIL_BALANCE":
        raise ToolError("Balance service unavailable")
    
    balances = MOCK_LEAVE_BALANCES.get(employee_id, {})
    if leave_type not in balances:
        return {"allocated_days": 0, "used_days": 0, "available_days": 0}
    return balances[leave_type]

def check_leave_policy(leave_type: str, requested_days: int, employee_id: str, execution_id: str) -> dict:
    log_action(execution_id, "Leave Triage Agent", "system", "system", "read", "check_leave_policy", "leave_policy", leave_type, "success")
    
    if leave_type == "FAIL_POLICY":
        raise ToolError("Policy service unavailable")
        
    policy = MOCK_LEAVE_POLICIES.get(leave_type)
    if not policy:
        return {"policy_compliant": True, "policy_name": "Default", "policy_section": "General", "applicable_rule": "None", "violation_reason": None}
    
    if "max_consecutive_days" in policy and requested_days > policy["max_consecutive_days"]:
        return {
            "policy_compliant": False,
            "policy_name": f"{leave_type.capitalize()} Leave Policy",
            "policy_section": "Limits",
            "applicable_rule": f"Max consecutive days is {policy['max_consecutive_days']}",
            "violation_reason": f"Requested {requested_days} days exceeds max of {policy['max_consecutive_days']} days."
        }
    return {
        "policy_compliant": True,
        "policy_name": f"{leave_type.capitalize()} Leave Policy",
        "policy_section": "Limits",
        "applicable_rule": f"Max consecutive days is {policy.get('max_consecutive_days', 'N/A')}",
        "violation_reason": None
    }

def get_employee_leave_history(employee_id: str, execution_id: str) -> list:
    log_action(execution_id, "Leave Triage Agent", "system", "system", "read", "get_employee_leave_history", "leave_history", employee_id, "success")
    return MOCK_LEAVE_HISTORY.get(employee_id, [])

def draft_approval_note(recommendation: str, policy_result: dict, balance_result: dict, requested_dates: dict, leave_type: str, relevant_evidence: str, execution_id: str) -> str:
    log_action(execution_id, "Leave Triage Agent", "system", "system", "generate", "draft_approval_note", "draft_note", "N/A", "success")
    note = f"DRAFT HR NOTE:\nRecommendation: {recommendation.upper()}\nLeave Type: {leave_type}\nDates: {requested_dates.get('start')} to {requested_dates.get('end')}\n"
    if recommendation == "approve":
        note += "Leave request appears compliant with the applicable policy and the employee has sufficient leave balance. Recommended for HR approval."
    elif recommendation == "reject":
        note += f"Leave request is NOT recommended for approval. Evidence: {relevant_evidence}"
    else:
        note += f"Leave request requires manual review. Evidence: {relevant_evidence}"
    return note
