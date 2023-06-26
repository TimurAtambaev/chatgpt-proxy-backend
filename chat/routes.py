"""Модуль с инициализацией роутов."""
from fastapi import APIRouter, FastAPI

from chat.rest.views import chat


def init_routes(app: FastAPI) -> None:
    """Инициализация роутов."""
    main_router = APIRouter()
    main_router.include_router(chat.router, tags=["chat"])
    app.include_router(main_router)
