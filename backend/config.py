import os
from typing import List
from zoneinfo import ZoneInfo
from datetime import datetime, date
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Server & CORS
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    COMPANY_NAME: str = "Dayflow"

    # Application Timezone for Attendance & Audit
    APP_TIMEZONE: str = "Asia/Kolkata"

    # Database
    DATABASE_URL: str = "postgresql://postgres:<YOUR_POSTGRES_PASSWORD>@localhost:5432/dayflow_hrms"

    # Security & JWT
    SECRET_KEY: str = "dev_secret_key_dayflow_hrms_super_secure_random_hex_2026_test"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 8

    # Groq LLM (Optional)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-8b-8192"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    def get_current_time(self) -> datetime:
        """Return current datetime in the configured application timezone."""
        return datetime.now(ZoneInfo(self.APP_TIMEZONE))

    def get_current_date(self) -> date:
        """Return current date in the configured application timezone."""
        return self.get_current_time().date()

settings = Settings()
