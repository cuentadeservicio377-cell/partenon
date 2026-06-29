"""Gateway smoke-test routes for Phase 5.

These endpoints are testing-only wrappers around the Hermes gateway skill
tools. They let the dashboard and CI exercise command parsing, attachment
routing, and guard checks without a live Telegram bot.
"""

import importlib.util
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from partenon_api.auth import WorkspaceContext, get_current_workspace

router = APIRouter(prefix="/gateway", tags=["gateway"])


def _load_tool(name: str):
    """Load a gateway skill tool module by file path.

    The skill lives under the Hermes profile tree, which uses hyphens in
    directory names that are not valid Python package identifiers. We load
    the module directly from disk so the API can call it without renaming
    the Hermes profile directories.
    """
    repo_root = Path(__file__).resolve().parents[2]
    tool_path = (
        repo_root
        / "hermes"
        / "profiles"
        / "partenon-scribe"
        / "skills"
        / "gateway"
        / "tools"
        / f"{name}.py"
    )
    spec = importlib.util.spec_from_file_location(f"gateway_tool_{name}", tool_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_parse_command = _load_tool("parse_command").parse_command
_route_attachment = _load_tool("route_attachment").route_attachment
_check_guard = _load_tool("check_guard").check_guard


class DryRunRequest(BaseModel):
    message: str = ""
    user_id: str = ""
    chat_id: str = ""
    is_group: bool = False
    bot_username: str = ""
    file_name: Optional[str] = None
    mime_type: Optional[str] = None


class DryRunResponse(BaseModel):
    command: Dict[str, Any]
    guard: Dict[str, Any]
    attachment: Optional[Dict[str, Any]] = None


@router.post("/dry_run", response_model=DryRunResponse)
async def gateway_dry_run(
    body: DryRunRequest,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> Dict[str, Any]:
    """Run command parsing, guard checks, and attachment routing in one call."""
    command = _parse_command(body.message)
    guard = _check_guard(
        user_id=body.user_id or ctx.username,
        message=body.message,
        is_group=body.is_group,
        bot_username=body.bot_username,
    )
    attachment = None
    if body.file_name and body.mime_type:
        attachment = _route_attachment(body.file_name, body.mime_type, context=body.message)

    return {"command": command, "guard": guard, "attachment": attachment}
