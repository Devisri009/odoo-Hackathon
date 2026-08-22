import os

def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "mock")

def get_model_name() -> str:
    return os.getenv("GROQ_MODEL", "llama3-8b-8192")

def get_escalation_days() -> int:
    """Number of overdue days after which non-critical tasks require HR escalation."""
    return int(os.getenv("ONBOARDING_ESCALATION_DAYS", "7"))

def get_current_mock_date() -> str:
    """Default evaluation reference date for deterministic mock tests."""
    return os.getenv("ONBOARDING_REFERENCE_DATE", "2026-08-22")
