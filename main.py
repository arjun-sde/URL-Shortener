import logging
from contextlib import asynccontextmanager
from logging.config import dictConfig

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette_context.middleware import ContextMiddleware

from app.api.v1 import v1_router
from app.core.config import settings
from app.core import logging_config

# Configure logging
dictConfig(logging_config)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown of application resources."""
    logger.info("Application starting up...")
    try:
        yield
    finally:
        logger.info("Application shutting down...")


def get_application() -> FastAPI:
    """Factory to build the FastAPI app with all configurations."""
    middleware = [
        Middleware(ContextMiddleware),
        Middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
    ]

    _app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        lifespan=lifespan,
        middleware=middleware,
    )



    return _app


# The ASGI app instance used by uvicorn
app = get_application()

# Register routers (v1 APIs)
app.include_router(v1_router, prefix=settings.API_V1_STR)
