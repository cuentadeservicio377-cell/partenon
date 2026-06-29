"""Mission routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.events import get_bus
from partenon_api.models import Mission, MissionCreate, MissionUpdate
from partenon_api.store import get_mission_store
from partenon_api.utils import now_iso

router = APIRouter(prefix="/missions", tags=["missions"])


def _serialize(items: list) -> list:
    return [Mission(**item).model_dump() for item in items]


@router.get("")
async def list_missions(
    request: Request,
    profile: str | None = Query(None),
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_mission_store(request.app.state.memory_client)
    missions = await store.list_missions(ctx.workspace_id, profile=profile)
    return {"missions": _serialize(missions)}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_mission(
    request: Request,
    body: MissionCreate,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_mission_store(request.app.state.memory_client)
    mission = body.model_dump()
    mission["workspace_id"] = ctx.workspace_id
    mission["created_at"] = now_iso()
    mission["updated_at"] = now_iso()
    mission = await store.create_mission(ctx.workspace_id, mission)
    await get_bus().broadcast("mission.created", Mission(**mission).model_dump())
    return {"mission": Mission(**mission).model_dump()}


@router.patch("/{mission_id}")
async def update_mission(
    request: Request,
    mission_id: str,
    body: MissionUpdate,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_mission_store(request.app.state.memory_client)
    patch = body.model_dump(exclude_unset=True)
    patch["updated_at"] = now_iso()
    updated = await store.update_mission(ctx.workspace_id, mission_id, patch)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    await get_bus().broadcast("mission.updated", Mission(**updated).model_dump())
    return {"mission": Mission(**updated).model_dump()}


@router.delete("/{mission_id}")
async def delete_mission(
    request: Request,
    mission_id: str,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_mission_store(request.app.state.memory_client)
    deleted = await store.delete_mission(ctx.workspace_id, mission_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    await get_bus().broadcast("mission.deleted", {"id": mission_id})
    return {"deleted": True}
