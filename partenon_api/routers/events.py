"""Workflow event routes."""

from fastapi import APIRouter, Depends, Request, status

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.config import get_data_dir
from partenon_api.events import get_bus
from partenon_api.models import Event, EventCreate
from partenon_api.store import get_event_store
from partenon_core.tools.workflow_engine import WorkflowEngine

router = APIRouter(prefix="/events", tags=["events"])


@router.get("")
async def list_events(
    request: Request,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_event_store(request.app.state.memory_client)
    events = await store.list_events(ctx.workspace_id)
    return {"events": [Event(**e).model_dump() for e in events]}


@router.post("", status_code=status.HTTP_201_CREATED)
async def emit_event(
    request: Request,
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
    store = get_event_store(request.app.state.memory_client)
    result["workspace_id"] = ctx.workspace_id
    event = await store.upsert_event(result)
    await get_bus().broadcast("event.created", Event(**event).model_dump())
    return {"event": Event(**event).model_dump()}
