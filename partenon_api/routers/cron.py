"""Cron job routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.events import get_bus
from partenon_api.models import CronJob, CronJobCreate, CronJobUpdate
from partenon_api.store import get_cron_store
from partenon_api.utils import filter_by_workspace, new_id, now_iso

router = APIRouter(prefix="/cron", tags=["cron"])


def _serialize(items: list) -> list:
    return [CronJob(**item).model_dump() for item in items]


@router.get("")
async def list_cron_jobs(
    profile: str | None = Query(None),
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_cron_store()
    jobs = filter_by_workspace(store.read_list(), ctx.workspace_id)
    if profile:
        jobs = [j for j in jobs if j.get("profile") == profile]
    return {"cron": _serialize(jobs)}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_cron_job(
    body: CronJobCreate,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_cron_store()
    job = body.model_dump()
    job["id"] = new_id("cron")
    job["workspace_id"] = ctx.workspace_id
    job["created_at"] = now_iso()
    job["updated_at"] = now_iso()
    items = store.read_list()
    items.append(job)
    store.write_list(items)
    await get_bus().broadcast("cron.created", CronJob(**job).model_dump())
    return {"cron": CronJob(**job).model_dump()}


@router.patch("/{job_id}")
async def update_cron_job(
    job_id: str,
    body: CronJobUpdate,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_cron_store()
    jobs = filter_by_workspace(store.read_list(), ctx.workspace_id)
    for i, item in enumerate(jobs):
        if item["id"] == job_id:
            patch = body.model_dump(exclude_unset=True)
            patch["updated_at"] = now_iso()
            jobs[i] = {**item, **patch}
            all_items = store.read_list()
            for j, raw in enumerate(all_items):
                if raw.get("id") == job_id:
                    all_items[j] = jobs[i]
                    break
            store.write_list(all_items)
            await get_bus().broadcast("cron.updated", CronJob(**jobs[i]).model_dump())
            return {"cron": CronJob(**jobs[i]).model_dump()}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cron job not found")


@router.delete("/{job_id}")
async def delete_cron_job(
    job_id: str,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_cron_store()
    jobs = filter_by_workspace(store.read_list(), ctx.workspace_id)
    if not any(j["id"] == job_id for j in jobs):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cron job not found")
    store.delete_from_list(job_id)
    await get_bus().broadcast("cron.deleted", {"id": job_id})
    return {"deleted": True}
