"""Partenon Comms MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("partenon-comms")


@mcp.tool()
def comms_generate_copy(topic: str, channel: str = "email", dry_run: bool = True) -> dict:
    """Generate marketing copy for a channel."""
    if dry_run:
        return {"ok": True, "dry_run": True, "copy": f"Sample {channel} copy about {topic}"}
    return {"ok": False, "error": "live execution requires provider credentials"}


@mcp.tool()
def comms_plan_content_calendar(days: int = 30, dry_run: bool = True) -> dict:
    """Plan a content calendar."""
    if dry_run:
        return {"ok": True, "dry_run": True, "calendar": []}
    return {"ok": False, "error": "live execution requires provider credentials"}


@mcp.tool()
def comms_build_presentation(title: str, dry_run: bool = True) -> dict:
    """Build a presentation outline."""
    if dry_run:
        return {"ok": True, "dry_run": True, "slides": [{"title": title, "bullets": []}]}
    return {"ok": False, "error": "live execution requires provider credentials"}


if __name__ == "__main__":
    mcp.run()
