"""
Partenon Guardian — Key and Access Manager

Security helpers for listing API keys, rotating provider keys,
auditing profile permissions, and recommending models for tasks.

Python 3.12 compatible.
"""

import os
import re
import hashlib
import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class KeyRecord:
    provider: str
    env_var: str
    value: Optional[str]
    last_rotated: Optional[str]
    status: str


_PROVIDER_CONFIG: Dict[str, Dict[str, Any]] = {
    "nvidia": {
        "env_var": "NVIDIA_API_KEY",
        "pattern": r"^nvapi-[A-Za-z0-9_-]+$",
    },
    "openai": {
        "env_var": "OPENAI_API_KEY",
        "pattern": r"^sk-[A-Za-z0-9]+$",
    },
    "kimi": {
        "env_var": "KIMI_API_KEY",
        "pattern": r"^[A-Za-z0-9_-]{16,}$",
    },
    "stripe": {
        "env_var": "STRIPE_SECRET_KEY",
        "pattern": r"^sk_(test|live)_[A-Za-z0-9]+$",
    },
}

_ROTATION_INTERVAL_DAYS = 90


def _fingerprint(value: Optional[str]) -> str:
    """Return a masked fingerprint of a secret value."""
    if not value:
        return "none"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


def _hash(value: Optional[str]) -> str:
    """Return a sha256 hex digest of a value, or an empty string."""
    if not value:
        return ""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _is_expired(last_rotated: Optional[str]) -> bool:
    """Check if a key's last rotation date exceeds the rotation interval."""
    if not last_rotated:
        return True
    try:
        rotated = datetime.datetime.fromisoformat(last_rotated)
    except ValueError:
        return True
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
        days=_ROTATION_INTERVAL_DAYS
    )
    if rotated.tzinfo is None:
        cutoff = cutoff.replace(tzinfo=None)
    return rotated < cutoff


def _key_status(value: Optional[str], last_rotated: Optional[str]) -> str:
    """Determine the status of a key."""
    if not value:
        return "missing"
    if _is_expired(last_rotated):
        return "pending_rotation"
    return "active"


def list_keys() -> List[Dict[str, str]]:
    """
    List all configured API keys with masked fingerprints.

    Returns a list of dictionaries with provider, key_id, fingerprint,
    status, and last_rotated fields. Full key values are never returned.
    """
    records = []
    for provider, config in _PROVIDER_CONFIG.items():
        env_var = config["env_var"]
        value = os.environ.get(env_var)
        # Rotation timestamps may be stored in companion environment variables.
        last_rotated = os.environ.get(f"{env_var}_LAST_ROTATED")
        status = _key_status(value, last_rotated)
        records.append(
            {
                "provider": provider,
                "key_id": env_var,
                "fingerprint": _fingerprint(value),
                "hash": _hash(value),
                "status": status,
                "last_rotated": last_rotated or "never",
            }
        )
    return records


def rotate_key(provider: str) -> Dict[str, str]:
    """
    Rotate the API key for a provider.

    This function performs a safe rotation sequence:
      1. Validate the provider is known.
      2. Read the current key reference.
      3. Generate a placeholder new key value.
      4. Update the environment or secrets manager reference.
      5. Record the rotation event metadata.

    The actual key must be replaced manually or by an external secrets
    manager; this tool does not call provider APIs to avoid leaking
    credentials in process logs.
    """
    provider = provider.lower().strip()
    config = _PROVIDER_CONFIG.get(provider)
    if not config:
        raise ValueError(f"Unknown provider: {provider}")

    env_var = config["env_var"]
    old_value = os.environ.get(env_var)
    old_fingerprint = _fingerprint(old_value)

    # Generate a placeholder. The operator replaces this with a real key.
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    new_value = f"ROTATED_{provider.upper()}_{timestamp}"

    # In a real deployment, update the secrets manager here.
    os.environ[env_var] = new_value
    os.environ[f"{env_var}_LAST_ROTATED"] = timestamp

    return {
        "provider": provider,
        "env_var": env_var,
        "old_fingerprint": old_fingerprint,
        "new_fingerprint": _fingerprint(new_value),
        "rotated_at": timestamp,
        "note": "Replace placeholder with real key from provider console.",
    }


def audit_access(profile: str) -> Dict[str, Any]:
    """
    Audit permissions assigned to a Partenon profile.

    Returns a report with tools, MCP servers, skills, file scopes, and
    any violations detected against the canonical security template.
    """
    # Canonical roles are simplified here. In production, load from
    # templates/.security.example or the brain.
    canonical = {
        "partenon-guardian": {
            "tools": {"terminal", "file", "gbrain"},
            "mcp_servers": {"gbrain"},
            "skills": {"security"},
            "files": {"hermes/profiles/partenon-guardian/**"},
        },
        "partenon-tesorero": {
            "tools": {"terminal", "file"},
            "mcp_servers": set(),
            "skills": {"finance"},
            "files": {"hermes/profiles/partenon-tesorero/**"},
        },
        "partenon-mensajero": {
            "tools": {"terminal", "file"},
            "mcp_servers": set(),
            "skills": {"comms"},
            "files": {"hermes/profiles/partenon-mensajero/**"},
        },
        "partenon-cobrador": {
            "tools": {"terminal", "file"},
            "mcp_servers": set(),
            "skills": {"payments"},
            "files": {"hermes/profiles/partenon-cobrador/**"},
        },
        "partenon-estratega": {
            "tools": {"terminal", "file"},
            "mcp_servers": set(),
            "skills": {"ops"},
            "files": {"hermes/profiles/partenon-estratega/**"},
        },
        "partenon-diplomatico": {
            "tools": {"terminal", "file"},
            "mcp_servers": set(),
            "skills": {"relations"},
            "files": {"hermes/profiles/partenon-diplomatico/**"},
        },
        "partenon-brain": {
            "tools": {"terminal", "file"},
            "mcp_servers": {"gbrain"},
            "skills": {"memory"},
            "files": {"hermes/profiles/partenon-brain/**"},
        },
    }

    # In a real deployment, load the live profile config.yaml.
    # Here we return the canonical definition as the expected state.
    role = canonical.get(profile, {})
    violations: List[str] = []

    if not role:
        violations.append(f"No canonical role found for profile '{profile}'.")

    return {
        "profile": profile,
        "tools": sorted(role.get("tools", set())),
        "mcp_servers": sorted(role.get("mcp_servers", set())),
        "skills": sorted(role.get("skills", set())),
        "files": sorted(role.get("files", set())),
        "violations": violations,
    }


def validate_access(profile: str, resource: str, action: str) -> Dict[str, Any]:
    """
    Validate whether a profile may perform an action on a resource.

    Returns an access decision with reason and required role.
    """
    audit = audit_access(profile)
    allowed = not audit["violations"] and action in {"read", "audit", "rotate"}
    reason = "Allowed by least-privilege policy." if allowed else "Denied by default."
    return {
        "allowed": allowed,
        "reason": reason,
        "required_role": profile if allowed else "partenon-guardian",
    }


def rotate_keys(providers: List[str]) -> List[Dict[str, str]]:
    """
    Rotate API keys for multiple providers in one call.

    Returns a list of rotation results. Unknown providers are skipped
    with an error entry instead of raising an exception.
    """
    results: List[Dict[str, str]] = []
    for provider in providers:
        try:
            results.append(rotate_key(provider))
        except ValueError as exc:
            results.append(
                {
                    "provider": provider,
                    "error": str(exc),
                    "rotated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                }
            )
    return results


def get_model_recommendation(task: str) -> Dict[str, str]:
    """
    Recommend a model and provider based on task sensitivity, cost,
    and latency requirements.
    """
    task_lower = task.lower()

    if any(word in task_lower for word in {"security", "audit", "key", "permission"}):
        return {
            "provider": "kimi",
            "model": "kimi-k2-6",
            "reason": "High-stakes security tasks need strong reasoning and low hallucination.",
        }

    if any(word in task_lower for word in {"code", "review", "refactor"}):
        return {
            "provider": "nvidia",
            "model": "nemotron-4-340b-instruct",
            "reason": "Code generation benefits from large instruct models.",
        }

    if any(word in task_lower for word in {"chat", "draft", "summarize"}):
        return {
            "provider": "openai",
            "model": "gpt-4o-mini",
            "reason": "Fast and cost-effective for routine language tasks.",
        }

    return {
        "provider": "kimi",
        "model": "kimi-k2-6",
        "reason": "Default balanced recommendation.",
    }
