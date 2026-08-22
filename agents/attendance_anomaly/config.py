import os

def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "mock")

def get_model_name() -> str:
    return os.getenv("GROQ_MODEL", "llama3-8b-8192")

def get_systemic_threshold() -> float:
    # 30% of employees
    return float(os.getenv("SYSTEMIC_THRESHOLD_PERCENT", "0.3"))
