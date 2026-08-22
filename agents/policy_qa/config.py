import os

def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "mock")

def get_model_name() -> str:
    return os.getenv("GROQ_MODEL", "llama3-8b-8192")

def get_relevance_threshold() -> float:
    return float(os.getenv("POLICY_RELEVANCE_THRESHOLD", "1.5"))
