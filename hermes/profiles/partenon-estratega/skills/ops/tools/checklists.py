"""
Partenon Strategist — Checklists Tool
Manages project checklists by type and industry.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


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


def _default_industry() -> str:
    """Read industry from company.yaml if available."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "partenon-core":
            config_path = parent / "config" / "company.yaml"
            break
        config_path = parent / "partenon-core" / "config" / "company.yaml"
        if config_path.exists():
            break
    else:
        return "consulting"

    if not config_path.exists():
        return "consulting"

    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("company", {}).get("industry", "consulting")
    except Exception:
        return "consulting"


class Checklists:
    """Checklist management with templates by industry."""

    CHECKLIST_TEMPLATES = {
        "events": {
            "pre-event": [
                "Confirm date and venue with client",
                "Hire providers (catering, music, photographer)",
                "Prepare furniture and decoration",
                "Coordinate transport logistics",
                "Briefing with work team",
                "Confirm guest attendance",
                "Prepare equipment checklist",
            ],
            "during-event": [
                "Setup at venue",
                "Guest reception",
                "Real-time coordination",
                "Resolve unexpected issues",
                "Photographic documentation",
            ],
            "post-event": [
                "Dismantle and collect equipment",
                "Furniture inventory",
                "Final invoicing to client",
                "Evaluation with client",
                "Archive photos and documents",
            ],
        },
        "legal": {
            "pre-trial": [
                "Review contract and case background",
                "Research relevant jurisprudence",
                "Prepare legal strategy",
                "Schedule hearings and deadlines",
                "Gather documentation",
            ],
            "during-trial": [
                "Prepare writings and claims",
                "Attend hearings",
                "Continuous communication with client",
                "Update file",
                "Follow up on resolutions",
            ],
            "post-trial": [
                "Analyze sentence",
                "Execution or appeal as applicable",
                "Administrative case closure",
                "Final report to client",
                "Archive file",
            ],
        },
        "consulting": {
            "pre-project": [
                "Define scope and objectives",
                "Assign responsibles",
                "Set key dates",
                "Confirm required resources",
                "Kickoff meeting with client",
            ],
            "during-project": [
                "Weekly progress follow-up",
                "Continuous communication with client",
                "Quality control of deliverables",
                "Process documentation",
                "Change management",
            ],
            "post-project": [
                "Final document delivery",
                "Client training",
                "Results evaluation",
                "Request testimonial or reference",
                "Administrative closure",
            ],
        },
        "retail": {
            "pre-sale": [
                "Verify available inventory",
                "Confirm current prices",
                "Prepare quote",
                "Verify shipping policies",
            ],
            "during-sale": [
                "Confirm payment",
                "Prepare order",
                "Coordinate shipping or delivery",
                "Send confirmation to customer",
            ],
            "post-sale": [
                "Follow up on delivery",
                "Request feedback",
                "Manage warranty if applicable",
                "Customer loyalty",
            ],
        },
    }

    def __init__(self):
        self.industry = _default_industry()
        self.data_dir = _resolve_data_dir()
        self.checklists_file = self.data_dir / "checklists.json"
        self._checklists = None

    def _load(self) -> Dict[str, Any]:
        """Load checklists from JSON."""
        if self._checklists is not None:
            return self._checklists

        if self.checklists_file.exists():
            try:
                with open(self.checklists_file, "r", encoding="utf-8") as f:
                    self._checklists = json.load(f)
                    return self._checklists
            except Exception:
                pass

        self._checklists = {}
        return self._checklists

    def _save(self):
        """Save checklists to JSON."""
        with open(self.checklists_file, "w", encoding="utf-8") as f:
            json.dump(self._checklists, f, ensure_ascii=False, indent=2)

    def get_template(self, industry: str = None, checklist_type: str = None) -> Dict[str, List[str]]:
        """Get checklist template for industry."""
        if not industry:
            industry = self.industry

        templates = self.CHECKLIST_TEMPLATES.get(industry, self.CHECKLIST_TEMPLATES["consulting"])

        if checklist_type:
            return {checklist_type: templates.get(checklist_type, [])}

        return templates

    def create_project_checklist(
        self, project_id: str, industry: str = None
    ) -> Dict[str, Any]:
        """Create checklist for a project based on industry templates."""
        self._load()

        templates = self.get_template(industry)

        checklist = {}
        for phase, items in templates.items():
            checklist[phase] = [
                {
                    "item": item,
                    "completed": False,
                    "completed_at": None,
                }
                for item in items
            ]

        self._checklists[project_id] = {
            "project_id": project_id,
            "created_at": datetime.now().isoformat(),
            "phases": checklist,
        }
        self._save()

        total_items = sum(len(v) for v in checklist.values())
        return {
            "success": True,
            "checklist": self._checklists[project_id],
            "message": f"Checklist created for {project_id} with {total_items} items",
        }

    def get_checklist(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get checklist for a project."""
        self._load()
        return self._checklists.get(project_id)

    def toggle_item(
        self, project_id: str, phase: str, item_index: int
    ) -> Dict[str, Any]:
        """Toggle completion status of a checklist item."""
        self._load()

        checklist = self._checklists.get(project_id)
        if not checklist:
            return {
                "success": False,
                "error": f"No checklist for {project_id}",
            }

        phases = checklist.get("phases", {})
        if phase not in phases:
            return {
                "success": False,
                "error": f"Phase '{phase}' not found",
            }

        items = phases[phase]
        if item_index < 0 or item_index >= len(items):
            return {
                "success": False,
                "error": f"Invalid item {item_index}",
            }

        item = items[item_index]
        item["completed"] = not item["completed"]
        item["completed_at"] = datetime.now().isoformat() if item["completed"] else None

        self._save()

        status = "completed" if item["completed"] else "pending"
        return {
            "success": True,
            "item": item,
            "message": f"'{item['item']}' marked as {status}",
        }

    def add_custom_item(
        self, project_id: str, phase: str, item_text: str
    ) -> Dict[str, Any]:
        """Add a custom item to a checklist."""
        self._load()

        checklist = self._checklists.get(project_id)
        if not checklist:
            result = self.create_project_checklist(project_id)
            if not result["success"]:
                return result
            checklist = self._checklists[project_id]

        phases = checklist.setdefault("phases", {})
        phase_items = phases.setdefault(phase, [])

        phase_items.append({
            "item": item_text,
            "completed": False,
            "completed_at": None,
            "custom": True,
        })

        self._save()

        return {
            "success": True,
            "message": f"Item added to {phase}: {item_text}",
        }

    def get_progress(self, project_id: str) -> Dict[str, Any]:
        """Get checklist progress for a project."""
        self._load()

        checklist = self._checklists.get(project_id)
        if not checklist:
            return {
                "success": False,
                "error": f"No checklist for {project_id}",
            }

        phases = checklist.get("phases", {})

        total_items = 0
        completed_items = 0
        phase_progress = {}

        for phase, items in phases.items():
            phase_total = len(items)
            phase_completed = sum(1 for item in items if item["completed"])
            total_items += phase_total
            completed_items += phase_completed

            phase_progress[phase] = {
                "total": phase_total,
                "completed": phase_completed,
                "progress": round(phase_completed / phase_total * 100, 1) if phase_total > 0 else 0,
            }

        overall_progress = round(completed_items / total_items * 100, 1) if total_items > 0 else 0

        return {
            "success": True,
            "project_id": project_id,
            "total_items": total_items,
            "completed": completed_items,
            "overall_progress": overall_progress,
            "by_phase": phase_progress,
        }

    def format_checklist(self, project_id: str) -> str:
        """Format checklist for display."""
        self._load()

        checklist = self._checklists.get(project_id)
        if not checklist:
            return f"No checklist for {project_id}."

        progress = self.get_progress(project_id)
        lines = [
            f"Checklist — {project_id}",
            f"Progress: {progress['overall_progress']}% ({progress['completed']}/{progress['total_items']})",
            "",
        ]

        for phase, items in checklist.get("phases", {}).items():
            phase_prog = progress["by_phase"].get(phase, {})
            lines.append(
                f"{phase.replace('-', ' ').title()} ({phase_prog.get('completed', 0)}/{phase_prog.get('total', 0)})"
            )

            for item in items:
                check = "[x]" if item["completed"] else "[ ]"
                lines.append(f"  {check} {item['item']}")

            lines.append("")

        return "\n".join(lines)

    def format_progress(self, project_id: str) -> str:
        """Format progress for display."""
        progress = self.get_progress(project_id)

        if not progress["success"]:
            return progress["error"]

        lines = [
            f"Progress — {project_id}",
            "",
            f"{progress['completed']}/{progress['total_items']} items completed",
            f"Overall progress: {progress['overall_progress']}%",
            "",
        ]

        filled = int(progress['overall_progress'] / 10)
        bar = "=" * filled + "-" * (10 - filled)
        lines.append(f"[{bar}] {progress['overall_progress']}%")
        lines.append("")

        for phase, data in progress["by_phase"].items():
            phase_filled = int(data["progress"] / 10)
            phase_bar = "=" * phase_filled + "-" * (10 - phase_filled)
            lines.append(f"{phase.replace('-', ' ').title()}: [{phase_bar}] {data['progress']}%")

        return "\n".join(lines)


# Singleton
_checklists_instance = None


def get_checklists() -> Checklists:
    """Get or create singleton Checklists instance."""
    global _checklists_instance
    if _checklists_instance is None:
        _checklists_instance = Checklists()
    return _checklists_instance
