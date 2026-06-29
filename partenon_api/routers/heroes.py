"""Hero aggregate status routes."""

from fastapi import APIRouter, Depends, Request

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.constants import PROFILES
from partenon_api.models import HeroStatus
from partenon_api.store import get_store

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.get("")
async def list_heroes(
    request: Request,
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    store = get_store(request.app.state.memory_client)
    missions = await store.list_missions(ctx.workspace_id)
    cron_jobs = await store.list_cron_jobs(ctx.workspace_id)
    nudges = await store.list_nudges(ctx.workspace_id)

    heroes = []
    for profile in PROFILES:
        pid = profile["id"]
        profile_missions = [m for m in missions if m.get("profile") == pid]
        profile_cron = [c for c in cron_jobs if c.get("profile") == pid]
        profile_nudges = [n for n in nudges if n.get("target_profile") in (pid, "all")]
        heroes.append(
            HeroStatus(
                profile=pid,  # type: ignore[arg-type]
                name=profile["name"],
                color=profile["color"],
                active_missions=len([m for m in profile_missions if m.get("status") != "done"]),
                done_missions=len([m for m in profile_missions if m.get("status") == "done"]),
                active_cron=len([c for c in profile_cron if c.get("enabled")]),
                pending_nudges=len(profile_nudges),
            ).model_dump()
        )

    return {"heroes": heroes}
