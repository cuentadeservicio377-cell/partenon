"""Partenon Slack notification adapter.

Wraps the Slack SDK so the Strategist can post channel notifications.
Dry-run by default; live sends require SLACK_BOT_TOKEN.
"""

import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from mcp_servers._shared.live_mode import is_live


def _client() -> WebClient:
    token = os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        raise RuntimeError("SLACK_BOT_TOKEN not configured")
    return WebClient(token=token)


def send_message(channel: str, text: str) -> dict:
    """Send a Slack message to a channel."""
    if not is_live("slack"):
        return {"ok": True, "dry_run": True, "channel": channel, "message": text}
    try:
        response = _client().chat_postMessage(channel=channel, text=text)
        return {"ok": True, "dry_run": False, "channel": channel, "ts": response["ts"]}
    except SlackApiError as e:
        return {"ok": False, "error": str(e)}


def notify_task_overdue(task_id: str, title: str, due_date: str, channel: str = "#general") -> dict:
    """Post a task-overdue notification to Slack."""
    text = f"Task overdue: *{title}* ({task_id}) was due on {due_date}."
    return send_message(channel, text)
