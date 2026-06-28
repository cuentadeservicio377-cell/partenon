"""
Partenon Diplomat — Log Interaction Tool
Convenience wrapper to record communications with clients and vendors.
"""

import sys
from pathlib import Path
from typing import Any, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent))
from crm import RelationsCRM, get_relations_crm


def log_interaction(
    entity_id: str,
    channel: str,
    subject: str,
    summary: str,
    next_step: str = "",
    related_milestone: str = "",
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """
    Log a communication or interaction with a client or vendor.

    Args:
        entity_id: Client or vendor ID.
        channel: Communication channel (email, call, meeting, etc.).
        subject: Short subject line.
        summary: Summary of what was discussed.
        next_step: Agreed next action.
        related_milestone: Optional milestone ID.
        crm: RelationsCRM instance.

    Returns:
        Result from RelationsCRM.add_communication.
    """
    crm = crm or get_relations_crm()
    return crm.add_communication(
        entity_id=entity_id,
        channel=channel,
        subject=subject,
        summary=summary,
        next_step=next_step,
        related_milestone=related_milestone,
    )


def log_call(
    entity_id: str,
    subject: str,
    summary: str,
    next_step: str = "",
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """Log a phone call."""
    return log_interaction(
        entity_id=entity_id,
        channel="call",
        subject=subject,
        summary=summary,
        next_step=next_step,
        crm=crm,
    )


def log_email(
    entity_id: str,
    subject: str,
    summary: str,
    next_step: str = "",
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """Log an email exchange."""
    return log_interaction(
        entity_id=entity_id,
        channel="email",
        subject=subject,
        summary=summary,
        next_step=next_step,
        crm=crm,
    )


if __name__ == "__main__":
    print(
        log_interaction(
            entity_id="CLI-001",
            channel="email",
            subject="Proposal follow-up",
            summary="Client asked for a revised timeline. New draft to be sent by Friday.",
            next_step="Send revised proposal and confirm receipt.",
        )
    )
