"""Integration routes — thin wrappers over MCP servers."""

import json
import os
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.mcp_client import AsyncDomainClient
from partenon_api.models import IntegrationStatus

router = APIRouter(prefix="/integrations", tags=["integrations"])


# Re-export type alias for OpenAPI schema clarity
Payload = Dict[str, Any]


# Domain server configuration: module path and tool name prefix.
_DOMAIN_CONFIG: Dict[str, Dict[str, str]] = {
    "google_workspace": {
        "module": "mcp_servers.google_workspace.server",
        "tool_prefix": "workspace_",
    },
    "payments": {
        "module": "mcp_servers.payments.server",
        "tool_prefix": "payments_",
    },
    "slack": {
        "module": "mcp_servers.notifications.server",
        "tool_prefix": "slack_",
    },
    "memory": {
        "module": "mcp_servers.memory.server",
        "tool_prefix": "memory_",
    },
}


def _is_configured(domain: str) -> bool:
    """Return True if live credentials for a domain are present."""
    checks = {
        "google_workspace": bool(os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")),
        "payments": bool(os.environ.get("STRIPE_SECRET_KEY")),
        "slack": bool(os.environ.get("SLACK_BOT_TOKEN")),
        "memory": bool(os.environ.get("GBRAIN_DATABASE_URL")),
    }
    return checks.get(domain, False)


def _dry_run_response(domain: str, action: str) -> dict:
    """Return a short-circuit dry-run response for unconfigured domains."""
    return {
        "ok": True,
        "dry_run": True,
        "domain": domain,
        "action": action,
        "reason": "no live credentials configured",
    }


@router.get("")
async def list_integrations(
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    domains = list(_DOMAIN_CONFIG.keys())
    items = []
    for domain in domains:
        connected = _is_configured(domain)
        items.append(
            IntegrationStatus(
                domain=domain,
                connected=connected,
                mode="live" if connected else "dry_run",
            ).model_dump()
        )
    return {"integrations": items}


@router.post("/{domain}/{action}")
async def invoke_integration(
    domain: str,
    action: str,
    payload: Dict[str, Any],
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    config = _DOMAIN_CONFIG.get(domain)
    if config is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown integration domain")

    dry_run = payload.get("dry_run", True)

    # Short-circuit unconfigured domains to avoid spawning subprocesses when no
    # live credentials are present. Memory is a local dependency and is always
    # invoked. For non-memory domains with dry_run=False and no credentials,
    # return the same live-mode error the MCP server would produce.
    if domain != "memory" and not _is_configured(domain):
        if dry_run:
            return _dry_run_response(domain, action)
        return {
            "ok": False,
            "error": f"live execution requires {domain.replace('_', ' ')} credentials",
        }

    tool_name = f"{config['tool_prefix']}{action}"
    kwargs = dict(payload)
    kwargs.pop("dry_run", None)

    # Payments tools expect an explicit dry_run flag; other domain servers
    # handle dry-run internally based on environment variables.
    if domain == "payments":
        kwargs["dry_run"] = dry_run

    try:
        async with AsyncDomainClient(config["module"]) as client:
            result = await client.call_tool(tool_name, **kwargs)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Integration error: {e}",
        ) from e

    # Domain MCP servers may return a plain string (e.g. memory_put_page).
    # Normalize to a dict for a consistent JSON response shape.
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            return {"result": result}
    if result is None:
        return {"ok": True}
    return {"result": result}
