import sys
import importlib
import threading
from pathlib import Path
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = PROJECT_ROOT / "agents"

_lock = threading.Lock()

def _run_in_agent_context(agent_folder: str, entry_fn: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes an agent's entrypoint in an isolated import context to guarantee
    that internal relative/local module lookups (schemas, tools, etc.) resolve
    strictly to the respective agent folder without namespace collisions.
    """
    agent_path = str(AGENTS_DIR / agent_folder)
    with _lock:
        local_modules = ['schemas', 'tools', 'audit', 'config', 'mock_data', 'permissions', 'agent']
        saved = {}
        for m in local_modules:
            if m in sys.modules:
                saved[m] = sys.modules.pop(m)

        orig_path = list(sys.path)
        sys.path.insert(0, agent_path)
        try:
            mod = importlib.import_module("agent")
            fn = getattr(mod, entry_fn)
            return fn(data)
        finally:
            sys.path = orig_path
            for m in local_modules:
                if m in sys.modules:
                    sys.modules.pop(m)
            for m, mod_obj in saved.items():
                sys.modules[m] = mod_obj

def run_leave_triage(data: Dict[str, Any]) -> Dict[str, Any]:
    return _run_in_agent_context("leave_triage", "run_leave_triage", data)

def run_attendance_anomaly(data: Dict[str, Any]) -> Dict[str, Any]:
    return _run_in_agent_context("attendance_anomaly", "run_attendance_anomaly", data)

def run_policy_qa(data: Dict[str, Any]) -> Dict[str, Any]:
    return _run_in_agent_context("policy_qa", "run_policy_qa", data)

def run_onboarding(data: Dict[str, Any]) -> Dict[str, Any]:
    return _run_in_agent_context("onboarding", "run_onboarding", data)

def run_report_payslip(data: Dict[str, Any]) -> Dict[str, Any]:
    return _run_in_agent_context("report_payslip", "run_report_payslip", data)
