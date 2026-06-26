"""
Partenon Diplomat — Meeting Scheduler Tool
Creates meeting records, generates meet link placeholders, and logs the
interaction in `.relations`.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

sys.path.insert(0, str(Path(__file__).parent))
from crm import RelationsCRM, get_relations_crm


DEFAULT_DURATION_MINUTES = int(os.getenv("DEFAULT_MEETING_DURATION_MINUTES", "30"))
DEFAULT_TIMEZONE = os.getenv("DEFAULT_MEETING_TIMEZONE", "America/Mexico_City")


def _generate_meet_link(meeting_id: str) -> str:
    """Generate a placeholder video call link.

    In production this can be replaced by a Google Meet API call through the
    Google Workspace MCP.
    """
    return f"https://meet.partenon.local/{meeting_id}"


def _parse_iso_datetime(value: str) -> Optional[datetime]:
    """Parse an ISO datetime string."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                return None


def schedule_meeting(
    title: str,
    date: str,
    attendees: List[Dict[str, str]],
    duration_minutes: int = DEFAULT_DURATION_MINUTES,
    timezone: str = DEFAULT_TIMEZONE,
    description: str = "",
    entity_id: str = "",
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """
    Schedule a meeting with external stakeholders.

    Args:
        title: Meeting title.
        date: ISO datetime or date string.
        attendees: List of {"name", "email", "role"} dictionaries.
        duration_minutes: Meeting duration.
        timezone: Timezone for the meeting.
        description: Agenda or notes.
        entity_id: Optional client/vendor ID to link the meeting to.
        crm: RelationsCRM instance.

    Returns:
        Meeting record with link and logged interaction.
    """
    crm = crm or get_relations_crm()
    parsed_date = _parse_iso_datetime(date)
    if parsed_date is None:
        return {
            "success": False,
            "error": f"Invalid date format: {date}. Use ISO datetime or YYYY-MM-DD.",
        }

    if not attendees:
        return {
            "success": False,
            "error": "At least one attendee is required.",
        }

    meeting_id = str(uuid4())[:8].upper()
    end_date = parsed_date + timedelta(minutes=duration_minutes)
    meet_link = _generate_meet_link(meeting_id)

    meeting = {
        "id": f"MTG-{meeting_id}",
        "title": title,
        "date": parsed_date.isoformat(),
        "end_date": end_date.isoformat(),
        "timezone": timezone,
        "duration_minutes": duration_minutes,
        "attendees": attendees,
        "meet_link": meet_link,
        "description": description,
        "entity_id": entity_id,
        "status": "scheduled",
        "created_at": datetime.now().isoformat(),
    }

    # Log the scheduled meeting as a communication if linked to an entity
    if entity_id:
        attendee_names = ", ".join(
            [a.get("name", a.get("email", "")) for a in attendees]
        )
        summary = f"Scheduled meeting: {title}. Attendees: {attendee_names}."
        crm.add_communication(
            entity_id=entity_id,
            channel="meeting",
            subject=title,
            summary=summary,
            next_step="Send calendar invite and confirm attendance.",
            related_milestone=entity_id,
        )

    return {
        "success": True,
        "meeting": meeting,
        "message": f"Meeting scheduled: {title} on {parsed_date.isoformat()}.",
    }


def build_calendar_event(meeting: Dict[str, Any]) -> Dict[str, Any]:
    """Build a Google Calendar event payload from a meeting record."""
    return {
        "summary": meeting.get("title", "Partenon Meeting"),
        "description": meeting.get("description", ""),
        "start": {
            "dateTime": meeting.get("date", ""),
            "timeZone": meeting.get("timezone", DEFAULT_TIMEZONE),
        },
        "end": {
            "dateTime": meeting.get("end_date", ""),
            "timeZone": meeting.get("timezone", DEFAULT_TIMEZONE),
        },
        "attendees": [
            {"email": a.get("email", ""), "displayName": a.get("name", "")}
            for a in meeting.get("attendees", [])
            if a.get("email")
        ],
        "conferenceData": {
            "createRequest": {
                "requestId": meeting.get("id", str(uuid4())),
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            }
        },
    }


if __name__ == "__main__":
    result = schedule_meeting(
        title="Project Kickoff",
        date="2026-07-15T10:00:00",
        attendees=[
            {"name": "Jane Smith", "email": "jane@acme.test", "role": "client"},
        ],
        description="Review scope and next steps.",
        entity_id="CLI-001",
    )
    print(result)
