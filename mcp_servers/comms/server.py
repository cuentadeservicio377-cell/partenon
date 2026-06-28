"""Partenon Comms MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

from mcp_servers._shared.live_mode import is_live
from mcp_servers.google_workspace.client import GoogleWorkspaceClient

mcp = FastMCP("partenon-comms")


def _workspace_client() -> GoogleWorkspaceClient:
    return GoogleWorkspaceClient()


@mcp.tool()
def comms_brand_intake(answers: str, dry_run: bool = True) -> dict:
    """Run a brand interview and generate/update .design. Answers must be a JSON string."""
    if dry_run:
        return {"ok": True, "dry_run": True, "design_updated": True}
    return {"ok": False, "error": "live execution requires file system access"}


@mcp.tool()
def comms_plan_content_calendar(topic: str, days: int = 30, dry_run: bool = True) -> dict:
    """Plan a content calendar. In live mode, stores the plan in a Google Doc."""
    if dry_run:
        return {"ok": True, "dry_run": True, "calendar": []}
    if not is_live("google_workspace"):
        return {"ok": False, "error": "live execution requires Google Workspace credentials"}
    try:
        result = _workspace_client().create_document(f"Content Calendar: {topic}", f"Calendar for {topic} ({days} days)")
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def comms_generate_copy(topic: str, channel: str = "email", dry_run: bool = True) -> dict:
    """Generate marketing copy for a channel."""
    if dry_run:
        return {"ok": True, "dry_run": True, "copy": f"Sample {channel} copy about {topic}"}
    return {"ok": False, "error": "live execution requires provider credentials"}


@mcp.tool()
def comms_seo_geo_optimize(text: str, keywords: str, dry_run: bool = True) -> dict:
    """Optimize text for SEO/GEO. Keywords is a comma-separated string."""
    if dry_run:
        return {"ok": True, "dry_run": True, "optimized": text}
    return {"ok": False, "error": "live execution requires provider credentials"}


@mcp.tool()
def comms_publish_post(channel: str, content: str, dry_run: bool = True) -> dict:
    """Publish a post to a social channel."""
    if dry_run:
        return {"ok": True, "dry_run": True, "channel": channel, "published": False}
    return {"ok": False, "error": "live execution requires social API credentials"}


@mcp.tool()
def comms_schedule_content(channel: str, content: str, publish_at: str, dry_run: bool = True) -> dict:
    """Schedule content for later publication."""
    if dry_run:
        return {"ok": True, "dry_run": True, "scheduled": True}
    return {"ok": False, "error": "live execution requires social API credentials"}


@mcp.tool()
def comms_analyze_engagement(channel: str, dry_run: bool = True) -> dict:
    """Analyze engagement for a channel."""
    if dry_run:
        return {"ok": True, "dry_run": True, "channel": channel, "metrics": {}}
    return {"ok": False, "error": "live execution requires social API credentials"}


@mcp.tool()
def comms_build_presentation(title: str, dry_run: bool = True) -> dict:
    """Build a presentation. In live mode, creates a Google Slides deck."""
    if dry_run:
        return {"ok": True, "dry_run": True, "slides": [{"title": title, "bullets": []}]}
    if not is_live("google_workspace"):
        return {"ok": False, "error": "live execution requires Google Workspace credentials"}
    try:
        result = _workspace_client().create_presentation(title)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def comms_draft_email(subject: str, body: str, dry_run: bool = True) -> dict:
    """Draft a formal email."""
    if dry_run:
        return {"ok": True, "dry_run": True, "subject": subject, "body": body}
    return {"ok": False, "error": "live execution requires Gmail credentials"}
