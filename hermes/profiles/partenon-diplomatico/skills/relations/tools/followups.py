"""
Partenon Diplomat — Follow-ups Tool
Generates reminders and daily follow-up reports for clients and vendors.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Allow importing crm.py from the same directory
sys.path.insert(0, str(Path(__file__).parent))

from crm import RelationsCRM, get_relations_crm


# Default follow-up windows in days
DEFAULT_FOLLOW_UP_WINDOWS = [1, 3, 7]


def _parse_date(value: str) -> Optional[datetime]:
    """Parse an ISO date string into a datetime object."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return None


def _format_date(value: str) -> str:
    """Return a human-readable date string."""
    parsed = _parse_date(value)
    if parsed is None:
        return value
    return parsed.strftime("%Y-%m-%d")


def _today() -> datetime:
    """Return current datetime; overridable via PARTENON_TODAY for tests."""
    env_today = os.getenv("PARTENON_TODAY")
    if env_today:
        parsed = _parse_date(env_today)
        if parsed:
            return parsed
    return datetime.now()


def get_pending_followups(
    crm: Optional[RelationsCRM] = None,
    alert_days: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """
    Return pending reminders and milestones that need attention.

    Logic:
    - Reminders with date <= today and status 'pending'.
    - Milestones with date <= today and status not in closed/cancelled.
    - Urgency grows as the date passes.
    """
    crm = crm or get_relations_crm()
    data = crm._load()
    today = _today()
    windows = sorted(alert_days or DEFAULT_FOLLOW_UP_WINDOWS)
    followups: List[Dict[str, Any]] = []

    # Check explicit reminders
    for reminder in data.get("reminders", []):
        if reminder.get("status") != "pending":
            continue

        date = _parse_date(reminder.get("date", ""))
        if date is None:
            continue

        days_diff = (today - date).days
        if days_diff < 0:
            continue

        urgency = "low"
        for threshold in windows:
            if days_diff >= threshold:
                urgency = "high" if threshold == windows[-1] else "medium"

        entity = crm._find_entity(data, reminder.get("entity_id", ""))
        followups.append({
            "type": "reminder",
            "id": reminder["id"],
            "entity": entity["name"] if entity else reminder.get("entity_id", ""),
            "entity_id": reminder.get("entity_id", ""),
            "message": reminder.get("message", ""),
            "channel": reminder.get("channel", "email"),
            "target_date": reminder.get("date", ""),
            "days_overdue": days_diff,
            "urgency": urgency,
            "recommended_action": _recommend_action(reminder.get("message", ""), entity, days_diff),
        })

    # Check milestones without written confirmation or past due
    for section in ["clients", "vendors"]:
        for entity in data.get(section, []):
            entity_id = entity.get("id", "")
            for milestone in entity.get("milestones", []):
                status = milestone.get("status", "")
                if status in {"completed", "closed", "cancelled"}:
                    continue

                date = _parse_date(milestone.get("date", ""))
                if date is None:
                    continue

                days_diff = (today - date).days
                if days_diff < -windows[-1]:
                    continue

                urgency = "low"
                if not milestone.get("confirmed_in_writing", False):
                    urgency = "medium"
                for threshold in windows:
                    if days_diff >= threshold:
                        urgency = "high" if threshold == windows[-1] else "medium"

                followups.append({
                    "type": "milestone",
                    "id": milestone["id"],
                    "entity": entity.get("name", ""),
                    "entity_id": entity_id,
                    "message": milestone.get("description", ""),
                    "target_date": milestone.get("date", ""),
                    "milestone_status": status,
                    "confirmed_in_writing": milestone.get("confirmed_in_writing", False),
                    "days_overdue": max(0, days_diff),
                    "urgency": urgency,
                    "recommended_action": _recommend_milestone_action(milestone, entity, days_diff),
                })

    followups.sort(key=lambda x: (x["urgency"] != "high", x["urgency"] != "medium", -x["days_overdue"]))
    return followups


def _recommend_action(message: str, entity: Optional[Dict[str, Any]], days: int) -> str:
    """Recommend a follow-up action for a reminder."""
    name = entity["name"] if entity else "the entity"
    if days == 0:
        return f"Contact {name} today: {message}"
    if days <= 3:
        return f"Send reminder to {name}: {message}"
    return f"Escalate follow-up with {name}: {message}"


def _recommend_milestone_action(milestone: Dict[str, Any], entity: Dict[str, Any], days: int) -> str:
    """Recommend a follow-up action for a milestone."""
    name = entity.get("name", "the entity")
    description = milestone.get("description", "")
    confirmed = milestone.get("confirmed_in_writing", False)

    if not confirmed:
        return f"Request written confirmation from {name} for: {description}"

    if days <= 0:
        return f"Check progress with {name} before: {milestone.get('date', '')}"

    return f"Review blocker with {name} for: {description}"


def build_reminder_message(followup: Dict[str, Any], signature: str = "") -> Dict[str, str]:
    """Build a formal reminder message for a follow-up item."""
    name = followup.get("entity", "")
    message = followup.get("message", "")
    date = _format_date(followup.get("target_date", ""))
    days = followup.get("days_overdue", 0)
    followup_type = followup.get("type", "follow-up")

    subject = f"Follow-up: {message[:60]}"
    body_lines = [
        f"Dear {name},",
        "",
        f"We are reaching out to follow up on: {message}.",
    ]

    if followup_type == "milestone":
        if not followup.get("confirmed_in_writing", False):
            body_lines.append(f"The agreed date is {date}. We kindly request written confirmation to close this point.")
        else:
            body_lines.append(f"The milestone is scheduled for {date}. Please validate the progress.")
    else:
        body_lines.append(f"This reminder is scheduled for {date}.")

    if days > 0:
        body_lines.append(f"We are {days} day(s) past the target date.")

    body_lines.extend([
        "",
        "We look forward to your response.",
        "",
        "Best regards,",
        "The Partenon team",
    ])

    if signature:
        body_lines.append(signature)

    return {
        "subject": subject,
        "body": "\n".join(body_lines),
    }


def schedule_reminder(
    entity_id: str,
    message: str,
    date: str,
    channel: str = "email",
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """Schedule a new follow-up reminder."""
    crm = crm or get_relations_crm()
    return crm.add_reminder(entity_id, message, date, channel=channel, reminder_type="follow-up")


def run_daily_followups(
    alert_days: Optional[List[int]] = None,
    channels: Optional[List[str]] = None,
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """
    Daily cron entry point: list pending follow-ups and suggest actions.

    Returns a structured report. Sending emails or calendar events is left
    to the caller / MCP layer.
    """
    crm = crm or get_relations_crm()
    channels = channels or ["gmail", "google_workspace"]
    followups = get_pending_followups(crm=crm, alert_days=alert_days)

    report_lines = [
        "Daily Follow-ups — Diplomat",
        f"Date: {_today().strftime('%Y-%m-%d')}",
        f"Total pending: {len(followups)}",
        "",
    ]

    actions = []
    for item in followups:
        urgency = item["urgency"].upper()
        entity = item["entity"]
        message = item["message"]
        action = item["recommended_action"]

        report_lines.append(f"[{urgency}] {entity}: {message}")
        report_lines.append(f"    Action: {action}")
        report_lines.append("")

        actions.append({
            "urgency": item["urgency"],
            "type": item["type"],
            "entity_id": item["entity_id"],
            "entity": entity,
            "message": message,
            "recommended_action": action,
            "suggested_channels": channels,
        })

    if not followups:
        report_lines.append("No pending follow-ups for today.")

    return {
        "success": True,
        "total": len(followups),
        "date": _today().isoformat(),
        "report": "\n".join(report_lines),
        "actions": actions,
    }


if __name__ == "__main__":
    result = run_daily_followups()
    print(result["report"])
