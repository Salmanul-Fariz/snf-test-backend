"""Tests for health and diagnostics endpoints."""

import re
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient


def test_health_returns_ok(client: TestClient) -> None:
    """GET /health returns status OK."""
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "OK"
    assert "healthy" in data["message"].lower()


def test_db_health_returns_structure(client: TestClient) -> None:
    """GET /db-health returns connected or disconnected and message."""
    r = client.get("/db-health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] in ("connected", "disconnected")
    assert "message" in data


def test_db_health_when_connected(client: TestClient) -> None:
    """GET /db-health returns connected when DB is available."""
    with patch(
        "app.services.diagnostics.check_db_connection_with_message",
        return_value=(True, "Database connection successful"),
    ):
        from app.main import app
        c = TestClient(app)
        r = c.get("/db-health")
    assert r.status_code == 200
    assert r.json()["status"] == "connected"


def test_system_info_returns_required_fields(client: TestClient) -> None:
    """GET /system-info returns app_version, database_status, timestamp, container_hostname."""
    r = client.get("/system-info")
    assert r.status_code == 200
    data = r.json()
    assert "app_version" in data
    assert data["database_status"] in ("connected", "disconnected")
    assert "timestamp" in data
    assert "container_hostname" in data
    # ISO format timestamp
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", data["timestamp"])
