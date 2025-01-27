from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from settings.config import settings


def apply_middleware(app: FastAPI) -> FastAPI:
    """
    Применяем middleware.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.SERVICE_API_CORS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
