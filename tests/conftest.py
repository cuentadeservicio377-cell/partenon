"""Shared test fixtures."""

import os
import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_data_dir(monkeypatch):
    """Provide a temporary data directory and patch the API to use it."""
    path = Path(tempfile.mkdtemp())
    monkeypatch.setenv("PARTENON_DATA_DIR", str(path))
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture
def api_client(temp_data_dir):
    """Return a FastAPI TestClient with auth secret set."""
    os.environ.setdefault("DASHBOARD_AUTH_SECRET", "test-secret-32-chars-long")
    os.environ.setdefault("DASHBOARD_APP_USERNAME", "admin")
    os.environ.setdefault("DASHBOARD_APP_PASSWORD", "partenon")

    from fastapi.testclient import TestClient

    from partenon_api.main import app

    return TestClient(app)


@pytest.fixture
def auth_token():
    """Return a valid JWT for the default workspace."""
    from partenon_api.auth import create_access_token

    return create_access_token("admin", "default")
