"""
Partenon Guardian — Policy Manager

Helpers for setting, retrieving, and validating role-based access
policies for Partenon profiles.

Python 3.12 compatible.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


_CANONICAL_ROLES: Dict[str, Dict[str, Any]] = {
    "partenon-guardian": {
        "tools": ["terminal", "file", "gbrain"],
        "mcp_servers": ["gbrain"],
        "skills": ["security"],
        "files": ["hermes/profiles/partenon-guardian/**"],
        "actions": [
            "list_keys",
            "rotate_key",
            "rotate_keys",
            "audit_access",
            "validate_access",
            "manage_secrets",
            "allocate_gpu",
            "set_policies",
            "audit_log",
        ],
    },
    "partenon-scribe": {
        "tools": ["terminal", "file"],
        "mcp_servers": [],
        "skills": ["finance"],
        "files": ["hermes/profiles/partenon-scribe/**"],
        "actions": ["read_financial_data"],
    },
    "partenon-herald": {
        "tools": ["terminal", "file"],
        "mcp_servers": [],
        "skills": ["comms"],
        "files": ["hermes/profiles/partenon-herald/**"],
        "actions": ["send_message"],
    },
    "partenon-collector": {
        "tools": ["terminal", "file"],
        "mcp_servers": [],
        "skills": ["payments"],
        "files": ["hermes/profiles/partenon-collector/**"],
        "actions": ["manage_payments"],
    },
    "partenon-strategist": {
        "tools": ["terminal", "file"],
        "mcp_servers": [],
        "skills": ["ops"],
        "files": ["hermes/profiles/partenon-strategist/**"],
        "actions": ["manage_operations"],
    },
    "partenon-diplomat": {
        "tools": ["terminal", "file"],
        "mcp_servers": [],
        "skills": ["relations"],
        "files": ["hermes/profiles/partenon-diplomat/**"],
        "actions": ["manage_relations"],
    },
    "partenon-brain": {
        "tools": ["terminal", "file"],
        "mcp_servers": ["gbrain"],
        "skills": ["memory"],
        "files": ["hermes/profiles/partenon-brain/**"],
        "actions": ["manage_memory"],
    },
}


def _policies_dir() -> Path:
    """Return the directory where active policy files are stored."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "partenon-guardian":
            return parent / "data" / "policies"
    return Path(__file__).resolve().parents[3] / "data" / "policies"


def _policy_file(profile: str) -> Path:
    """Return the policy file path for a profile."""
    return _policies_dir() / f"{profile}.json"


def set_policies(
    profile: str,
    permissions: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Write the active RBAC policy for a profile.

    The policy is validated against the canonical role definition.
    Any permission not justified by the canonical role is flagged as
    a violation but still recorded for operator review.
    """
    permissions = permissions or {}
    canonical = _CANONICAL_ROLES.get(profile, {})
    violations: List[str] = []

    for key in ("tools", "mcp_servers", "skills", "files", "actions"):
        allowed = set(canonical.get(key, []))
        requested = set(permissions.get(key, []))
        extra = requested - allowed
        if extra:
            violations.append(f"{key}: {sorted(extra)} exceed canonical role for '{profile}'.")

    policy = {
        "profile": profile,
        "permissions": {
            "tools": sorted(permissions.get("tools", canonical.get("tools", []))),
            "mcp_servers": sorted(permissions.get("mcp_servers", canonical.get("mcp_servers", []))),
            "skills": sorted(permissions.get("skills", canonical.get("skills", []))),
            "files": sorted(permissions.get("files", canonical.get("files", []))),
            "actions": sorted(permissions.get("actions", canonical.get("actions", []))),
        },
        "violations": violations,
        "canonical": bool(canonical),
    }

    policy_path = _policy_file(profile)
    policy_path.parent.mkdir(parents=True, exist_ok=True)
    with open(policy_path, "w", encoding="utf-8") as f:
        json.dump(policy, f, ensure_ascii=False, indent=2)

    return {"success": True, "profile": profile, "policy_path": str(policy_path), **policy}


def get_policy(profile: str) -> Dict[str, Any]:
    """Return the active policy for a profile, or the canonical default."""
    policy_path = _policy_file(profile)
    if policy_path.exists():
        with open(policy_path, "r", encoding="utf-8") as f:
            return json.load(f)
    canonical = _CANONICAL_ROLES.get(profile, {})
    if not canonical:
        return {"profile": profile, "error": "No canonical role found."}
    return {
        "profile": profile,
        "permissions": {k: sorted(v) for k, v in canonical.items() if k != "canonical"},
        "violations": [],
        "canonical": True,
    }
