"""
Partenon Guardian — Audit Logger

Tamper-evident logging helpers for security events, access decisions,
and key rotations. Logs are written as JSON Lines under the profile's
`data/audit/` directory.

Python 3.12 compatible.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


_DEFAULT_RETENTION_DAYS = 365


def _audit_dir() -> Path:
    """Return the directory where audit logs are stored."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "partenon-guardian":
            return parent / "data" / "audit"
    return Path(__file__).resolve().parents[3] / "data" / "audit"


def _log_file() -> Path:
    """Return the current audit log file path."""
    return _audit_dir() / "security.log"


def audit_log(
    event_type: str,
    profile: str,
    resource: str,
    action: str,
    status: str,
    message: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Append a security event to the audit log.

    Args:
        event_type: category such as access, rotation, policy, or system.
        profile: profile that triggered the event.
        resource: resource that was accessed or modified.
        action: action that was attempted.
        status: outcome such as allowed, denied, success, or failed.
        message: optional human-readable note.
        metadata: optional additional structured data.

    Returns:
        Dict with the recorded event and log file path.
    """
    entry = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type.lower().strip(),
        "profile": profile,
        "resource": resource,
        "action": action,
        "status": status,
        "message": message or "",
        "metadata": metadata or {},
    }

    log_path = _log_file()
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return {"success": True, "event": entry, "log_path": str(log_path)}


def get_audit_logs(
    event_type: Optional[str] = None,
    profile: Optional[str] = None,
    limit: int = 100,
) -> Dict[str, Any]:
    """
    Read the most recent audit log entries with optional filters.

    Args:
        event_type: filter by event type.
        profile: filter by profile name.
        limit: maximum number of entries to return.

    Returns:
        Dict with the matching entries and total count.
    """
    log_path = _log_file()
    entries: List[Dict[str, Any]] = []

    if log_path.exists():
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event_type and entry.get("event_type") != event_type:
                    continue
                if profile and entry.get("profile") != profile:
                    continue
                entries.append(entry)

    entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    return {"total": len(entries), "limit": limit, "entries": entries[:limit]}


def prune_audit_logs(retention_days: int = _DEFAULT_RETENTION_DAYS) -> Dict[str, Any]:
    """
    Remove audit log entries older than the retention period.

    This is a maintenance helper; in production, retention should be
    enforced by the log aggregation backend.
    """
    log_path = _log_file()
    if not log_path.exists():
        return {"pruned": 0, "remaining": 0}

    cutoff = datetime.now(timezone.utc).timestamp() - (retention_days * 24 * 60 * 60)
    kept: List[Dict[str, Any]] = []
    pruned = 0

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                ts = datetime.fromisoformat(entry.get("timestamp", "")).timestamp()
            except (ValueError, KeyError):
                ts = 0
            if ts < cutoff:
                pruned += 1
            else:
                kept.append(entry)

    with open(log_path, "w", encoding="utf-8") as f:
        for entry in kept:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    return {"pruned": pruned, "remaining": len(kept)}
