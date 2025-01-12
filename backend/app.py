import os
import logging
from datetime import timedelta
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles


from backend.routes.chat import router as chat_router  # <-- import your chat router

# logger = SetupLogging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager: runs any startup/shutdown logic if needed.
    """
    # STARTUP LOGIC
    yield
    # SHUTDOWN LOGIC


def create_app() -> FastAPI:

    # logger.info(f'!!! Starting App: agent poc !!!')

    # Allowed CORS origins
    # allowed_origins_str = config.get('domains', 'allowed_origins', fallback='')
    # allowed_origins_list = [
    #     origin.strip()
    #     for origin in allowed_origins_str.split(',')
    #     if origin.strip()
    # ]

    # 3) Build middleware
    middleware = [
        Middleware(
            CORSMiddleware,
            # allow_origins=allowed_origins_list,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*']
        )
    ]

    # 4) Create the FastAPI app
    app = FastAPI(
        title="agent poc api",
        version="1.0.0",
        docs_url="/docs",
        description="api for pydantic ai agent poc",
        lifespan=lifespan,
        middleware=middleware
    )

    # 7) Include your chat router so `/chat` route works
    app.include_router(chat_router)

    # 10) Minimal 400 handler for pydantic validation
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=400,
            content=jsonable_encoder({"detail": "Invalid request body"})
        )

    # 11) Health check route
    @app.get("/ping")
    async def ping():
        return JSONResponse(status_code=200, content={"message": "pong"})

    return app
