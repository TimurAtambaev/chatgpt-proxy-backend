"""Модуль инициализации приложения."""
from aiohttp import hdrs
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware

from chat.config import settings
from chat.middlewares import ContextRequestMiddleware
from chat.routes import init_routes


def init_app() -> FastAPI:
    """Инициализация приложения."""
    app = FastAPI()

    # middlewares
    app.add_middleware(ContextRequestMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.PUBLIC_CORS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=(hdrs.CONTENT_TYPE, hdrs.AUTHORIZATION),
    )
    init_routes(app)

    # events
    app.state.test_mode = settings.GS_ENVIRONMENT == "test"
    add_pagination(app)

    return app


application = init_app()
