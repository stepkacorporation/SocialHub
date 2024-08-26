import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

ENVIRONMENT = os.getenv('ENVIRONMENT', 'dev')
DOTENV = os.path.join(os.path.dirname(__file__), f'.env.{ENVIRONMENT}')


class Settings(BaseSettings):
    # PostgreSQL settings
    postgres_user: str = Field(..., alias='POSTGRES_USER')
    postgres_password: str = Field(..., alias='POSTGRES_PASSWORD')
    postgres_db: str = Field(..., alias='POSTGRES_DB')
    postgres_host: str = Field(..., alias='POSTGRES_HOST')
    postgres_port: str = Field(..., alias='POSTGRES_PORT')

    # JWT settings
    secret_key_access: str = Field(..., alias='SECRET_KEY_ACCESS')
    secret_key_refresh: str = Field(..., alias='SECRET_KEY_REFRESH')
    algorithm: str = Field(..., alias='ALGORITHM')
    access_token_expire_minutes: int = Field(..., alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_expire_days: int = Field(..., alias='REFRESH_TOKEN_EXPIRE_DAYS')

    model_config = SettingsConfigDict(
        env_file=DOTENV,
        env_file_encoding='utf-8'
    )


settings = Settings()
