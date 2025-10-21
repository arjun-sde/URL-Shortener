from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastURL Shortener"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    BASE_URL: str = "http://localhost:8000"
    HASHIDS_SALT: str = "change_this_to_a_secure_random_salt"
    HASHIDS_MIN_LENGTH: int = 6
    ENABLE_MULTI_TENANT: bool = False
    LOG_LEVEL: str = "INFO"

    # Pydantic v2 uses model_config instead of Config
    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }


settings = Settings()
