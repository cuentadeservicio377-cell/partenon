"""
Partenon Strategist — Projects Tool
Manages projects, assignments, and project lifecycle.
"""

import json
from datetime import datetime, timedelta
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


class Projects:
    """Project management tool."""

    PROJECT_STATUSES = [
        "planned",
        "in_progress",
        "paused",
        "completed",
        "canceled",
        "delivered",
    ]

    def __init__(self):
        self.industry = _default_industry()
        self.data_dir = _resolve_data_dir()
        self.projects_file = self.data_dir / "projects.json"
        self._projects = None
        self._next_id = 1

    def _load(self) -> List[Dict[str, Any]]:
        """Load projects from JSON."""
        if self._projects is not None:
            return self._projects

        if self.projects_file.exists():
            try:
                with open(self.projects_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._projects = data.get("projects", [])
                    self._next_id = data.get("next_id", 1)
                    return self._projects
            except Exception:
                pass

        self._projects = []
        self._next_id = 1
        return self._projects

    def _save(self):
        """Save projects to JSON."""
        data = {
            "projects": self._projects,
            "next_id": self._next_id,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.projects_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _generate_project_id(self) -> str:
        """Generate project ID (PROJ-001, PROJ-002, etc.)."""
        project_id = f"PROJ-{self._next_id:03d}"
        self._next_id += 1
        return project_id

    def create_project(
        self,
        name: str,
        client_id: str = None,
        client_name: str = None,
        description: str = None,
        start_date: str = None,
        delivery_date: str = None,
        amount: float = 0,
        type: str = None,
        notes: str = None,
    ) -> Dict[str, Any]:
        """Create a new project."""
        self._load()

        if start_date and isinstance(start_date, str):
            try:
                start_date_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            except ValueError:
                start_date_dt = datetime.now()
        else:
            start_date_dt = datetime.now()

        if delivery_date and isinstance(delivery_date, str):
            try:
                delivery_date_dt = datetime.fromisoformat(delivery_date.replace("Z", "+00:00"))
            except ValueError:
                delivery_date_dt = start_date_dt + timedelta(days=30)
        else:
            delivery_date_dt = start_date_dt + timedelta(days=30)

        project = {
            "id": self._generate_project_id(),
            "name": name,
            "client_id": client_id,
            "client_name": client_name or "Client not specified",
            "description": description or "",
            "type": type or self.industry,
            "status": "planned",
            "amount": amount,
            "created_at": datetime.now().isoformat(),
            "start_date": start_date_dt.isoformat(),
            "delivery_date": delivery_date_dt.isoformat(),
            "completed_at": None,
            "progress": 0,
            "tasks": [],
            "checklist": [],
            "notes": notes or "",
            "history": [
                {"action": "Created", "date": datetime.now().isoformat()}
            ],
        }

        self._projects.append(project)
        self._save()

        return {
            "success": True,
            "project": project,
            "message": f"Project created: {name} ({project['id']})",
        }

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID."""
        self._load()

        for project in self._projects:
            if project["id"].lower() == project_id.lower():
                return project

        return None

    def find_project(self, query: str) -> Optional[Dict[str, Any]]:
        """Find project by name or ID."""
        self._load()

        query_lower = query.lower()

        for project in self._projects:
            if project["id"].lower() == query_lower:
                return project
            if query_lower in project["name"].lower():
                return project

        return None

    def update_project(self, project_id: str, **updates) -> Dict[str, Any]:
        """Update project fields."""
        self._load()

        for project in self._projects:
            if project["id"].lower() == project_id.lower():
                safe_updates = {
                    k: v
                    for k, v in updates.items()
                    if k not in ["id", "history", "tasks", "checklist"]
                }
                project.update(safe_updates)
                project["history"].append({
                    "action": f"Updated: {', '.join(safe_updates.keys())}",
                    "date": datetime.now().isoformat(),
                })
                self._save()

                return {
                    "success": True,
                    "project": project,
                    "message": f"Project {project_id} updated",
                }

        return {
            "success": False,
            "error": f"Project {project_id} not found",
        }

    def update_status(
        self, project_id: str, new_status: str, notes: str = None
    ) -> Dict[str, Any]:
        """Update project status."""
        if new_status not in self.PROJECT_STATUSES:
            return {
                "success": False,
                "error": f"Invalid status. Valid: {', '.join(self.PROJECT_STATUSES)}",
            }

        self._load()

        for project in self._projects:
            if project["id"].lower() == project_id.lower():
                previous_status = project["status"]
                project["status"] = new_status

                if new_status == "completed":
                    project["completed_at"] = datetime.now().isoformat()
                    project["progress"] = 100

                project["history"].append({
                    "action": f"Status change: {previous_status} -> {new_status}",
                    "date": datetime.now().isoformat(),
                    "notes": notes or "",
                })
                self._save()

                return {
                    "success": True,
                    "project": project,
                    "message": f"{project['name']}: {previous_status} -> {new_status}",
                }

        return {
            "success": False,
            "error": f"Project {project_id} not found",
        }

    def update_progress(self, project_id: str, progress: int) -> Dict[str, Any]:
        """Update project progress percentage."""
        progress = max(0, min(100, progress))

        result = self.update_project(project_id, progress=progress)

        if result["success"]:
            result["message"] = f"Progress for {project_id}: {progress}%"

        return result

    def list_projects(
        self, status: str = None, client_id: str = None
    ) -> List[Dict[str, Any]]:
        """List projects, optionally filtered."""
        self._load()

        projects = self._projects

        if status:
            projects = [p for p in projects if p["status"] == status]

        if client_id:
            projects = [p for p in projects if p.get("client_id") == client_id]

        return projects

    def get_active_projects(self) -> List[Dict[str, Any]]:
        """Get active (non-completed) projects."""
        return self.list_projects()

    def get_overdue_projects(self) -> List[Dict[str, Any]]:
        """Get projects past their delivery date."""
        self._load()
        now = datetime.now()

        overdue = []
        for project in self._projects:
            if project["status"] in ["planned", "in_progress", "paused"]:
                delivery_date = datetime.fromisoformat(project["delivery_date"])
                if delivery_date < now:
                    overdue.append(project)

        return overdue

    def get_projects_summary(self) -> Dict[str, Any]:
        """Get projects summary."""
        self._load()

        total = len(self._projects)
        active = len([p for p in self._projects if p["status"] in ["planned", "in_progress", "paused"]])
        completed = len([p for p in self._projects if p["status"] in ["completed", "delivered"]])
        overdue = len(self.get_overdue_projects())

        active_projects = [p for p in self._projects if p["status"] in ["planned", "in_progress"]]
        avg_progress = (
            sum(p["progress"] for p in active_projects) / len(active_projects)
            if active_projects
            else 0
        )

        return {
            "total": total,
            "active": active,
            "completed": completed,
            "overdue": overdue,
            "canceled": len([p for p in self._projects if p["status"] == "canceled"]),
            "average_progress": round(avg_progress, 1),
            "upcoming_deadlines": self._get_upcoming_deadlines(),
        }

    def _get_upcoming_deadlines(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get projects with deadlines in the next N days."""
        self._load()
        now = datetime.now()
        upcoming = []

        for project in self._projects:
            if project["status"] in ["planned", "in_progress"]:
                delivery_date = datetime.fromisoformat(project["delivery_date"])
                days_left = (delivery_date - now).days

                if 0 <= days_left <= days:
                    upcoming.append({
                        "project": project,
                        "days_left": days_left,
                        "delivery_date": delivery_date.strftime("%Y-%m-%d"),
                    })

        upcoming.sort(key=lambda x: x["days_left"])
        return upcoming

    def format_project_summary(self, summary: Dict[str, Any]) -> str:
        """Format projects summary for display."""
        lines = [
            "Project Summary",
            "",
            f"Total: {summary['total']}",
            f"Active: {summary['active']}",
            f"Completed: {summary['completed']}",
            f"Overdue: {summary['overdue']}",
            f"Average progress: {summary['average_progress']}%",
        ]

        if summary["upcoming_deadlines"]:
            lines.extend(["", "Upcoming deadlines:"])
            for item in summary["upcoming_deadlines"]:
                project = item["project"]
                marker = "URGENT" if item["days_left"] <= 2 else "upcoming"
                lines.append(
                    f"{marker} {project['name']} — {item['days_left']} days ({item['delivery_date']})"
                )

        return "\n".join(lines)


# Singleton
_projects_instance = None


def get_projects() -> Projects:
    """Get or create singleton Projects instance."""
    global _projects_instance
    if _projects_instance is None:
        _projects_instance = Projects()
    return _projects_instance
