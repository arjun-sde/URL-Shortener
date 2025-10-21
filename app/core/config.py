from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    BASE_URL: str = Field("http://localhost:8000", env="BASE_URL")
    HASHIDS_SALT: str = Field("change_this", env="HASHIDS_SALT")
    HASHIDS_MIN_LENGTH: int = Field(6, env="HASHIDS_MIN_LENGTH")
    ENABLE_MULTI_TENANT: bool = Field(True, env="ENABLE_MULTI_TENANT")
    log_level: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
