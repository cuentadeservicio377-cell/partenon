"""Partenon Relations MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

from mcp_servers._shared.live_mode import is_live
from mcp_servers.google_workspace.client import GoogleWorkspaceClient

mcp = FastMCP("partenon-relations")


def _workspace_client() -> GoogleWorkspaceClient:
    return GoogleWorkspaceClient()


@mcp.tool()
def relations_register_client(name: str, email: str = "", dry_run: bool = True) -> dict:
    """Register a client."""
    if dry_run:
        return {"ok": True, "dry_run": True, "client_id": "CLI-001", "name": name}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_register_vendor(name: str, email: str = "", dry_run: bool = True) -> dict:
    """Register a vendor."""
    if dry_run:
        return {"ok": True, "dry_run": True, "vendor_id": "VEN-001", "name": name}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_log_interaction(entity_id: str, text: str, dry_run: bool = True) -> dict:
    """Log an interaction with a client or vendor."""
    if dry_run:
        return {"ok": True, "dry_run": True, "entity_id": entity_id}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_track_milestone(entity_id: str, title: str, due_date: str, dry_run: bool = True) -> dict:
    """Track a milestone for a relationship."""
    if dry_run:
        return {"ok": True, "dry_run": True, "milestone_id": "MIL-001"}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_track_deliverable(entity_id: str, title: str, status: str = "pending", dry_run: bool = True) -> dict:
    """Track a deliverable for a relationship."""
    if dry_run:
        return {"ok": True, "dry_run": True, "deliverable_id": "DEL-001"}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_rate_relationship(entity_id: str, rating: str, reason: str = "", dry_run: bool = True) -> dict:
    """Rate a relationship A/B/C/D with a reason."""
    if dry_run:
        return {"ok": True, "dry_run": True, "entity_id": entity_id, "rating": rating}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_run_followups(dry_run: bool = True) -> dict:
    """Run daily follow-up report."""
    if dry_run:
        return {"ok": True, "dry_run": True, "actions": []}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_generate_proposal(entity_id: str, amount: float, dry_run: bool = True) -> dict:
    """Generate a proposal for a client."""
    if dry_run:
        return {"ok": True, "dry_run": True, "entity_id": entity_id, "amount": amount}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_sync_contacts(direction: str = "export", dry_run: bool = True) -> dict:
    """Sync contacts with an external CRM."""
    if dry_run:
        return {"ok": True, "dry_run": True, "direction": direction, "synced": 0}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_schedule_meeting(
    entity_id: str, title: str, start: str, end: str = "", attendees_json: str = "[]", dry_run: bool = True
) -> dict:
    """Schedule a meeting with a contact. In live mode, creates a Calendar event."""
    if dry_run:
        return {"ok": True, "dry_run": True, "meeting_id": "MTG-001"}
    if not is_live("google_workspace"):
        return {"ok": False, "error": "live execution requires calendar credentials"}
    try:
        import json
        attendees = json.loads(attendees_json)
        end_time = end or start
        result = _workspace_client().create_calendar_event(title, start, end_time, attendees)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}
