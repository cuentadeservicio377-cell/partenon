"""Configuration for the Partenon API."""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.resolve()
DATA_DIR = PROJECT_ROOT / "data"

DEFAULT_WORKSPACE_ID = "default"
DEFAULT_API_HOST = "127.0.0.1"
DEFAULT_API_PORT = 8000
DEFAULT_DASHBOARD_ORIGIN = "http://localhost:3000"


def get_secret() -> str:
    """Return the JWT signing secret.

    PARTENON_API_SECRET is preferred. DASHBOARD_AUTH_SECRET is accepted as a
    fallback so the dashboard and API can share authentication without extra
    setup.
    """
    secret = os.environ.get("PARTENON_API_SECRET") or os.environ.get("DASHBOARD_AUTH_SECRET")
    if not secret:
        raise RuntimeError(
            "PARTENON_API_SECRET or DASHBOARD_AUTH_SECRET must be set"
        )
    return secret


def get_api_host() -> str:
    return os.environ.get("PARTENON_API_HOST", DEFAULT_API_HOST)


def get_api_port() -> int:
    return int(os.environ.get("PARTENON_API_PORT", DEFAULT_API_PORT))


def get_dashboard_origin() -> str:
    return os.environ.get("DASHBOARD_ORIGIN", DEFAULT_DASHBOARD_ORIGIN)


def get_data_dir() -> Path:
    path = Path(os.environ.get("PARTENON_DATA_DIR", DATA_DIR))
    path.mkdir(parents=True, exist_ok=True)
    return path
