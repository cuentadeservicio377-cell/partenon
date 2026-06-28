"""
Partenon Strategist — Tasks Tool
Manages tasks within projects.
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional


def _resolve_data_dir() -> Path:
    """Resolve data directory relative to partenon_core."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "partenon_core":
            data_dir = parent / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            return data_dir
        candidate = parent / "partenon_core" / "data"
        if candidate.exists() and candidate.is_dir():
            return candidate
    for parent in current.parents:
        if (parent / "partenon_core").exists():
            data_dir = parent / "partenon_core" / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            return data_dir
    local = Path(__file__).resolve().parent / "data"
    local.mkdir(parents=True, exist_ok=True)
    return local


class Tasks:
    """Task management tool."""

    TASK_STATUSES = [
        "pending",
        "in_progress",
        "blocked",
        "completed",
        "canceled",
    ]

    PRIORITIES = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "urgent": 4,
    }

    def __init__(self):
        self.data_dir = _resolve_data_dir()
        self.tasks_file = self.data_dir / "tasks.json"
        self._tasks = None
        self._next_id = 1

    def _load(self) -> List[Dict[str, Any]]:
        """Load tasks from JSON."""
        if self._tasks is not None:
            return self._tasks

        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._tasks = data.get("tasks", [])
                    self._next_id = data.get("next_id", 1)
                    return self._tasks
            except Exception:
                pass

        self._tasks = []
        self._next_id = 1
        return self._tasks

    def _save(self):
        """Save tasks to JSON."""
        data = {
            "tasks": self._tasks,
            "next_id": self._next_id,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _generate_task_id(self) -> str:
        """Generate task ID (TASK-001, TASK-002, etc.)."""
        task_id = f"TASK-{self._next_id:03d}"
        self._next_id += 1
        return task_id

    def create_task(
        self,
        project_id: str,
        title: str,
        description: str = None,
        assignee: str = None,
        due_date: str = None,
        priority: str = "medium",
        dependencies: List[str] = None,
        tags: List[str] = None,
    ) -> Dict[str, Any]:
        """Create a new task."""
        self._load()

        if priority not in self.PRIORITIES:
            priority = "medium"

        if due_date and isinstance(due_date, str):
            try:
                due_date_dt = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except ValueError:
                due_date_dt = datetime.now() + timedelta(days=7)
        else:
            due_date_dt = datetime.now() + timedelta(days=7)

        task = {
            "id": self._generate_task_id(),
            "project_id": project_id,
            "title": title,
            "description": description or "",
            "assignee": assignee or "Unassigned",
            "status": "pending",
            "priority": priority,
            "priority_value": self.PRIORITIES[priority],
            "created_at": datetime.now().isoformat(),
            "due_date": due_date_dt.isoformat(),
            "completed_at": None,
            "dependencies": dependencies or [],
            "tags": tags or [],
            "comments": [],
        }

        self._tasks.append(task)
        self._save()

        return {
            "success": True,
            "task": task,
            "message": f"Task created: {title} ({task['id']})",
        }

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task by ID."""
        self._load()

        for task in self._tasks:
            if task["id"].lower() == task_id.lower():
                return task

        return None

    def update_task(self, task_id: str, **updates) -> Dict[str, Any]:
        """Update task fields."""
        self._load()

        for task in self._tasks:
            if task["id"].lower() == task_id.lower():
                safe_updates = {
                    k: v
                    for k, v in updates.items()
                    if k not in ["id", "project_id", "created_at"]
                }
                task.update(safe_updates)
                self._save()

                return {
                    "success": True,
                    "task": task,
                    "message": f"Task {task_id} updated",
                }

        return {
            "success": False,
            "error": f"Task {task_id} not found",
        }

    def complete_task(self, task_id: str, comment: str = None) -> Dict[str, Any]:
        """Mark task as completed."""
        result = self.update_task(
            task_id,
            status="completed",
            completed_at=datetime.now().isoformat(),
        )

        if result["success"] and comment:
            task = result["task"]
            task["comments"].append({
                "type": "completion",
                "text": comment,
                "date": datetime.now().isoformat(),
            })
            self._save()

        if result["success"]:
            result["message"] = f"Task {task_id} completed"

        return result

    def list_tasks(
        self,
        project_id: str = None,
        status: str = None,
        assignee: str = None,
        priority: str = None,
    ) -> List[Dict[str, Any]]:
        """List tasks with optional filters."""
        self._load()

        tasks = self._tasks

        if project_id:
            tasks = [t for t in tasks if t["project_id"].lower() == project_id.lower()]

        if status:
            tasks = [t for t in tasks if t["status"] == status]

        if assignee:
            tasks = [t for t in tasks if assignee.lower() in t["assignee"].lower()]

        if priority:
            tasks = [t for t in tasks if t["priority"] == priority]

        tasks.sort(key=lambda t: (-t["priority_value"], t["due_date"]))

        return tasks

    def get_pending_tasks(self, project_id: str = None) -> List[Dict[str, Any]]:
        """Get pending tasks."""
        return self.list_tasks(project_id=project_id, status="pending")

    def get_tasks_by_project(self, project_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a project."""
        return self.list_tasks(project_id=project_id)

    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """Get overdue tasks."""
        self._load()
        now = datetime.now()

        overdue = []
        for task in self._tasks:
            if task["status"] in ["pending", "in_progress", "blocked"]:
                due_date = datetime.fromisoformat(task["due_date"])
                if due_date < now:
                    overdue.append(task)

        overdue.sort(key=lambda t: -t["priority_value"])
        return overdue

    def get_tasks_summary(self, project_id: str = None) -> Dict[str, Any]:
        """Get tasks summary."""
        tasks = self.list_tasks(project_id=project_id)

        total = len(tasks)
        pending = len([t for t in tasks if t["status"] == "pending"])
        in_progress = len([t for t in tasks if t["status"] == "in_progress"])
        blocked = len([t for t in tasks if t["status"] == "blocked"])
        completed = len([t for t in tasks if t["status"] == "completed"])
        overdue = len([
            t for t in tasks
            if t["status"] in ["pending", "in_progress", "blocked"]
            and datetime.fromisoformat(t["due_date"]) < datetime.now()
        ])

        completion_rate = (completed / total * 100) if total > 0 else 0

        return {
            "total": total,
            "pending": pending,
            "in_progress": in_progress,
            "blocked": blocked,
            "completed": completed,
            "overdue": overdue,
            "completion_rate": round(completion_rate, 1),
            "upcoming_deadlines": self._get_upcoming_deadlines(project_id),
        }

    def _get_upcoming_deadlines(
        self, project_id: str = None, days: int = 3
    ) -> List[Dict[str, Any]]:
        """Get tasks with deadlines in the next N days."""
        self._load()
        now = datetime.now()
        upcoming = []

        for task in self._tasks:
            if task["status"] in ["pending", "in_progress", "blocked"]:
                if project_id and task["project_id"].lower() != project_id.lower():
                    continue

                due_date = datetime.fromisoformat(task["due_date"])
                days_left = (due_date - now).days

                if 0 <= days_left <= days:
                    upcoming.append({
                        "task": task,
                        "days_left": days_left,
                        "due_date": due_date.strftime("%Y-%m-%d"),
                    })

        upcoming.sort(key=lambda x: x["days_left"])
        return upcoming

    def format_task_list(self, tasks: List[Dict[str, Any]], title: str = "Tasks") -> str:
        """Format task list for display."""
        if not tasks:
            return f"No {title.lower()}."

        lines = [f"{title} ({len(tasks)})", ""]

        status_markers = {
            "pending": "[ ]",
            "in_progress": "[~]",
            "blocked": "[B]",
            "completed": "[x]",
            "canceled": "[-]",
        }

        priority_markers = {
            "low": "",
            "medium": "",
            "high": "HIGH",
            "urgent": "URGENT",
        }

        for task in tasks:
            status_marker = status_markers.get(task["status"], "•")
            priority_marker = priority_markers.get(task["priority"], "")

            due_date = datetime.fromisoformat(task["due_date"])
            is_overdue = (
                due_date < datetime.now()
                and task["status"] not in ["completed", "canceled"]
            )
            overdue_marker = " OVERDUE" if is_overdue else ""

            lines.append(
                f"{status_marker} {priority_marker} {task['title']} ({task['id']}){overdue_marker}"
            )
            lines.append(f"   Status: {task['status']} | Priority: {task['priority']}")
            lines.append(
                f"   Assignee: {task['assignee']} | Due: {due_date.strftime('%Y-%m-%d')}"
            )

            if task["description"]:
                lines.append(f"   {task['description'][:80]}...")

            lines.append("")

        return "\n".join(lines)

    def format_tasks_summary(self, summary: Dict[str, Any]) -> str:
        """Format tasks summary for display."""
        lines = [
            "Task Summary",
            "",
            f"Total: {summary['total']}",
            f"Pending: {summary['pending']}",
            f"In progress: {summary['in_progress']}",
            f"Blocked: {summary['blocked']}",
            f"Completed: {summary['completed']}",
            f"Overdue: {summary['overdue']}",
            f"Completion rate: {summary['completion_rate']}%",
        ]

        if summary["upcoming_deadlines"]:
            lines.extend(["", "Upcoming deadlines:"])
            for item in summary["upcoming_deadlines"]:
                task = item["task"]
                marker = "URGENT" if item["days_left"] <= 1 else "upcoming"
                lines.append(
                    f"{marker} {task['title']} — {item['days_left']} days ({item['due_date']})"
                )

        return "\n".join(lines)


# Singleton
_tasks_instance = None


def get_tasks() -> Tasks:
    """Get or create singleton Tasks instance."""
    global _tasks_instance
    if _tasks_instance is None:
        _tasks_instance = Tasks()
    return _tasks_instance
