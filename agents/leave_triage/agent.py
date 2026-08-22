import json
import uuid
from datetime import datetime
from pydantic import ValidationError
from groq import Groq

from schemas import LeaveTriageRequest, LeaveTriageResponse, HITLRequest
from tools import (
    get_leave_request, get_leave_balance, check_leave_policy, 
    get_employee_leave_history, draft_approval_note, ToolError
)
from audit import log_action
from config import get_groq_api_key, get_model_name

def run_leave_triage(request_data: dict) -> dict:
    execution_id = str(uuid.uuid4())
    warnings = []
    
    # 1. Validation
    try:
        req = LeaveTriageRequest(**request_data)
        validation_passed = True
    except ValidationError as e:
        validation_passed = False
        warnings.append(f"Validation Error: {str(e)}")
        return _build_response(
            request_data.get("request_id", str(uuid.uuid4())),
            execution_id,
            False,
            "review",
            False,
            False,
            validation_passed,
            "Request failed initial schema validation.",
            "DRAFT HR NOTE: Request data is invalid or missing required fields.",
            warnings
        )
    
    # Fetch Data deterministically
    try:
        leave_req = get_leave_request(req.leave_request_id, execution_id)
    except ToolError as e:
        warnings.append(str(e))
        return _build_response(
            req.request_id, execution_id, False, "review", False, False, True, 
            "Leave request not found.", "DRAFT HR NOTE: Could not locate leave request.", warnings
        )
    
    requested_days = (req.end_date - req.start_date).days + 1
    
    balance_sufficient = False
    balance_result = {}
    try:
        balance_result = get_leave_balance(req.employee_id, req.leave_type, execution_id)
        if balance_result.get("available_days", 0) >= requested_days:
            balance_sufficient = True
    except ToolError as e:
        warnings.append(str(e))
    
    policy_compliant = False
    policy_result = {}
    try:
        policy_result = check_leave_policy(req.leave_type, requested_days, req.employee_id, execution_id)
        policy_compliant = policy_result.get("policy_compliant", False)
    except ToolError as e:
        warnings.append(str(e))
    
    # Initial deterministic reasoning
    recommendation = "review"
    reasoning = ""
    
    if len(warnings) > 0:
        recommendation = "review"
        reasoning = "Tool failures or missing information require manual review."
    elif not balance_sufficient:
        recommendation = "reject"
        reasoning = f"Insufficient leave balance. Requested {requested_days}, available {balance_result.get('available_days', 0)}."
    elif not policy_compliant:
        recommendation = "reject"
        reasoning = f"Policy violation: {policy_result.get('violation_reason')}"
    elif balance_sufficient and policy_compliant:
        recommendation = "approve"
        reasoning = "Policy is satisfied and balance is sufficient."
    
    draft_note = draft_approval_note(
        recommendation=recommendation,
        policy_result=policy_result,
        balance_result=balance_result,
        requested_dates={"start": str(req.start_date), "end": str(req.end_date)},
        leave_type=req.leave_type,
        relevant_evidence=reasoning,
        execution_id=execution_id
    )

    # Use LLM if configured
    llm_result = _call_llm_for_triage(
        req.model_dump(mode='json'),
        leave_req,
        balance_result,
        policy_result,
        warnings,
        execution_id
    )
    
    recommendation = llm_result.get("recommendation", recommendation)
    reasoning = llm_result.get("reasoning_summary", reasoning)
    draft_note = llm_result.get("draft_note", draft_note)

    return _build_response(
        req.request_id,
        execution_id,
        True,
        recommendation,
        policy_compliant,
        balance_sufficient,
        True,
        reasoning,
        draft_note,
        warnings
    )

def _call_llm_for_triage(req_data, leave_req, balance_result, policy_result, warnings, execution_id):
    api_key = get_groq_api_key()
    if not api_key or api_key == "mock":
        # Fallback to deterministic logic
        if len(warnings) > 0:
            rec = "review"
            reason = "Tool failures occurred."
        elif balance_result.get("available_days", 0) < (datetime.fromisoformat(req_data['end_date']) - datetime.fromisoformat(req_data['start_date'])).days + 1:
            rec = "reject"
            reason = "Insufficient balance."
        elif not policy_result.get("policy_compliant", True):
            rec = "reject"
            reason = "Policy violation."
        else:
            rec = "approve"
            reason = "Sufficient balance and compliant."
            
        return {
            "recommendation": rec,
            "reasoning_summary": reason,
            "draft_note": f"DRAFT HR NOTE: {rec.upper()} - {reason}"
        }

    client = Groq(api_key=api_key)
    model = get_model_name()
    
    prompt = f"""
    You are the Leave Triage Agent.
    Based on the following data, determine if the leave request should be approved, rejected, or marked for review.
    
    Request: {json.dumps(req_data)}
    Leave Data: {json.dumps(leave_req)}
    Balance: {json.dumps(balance_result)}
    Policy: {json.dumps(policy_result)}
    Warnings/Errors: {json.dumps(warnings)}
    
    Rules:
    - If warnings exist, recommendation MUST be 'review'.
    - If balance is insufficient, recommendation MUST be 'reject'.
    - If policy is violated, recommendation MUST be 'reject'.
    - If balance sufficient AND policy compliant AND no warnings, recommendation MUST be 'approve'.
    
    Provide your output as a JSON object with:
    - recommendation: "approve", "reject", or "review"
    - reasoning_summary: A concise explanation using observable evidence.
    - draft_note: A short DRAFT note for the HR reviewer summarizing the findings.
    
    Respond with JSON ONLY.
    """
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        return {
            "recommendation": "review",
            "reasoning_summary": "LLM synthesis failed, fallback to manual review.",
            "draft_note": "DRAFT HR NOTE: Manual review required due to system error."
        }

def _build_response(req_id, exec_id, success, rec, pol_comp, bal_suff, val_pass, reasoning, draft, warnings):
    hitl_id = f"HITL-{uuid.uuid4()}"
    
    # HITL logic
    hitl = HITLRequest(
        hitl_id=hitl_id,
        execution_id=exec_id,
        leave_request_id=req_id,
        requested_by_agent="Leave Triage Agent",
        recommendation=rec,
        draft_note=draft
    )
    
    log_action(exec_id, "Leave Triage Agent", "system", "system", "create", "N/A", "hitl_record", hitl_id, "success")
    
    res = LeaveTriageResponse(
        request_id=req_id,
        agent_name="Leave Triage Agent",
        success=success,
        recommendation=rec,
        policy_compliant=pol_comp,
        balance_sufficient=bal_suff,
        validation_passed=val_pass,
        reasoning_summary=reasoning,
        draft_note=draft,
        requires_human_approval=True,
        hitl_id=hitl_id,
        warnings=warnings
    )
    return res.model_dump(mode='json')
