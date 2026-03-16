"""Schemas for health and system-info endpoints."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """GET /health response."""

    status: Literal["OK"] = "OK"
    message: str = "Service is healthy"


class DbHealthResponse(BaseModel):
    """GET /db-health response."""

    status: Literal["connected", "disconnected"]
    message: str


class SystemInfoResponse(BaseModel):
    """GET /system-info response."""

    app_version: str = Field(..., description="Application version")
    database_status: Literal["connected", "disconnected"]
    timestamp: datetime = Field(..., description="Server timestamp (UTC)")
    container_hostname: str = Field(..., description="Container hostname")
