"""
G-Brain MCP server for Partenon.
Exposes shared memory: profiles, missions and entities.
"""

import json
import os
from typing import Any, Dict, Optional

from mcp.server.fastmcp import FastMCP

from .tools import GBrainStore


mcp = FastMCP("gbrain")
store: Optional[GBrainStore] = None


def get_store() -> GBrainStore:
    global store
    if store is None:
        store = GBrainStore(os.getenv("GBrain_DATABASE_URL"))
    return store


@mcp.tool()
def gbrain_read_profile(profile: str, scope: str = "default") -> str:
    """Read a profile scope from G-Brain."""
    data = get_store().read_profile(profile, scope)
    return json.dumps(data, ensure_ascii=False)


@mcp.tool()
def gbrain_write_profile(profile: str, scope: str, content: str) -> str:
    """Write a profile scope to G-Brain. Content must be a JSON string."""
    parsed = json.loads(content)
    return get_store().write_profile(profile, scope, parsed)


@mcp.tool()
def gbrain_write_mission(
    mission_id: str,
    profile: str,
    title: str,
    status: str,
    input_data: Optional[str] = None,
    output_data: Optional[str] = None,
    learnings: Optional[str] = None,
) -> str:
    """Register or update a mission. input_data and output_data are JSON strings."""
    return get_store().write_mission(
        mission_id=mission_id,
        profile=profile,
        title=title,
        status=status,
        input_data=json.loads(input_data) if input_data else None,
        output_data=json.loads(output_data) if output_data else None,
        learnings=learnings,
    )


@mcp.tool()
def gbrain_search_missions(profile: Optional[str] = None, status: Optional[str] = None) -> str:
    """Search missions by profile and/or status."""
    rows = get_store().search_missions(profile, status)
    return json.dumps(rows, ensure_ascii=False)


@mcp.tool()
def gbrain_search_entities(query: str, kind: Optional[str] = None) -> str:
    """Search entities by name and optional kind (client, vendor, product)."""
    rows = get_store().search_entities(query, kind)
    return json.dumps(rows, ensure_ascii=False)


@mcp.tool()
def gbrain_store_learning(profile: str, insight: str) -> str:
    """Store a learning insight for a profile."""
    return get_store().store_learning(profile, insight)


if __name__ == "__main__":
    mcp.run()
