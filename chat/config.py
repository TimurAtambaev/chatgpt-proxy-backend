"""Модуль с настройками проекта."""
import os

import openai
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Класс настроек."""

    ALEMBIC_PATH: str = "/etc/chat/alembic.ini"
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    GS_ENVIRONMENT: str = "test"
    GS_LISTEN: str = "http://0.0.0.0:8080"
    OPENAI_API_KEY: str = ""
    GPT_MODEL: str = "gpt-3.5-turbo"
    GPT_TEMPERATURE: int = 0
    PUBLIC_CORS: str = ""

    # Database settings
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str


settings = Settings()
openai.api_key = settings.OPENAI_API_KEY
