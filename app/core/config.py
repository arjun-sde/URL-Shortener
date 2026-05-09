from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastURL Shortener"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/url_shortener"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    BASE_URL: str = "http://localhost:8000"
    DEFAULT_DOMAIN: str = "default"
    SHORT_CODE_MIN_LENGTH: int = 7
    SNOWFLAKE_MACHINE_ID: int = Field(default=1, ge=0, le=1023)
    SNOWFLAKE_EPOCH_MS: int = 1704067200000
    ENABLE_MULTI_TENANT: bool = False
    LOG_LEVEL: str = "INFO"

    # Pydantic v2 uses model_config instead of Config
    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
