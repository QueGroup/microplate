from fastapi import FastAPI
from presentation.api import (
    healthcheck_router,
    metrics_handler,
    setup_exception_handlers,
)
from presentation.api.middlewares import logging_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(
        BaseHTTPMiddleware,
        dispatch=logging_middleware,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )


def init_routes(app: FastAPI) -> None:
    prefix: str = "/api/v1"
    app.include_router(
        router=healthcheck_router,
        tags=["healthcheck"],
    )
    app.add_route("/metrics", metrics_handler)
    setup_exception_handlers(app)
