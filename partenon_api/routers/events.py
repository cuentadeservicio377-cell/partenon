"""Workflow event routes."""

from fastapi import APIRouter, Depends, status

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.config import get_data_dir
from partenon_api.events import get_bus
from partenon_api.models import Event, EventCreate
from partenon_api.store import JsonStore
from partenon_api.utils import filter_by_workspace
from partenon_core.tools.workflow_engine import WorkflowEngine

router = APIRouter(prefix="/events", tags=["events"])


def _event_store() -> JsonStore:
    return JsonStore(get_data_dir() / "events.json")


def _list_events(workspace_id: str) -> list:
    store = _event_store()
    data = store.read_dict()
    events = data.get("events", [])
    if not isinstance(events, list):
        return []
    return filter_by_workspace(events, workspace_id)


@router.get("")
async def list_events(
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    return {"events": [Event(**e).model_dump() for e in _list_events(ctx.workspace_id)]}


@router.post("", status_code=status.HTTP_201_CREATED)
async def emit_event(
    body: EventCreate,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    engine = WorkflowEngine(data_dir=str(get_data_dir()))
    result = engine.emit_event(
        type=body.type,
        source=body.source,
        entity_id=body.entity_id,
        entity_type=body.entity_type,
        data=body.data,
    )
    # Tag event with workspace_id after it has been persisted.
    store = _event_store()
    data = store.read_dict()
    events = data.get("events", [])
    for event in events:
        if event.get("id") == result["id"]:
            event["workspace_id"] = ctx.workspace_id
            break
    store.write_dict(data)

    result["workspace_id"] = ctx.workspace_id
    await get_bus().broadcast("event.created", Event(**result).model_dump())
    return {"event": Event(**result).model_dump()}
