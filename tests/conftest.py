"""Shared test fixtures."""

import os
import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture(scope="session", autouse=True)
def _set_json_store_mode():
    """Force the synchronous JSON fallback for the entire test suite.

    This keeps unit tests fast and avoids spawning an MCP subprocess unless a
    test explicitly exercises the MCP runtime.
    """
    previous = os.environ.get("PARTENON_STORE_MODE")
    os.environ["PARTENON_STORE_MODE"] = "json"
    yield
    if previous is None:
        os.environ.pop("PARTENON_STORE_MODE", None)
    else:
        os.environ["PARTENON_STORE_MODE"] = previous


@pytest.fixture
def temp_data_dir(monkeypatch):
    """Provide a temporary data directory and patch the API to use it."""
    path = Path(tempfile.mkdtemp())
    monkeypatch.setenv("PARTENON_DATA_DIR", str(path))
    # Use the synchronous JSON fallback so tests run without spawning an MCP
    # subprocess on every test case. Production code still exercises the MCP
    # path when PARTENON_STORE_MODE is not set to "json".
    monkeypatch.setenv("PARTENON_STORE_MODE", "json")
    monkeypatch.setenv(
        "GBRAIN_DATABASE_URL",
        f"sqlite:///{path / 'gbrain.db'}",
    )
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

    with TestClient(app) as client:
        yield client


@pytest.fixture
def auth_token():
    """Return a valid JWT for the default workspace."""
    from partenon_api.auth import create_access_token

    return create_access_token("admin", "default")
