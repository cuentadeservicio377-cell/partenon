"""Partenon Ops MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

from mcp_servers._shared.live_mode import is_live
from mcp_servers.google_workspace.client import GoogleWorkspaceClient

mcp = FastMCP("partenon-ops")


def _workspace_client() -> GoogleWorkspaceClient:
    return GoogleWorkspaceClient()


@mcp.tool()
def ops_create_project(name: str, client: str, dry_run: bool = True) -> dict:
    """Create a project."""
    if dry_run:
        return {"ok": True, "dry_run": True, "project_id": "PROJ-001", "name": name, "client": client}
    return {"ok": False, "error": "live execution requires workspace credentials"}


@mcp.tool()
def ops_create_task(project_id: str, title: str, owner: str = "", dry_run: bool = True) -> dict:
    """Create a task inside a project."""
    if dry_run:
        return {"ok": True, "dry_run": True, "task_id": "TASK-001", "project_id": project_id, "title": title}
    return {"ok": False, "error": "live execution requires workspace credentials"}


@mcp.tool()
def ops_generate_checklist(project_id: str, template: str = "consulting", dry_run: bool = True) -> dict:
    """Generate a checklist for a project."""
    if dry_run:
        return {"ok": True, "dry_run": True, "project_id": project_id, "items": []}
    return {"ok": False, "error": "live execution requires workspace credentials"}


@mcp.tool()
def ops_define_goal(title: str, target: int = 1, dry_run: bool = True) -> dict:
    """Define a goal or OKR."""
    if dry_run:
        return {"ok": True, "dry_run": True, "goal_id": "GOAL-001", "title": title}
    return {"ok": False, "error": "live execution requires workspace credentials"}


@mcp.tool()
def ops_generate_briefing(profile: str, dry_run: bool = True) -> dict:
    """Generate a daily briefing for a profile."""
    if dry_run:
        return {"ok": True, "dry_run": True, "profile": profile, "briefing": []}
    return {"ok": False, "error": "live execution requires workspace credentials"}


@mcp.tool()
def ops_create_calendar_event(title: str, start: str, end: str, dry_run: bool = True) -> dict:
    """Create a calendar event."""
    if dry_run:
        return {"ok": True, "dry_run": True, "event_id": "EVENT-001", "title": title}
    if not is_live("google_workspace"):
        return {"ok": False, "error": "live execution requires Google Calendar credentials"}
    try:
        result = _workspace_client().create_calendar_event(title, start, end)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def ops_draft_email(recipient: str, subject: str, body: str, dry_run: bool = True) -> dict:
    """Draft a formal email."""
    if dry_run:
        return {"ok": True, "dry_run": True, "recipient": recipient, "subject": subject}
    return {"ok": False, "error": "live execution requires Gmail credentials"}


@mcp.tool()
def ops_store_note(title: str, content: str, dry_run: bool = True) -> dict:
    """Store a note."""
    if dry_run:
        return {"ok": True, "dry_run": True, "note_id": "NOTE-001", "title": title}
    return {"ok": False, "error": "live execution requires workspace credentials"}
