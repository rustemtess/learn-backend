import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "JS Academy API"
    secret_key: str = "super-secret-key-change-me"
    access_token_expire_minutes: int = 60 * 24
    # Use environment variable for database URL, fallback to SQLite for local dev
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./jsacademy.db")
    # Allowed origins for CORS
    cors_origins: str = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")

    class Config:
        env_file = ".env"


settings = Settings()

