from datetime import datetime
import uuid
from typing import List, Dict, Any
from schemas import AuditLog

_AUDIT_DB: List[Dict[str, Any]] = []

def log_action(execution_id: str, agent_name: str, actor_type: str, actor_id: str, action: str, tool_name: str, resource_type: str, resource_id: str, result: str):
    log = AuditLog(
        audit_id=str(uuid.uuid4()),
        execution_id=execution_id,
        agent_name=agent_name,
        actor_type=actor_type,
        actor_id=actor_id,
        action=action,
        tool_name=tool_name,
        resource_type=resource_type,
        resource_id=resource_id,
        result=result
    )
    _AUDIT_DB.append(log.model_dump(mode='json'))

def get_audit_logs() -> List[Dict[str, Any]]:
    return _AUDIT_DB
