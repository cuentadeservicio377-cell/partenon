"""
Partenon Guardian — Secrets Manager

Vault-style helpers for listing, storing, rotating, and deleting
API key references without exposing secret values.

Python 3.12 compatible.
"""

import os
import re
from typing import Any, Dict, List, Optional


_SECRET_PATTERNS: Dict[str, str] = {
    "nvidia": r"^nvapi-[A-Za-z0-9_-]+$",
    "openai": r"^sk-[A-Za-z0-9]+$",
    "kimi": r"^[A-Za-z0-9_-]{16,}$",
    "stripe": r"^sk_(test|live)_[A-Za-z0-9]+$",
}


def _fingerprint(value: Optional[str]) -> str:
    """Return a masked fingerprint of a secret value."""
    if not value:
        return "none"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def _validate(provider: str, value: str) -> bool:
    """Check whether a value matches the expected format for a provider."""
    pattern = _SECRET_PATTERNS.get(provider.lower())
    if not pattern:
        return False
    return bool(re.match(pattern, value))


def manage_secrets(
    action: str,
    key_id: str,
    value: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Manage a secret reference for an external provider.

    Actions:
      - list: return all configured secret references.
      - store: save a new secret reference (value required).
      - rotate: replace an existing secret reference.
      - delete: remove a secret reference from the environment.

    The actual secret value is never returned; only its fingerprint,
    status, and policy metadata.
    """
    action = action.lower().strip()
    metadata = metadata or {}
    provider = key_id.lower().strip()
    env_var = key_id.upper()

    if action == "list":
        records: List[Dict[str, str]] = []
        for provider_name in _SECRET_PATTERNS:
            var = provider_name.upper() + "_API_KEY"
            if provider_name == "stripe":
                var = "STRIPE_SECRET_KEY"
            val = os.environ.get(var)
            records.append(
                {
                    "provider": provider_name,
                    "key_id": var,
                    "fingerprint": _fingerprint(val),
                    "status": "active" if val else "missing",
                }
            )
        return {"action": "list", "secrets": records}

    if action == "store":
        if not value:
            return {"action": "store", "key_id": key_id, "error": "Value is required to store a secret."}
        if not _validate(provider, value):
            return {
                "action": "store",
                "key_id": key_id,
                "error": f"Value does not match expected pattern for provider '{provider}'.",
            }
        os.environ[env_var] = value
        return {
            "action": "store",
            "key_id": key_id,
            "fingerprint": _fingerprint(value),
            "status": "active",
            "policy": {
                "mask_in_logs": True,
                "rotation_days": metadata.get("rotation_days", 90),
                "last_rotated": metadata.get("last_rotated"),
            },
        }

    if action == "rotate":
        if not value:
            return {"action": "rotate", "key_id": key_id, "error": "New value is required to rotate a secret."}
        if not _validate(provider, value):
            return {
                "action": "rotate",
                "key_id": key_id,
                "error": f"Value does not match expected pattern for provider '{provider}'.",
            }
        old_value = os.environ.get(env_var)
        os.environ[env_var] = value
        return {
            "action": "rotate",
            "key_id": key_id,
            "old_fingerprint": _fingerprint(old_value),
            "new_fingerprint": _fingerprint(value),
            "status": "active",
            "policy": {
                "mask_in_logs": True,
                "rotation_days": metadata.get("rotation_days", 90),
            },
        }

    if action == "delete":
        old_value = os.environ.get(env_var)
        if env_var in os.environ:
            del os.environ[env_var]
        return {
            "action": "delete",
            "key_id": key_id,
            "old_fingerprint": _fingerprint(old_value),
            "status": "deleted",
        }

    return {"action": action, "key_id": key_id, "error": f"Unknown action: {action}"}
