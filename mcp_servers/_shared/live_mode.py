"""Shared helpers for deciding dry-run vs live execution per integration."""

import os


def is_live(service: str) -> bool:
    """Return True if the named service has credentials and may run live.

    Supported services:
      - google_workspace: GOOGLE_SERVICE_ACCOUNT_JSON or both GOOGLE_OAUTH_CLIENT_ID/SECRET
      - stripe: STRIPE_SECRET_KEY
      - slack: SLACK_BOT_TOKEN
      - gbrain: GBRAIN_DATABASE_URL (non-sqlite fallback counts as live)
    """
    service = service.lower()
    if service == "google_workspace":
        return bool(
            os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")
            or (
                os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
                and os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
            )
        )
    if service == "stripe":
        return bool(os.environ.get("STRIPE_SECRET_KEY"))
    if service == "slack":
        return bool(os.environ.get("SLACK_BOT_TOKEN"))
    if service in {"gbrain", "memory"}:
        url = os.environ.get("GBRAIN_DATABASE_URL", "")
        return bool(url) and not url.startswith("sqlite:")
    return False


def require_live(service: str) -> None:
    """Raise RuntimeError if the service is not in live mode."""
    if not is_live(service):
        raise RuntimeError(f"{service} is not in live mode: missing credentials")
