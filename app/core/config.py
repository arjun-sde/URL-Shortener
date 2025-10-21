import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fast URL Shortener"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/url_shortener")
    BASE_URL: str = os.getenv("BASE_URL", "http://localhost:8000")

settings = Settings()
