"""Diagnostics and system info service."""

import socket
from datetime import datetime, timezone
from typing import Tuple

from app.core.config import get_settings
from app.database.session import check_db_connection, check_db_connection_with_message
from app.schemas.health import SystemInfoResponse


def get_container_hostname() -> str:
    """Return container/host hostname."""
    try:
        return socket.gethostname()
    except Exception:
        return "unknown"


def get_system_info() -> SystemInfoResponse:
    """Build system info for GET /system-info."""
    settings = get_settings()
    db_ok = check_db_connection()
    return SystemInfoResponse(
        app_version=settings.app_version,
        database_status="connected" if db_ok else "disconnected",
        timestamp=datetime.now(timezone.utc),
        container_hostname=get_container_hostname(),
    )


def get_db_health() -> Tuple[str, str]:
    """Return (status, message) for database health."""
    ok, message = check_db_connection_with_message()
    return ("connected", message) if ok else ("disconnected", message)
