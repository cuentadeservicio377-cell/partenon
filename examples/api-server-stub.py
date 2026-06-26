#!/usr/bin/env python3
"""
REST API server stub — Partenon web promise placeholder.

This FastAPI application implements the REST endpoints documented on
`web/developers.html`:

  GET    /api/v1/heroes
  GET    /api/v1/heroes/:id
  POST   /api/v1/missions
  GET    /api/v1/missions/:id
  GET    /api/v1/mcp/tools
  POST   /api/v1/mcp/call

It is NOT a production API; it returns the documented JSON shapes so front-end
and integration work can proceed while real backends are built.

Usage:
  pip install fastapi uvicorn
  uvicorn examples.api-server-stub:app --reload --port 8000
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Partenon API Stub", version="0.1.0")

HEROES = [
    {"id": "scribe", "name": "The Scribe", "role": "Financial Architect", "status": "active"},
    {"id": "herald", "name": "The Herald", "role": "Voice of the Brand", "status": "active"},
    {"id": "collector", "name": "The Collector", "role": "Payment Guardian", "status": "active"},
    {"id": "guardian", "name": "The Guardian", "role": "Sentinel of Systems", "status": "active"},
    {"id": "strategist", "name": "The Strategist", "role": "Master of Operations", "status": "active"},
    {"id": "diplomat", "name": "The Diplomat", "role": "Bridge Between Worlds", "status": "active"},
    {"id": "brain", "name": "The Brain", "role": "Central Intelligence", "status": "active"},
]

MCP_TOOLS = [
    {"name": "create_spreadsheet", "server": "google_workspace", "description": "Create a Google Sheet"},
    {"name": "append_rows", "server": "google_workspace", "description": "Append rows to a sheet"},
    {"name": "create_payment_link", "server": "stripe", "description": "Create a Stripe payment link"},
    {"name": "create_invoice", "server": "stripe", "description": "Create a Stripe invoice"},
    {"name": "manage_secrets", "server": "security", "description": "Manage API keys"},
    {"name": "schedule_meeting", "server": "calendar", "description": "Schedule a calendar event"},
    {"name": "share_context", "server": "gbrain", "description": "Share context via MCP"},
]

MISSIONS: Dict[str, Dict[str, Any]] = {}


class MissionCreate(BaseModel):
    hero: str
    type: str
    input_data: Optional[Dict[str, Any]] = None


class MCPToolCall(BaseModel):
    name: str
    arguments: Dict[str, Any]


def _now():
    return datetime.now(timezone.utc).isoformat()


@app.get("/api/v1/heroes")
def list_heroes() -> List[Dict[str, Any]]:
    return HEROES


@app.get("/api/v1/heroes/{hero_id}")
def get_hero(hero_id: str) -> Dict[str, Any]:
    for hero in HEROES:
        if hero["id"] == hero_id:
            return hero
    raise HTTPException(status_code=404, detail="Hero not found")


@app.post("/api/v1/missions")
def create_mission(payload: MissionCreate) -> Dict[str, Any]:
    if payload.hero not in {h["id"] for h in HEROES}:
        raise HTTPException(status_code=400, detail="Unknown hero")
    mission_id = str(uuid.uuid4())
    mission = {
        "id": mission_id,
        "hero": payload.hero,
        "type": payload.type,
        "status": "completed",
        "created_at": _now(),
        "output": {"message": f"Stub mission completed for {payload.hero}/{payload.type}"},
    }
    MISSIONS[mission_id] = mission
    return mission


@app.get("/api/v1/missions/{mission_id}")
def get_mission(mission_id: str) -> Dict[str, Any]:
    if mission_id not in MISSIONS:
        raise HTTPException(status_code=404, detail="Mission not found")
    return MISSIONS[mission_id]


@app.get("/api/v1/mcp/tools")
def list_mcp_tools() -> List[Dict[str, Any]]:
    return MCP_TOOLS


@app.post("/api/v1/mcp/call")
def call_mcp_tool(payload: MCPToolCall) -> Dict[str, Any]:
    tool_names = {t["name"] for t in MCP_TOOLS}
    if payload.name not in tool_names:
        raise HTTPException(status_code=400, detail="Unknown MCP tool")
    return {
        "tool": payload.name,
        "arguments": payload.arguments,
        "result": {"status": "stub_success", "message": "Tool call executed in stub mode"},
    }


@app.get("/api/v1/status")
def system_status() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "version": "0.1.0-stub",
        "heroes": {h["id"]: {"status": h["status"], "lastMission": _now()} for h in HEROES},
        "mcp": {
            "connectedAgents": len(HEROES),
            "contextObjects": len(MISSIONS),
            "lastInsight": _now(),
        },
        "integrations": {
            "google_workspace": "connected",
            "stripe": "connected",
            "nvidia": "connected",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
