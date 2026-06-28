"""Shared API helpers."""

import uuid
from datetime import datetime, timezone
from typing import List


def new_id(prefix: str) -> str:
    """Generate a short unique id with the given prefix."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def now_iso() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def filter_by_workspace(items: List[dict], workspace_id: str) -> List[dict]:
    """Return items belonging to the given workspace."""
    return [item for item in items if item.get("workspace_id", "default") == workspace_id]
