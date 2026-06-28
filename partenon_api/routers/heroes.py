"""Hero aggregate status routes."""

from fastapi import APIRouter, Depends

from partenon_api.auth import WorkspaceContext, get_current_workspace
from partenon_api.constants import PROFILES
from partenon_api.models import HeroStatus
from partenon_api.store import get_cron_store, get_mission_store, get_nudge_store
from partenon_api.utils import filter_by_workspace

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.get("")
async def list_heroes(
    ctx: WorkspaceContext = Depends(get_current_workspace),
) -> dict:
    missions = filter_by_workspace(get_mission_store().read_list(), ctx.workspace_id)
    cron_jobs = filter_by_workspace(get_cron_store().read_list(), ctx.workspace_id)
    nudges = filter_by_workspace(get_nudge_store().read_list(), ctx.workspace_id)

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
