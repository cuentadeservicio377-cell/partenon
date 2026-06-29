"""Tests for observability endpoints: health and metrics."""

import os

import pytest
from fastapi.testclient import TestClient

from partenon_api.main import app


@pytest.fixture
def api_client_with_env(monkeypatch, temp_data_dir):
    """Provide a fresh TestClient with auth env set."""
    os.environ.setdefault("DASHBOARD_AUTH_SECRET", "test-secret-32-chars-long")

    with TestClient(app) as client:
        yield client


class TestHealthEndpoints:
    def test_health_returns_ok(self, api_client_with_env):
        response = api_client_with_env.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.json()["service"] == "partenon-api"

    def test_health_live_returns_ok(self, api_client_with_env):
        response = api_client_with_env.get("/health/live")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_health_ready_json_mode(self, api_client_with_env):
        response = api_client_with_env.get("/health/ready")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True
        assert data["store"] == "json"

    def test_metrics_returns_prometheus_text(self, api_client_with_env):
        response = api_client_with_env.get("/metrics")
        assert response.status_code == 200
        assert "# HELP" in response.text
