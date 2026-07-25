from functools import lru_cache
from typing import List, Optional, Any

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- App ---
    PROJECT_NAME: str = "ModaMar"
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    SECRET_KEY: str = Field(
        default="CHANGE_ME_IN_PRODUCTION",
        description="Secret used for general crypto. MUST be overridden via env in prod.",
    )

    # --- Database ---
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: Optional[int] = None
    POSTGRES_DB: Optional[str] = None
    DATABASE_URL: Optional[str] = None

    @model_validator(mode="after")
    def assemble_db_connection_and_keys(self) -> 'Settings':
        if not self.DATABASE_URL:
            if all([
                self.POSTGRES_USER,
                self.POSTGRES_PASSWORD,
                self.POSTGRES_HOST,
                self.POSTGRES_PORT,
                self.POSTGRES_DB,
            ]):
                self.DATABASE_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
        # Fallback JWT_SECRET_KEY to SECRET_KEY if not explicitly set
        if self.JWT_SECRET_KEY == "CHANGE_ME_IN_PRODUCTION":
            self.JWT_SECRET_KEY = self.SECRET_KEY
            
        return self

    # --- Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"

    # --- JWT / Auth ---
    JWT_SECRET_KEY: str = Field(
        default="CHANGE_ME_IN_PRODUCTION",
        description="Secret used to sign JWTs. MUST be overridden via env in prod.",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 90
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # --- OTP ---
    OTP_LENGTH: int = 6
    OTP_EXPIRE_MINUTES: int = 10
    OTP_MAX_ATTEMPTS: int = 5
    OTP_RESEND_COOLDOWN_SECONDS: int = 60

    # --- SMS provider ---
    SMS_PROVIDER: str = "console"  # termii | africastalking | console (dev fallback)
    SMS_PROVIDER_API_KEY: str = ""
    SMS_SENDER_ID: str = "MODAMAR"
    
    TERMII_API_KEY: Optional[str] = None
    TERMII_SENDER_ID: str = "MODAMAR"
    TERMII_BASE_URL: str = "https://api.ng.termii.com/api"

    AFRICASTALKING_USERNAME: Optional[str] = None
    AFRICASTALKING_API_KEY: Optional[str] = None

    # --- Media storage (Cloudinary) ---
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # --- Payments (Paystack) ---
    PAYSTACK_SECRET_KEY: str = ""
    PAYSTACK_PUBLIC_KEY: str = ""

    # --- CORS ---
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()