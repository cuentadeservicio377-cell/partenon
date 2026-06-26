"""
Partenon Strategist — Briefings Tool
Generates morning briefing, midday pulse, evening wrap, weekly planning, and weekly retro.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

# Robust import for GoalsEngine: works as package or standalone script.
try:
    from .goals import GoalsEngine
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from goals import GoalsEngine


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


def _load_json(data_dir: Path, filename: str) -> Dict[str, Any]:
    try:
        with open(data_dir / filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _default_currency(data_dir: Path) -> str:
    """Read currency from company.yaml if available."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "partenon-core":
            config_path = parent / "config" / "company.yaml"
            break
        config_path = parent / "partenon-core" / "config" / "company.yaml"
        if config_path.exists():
            break
    else:
        return "MXN"

    if not config_path.exists():
        return "MXN"

    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("company", {}).get("currency", "MXN")
    except Exception:
        return "MXN"


class Briefings:
    """Generates proactive daily and weekly briefings."""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else _resolve_data_dir()
        self.currency = _default_currency(self.data_dir)

    def generate_morning_briefing(self, user_name: str = "Boss") -> str:
        """Generate the morning briefing."""
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")

        goals_data = _load_json(self.data_dir, "goals.json")
        tasks_data = _load_json(self.data_dir, "tasks.json")
        pipeline_data = _load_json(self.data_dir, "pipeline.json")
        projects_data = _load_json(self.data_dir, "projects.json")
        quotes_data = _load_json(self.data_dir, "quotes.json")
        clients_data = _load_json(self.data_dir, "clients.json")

        # 1. Weekly goals
        goals = goals_data.get("goals", [])
        active_goals = [g for g in goals if g["status"] == "active"]
        goals_text = []
        for goal in active_goals[:3]:
            progress = goal["progress"]
            target = goal["target"]
            pct = (progress / target * 100) if target > 0 else 0
            status = "completed" if pct >= 100 else "on track" if pct >= 50 else "behind"
            goals_text.append(
                f"   {goal['title']} -> {progress:.0f}/{target:.0f} ({pct:.0f}%) — {status}"
            )

        if not goals_text:
            goals_text = ["   No active goals. Shall we define one for this week?"]

        # 2. Critical today
        tasks = tasks_data.get("tasks", [])
        critical_today = []
        for task in tasks:
            if task.get("status") in ["pending", "in_progress", "blocked"]:
                due_date = task.get("due_date")
                if due_date == today_str:
                    critical_today.append(f"   {task['title']} (due today)")

        for task in tasks:
            if task.get("status") in ["pending", "in_progress", "blocked"]:
                due_date = task.get("due_date")
                if due_date and due_date < today_str:
                    days = (today - datetime.strptime(due_date, "%Y-%m-%d")).days
                    critical_today.append(f"   {task['title']} (overdue {days} days)")

        entries = pipeline_data.get("entries", [])
        for entry in entries:
            if entry.get("status") == "quoted":
                date = entry.get("updated_at") or entry.get("created_at")
                if date:
                    try:
                        fdt = datetime.strptime(date, "%Y-%m-%d")
                        days = (today - fdt).days
                        if days >= 3:
                            critical_today.append(
                                f"   {entry.get('customer_name', 'Customer')} quoted {days} days ago"
                            )
                    except ValueError:
                        pass

        if not critical_today:
            critical_today = ["   Nothing critical today. Good time to advance projects."]

        # 3. Pipeline
        total_value = sum(e.get("amount", 0) for e in entries)
        num_opps = len(entries)
        by_status: Dict[str, int] = {}
        for e in entries:
            status = e.get("status", "other")
            by_status[status] = by_status.get(status, 0) + 1

        pipeline_text = f"{num_opps} opportunities, {self.currency} {total_value:,.0f} at stake"
        if by_status:
            pipeline_text += f" ({', '.join(f'{v} {k}' for k, v in list(by_status.items())[:3])})"

        # 4. Finances
        quotes = quotes_data.get("quotes", [])
        to_collect = [q for q in quotes if q.get("status") == "approved"]
        total_to_collect = sum(q.get("total", 0) for q in to_collect)
        overdue = []
        for q in to_collect:
            expected_payment = q.get("expected_payment_date")
            if expected_payment and expected_payment < today_str:
                overdue.append(q)

        finances_text = f"{self.currency} {total_to_collect:,.0f} to collect"
        if overdue:
            finances_text += f" ({len(overdue)} overdue{'s' if len(overdue) > 1 else ''})"

        # 5. Alerts
        projects = projects_data.get("projects", [])
        delayed = 0
        for p in projects:
            if p.get("status") in ["planned", "in_progress", "paused"]:
                delivery_date = p.get("delivery_date")
                if delivery_date and delivery_date < today_str:
                    delayed += 1

        alerts = []
        if delayed > 0:
            alerts.append(f"{delayed} delayed project{'s' if delayed > 1 else ''}")

        clients = clients_data.get("clients", [])
        week_start = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")
        new_this_week = [c for c in clients if c.get("created_at", "") >= week_start]
        if not new_this_week:
            alerts.append("0 new clients this week")

        lines = [
            f"Good morning, {user_name}.",
            "",
            "This week's goals:",
        ]
        lines.extend(goals_text)
        lines.append("")
        lines.append("Critical today:")
        lines.extend(critical_today[:5])
        lines.append("")
        lines.append(f"Pipeline: {pipeline_text}")
        lines.append(f"Finances: {finances_text}")

        if alerts:
            lines.append(f"Alerts: {', '.join(alerts)}")

        lines.append("")
        lines.append("Which one do we start with?")

        return "\n".join(lines)

    def generate_midday_pulse(self, user_name: str = "Boss") -> str:
        """Generate the midday pulse."""
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")

        tasks_data = _load_json(self.data_dir, "tasks.json")
        tasks = tasks_data.get("tasks", [])

        done_today = [t for t in tasks if t.get("completed_at") == today_str]
        pending = [
            t for t in tasks
            if t.get("status") in ["pending", "in_progress"]
            and t.get("due_date") == today_str
        ]

        lines = [
            f"How is the morning going, {user_name}?",
            "",
        ]

        if done_today:
            lines.append(f"Done: {len(done_today)} task{'s' if len(done_today) > 1 else ''}")
            for t in done_today[:3]:
                lines.append(f"   - {t['title']}")
        else:
            lines.append("Nothing marked as done yet today.")

        if pending:
            lines.append("")
            lines.append(f"Pending for today: {len(pending)} task{'s' if len(pending) > 1 else ''}")
            for t in pending[:3]:
                lines.append(f"   - {t['title']}")

        lines.append("")
        if done_today:
            lines.append("If you are doing well, great. If not, let's block 30 min now for the most important thing.")
        else:
            lines.append("Do you need help prioritizing what is left of the day?")

        return "\n".join(lines)

    def generate_evening_wrap(self, user_name: str = "Boss") -> str:
        """Generate the evening wrap."""
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        tomorrow = (today + timedelta(days=1)).strftime("%Y-%m-%d")

        tasks_data = _load_json(self.data_dir, "tasks.json")
        tasks = tasks_data.get("tasks", [])

        done_today = [t for t in tasks if t.get("completed_at") == today_str]
        pending_today = [
            t for t in tasks
            if t.get("status") in ["pending", "in_progress"]
            and t.get("due_date") == today_str
        ]
        for_tomorrow = [
            t for t in tasks
            if t.get("status") in ["pending", "in_progress"]
            and t.get("due_date") == tomorrow
        ]

        lines = [
            f"End of day, {user_name}.",
            "",
        ]

        if done_today:
            lines.append(f"Done today: {len(done_today)} task{'s' if len(done_today) > 1 else ''}")
            for t in done_today[:5]:
                lines.append(f"   - {t['title']}")
        else:
            lines.append("Nothing marked as done today. Tomorrow is another day.")

        if pending_today:
            lines.append("")
            lines.append(f"Left pending: {len(pending_today)} task{'s' if len(pending_today) > 1 else ''}")
            for t in pending_today[:3]:
                lines.append(f"   - {t['title']} -> moved to tomorrow")

        if for_tomorrow:
            lines.append("")
            lines.append("For tomorrow:")
            for t in for_tomorrow[:3]:
                lines.append(f"   - {t['title']}")

        lines.append("")
        lines.append("Anything else before closing?")

        return "\n".join(lines)

    def generate_weekly_planning(self, user_name: str = "Boss") -> str:
        """Generate Monday weekly planning."""
        engine = GoalsEngine(str(self.data_dir))
        suggestions = engine.suggest_weekly_goals()

        lines = [
            f"Weekly Planning — {user_name}",
            "",
            "Based on what I see in your business, I suggest these goals:",
            "",
        ]

        for i, s in enumerate(suggestions[:3], 1):
            lines.append(f"{i}. {s['title']}")
            lines.append(f"   Reason: {s['reason']}")
            lines.append(f"   Department: {s['department']}")
            lines.append("")

        if not suggestions:
            lines.append("I don't have enough data to suggest goals.")
            lines.append("What do you want to achieve this week?")

        lines.append("Tell me which ones you accept or propose your own.")

        return "\n".join(lines)

    def generate_weekly_retro(self, user_name: str = "Boss") -> str:
        """Generate Sunday weekly retro."""
        today = datetime.now()
        week_start = (today - timedelta(days=today.weekday())).strftime("%Y-%m-%d")

        goals_data = _load_json(self.data_dir, "goals.json")
        tasks_data = _load_json(self.data_dir, "tasks.json")
        pipeline_data = _load_json(self.data_dir, "pipeline.json")
        projects_data = _load_json(self.data_dir, "projects.json")

        goals = goals_data.get("goals", [])
        goals_text = []
        for goal in goals:
            pct = (goal["progress"] / goal["target"] * 100) if goal["target"] > 0 else 0
            if goal["status"] == "completed":
                goals_text.append(f"   Completed: {goal['title']} -> {goal['progress']:.0f}/{goal['target']:.0f}")
            elif goal["status"] == "active":
                goals_text.append(f"   Active: {goal['title']} -> {pct:.0f}%")
            elif goal["status"] == "missed":
                goals_text.append(f"   Missed: {goal['title']} -> {pct:.0f}%")

        tasks = tasks_data.get("tasks", [])
        completed = [t for t in tasks if t.get("status") == "completed"]
        overdue = [
            t for t in tasks
            if t.get("status") in ["pending", "in_progress", "blocked"]
            and t.get("due_date", "") < today.strftime("%Y-%m-%d")
        ]

        entries = pipeline_data.get("entries", [])
        new_leads = len([e for e in entries if e.get("created_at", "") >= week_start])
        quoted = len([e for e in entries if e.get("status") == "quoted"])
        closed = len([e for e in entries if e.get("status") == "closed"])
        closed_amount = sum(e.get("amount", 0) for e in entries if e.get("status") == "closed")

        projects = projects_data.get("projects", [])
        delayed = 0
        for p in projects:
            if p.get("status") in ["planned", "in_progress", "paused"]:
                delivery_date = p.get("delivery_date")
                if delivery_date and delivery_date < today.strftime("%Y-%m-%d"):
                    delayed += 1

        lines = [
            f"Weekly Retro — Week of {week_start}",
            "",
            "Goals:",
        ]
        if goals_text:
            lines.extend(goals_text)
        else:
            lines.append("   No goals recorded this week.")

        lines.extend([
            "",
            "Numbers:",
            f"   New leads: {new_leads}",
            f"   Quotes: {quoted}",
            f"   Closed: {closed} ({self.currency} {closed_amount:,.0f})",
            f"   Tasks completed: {len(completed)}",
            f"   Tasks overdue: {len(overdue)}",
            f"   Delayed projects: {delayed}",
            "",
            "Detected patterns:",
            "   Review after accumulating more data.",
            "",
            "Suggestions for next week:",
            "   1. Review overdue tasks and reassign viable ones.",
            "   2. Identify projects at risk of delay before Wednesday.",
            "",
            "Do we adjust anything?",
        ])

        return "\n".join(lines)


# Singleton
_briefings_instance = None


def get_briefings() -> Briefings:
    """Get or create singleton Briefings instance."""
    global _briefings_instance
    if _briefings_instance is None:
        _briefings_instance = Briefings()
    return _briefings_instance


if __name__ == "__main__":
    mb = Briefings()
    print("=== MORNING BRIEFING ===")
    print(mb.generate_morning_briefing("Pablo"))
    print("\n=== MIDDAY PULSE ===")
    print(mb.generate_midday_pulse("Pablo"))
    print("\n=== EVENING WRAP ===")
    print(mb.generate_evening_wrap("Pablo"))
    print("\n=== WEEKLY PLANNING ===")
    print(mb.generate_weekly_planning("Pablo"))
    print("\n=== WEEKLY RETRO ===")
    print(mb.generate_weekly_retro("Pablo"))
