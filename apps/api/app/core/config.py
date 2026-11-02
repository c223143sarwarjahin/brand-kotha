from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # General Project Info
    APP_NAME: str = "BrandKotha"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"

    # CORS Origins
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Database
    DATABASE_URL: str = (
        "postgresql+asyncpg://brandkotha_user:brandkotha_secret_password@localhost:5432/brandkotha_db"
    )
    SYNC_DATABASE_URL: str = (
        "postgresql://brandkotha_user:brandkotha_secret_password@localhost:5432/brandkotha_db"
    )

    # Redis & Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # Authentication & Security
    JWT_SECRET_KEY: str = "default_insecure_development_secret_key_change_me_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Monetization Feature Flag
    CHARGE_ENABLED: bool = False
    DEFAULT_COMMISSION_PCT: float = 10.00
    DEFAULT_LEAD_FEE_BDT: int = 199


settings = Settings()
