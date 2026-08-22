import os

def get_groq_api_key() -> str:
    return os.getenv("GROQ_API_KEY", "mock")

def get_model_name() -> str:
    return os.getenv("GROQ_MODEL", "llama3-8b-8192")
