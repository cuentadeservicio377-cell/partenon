"""Mission routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.events import get_bus
from partenon_api.models import Mission, MissionCreate, MissionUpdate
from partenon_api.store import get_mission_store
from partenon_api.utils import filter_by_workspace, new_id, now_iso

router = APIRouter(prefix="/missions", tags=["missions"])


def _serialize(items: list) -> list:
    return [Mission(**item).model_dump() for item in items]


@router.get("")
async def list_missions(
    profile: str | None = Query(None),
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_mission_store()
    missions = filter_by_workspace(store.read_list(), ctx.workspace_id)
    if profile:
        missions = [m for m in missions if m.get("profile") == profile]
    return {"missions": _serialize(missions)}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_mission(
    body: MissionCreate,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_mission_store()
    mission = body.model_dump()
    mission["id"] = new_id("mission")
    mission["workspace_id"] = ctx.workspace_id
    mission["created_at"] = now_iso()
    mission["updated_at"] = now_iso()
    items = store.read_list()
    items.append(mission)
    store.write_list(items)
    await get_bus().broadcast("mission.created", Mission(**mission).model_dump())
    return {"mission": Mission(**mission).model_dump()}


@router.patch("/{mission_id}")
async def update_mission(
    mission_id: str,
    body: MissionUpdate,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_mission_store()
    missions = filter_by_workspace(store.read_list(), ctx.workspace_id)
    for i, item in enumerate(missions):
        if item["id"] == mission_id:
            patch = body.model_dump(exclude_unset=True)
            patch["updated_at"] = now_iso()
            missions[i] = {**item, **patch}
            all_items = store.read_list()
            for j, raw in enumerate(all_items):
                if raw.get("id") == mission_id:
                    all_items[j] = missions[i]
                    break
            store.write_list(all_items)
            await get_bus().broadcast("mission.updated", Mission(**missions[i]).model_dump())
            return {"mission": Mission(**missions[i]).model_dump()}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")


@router.delete("/{mission_id}")
async def delete_mission(
    mission_id: str,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_mission_store()
    missions = filter_by_workspace(store.read_list(), ctx.workspace_id)
    if not any(m["id"] == mission_id for m in missions):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mission not found")
    store.delete_from_list(mission_id)
    await get_bus().broadcast("mission.deleted", {"id": mission_id})
    return {"deleted": True}
