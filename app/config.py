from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "JS Academy API"
    secret_key: str = "super-secret-key-change-me"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "sqlite:///./jsacademy.db"

    class Config:
        env_file = ".env"


settings = Settings()

