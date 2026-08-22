import os

def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "mock")

def get_model_name() -> str:
    return os.getenv("GROQ_MODEL", "llama3-8b-8192")

def get_default_report_period() -> str:
    return os.getenv("DEFAULT_REPORT_PERIOD", "2026-07")
