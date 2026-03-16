"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import __version__
from app.api.routes import api_router
from app.core.config import get_settings
from app.core.logging import get_logger, setup_logging

setup_logging()
_logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    s = get_settings()
    _logger.info("DB config: POSTGRES_HOST=%s (use localhost when running outside Docker)", s.postgres_host)
    yield
    # Optional: cleanup on shutdown


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Backend for local infrastructure testing (API, DB, Docker).",
        lifespan=lifespan,
    )
    app.include_router(api_router, prefix="")
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    from app.core.config import get_settings
    s = get_settings()
    uvicorn.run(
        "app.main:app",
        host=s.host,
        port=s.port,
        reload=s.debug,
        reload_excludes=[".venv", "venv", "__pycache__", ".git", "*.pyc"],
    )
