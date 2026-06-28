"""Partenon Google Workspace MCP server.

Exposes Sheets, Docs, Slides, Calendar and Gmail tools to Partenon heroes.
Dry-run by default; live calls only when Google credentials are configured.
"""

import json

from mcp.server.fastmcp import FastMCP

from mcp_servers._shared.live_mode import is_live
from mcp_servers.google_workspace.client import GoogleWorkspaceClient

mcp = FastMCP("partenon-google-workspace")


def _client() -> GoogleWorkspaceClient:
    return GoogleWorkspaceClient()


def _dry_response(tool: str) -> dict:
    return {"ok": True, "dry_run": True, "tool": tool}


@mcp.tool()
def workspace_create_spreadsheet(title: str) -> dict:
    """Create a Google Sheets spreadsheet."""
    if not is_live("google_workspace"):
        return {**_dry_response("workspace_create_spreadsheet"), "spreadsheet_id": "sheet_123", "title": title}
    try:
        result = _client().create_spreadsheet(title)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def workspace_write_to_sheets(spreadsheet_id: str, range_name: str, values_json: str) -> dict:
    """Write values to a Google Sheet. values_json is a JSON string of a 2D list."""
    values = json.loads(values_json)
    if not is_live("google_workspace"):
        return {**_dry_response("workspace_write_to_sheets"), "updated_cells": sum(len(row) for row in values)}
    try:
        result = _client().write_to_sheets(spreadsheet_id, range_name, values)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def workspace_read_sheet(spreadsheet_id: str, range_name: str) -> dict:
    """Read values from a Google Sheet."""
    if not is_live("google_workspace"):
        return {**_dry_response("workspace_read_sheet"), "values": []}
    try:
        result = _client().read_sheet(spreadsheet_id, range_name)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def workspace_create_document(title: str, content: str = "") -> dict:
    """Create a Google Doc with optional content."""
    if not is_live("google_workspace"):
        return {**_dry_response("workspace_create_document"), "document_id": "doc_123", "title": title}
    try:
        result = _client().create_document(title, content or None)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def workspace_create_presentation(title: str) -> dict:
    """Create a Google Slides presentation."""
    if not is_live("google_workspace"):
        return {**_dry_response("workspace_create_presentation"), "presentation_id": "slides_123", "title": title}
    try:
        result = _client().create_presentation(title)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def workspace_create_calendar_event(
    summary: str, start: str, end: str, attendees_json: str = "[]", description: str = ""
) -> dict:
    """Create a Google Calendar event."""
    attendees = json.loads(attendees_json)
    if not is_live("google_workspace"):
        return {**_dry_response("workspace_create_calendar_event"), "event_id": "evt_123", "html_link": ""}
    try:
        result = _client().create_calendar_event(summary, start, end, attendees, description)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def workspace_send_email(to: str, subject: str, body: str) -> dict:
    """Send an email via Gmail."""
    if not is_live("google_workspace"):
        return {**_dry_response("workspace_send_email"), "message_id": "msg_123"}
    try:
        result = _client().send_email(to, subject, body)
        return {"ok": True, "dry_run": False, **result}
    except Exception as e:
        return {"ok": False, "error": str(e)}


if __name__ == "__main__":
    mcp.run()
