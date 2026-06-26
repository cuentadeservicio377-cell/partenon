"""
Partenon Diplomat — Relations tools package.
"""

from .crm import RelationsCRM, get_relations_crm
from .followups import (
    build_reminder_message,
    get_pending_followups,
    run_daily_followups,
    schedule_reminder,
)

__all__ = [
    "RelationsCRM",
    "get_relations_crm",
    "build_reminder_message",
    "get_pending_followups",
    "run_daily_followups",
    "schedule_reminder",
]
