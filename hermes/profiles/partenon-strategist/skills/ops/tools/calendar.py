"""
Partenon Strategist — Calendar Tool
Manages calendar events, meetings, and reminders.
Integrates with Google Calendar MCP when credentials are available;
otherwise stores events locally for review.
"""

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


def _resolve_data_dir() -> Path:
    """Resolve data directory relative to partenon-core."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "partenon-core":
            data_dir = parent / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            return data_dir
        candidate = parent / "partenon-core" / "data"
        if candidate.exists() and candidate.is_dir():
            return candidate
    for parent in current.parents:
        if (parent / "partenon-core").exists():
            data_dir = parent / "partenon-core" / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            return data_dir
    local = Path(__file__).resolve().parent / "data"
    local.mkdir(parents=True, exist_ok=True)
    return local


def _parse_datetime(value: str) -> datetime:
    """Parse an ISO datetime string, falling back to now on error."""
    if not value:
        return datetime.now()
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return datetime.now()


class Calendar:
    """Calendar management tool for events, meetings, and reminders."""

    def __init__(self):
        self.data_dir = _resolve_data_dir()
        self.calendar_file = self.data_dir / "calendar.json"
        self._calendar = None

    def _load(self) -> Dict[str, Any]:
        """Load calendar data from JSON."""
        if self._calendar is not None:
            return self._calendar

        if self.calendar_file.exists():
            try:
                with open(self.calendar_file, "r", encoding="utf-8") as f:
                    self._calendar = json.load(f)
                    return self._calendar
            except Exception:
                pass

        self._calendar = {"events": [], "reminders": []}
        return self._calendar

    def _save(self):
        """Save calendar data to JSON."""
        with open(self.calendar_file, "w", encoding="utf-8") as f:
            json.dump(self._calendar, f, ensure_ascii=False, indent=2)

    def create_event(
        self,
        summary: str,
        start_time: str,
        end_time: str,
        attendees: List[str] = None,
        description: str = "",
        location: str = "",
        reminder_minutes: int = 15,
    ) -> Dict[str, Any]:
        """Create a calendar event."""
        self._load()

        event = {
            "id": f"EVT-{uuid.uuid4().hex[:8].upper()}",
            "summary": summary,
            "start_time": _parse_datetime(start_time).isoformat(),
            "end_time": _parse_datetime(end_time).isoformat(),
            "attendees": attendees or [],
            "description": description,
            "location": location,
            "reminder_minutes": reminder_minutes,
            "created_at": datetime.now().isoformat(),
            "source": "calendar_tool",
        }

        self._calendar["events"].append(event)
        self._save()

        return {
            "success": True,
            "event": event,
            "message": f"Event created: {summary} ({event['id']})",
        }

    def list_events(
        self, start_date: str = None, end_date: str = None
    ) -> List[Dict[str, Any]]:
        """List events in a date range."""
        self._load()

        start_dt = _parse_datetime(start_date) if start_date else datetime.now()
        end_dt = _parse_datetime(end_date) if end_date else start_dt + timedelta(days=7)

        events = []
        for event in self._calendar.get("events", []):
            event_start = _parse_datetime(event.get("start_time", ""))
            if start_dt <= event_start <= end_dt:
                events.append(event)

        events.sort(key=lambda e: e.get("start_time", ""))
        return events

    def schedule_meeting(
        self,
        title: str,
        date: str,
        attendees: List[str] = None,
        duration_minutes: int = 30,
        description: str = "",
    ) -> Dict[str, Any]:
        """Schedule a meeting with a default duration."""
        start_dt = _parse_datetime(date)
        end_dt = start_dt + timedelta(minutes=duration_minutes)

        return self.create_event(
            summary=title,
            start_time=start_dt.isoformat(),
            end_time=end_dt.isoformat(),
            attendees=attendees or [],
            description=description,
            reminder_minutes=60,
        )

    def send_reminder(
        self, subject: str, message: str, recipient: str, send_at: str = None
    ) -> Dict[str, Any]:
        """Store a reminder to be sent via Gmail MCP when integrated."""
        self._load()

        reminder = {
            "id": f"RMD-{uuid.uuid4().hex[:8].upper()}",
            "subject": subject,
            "message": message,
            "recipient": recipient,
            "send_at": send_at or datetime.now().isoformat(),
            "created_at": datetime.now().isoformat(),
            "sent": False,
        }

        self._calendar.setdefault("reminders", []).append(reminder)
        self._save()

        return {
            "success": True,
            "reminder": reminder,
            "message": f"Reminder queued for {recipient}: {subject}",
        }

    def format_events(self, events: List[Dict[str, Any]], title: str = "Events") -> str:
        """Format events for display."""
        if not events:
            return f"No {title.lower()}."

        lines = [f"{title} ({len(events)})", ""]
        for event in events:
            start = _parse_datetime(event.get("start_time", ""))
            lines.append(f"• {event.get('summary')} — {start.strftime('%Y-%m-%d %H:%M')}")
            if event.get("location"):
                lines.append(f"   Location: {event['location']}")
            if event.get("attendees"):
                lines.append(f"   Attendees: {', '.join(event['attendees'])}")

        return "\n".join(lines)


# Singleton
_calendar_instance = None


def get_calendar() -> Calendar:
    """Get or create singleton Calendar instance."""
    global _calendar_instance
    if _calendar_instance is None:
        _calendar_instance = Calendar()
    return _calendar_instance
