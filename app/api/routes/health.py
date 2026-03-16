"""Health check and diagnostics endpoints."""

from fastapi import APIRouter, status

from app.core.logging import get_logger
from app.schemas.health import DbHealthResponse, HealthResponse, SystemInfoResponse
from app.services.diagnostics import get_db_health, get_system_info

logger = get_logger(__name__)
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
)
def health() -> HealthResponse:
    """Return service health status. Use for liveness probes."""
    logger.info("Health check requested")
    return HealthResponse(status="OK", message="Service is healthy")


@router.get(
    "/db-health",
    response_model=DbHealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Database health check",
)
def db_health() -> DbHealthResponse:
    """Verify database connectivity."""
    status_val, message = get_db_health()
    logger.info("DB health check", extra={"db_status": status_val})
    return DbHealthResponse(status=status_val, message=message)


@router.get(
    "/system-info",
    response_model=SystemInfoResponse,
    status_code=status.HTTP_200_OK,
    summary="System diagnostics",
)
def system_info() -> SystemInfoResponse:
    """Return app version, database status, timestamp, and container hostname."""
    info = get_system_info()
    logger.info(
        "System info requested",
        extra={
            "app_version": info.app_version,
            "database_status": info.database_status,
            "hostname": info.container_hostname,
        },
    )
    return info
