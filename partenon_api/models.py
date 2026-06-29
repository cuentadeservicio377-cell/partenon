"""Pydantic models for API requests and responses."""

from typing import Literal, Optional

from pydantic import BaseModel, Field

from partenon_api.config import DEFAULT_WORKSPACE_ID
from partenon_api.utils import now_iso

Status = Literal["ideas", "backlog", "to_do", "in_progress", "review", "done"]
ProfileId = Literal[
    "partenon-scribe",
    "partenon-herald",
    "partenon-collector",
    "partenon-guardian",
    "partenon-strategist",
    "partenon-diplomat",
    "partenon-brain",
]


class MissionBase(BaseModel):
    profile: ProfileId
    title: str = Field(..., min_length=1, max_length=200)
    status: Status = "backlog"
    priority: Literal["low", "medium", "high"] = "medium"
    description: str = ""


class MissionCreate(MissionBase):
    workspace_id: Optional[str] = None


class MissionUpdate(BaseModel):
    profile: Optional[ProfileId] = None
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[Status] = None
    priority: Optional[Literal["low", "medium", "high"]] = None
    description: Optional[str] = None


class Mission(MissionBase):
    id: str
    workspace_id: str = DEFAULT_WORKSPACE_ID
    created_at: str
    updated_at: str


class CronJobBase(BaseModel):
    profile: ProfileId
    schedule: str = Field(..., min_length=1, max_length=200)
    command: str = Field(..., min_length=1, max_length=1000)
    enabled: bool = True
    note: str = ""


class CronJobCreate(CronJobBase):
    workspace_id: Optional[str] = None


class CronJobUpdate(BaseModel):
    profile: Optional[ProfileId] = None
    schedule: Optional[str] = Field(None, min_length=1, max_length=200)
    command: Optional[str] = Field(None, min_length=1, max_length=1000)
    enabled: Optional[bool] = None
    note: Optional[str] = None


class CronJob(CronJobBase):
    id: str
    workspace_id: str = DEFAULT_WORKSPACE_ID
    created_at: str = Field(default_factory=now_iso)
    updated_at: str = Field(default_factory=now_iso)


class EventCreate(BaseModel):
    type: str = Field(..., min_length=1, max_length=100)
    source: str = Field(..., min_length=1, max_length=100)
    entity_id: str = Field(..., min_length=1, max_length=200)
    entity_type: str = Field(..., min_length=1, max_length=100)
    data: dict = Field(default_factory=dict)


class Event(BaseModel):
    id: str
    type: str
    source: str
    entity_id: str
    entity_type: str
    data: dict
    timestamp: str
    processed: bool = False
    actions_executed: list = Field(default_factory=list)
    workspace_id: str = DEFAULT_WORKSPACE_ID


class HeroStatus(BaseModel):
    profile: ProfileId
    name: str
    color: str
    active_missions: int
    done_missions: int
    active_cron: int
    pending_nudges: int


class IntegrationStatus(BaseModel):
    domain: str
    connected: bool
    mode: Literal["dry_run", "live"]
    last_error: Optional[str] = None
