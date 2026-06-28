"""
Partenon Strategist — Notes Tool
Stores project notes, client context, and detail tracking.
Shares context with the Brain via local JSON and G-Brain when available.
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


class Notes:
    """Note and detail tracking tool for projects and clients."""

    def __init__(self):
        self.data_dir = _resolve_data_dir()
        self.notes_file = self.data_dir / "notes.json"
        self._notes = None

    def _load(self) -> Dict[str, Any]:
        """Load notes data from JSON."""
        if self._notes is not None:
            return self._notes

        if self.notes_file.exists():
            try:
                with open(self.notes_file, "r", encoding="utf-8") as f:
                    self._notes = json.load(f)
                    return self._notes
            except Exception:
                pass

        self._notes = {"notes": []}
        return self._notes

    def _save(self):
        """Save notes data to JSON."""
        with open(self.notes_file, "w", encoding="utf-8") as f:
            json.dump(self._notes, f, ensure_ascii=False, indent=2)

    def add_note(
        self,
        content: str,
        project_id: str = None,
        client_name: str = None,
        tags: List[str] = None,
    ) -> Dict[str, Any]:
        """Add a note linked to a project or client."""
        self._load()

        note = {
            "id": f"NOTE-{uuid.uuid4().hex[:8].upper()}",
            "content": content,
            "project_id": project_id,
            "client_name": client_name,
            "tags": tags or [],
            "created_at": datetime.now().isoformat(),
        }

        self._notes["notes"].append(note)
        self._save()

        return {
            "success": True,
            "note": note,
            "message": f"Note saved ({note['id']})",
        }

    def get_notes(
        self,
        project_id: str = None,
        client_name: str = None,
        query: str = None,
        tags: List[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get notes filtered by project, client, query, or tags."""
        self._load()

        notes = self._notes.get("notes", [])

        if project_id:
            notes = [n for n in notes if n.get("project_id") == project_id]

        if client_name:
            notes = [
                n for n in notes
                if n.get("client_name", "").lower() == client_name.lower()
            ]

        if query:
            query_lower = query.lower()
            notes = [n for n in notes if query_lower in n.get("content", "").lower()]

        if tags:
            notes = [
                n for n in notes
                if any(tag.lower() in [t.lower() for t in n.get("tags", [])] for tag in tags)
            ]

        notes.sort(key=lambda n: n.get("created_at", ""), reverse=True)
        return notes

    def get_project_context(
        self, project_id: str, client_name: str = None
    ) -> Dict[str, Any]:
        """Return aggregated context for a project or client."""
        self._load()

        notes = self.get_notes(project_id=project_id, client_name=client_name)
        tags = set()
        for note in notes:
            tags.update(note.get("tags", []))

        return {
            "project_id": project_id,
            "client_name": client_name,
            "note_count": len(notes),
            "tags": sorted(tags),
            "latest_notes": notes[:5],
            "summary": "\n".join(f"- {n.get('content', '')}" for n in notes[:5]),
        }

    def format_notes(self, notes: List[Dict[str, Any]], title: str = "Notes") -> str:
        """Format notes for display."""
        if not notes:
            return f"No {title.lower()}."

        lines = [f"{title} ({len(notes)})", ""]
        for note in notes:
            created = note.get("created_at", "")
            try:
                created_dt = datetime.fromisoformat(created)
                created_str = created_dt.strftime("%Y-%m-%d %H:%M")
            except ValueError:
                created_str = created

            lines.append(f"• {note.get('content', '')}")
            meta = []
            if note.get("project_id"):
                meta.append(f"project: {note['project_id']}")
            if note.get("client_name"):
                meta.append(f"client: {note['client_name']}")
            if note.get("tags"):
                meta.append(f"tags: {', '.join(note['tags'])}")
            meta.append(created_str)
            lines.append(f"   {' | '.join(meta)}")

        return "\n".join(lines)


# Singleton
_notes_instance = None


def get_notes() -> Notes:
    """Get or create singleton Notes instance."""
    global _notes_instance
    if _notes_instance is None:
        _notes_instance = Notes()
    return _notes_instance
