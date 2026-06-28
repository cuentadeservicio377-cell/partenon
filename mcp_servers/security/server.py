"""Partenon Security MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

from mcp_servers.security.key_manager import (
    audit_key_strength,
    detect_key_provider,
    recommend_model,
    rotate_key_live,
)

mcp = FastMCP("partenon-security")


@mcp.tool()
def security_list_keys(dry_run: bool = True) -> dict:
    """Audit API keys and flag keys older than 90 days."""
    if dry_run:
        return {"ok": True, "dry_run": True, "keys": []}
    return {"ok": False, "error": "live execution requires key store access"}


@mcp.tool()
def security_rotate_key(provider: str, dry_run: bool = True) -> dict:
    """Rotate the API key for a provider."""
    if dry_run:
        return {"ok": True, "dry_run": True, "provider": provider, "rotated": False}
    return {"ok": False, "error": "live execution requires key store access"}


@mcp.tool()
def security_audit_access(profile: str, dry_run: bool = True) -> dict:
    """Audit the permissions assigned to a Partenon profile."""
    if dry_run:
        return {"ok": True, "dry_run": True, "profile": profile, "violations": []}
    return {"ok": False, "error": "live execution requires policy store access"}


@mcp.tool()
def security_validate_access(profile: str, resource: str, action: str, dry_run: bool = True) -> dict:
    """Check whether a profile is allowed to perform an action on a resource."""
    if dry_run:
        return {"ok": True, "dry_run": True, "allowed": True, "reason": "dry-run"}
    return {"ok": False, "error": "live execution requires policy store access"}


@mcp.tool()
def security_manage_secrets(action: str, key_id: str, value: str = "", dry_run: bool = True) -> dict:
    """Vault-style management of API key references."""
    if dry_run:
        return {"ok": True, "dry_run": True, "action": action, "key_id": key_id}
    return {"ok": False, "error": "live execution requires secrets manager"}


@mcp.tool()
def security_allocate_gpu(task: str, dry_run: bool = True) -> dict:
    """Recommend a GPU/model allocation for a task."""
    if dry_run:
        return {"ok": True, "dry_run": True, "recommendation": "nvidia-l4"}
    return {"ok": False, "error": "live execution requires GPU provider credentials"}


@mcp.tool()
def security_set_policy(policy_name: str, policy_text: str, dry_run: bool = True) -> dict:
    """Set a security policy."""
    if dry_run:
        return {"ok": True, "dry_run": True, "policy": policy_name}
    return {"ok": False, "error": "live execution requires policy store access"}


@mcp.tool()
def security_audit_log(event: str, dry_run: bool = True) -> dict:
    """Log a security event."""
    if dry_run:
        return {"ok": True, "dry_run": True, "logged": True}
    return {"ok": False, "error": "live execution requires audit store access"}


@mcp.tool()
def security_audit_key_strength(key: str, dry_run: bool = True) -> dict:
    """Audit the strength of an API key."""
    result = audit_key_strength(key)
    return {"ok": True, "dry_run": dry_run, **result}


@mcp.tool()
def security_detect_key_provider(key: str, dry_run: bool = True) -> dict:
    """Detect the provider of an API key from its prefix."""
    return {"ok": True, "dry_run": dry_run, "provider": detect_key_provider(key)}


@mcp.tool()
def security_recommend_model(provider: str, budget_tier: str = "standard", latency: str = "normal", dry_run: bool = True) -> dict:
    """Recommend an AI model for a provider and budget tier."""
    result = recommend_model(provider, budget_tier, latency)
    return {"ok": True, "dry_run": dry_run, **result}


@mcp.tool()
def security_rotate_key_live(service: str, dry_run: bool = True) -> dict:
    """Placeholder for live key rotation. Never rotates without explicit approval."""
    if dry_run:
        return {"ok": True, "dry_run": True, "service": service, "rotated": False}
    return {"ok": True, "dry_run": False, **rotate_key_live(service)}
