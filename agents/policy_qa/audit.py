import uuid
from typing import List, Dict, Any
from schemas import AuditEntry

_AUDIT_LOGS: List[Dict[str, Any]] = []

def log_action(request_id: str, agent_name: str, action_type: str, tool_called: str, tool_result: str, details: str) -> str:
    """Log an audit entry and store in memory for verification."""
    audit_id = str(uuid.uuid4())
    entry = AuditEntry(
        audit_id=audit_id,
        request_id=request_id,
        agent_name=agent_name,
        action_type=action_type,
        tool_called=tool_called,
        tool_result=tool_result,
        details=details
    )
    _AUDIT_LOGS.append(entry.model_dump(mode='json'))
    return audit_id

def get_audit_logs() -> List[Dict[str, Any]]:
    return _AUDIT_LOGS

def clear_audit_logs():
    _AUDIT_LOGS.clear()
