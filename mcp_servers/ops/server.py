"""Partenon Ops MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("partenon-ops")


@mcp.tool()
def ops_create_project(name: str, client: str, dry_run: bool = True) -> dict:
    """Create a project."""
    if dry_run:
        return {"ok": True, "dry_run": True, "project_id": "PROJ-001", "name": name, "client": client}
    return {"ok": False, "error": "live execution requires workspace credentials"}


@mcp.tool()
def ops_create_task(project_id: str, title: str, dry_run: bool = True) -> dict:
    """Create a task inside a project."""
    if dry_run:
        return {"ok": True, "dry_run": True, "task_id": "TASK-001", "project_id": project_id, "title": title}
    return {"ok": False, "error": "live execution requires workspace credentials"}


@mcp.tool()
def ops_generate_briefing(profile: str, dry_run: bool = True) -> dict:
    """Generate a daily briefing for a profile."""
    if dry_run:
        return {"ok": True, "dry_run": True, "profile": profile, "briefing": []}
    return {"ok": False, "error": "live execution requires workspace credentials"}


if __name__ == "__main__":
    mcp.run()
