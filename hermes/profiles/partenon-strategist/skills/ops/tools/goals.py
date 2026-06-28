"""
Partenon Strategist — Goals Engine
Defines, tracks, and reports business goals with automatic tracking
based on data from other departments.
"""

import json
from dataclasses import dataclass, asdict
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


@dataclass
class Goal:
    id: str
    title: str
    type: str  # weekly, monthly, quarterly, yearly
    department: str
    target: float
    unit: str
    deadline: str
    created_at: str
    status: str = "active"  # active, met, missed, canceled
    progress: float = 0.0
    auto_track: bool = True
    kpi_source: str = ""  # e.g. "pipeline.contracted", "tasks.completed"
    notes: str = ""


class GoalsEngine:
    """Manages the full lifecycle of business goals."""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else _resolve_data_dir()
        self.goals_file = self.data_dir / "goals.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.goals_file.exists():
            self._save_goals([])

    def _load_goals(self) -> List[Dict[str, Any]]:
        try:
            with open(self.goals_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("goals", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_goals(self, goals: List[Dict[str, Any]]):
        with open(self.goals_file, "w", encoding="utf-8") as f:
            json.dump({"goals": goals, "updated_at": datetime.now().isoformat()}, f, indent=2, ensure_ascii=False)

    def _generate_id(self) -> str:
        goals = self._load_goals()
        count = len(goals) + 1
        return f"GOAL-{count:03d}"

    def create_goal(
        self,
        title: str,
        type: str = "weekly",
        department: str = "general",
        target: float = 1.0,
        unit: str = "unit",
        deadline: Optional[str] = None,
        auto_track: bool = True,
        kpi_source: str = "",
    ) -> Dict[str, Any]:
        """Create a new goal."""
        if deadline is None:
            if type == "weekly":
                deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            elif type == "monthly":
                deadline = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            else:
                deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        goal = Goal(
            id=self._generate_id(),
            title=title,
            type=type,
            department=department,
            target=target,
            unit=unit,
            deadline=deadline,
            created_at=datetime.now().strftime("%Y-%m-%d"),
            auto_track=auto_track,
            kpi_source=kpi_source,
        )

        goals = self._load_goals()
        goals.append(asdict(goal))
        self._save_goals(goals)
        return asdict(goal)

    def get_goals(
        self,
        status: Optional[str] = None,
        type: Optional[str] = None,
        department: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get filtered goals."""
        goals = self._load_goals()
        if status:
            goals = [g for g in goals if g["status"] == status]
        if type:
            goals = [g for g in goals if g["type"] == type]
        if department:
            goals = [g for g in goals if g["department"] == department]
        return goals

    def get_goal_by_id(self, goal_id: str) -> Optional[Dict[str, Any]]:
        """Find a goal by ID."""
        goals = self._load_goals()
        for goal in goals:
            if goal["id"] == goal_id:
                return goal
        return None

    def update_progress(self, goal_id: str, progress: float) -> Optional[Dict[str, Any]]:
        """Update goal progress."""
        goals = self._load_goals()
        for goal in goals:
            if goal["id"] == goal_id:
                goal["progress"] = min(progress, goal["target"])
                if goal["progress"] >= goal["target"]:
                    goal["status"] = "met"
                self._save_goals(goals)
                return goal
        return None

    def auto_track_goals(self) -> List[Dict[str, Any]]:
        """Update progress automatically based on KPI sources."""
        goals = self._load_goals()
        updated = []

        for goal in goals:
            if not goal.get("auto_track") or goal["status"] != "active":
                continue

            new_progress = self._calculate_kpi(goal["kpi_source"], goal)
            if new_progress is not None and new_progress != goal["progress"]:
                goal["progress"] = new_progress
                if goal["progress"] >= goal["target"]:
                    goal["status"] = "met"
                updated.append(goal)

        if updated:
            self._save_goals(goals)

        return updated

    def _calculate_kpi(self, kpi_source: str, goal: Dict[str, Any]) -> Optional[float]:
        """Calculate current KPI value by reading data from other tools."""
        if not kpi_source:
            return None

        try:
            if kpi_source.startswith("pipeline."):
                return self._kpi_pipeline(kpi_source, goal)
            elif kpi_source.startswith("tasks."):
                return self._kpi_tasks(kpi_source, goal)
            elif kpi_source.startswith("payments."):
                return self._kpi_payments(kpi_source, goal)
        except Exception:
            pass

        return None

    def _kpi_pipeline(self, kpi_source: str, goal: Dict[str, Any]) -> Optional[float]:
        """Read pipeline.json to calculate sales KPI."""
        pipeline_file = self.data_dir / "pipeline.json"
        if not pipeline_file.exists():
            return None

        with open(pipeline_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        entries = data.get("entries", [])
        status = kpi_source.split(".")[1] if "." in kpi_source else "contracted"

        created = datetime.strptime(goal["created_at"], "%Y-%m-%d")
        deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d")

        count = 0
        for entry in entries:
            if entry.get("status") == status:
                date = entry.get("updated_at") or entry.get("created_at")
                if date:
                    try:
                        fdt = datetime.strptime(date, "%Y-%m-%d")
                        if created <= fdt <= deadline:
                            count += 1
                    except ValueError:
                        count += 1
                else:
                    count += 1

        return float(count)

    def _kpi_tasks(self, kpi_source: str, goal: Dict[str, Any]) -> Optional[float]:
        """Read tasks.json to calculate operations KPI."""
        tasks_file = self.data_dir / "tasks.json"
        if not tasks_file.exists():
            return None

        with open(tasks_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        tasks = data.get("tasks", [])
        created = datetime.strptime(goal["created_at"], "%Y-%m-%d")
        deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d")

        count = 0
        for task in tasks:
            if task.get("status") == "completed":
                date = task.get("completed_at") or task.get("due_date")
                if date:
                    try:
                        fdt = datetime.strptime(date, "%Y-%m-%d")
                        if created <= fdt <= deadline:
                            count += 1
                    except ValueError:
                        pass

        return float(count)

    def _kpi_payments(self, kpi_source: str, goal: Dict[str, Any]) -> Optional[float]:
        """Read quotes.json to calculate financial KPI."""
        quotes_file = self.data_dir / "quotes.json"
        if not quotes_file.exists():
            return 0.0

        with open(quotes_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        quotes = data.get("quotes", [])
        created = datetime.strptime(goal["created_at"], "%Y-%m-%d")
        deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d")

        total = 0.0
        for quote in quotes:
            if quote.get("status") in ["approved", "paid"]:
                date = quote.get("approved_at") or quote.get("created_at")
                amount = quote.get("total", 0)
                if date:
                    try:
                        fdt = datetime.strptime(date, "%Y-%m-%d")
                        if created <= fdt <= deadline:
                            total += amount
                    except ValueError:
                        pass

        return total

    def get_goals_summary(self, type: Optional[str] = None) -> Dict[str, Any]:
        """Generate executive summary of goals."""
        goals = self.get_goals(type=type)
        active = [g for g in goals if g["status"] == "active"]
        met = [g for g in goals if g["status"] == "met"]
        missed = [g for g in goals if g["status"] == "missed"]

        today = datetime.now().date()
        urgent = []
        for goal in active:
            try:
                deadline = datetime.strptime(goal["deadline"], "%Y-%m-%d").date()
                days_left = (deadline - today).days
                if days_left <= 2:
                    urgent.append({**goal, "days_left": days_left})
            except ValueError:
                pass

        return {
            "total": len(goals),
            "active": len(active),
            "met": len(met),
            "missed": len(missed),
            "urgent": urgent,
            "by_department": self._group_by_department(goals),
            "average_progress": self._calculate_average_progress(active) if active else 0,
        }

    def _group_by_department(
        self, goals: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, int]]:
        result: Dict[str, Dict[str, int]] = {}
        for goal in goals:
            dep = goal.get("department", "general")
            if dep not in result:
                result[dep] = {"total": 0, "active": 0, "met": 0}
            result[dep]["total"] += 1
            if goal["status"] == "active":
                result[dep]["active"] += 1
            elif goal["status"] == "met":
                result[dep]["met"] += 1
        return result

    def _calculate_average_progress(self, goals: List[Dict[str, Any]]) -> float:
        if not goals:
            return 0.0
        total = sum(
            g["progress"] / g["target"] * 100 if g["target"] > 0 else 0 for g in goals
        )
        return round(total / len(goals), 1)

    def close_goal(
        self, goal_id: str, status: str = "met", notes: str = ""
    ) -> Optional[Dict[str, Any]]:
        """Close a goal manually."""
        goals = self._load_goals()
        for goal in goals:
            if goal["id"] == goal_id:
                goal["status"] = status
                goal["notes"] = notes
                self._save_goals(goals)
                return goal
        return None

    def suggest_weekly_goals(self) -> List[Dict[str, Any]]:
        """Suggest goals based on current data."""
        suggestions = []

        pipeline_file = self.data_dir / "pipeline.json"
        if pipeline_file.exists():
            with open(pipeline_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            entries = data.get("entries", [])
            prospects = [e for e in entries if e.get("status") in ["prospect", "quoted"]]
            if len(prospects) >= 3:
                target = min(2, len(prospects))
                suggestions.append({
                    "title": f"Close {target} contracts",
                    "type": "weekly",
                    "department": "sales",
                    "target": target,
                    "unit": "contracts",
                    "reason": f"You have {len(prospects)} active prospects",
                    "kpi_source": "pipeline.contracted",
                })

        tasks_file = self.data_dir / "tasks.json"
        if tasks_file.exists():
            with open(tasks_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            tasks = data.get("tasks", [])
            pending = [t for t in tasks if t.get("status") in ["pending", "in_progress"]]
            if len(pending) >= 5:
                target = min(5, len(pending))
                suggestions.append({
                    "title": f"Complete {target} pending tasks",
                    "type": "weekly",
                    "department": "operations",
                    "target": target,
                    "unit": "tasks",
                    "reason": f"You have {len(pending)} pending tasks",
                    "kpi_source": "tasks.completed",
                })

        return suggestions


# Singleton
_goals_instance = None


def get_goals() -> GoalsEngine:
    """Get or create singleton GoalsEngine instance."""
    global _goals_instance
    if _goals_instance is None:
        _goals_instance = GoalsEngine()
    return _goals_instance


if __name__ == "__main__":
    engine = GoalsEngine()
    goal = engine.create_goal(
        title="Close 2 contracts",
        type="weekly",
        department="sales",
        target=2,
        unit="contracts",
        kpi_source="pipeline.contracted",
    )
    print(f"Goal created: {goal['id']}")
    print(f"Summary: {engine.get_goals_summary()}")
