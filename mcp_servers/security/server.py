"""Partenon Security MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("partenon-security")


@mcp.tool()
def security_audit_keys(dry_run: bool = True) -> dict:
    """Audit API keys and flag keys older than 90 days."""
    if dry_run:
        return {"ok": True, "dry_run": True, "keys": []}
    return {"ok": False, "error": "live execution requires key store access"}


@mcp.tool()
def security_recommend_key_rotation(profile: str, dry_run: bool = True) -> dict:
    """Recommend key rotation for a profile."""
    if dry_run:
        return {"ok": True, "dry_run": True, "recommendations": []}
    return {"ok": False, "error": "live execution requires key store access"}


@mcp.tool()
def security_validate_policy(policy_text: str, dry_run: bool = True) -> dict:
    """Validate a security policy text."""
    if dry_run:
        return {"ok": True, "dry_run": True, "valid": True, "issues": []}
    return {"ok": False, "error": "live execution requires policy store access"}


if __name__ == "__main__":
    mcp.run()
