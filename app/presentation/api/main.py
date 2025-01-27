from fastapi import FastAPI

import uvicorn

from presentation.api.lifespan import lifespan
from presentation.api.middleware import apply_middleware
from presentation.api.router import apply_routes
from settings.config import settings


def create_app() -> FastAPI:
    app: FastAPI = FastAPI(
        title="WeatherAPI",
        docs_url="/api/docs/",
        debug=True,
        lifespan=lifespan,
    )

    app = apply_routes(apply_middleware(app))

    return app


if __name__ == "__main__":

    uvicorn.run(
        "main:create_app",
        factory=True,
        host=settings.SERVICE_API_HOST,
        port=settings.SERVICE_API_PORT,
        log_level="debug",
        reload=True,
        workers=1,
    )
