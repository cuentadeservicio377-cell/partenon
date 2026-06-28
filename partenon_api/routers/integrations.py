"""Integration routes — thin wrappers over MCP servers."""

import os
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.models import IntegrationStatus

router = APIRouter(prefix="/integrations", tags=["integrations"])


# Re-export type alias for OpenAPI schema clarity
Payload = Dict[str, Any]


def _is_configured(domain: str) -> bool:
    """Return True if live credentials for a domain are present."""
    checks = {
        "google_workspace": bool(os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")),
        "payments": bool(os.environ.get("STRIPE_SECRET_KEY")),
        "slack": bool(os.environ.get("SLACK_BOT_TOKEN")),
        "memory": bool(os.environ.get("GBRAIN_DATABASE_URL")),
    }
    return checks.get(domain, False)


@router.get("")
async def list_integrations(
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    domains = ["google_workspace", "payments", "slack", "memory"]
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
    dry_run = payload.get("dry_run", True)
    try:
        if domain == "google_workspace":
            return _invoke_google_workspace(action, payload)
        if domain == "slack":
            return _invoke_slack(action, payload)
        if domain == "payments":
            return _invoke_payments(action, payload, dry_run)
        if domain == "memory":
            return _invoke_memory(action, payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Integration error: {e}",
        ) from e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown integration domain")


def _invoke_google_workspace(action: str, payload: Dict[str, Any]) -> dict:
    from mcp_servers.google_workspace.client import GoogleWorkspaceClient

    client = GoogleWorkspaceClient()
    method = getattr(client, action, None)
    if not method:
        raise ValueError(f"Unknown Google Workspace action: {action}")
    return method(**payload)


def _invoke_slack(action: str, payload: Dict[str, Any]) -> dict:
    from mcp_servers.notifications.slack import notify_task_overdue, send_message

    if action == "send_message":
        return send_message(payload.get("channel", "#general"), payload.get("text", ""))
    if action == "notify_task_overdue":
        return notify_task_overdue(
            payload.get("task_id", ""),
            payload.get("title", ""),
            payload.get("due_date", ""),
            payload.get("channel", "#general"),
        )
    raise ValueError(f"Unknown Slack action: {action}")


def _invoke_payments(action: str, payload: Dict[str, Any], dry_run: bool) -> dict:
    import mcp_servers.payments.server as payments

    func = getattr(payments, f"payments_{action}", None)
    if not func:
        raise ValueError(f"Unknown payments action: {action}")
    kwargs = dict(payload)
    kwargs["dry_run"] = dry_run
    return func(**kwargs)


def _invoke_memory(action: str, payload: Dict[str, Any]) -> dict:
    import json

    import mcp_servers.memory.server as memory

    func = getattr(memory, action, None)
    if not func:
        raise ValueError(f"Unknown memory action: {action}")
    result = func(**payload)
    try:
        return json.loads(result) if isinstance(result, str) else result
    except json.JSONDecodeError:
        return {"result": result}
