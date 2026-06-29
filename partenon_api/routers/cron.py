"""Cron job routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.events import get_bus
from partenon_api.models import CronJob, CronJobCreate, CronJobUpdate
from partenon_api.store import get_cron_store
from partenon_api.utils import now_iso

router = APIRouter(prefix="/cron", tags=["cron"])


def _serialize(items: list) -> list:
    return [CronJob(**item).model_dump() for item in items]


@router.get("")
async def list_cron_jobs(
    request: Request,
    profile: str | None = Query(None),
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_cron_store(request.app.state.memory_client)
    jobs = await store.list_cron_jobs(ctx.workspace_id, profile=profile)
    return {"cron": _serialize(jobs)}


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_cron_job(
    request: Request,
    body: CronJobCreate,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_cron_store(request.app.state.memory_client)
    job = body.model_dump()
    job["workspace_id"] = ctx.workspace_id
    job["created_at"] = now_iso()
    job["updated_at"] = now_iso()
    job = await store.create_cron_job(ctx.workspace_id, job)
    await get_bus().broadcast("cron.created", CronJob(**job).model_dump())
    return {"cron": CronJob(**job).model_dump()}


@router.patch("/{job_id}")
async def update_cron_job(
    request: Request,
    job_id: str,
    body: CronJobUpdate,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_cron_store(request.app.state.memory_client)
    patch = body.model_dump(exclude_unset=True)
    patch["updated_at"] = now_iso()
    updated = await store.update_cron_job(ctx.workspace_id, job_id, patch)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cron job not found")
    await get_bus().broadcast("cron.updated", CronJob(**updated).model_dump())
    return {"cron": CronJob(**updated).model_dump()}


@router.delete("/{job_id}")
async def delete_cron_job(
    request: Request,
    job_id: str,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_cron_store(request.app.state.memory_client)
    deleted = await store.delete_cron_job(ctx.workspace_id, job_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cron job not found")
    await get_bus().broadcast("cron.deleted", {"id": job_id})
    return {"deleted": True}
