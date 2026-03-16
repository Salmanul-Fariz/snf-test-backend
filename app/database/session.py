"""SQLAlchemy session and engine setup."""

from contextlib import contextmanager
from typing import Generator, Tuple

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.core.logging import get_logger
from app.database.base import Base

logger = get_logger(__name__)
settings = get_settings()
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.debug,
    connect_args={"connect_timeout": 5},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """Create tables (Alembic handles migrations; this is for emergency init)."""
    Base.metadata.create_all(bind=engine)


def check_db_connection() -> bool:
    """Verify database connectivity. Returns True if connection succeeds."""
    ok, _ = check_db_connection_with_message()
    return ok


def check_db_connection_with_message() -> Tuple[bool, str]:
    """Verify database connectivity. Returns (success, message)."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "Database connection successful"
    except Exception as e:
        msg = str(e).strip() or type(e).__name__
        logger.warning("Database connection failed: %s", msg)
        hint = ""
        if settings.postgres_host == "postgres" and ("could not translate host name" in msg or "nodename nor servname" in msg):
            hint = " (Running outside Docker? Set POSTGRES_HOST=localhost in .env)"
        return False, f"Database connection failed: {msg}{hint}"


@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Dependency-friendly DB session context manager."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
