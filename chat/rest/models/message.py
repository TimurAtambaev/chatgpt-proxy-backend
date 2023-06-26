"""Модуль с pydantic-моделями запросов и ответов."""
from typing import List, Optional

from pydantic import BaseModel


class UserMessageModel(BaseModel):
    """Модель запроса пользователя."""

    username: str
    text: str
    session_id: Optional[int] = None


class ResponseGPTModel(BaseModel):
    """Модель ответа ChatGPT с передачей контекста диалога."""

    role: str
    content: str

    class Config:
        """Класс с настройками."""

        arbitrary_types_allowed = True
        orm_mode = True


class ResponseGPTModelSession(BaseModel):
    """Модель ответа ChatGPT с передачей списка сообщений и id сессии."""

    messages: List[ResponseGPTModel]
    session_id: int
