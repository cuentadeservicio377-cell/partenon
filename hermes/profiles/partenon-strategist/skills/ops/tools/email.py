"""
Partenon Strategist — Email Tool
Drafts, queues, and summarizes email threads.
Integrates with Gmail MCP when credentials are available;
otherwise stores drafts locally for review.
"""

import json
import uuid
from datetime import datetime
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


class Email:
    """Email drafting and parsing tool for the Strategist profile."""

    def __init__(self):
        self.data_dir = _resolve_data_dir()
        self.email_file = self.data_dir / "email.json"
        self._email = None

    def _load(self) -> Dict[str, Any]:
        """Load email data from JSON."""
        if self._email is not None:
            return self._email

        if self.email_file.exists():
            try:
                with open(self.email_file, "r", encoding="utf-8") as f:
                    self._email = json.load(f)
                    return self._email
            except Exception:
                pass

        self._email = {"drafts": [], "threads": []}
        return self._email

    def _save(self):
        """Save email data to JSON."""
        with open(self.email_file, "w", encoding="utf-8") as f:
            json.dump(self._email, f, ensure_ascii=False, indent=2)

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        cc: List[str] = None,
        bcc: List[str] = None,
    ) -> Dict[str, Any]:
        """Draft or queue an email. External sends require MCP confirmation."""
        self._load()

        draft = {
            "id": f"EML-{uuid.uuid4().hex[:8].upper()}",
            "to": to,
            "cc": cc or [],
            "bcc": bcc or [],
            "subject": subject,
            "body": body,
            "created_at": datetime.now().isoformat(),
            "sent": False,
            "source": "email_tool",
        }

        self._email["drafts"].append(draft)
        self._save()

        return {
            "success": True,
            "draft": draft,
            "message": (
                f"Email draft saved ({draft['id']}). "
                "Confirm to send via Gmail MCP."
            ),
        }

    def parse_threads(
        self, query: str = "is:unread", max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """Parse and summarize email threads matching a query.

        When Gmail MCP is not connected, returns locally stored threads
        filtered by the query string.
        """
        self._load()

        threads = self._email.get("threads", [])
        query_lower = query.lower()

        filtered = []
        for thread in threads:
            text = " ".join(
                [
                    thread.get("subject", ""),
                    thread.get("from", ""),
                    thread.get("snippet", ""),
                ]
            ).lower()
            if query_lower in text or not query:
                filtered.append(thread)

        filtered = filtered[:max_results]

        summaries = []
        for thread in filtered:
            summaries.append({
                "id": thread.get("id"),
                "subject": thread.get("subject", "No subject"),
                "from": thread.get("from", "Unknown"),
                "snippet": thread.get("snippet", ""),
                "unread": thread.get("unread", True),
                "timestamp": thread.get("timestamp"),
            })

        return summaries

    def store_thread(
        self,
        thread_id: str,
        subject: str,
        from_address: str,
        snippet: str,
        unread: bool = True,
        timestamp: str = None,
    ) -> Dict[str, Any]:
        """Store a thread summary for local parsing."""
        self._load()

        thread = {
            "id": thread_id,
            "subject": subject,
            "from": from_address,
            "snippet": snippet,
            "unread": unread,
            "timestamp": timestamp or datetime.now().isoformat(),
        }

        self._email["threads"].append(thread)
        self._save()

        return {
            "success": True,
            "thread": thread,
            "message": f"Thread stored: {subject}",
        }

    def format_threads(self, threads: List[Dict[str, Any]]) -> str:
        """Format thread summaries for display."""
        if not threads:
            return "No email threads found."

        lines = [f"Email Threads ({len(threads)})", ""]
        for thread in threads:
            marker = "●" if thread.get("unread") else "○"
            lines.append(
                f"{marker} {thread.get('subject', 'No subject')} — {thread.get('from', 'Unknown')}"
            )
            if thread.get("snippet"):
                lines.append(f"   {thread['snippet'][:120]}...")

        return "\n".join(lines)


# Singleton
_email_instance = None


def get_email() -> Email:
    """Get or create singleton Email instance."""
    global _email_instance
    if _email_instance is None:
        _email_instance = Email()
    return _email_instance
