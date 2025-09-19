from typing import Literal

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENVIRONMENT: Literal["local", "prod", "test"] = Field(default="local")
    PROJECT_NAME: str = Field(default="Project name")
    LOG_DIR: str = Field(default="logs")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


class DatabaseConfig(BaseSettings):
    DB_HOST: str = Field(default="localhost")
    DB_PASS: str = Field(default="postgres")
    DB_PORT: str = Field(default="5432")
    DB_USER: str = Field(default="postgres")
    DB_NAME: str = Field(default="app_db")
    DB_URL: str = Field(default="")

    @model_validator(mode="before")
    def build_db_url(cls, values):
        if not values.get("DB_URL"):
            values["DB_URL"] = (
                f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}"
                f"@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
            )
        return values


class AuthConfig(BaseSettings):
    JWT_SECRET: str = Field(default="secret-key")
    TOKEN_LIFETIME: int = Field(default=600)
    REFRESH_TOKEN_LIFETIME: int = Field(default=86400)
    COOKIE_NAME: str = Field(default="auth_cookie")
    ALGORITHM: str = Field(default="HS256")


class EmailConfig(BaseSettings):
    SENDER_EMAIL: str = Field(default="noreply@example.com")
    SENDER_PASSWORD: str = Field(default="email-password")
    SMTP_PORT: int = Field(default=465)
    SMTP_SERVER: str = Field(default="smtp.example.com")
    VERIFY_TOKEN_SECRET: str = Field(default="verify-secret")


class FrontendConfig(BaseSettings):
    FRONTEND_HOST: str = Field(default="http://localhost")
    FRONTEND_PORT: int = Field(default=3000)
    FRONTEND_LOGIN_PATH: str = Field(default="/login")
    FRONTEND_VERIFY_PATH: str = Field(default="/verify")


class RedisConfig(BaseSettings):
    REDIS_HOST: str = Field(default="localhost")
    REDIS_PORT: int = Field(default=6379)
    REDIS_PASSWORD: str = Field(default="somepass")
    REDIS_USER_PASSWORD: str = Field(default="someuserpass")
    REDIS_USER: str = Field(default="someuser")
    REDIS_URL: str = Field(default="")
    REDIS_NUMBER: str = Field(default="0")

    @model_validator(mode="before")
    def build_redis_url(cls, values):
        if not values.get("REDIS_URL"):
            values["REDIS_URL"] = (
                f"redis://{values['REDIS_USER']}:{values['REDIS_USER_PASSWORD']}"
                f"@{values['REDIS_HOST']}:{values['REDIS_PORT']}"
                f"/{values['REDIS_NUMBER']}"
            )
        return values


class AppConfig(
    BaseConfig,
    DatabaseConfig,
    AuthConfig,
    EmailConfig,
    FrontendConfig,
    RedisConfig,
):
    HOST: str = Field(default="0.0.0.0")
    V1_PREFIX: str = Field(default="/api/v1")
    HTTP_SECURE: str = Field(default="http")
    HTTP_PORT: int = Field(default=8000)

    TEMPLATES_DIR: str = Field(default="source/templates")
    TEMPLATE_VERIFICATION: str = Field(default="email_verification.html")
    TEMPLATE_REGISTRATION: str = Field(default="email_registration.html")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


class TestConfig(AppConfig):
    DB_NAME: str = Field(default="test_db")
    HTTP_PORT: int = Field(default=8001)

    model_config = SettingsConfigDict(
        env_file=[".env", ".env.test"],
        case_sensitive=True,
        extra="ignore",
    )


def config() -> AppConfig:
    env = BaseConfig().ENVIRONMENT
    return TestConfig() if env == "test" else AppConfig()


settings = config()
