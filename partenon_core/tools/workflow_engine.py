"""
Partenon Workflow Engine.

Handles events, triggers, and automatic handoffs between hero profiles.
This is the nervous system that makes departments talk to each other.
"""

import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

# Add paths for imports from other skills
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"


@dataclass
class Event:
    id: str
    type: str
    source: str
    entity_id: str
    entity_type: str
    data: dict
    timestamp: str
    processed: bool = False
    actions_executed: List[str] = None

    def __post_init__(self):
        if self.actions_executed is None:
            self.actions_executed = []


class WorkflowEngine:
    """Event-driven workflow engine."""

    WORKFLOWS = [
        {
            "id": "wf_contracted_to_project",
            "name": "Client contracted → Create project",
            "trigger": "client_contracted",
            "condition": None,
            "actions": [
                "create_operations_project",
                "create_initiative_goal",
                "generate_checklist",
                "notify_user",
            ],
        },
        {
            "id": "wf_task_overdue",
            "name": "Task overdue → Alert, reschedule, and notify Slack",
            "trigger": "task_overdue",
            "condition": None,
            "actions": ["urgent_nudge", "suggest_reschedule", "notify_slack"],
        },
        {
            "id": "wf_pipeline_stalled",
            "name": "Pipeline stalled → Nudge",
            "trigger": "pipeline_stalled",
            "condition": "days_without_movement >= 3",
            "actions": ["nudge_pipeline", "suggest_campaign"],
        },
        {
            "id": "wf_quote_approved",
            "name": "Quote approved → Documents + Finance",
            "trigger": "quote_approved",
            "condition": None,
            "actions": [
                "generate_contract",
                "register_expected_income",
                "create_project",
            ],
        },
        {
            "id": "wf_project_50pct",
            "name": "Project 50% → Risk review",
            "trigger": "project_progress_50",
            "condition": None,
            "actions": ["review_deadlines", "alert_if_behind"],
        },
        {
            "id": "wf_new_lead",
            "name": "New lead → Welcome + Task",
            "trigger": "new_client",
            "condition": None,
            "actions": ["register_client", "create_follow_up_task", "welcome_nudge"],
        },
        {
            "id": "wf_handoff_payment_confirmed",
            "name": "Collector confirms payment → Notify Scribe",
            "trigger": "payment_confirmed",
            "condition": None,
            "actions": ["notify_scribe_of_payment"],
        },
        {
            "id": "wf_handoff_budget_requested",
            "name": "Herald requests campaign budget → Notify Scribe",
            "trigger": "campaign_budget_requested",
            "condition": None,
            "actions": ["notify_scribe_of_budget_request"],
        },
        {
            "id": "wf_handoff_agreement_reached",
            "name": "Diplomat reaches agreement → Create project in Ops",
            "trigger": "agreement_reached",
            "condition": None,
            "actions": ["create_operations_project", "notify_strategist_of_deal"],
        },
        {
            "id": "wf_handoff_milestone_due",
            "name": "Strategist milestone due soon → Notify Diplomat",
            "trigger": "milestone_due_soon",
            "condition": None,
            "actions": ["notify_diplomat_of_milestone"],
        },
        {
            "id": "wf_handoff_key_rotation",
            "name": "Guardian flags key rotation → Notify affected profiles",
            "trigger": "key_rotation_required",
            "condition": None,
            "actions": ["notify_profiles_of_key_rotation"],
        },
        {
            "id": "wf_handoff_learning_recorded",
            "name": "Brain records learning → Suggest actions to relevant hero",
            "trigger": "learning_recorded",
            "condition": None,
            "actions": ["notify_relevant_hero_of_learning"],
        },
    ]

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else DATA_DIR
        self.events_file = self.data_dir / "events.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.events_file.exists():
            self._save_events([])

    def _load_events(self) -> list:
        try:
            with open(self.events_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("events", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_events(self, events: list):
        with open(self.events_file, "w", encoding="utf-8") as f:
            json.dump(
                {"events": events, "updated_at": datetime.now().isoformat()},
                f,
                indent=2,
                ensure_ascii=False,
            )

    def _load_json(self, filename: str) -> dict:
        try:
            with open(self.data_dir / filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def emit_event(
        self,
        type: str,
        source: str,
        entity_id: str,
        entity_type: str,
        data: dict = None,
    ) -> dict:
        """Emit a new event into the system."""
        event = Event(
            id=f"EVT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{type}",
            type=type,
            source=source,
            entity_id=entity_id,
            entity_type=entity_type,
            data=data or {},
            timestamp=datetime.now().isoformat(),
        )

        events = self._load_events()
        events.append(asdict(event))
        self._save_events(events)

        actions = self.process_event(asdict(event))
        event.actions_executed = actions

        events = self._load_events()
        for e in events:
            if e["id"] == event.id:
                e["actions_executed"] = actions
        self._save_events(events)

        return asdict(event)

    def process_event(self, event: dict) -> List[str]:
        """Process an event by executing matching workflows."""
        actions_executed = []

        for workflow in self.WORKFLOWS:
            if workflow["trigger"] == event["type"]:
                if self._evaluate_condition(workflow.get("condition"), event):
                    for action in workflow["actions"]:
                        try:
                            result = self._execute_action(action, event)
                            if result:
                                actions_executed.append(f"{workflow['id']}.{action}")
                        except Exception as e:
                            actions_executed.append(
                                f"{workflow['id']}.{action}:ERROR:{str(e)}"
                            )

        events = self._load_events()
        for e in events:
            if e["id"] == event["id"]:
                e["processed"] = True
                e["actions_executed"] = actions_executed
        self._save_events(events)

        return actions_executed

    def _evaluate_condition(self, condition: Optional[str], event: dict) -> bool:
        if not condition:
            return True
        if "days_without_movement >= 3" in condition:
            return event.get("data", {}).get("days_without_movement", 0) >= 3
        return True

    def _execute_action(self, action: str, event: dict) -> bool:
        data = event.get("data", {})
        handlers = {
            "create_operations_project": self._action_create_project,
            "create_initiative_goal": self._action_create_goal,
            "generate_checklist": self._action_generate_checklist,
            "notify_user": self._action_notify,
            "urgent_nudge": lambda d: self._action_nudge(event, "critical"),
            "suggest_reschedule": self._action_suggest_reschedule,
            "nudge_pipeline": lambda d: self._action_nudge(event, "medium"),
            "suggest_campaign": self._action_suggest_campaign,
            "generate_contract": self._action_generate_contract,
            "register_expected_income": self._action_register_income,
            "create_project": self._action_create_project,
            "review_deadlines": self._action_review_deadlines,
            "alert_if_behind": self._action_alert_behind,
            "register_client": self._action_register_client,
            "create_follow_up_task": self._action_create_follow_up_task,
            "welcome_nudge": lambda d: self._action_nudge(event, "low"),
            "notify_slack": lambda d: self._action_notify_slack(event),
            "notify_scribe_of_payment": lambda d: self._action_handoff_nudge(
                event, "scribe", "Payment confirmed; record as income."
            ),
            "notify_scribe_of_budget_request": lambda d: self._action_handoff_nudge(
                event, "scribe", "Herald requested campaign budget validation."
            ),
            "notify_strategist_of_deal": lambda d: self._action_handoff_nudge(
                event, "strategist", "Diplomat closed an agreement; create project and tasks."
            ),
            "notify_diplomat_of_milestone": lambda d: self._action_handoff_nudge(
                event, "diplomat", "Client milestone is due soon; confirm with the client."
            ),
            "notify_profiles_of_key_rotation": lambda d: self._action_handoff_nudge(
                event, "all", "Guardian flagged a key rotation; review affected integrations."
            ),
            "notify_relevant_hero_of_learning": lambda d: self._action_handoff_nudge(
                event, data.get("target_profile", "all"), "Brain recorded a learning relevant to your domain."
            ),
        }
        handler = handlers.get(action)
        return handler(data) if handler else False

    def _action_create_project(self, data: dict) -> bool:
        projects_file = self.data_dir / "projects.json"
        projects_data = self._load_json("projects.json")
        projects = projects_data.get("projects", [])
        next_id = len(projects) + 1
        project = {
            "id": f"PROJ-{next_id:03d}",
            "name": data.get("project_name", f"Project {data.get('client_name', 'New')}"),
            "client_id": data.get("client_id", ""),
            "client_name": data.get("client_name", ""),
            "status": "planned",
            "progress": 0,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "delivery_date": data.get(
                "delivery_date",
                (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            ),
            "description": data.get("description", ""),
            "amount": data.get("amount", 0),
        }
        projects.append(project)
        projects_data["projects"] = projects
        with open(projects_file, "w", encoding="utf-8") as f:
            json.dump(projects_data, f, indent=2, ensure_ascii=False)
        return True

    def _action_create_goal(self, data: dict) -> bool:
        goals_file = self.data_dir / "goals.json"
        goals_data = self._load_json("goals.json")
        goals = goals_data.get("goals", [])
        goal = {
            "id": f"GOAL-{len(goals) + 1:03d}",
            "title": f"Deliver {data.get('project_name', 'project')} on time",
            "type": "weekly",
            "department": "operations",
            "target": 1,
            "unit": "project",
            "created_at": datetime.now().isoformat(),
        }
        goals.append(goal)
        goals_data["goals"] = goals
        with open(goals_file, "w", encoding="utf-8") as f:
            json.dump(goals_data, f, indent=2, ensure_ascii=False)
        return True

    def _action_generate_checklist(self, data: dict) -> bool:
        checklists_file = self.data_dir / "checklists.json"
        checklists_data = self._load_json("checklists.json")
        checklists = checklists_data.get("checklists", [])
        checklist = {
            "id": f"CHK-{len(checklists) + 1:03d}",
            "project_id": data.get("project_id", ""),
            "title": f"Checklist {data.get('project_name', 'Project')}",
            "items": [
                {"title": "Define scope", "completed": False},
                {"title": "Assign owners", "completed": False},
                {"title": "Set key dates", "completed": False},
                {"title": "Client communication", "completed": False},
                {"title": "Administrative closure", "completed": False},
            ],
            "created": datetime.now().strftime("%Y-%m-%d"),
        }
        checklists.append(checklist)
        checklists_data["checklists"] = checklists
        with open(checklists_file, "w", encoding="utf-8") as f:
            json.dump(checklists_data, f, indent=2, ensure_ascii=False)
        return True

    def _action_notify(self, event: dict) -> bool:
        return True

    def _action_notify_slack(self, event: dict) -> bool:
        try:
            from mcp_servers.notifications.slack import notify_task_overdue

            data = event.get("data", {})
            result = notify_task_overdue(
                event.get("entity_id", "unknown"),
                data.get("title", "Unknown task"),
                data.get("due_date", "unknown"),
            )
            return bool(result.get("ok"))
        except Exception:
            return False

    def _action_handoff_nudge(self, event: dict, target: str, message: str) -> bool:
        nudges_file = self.data_dir / "nudges.json"
        nudges_data = self._load_json("nudges.json")
        nudges = nudges_data.get("nudges", [])
        nudge = {
            "id": f"NUD-{len(nudges) + 1:03d}",
            "event_id": event.get("id"),
            "type": "handoff",
            "target_profile": target,
            "urgency": "medium",
            "message": message,
            "created_at": datetime.now().isoformat(),
        }
        nudges.append(nudge)
        nudges_data["nudges"] = nudges
        with open(nudges_file, "w", encoding="utf-8") as f:
            json.dump(nudges_data, f, indent=2, ensure_ascii=False)
        return True

    def _action_nudge(self, event: dict, urgency: str) -> bool:
        nudges_file = self.data_dir / "nudges.json"
        nudges_data = self._load_json("nudges.json")
        nudges = nudges_data.get("nudges", [])
        nudge = {
            "id": f"NUD-{len(nudges) + 1:03d}",
            "event_id": event.get("id"),
            "urgency": urgency,
            "message": f"Nudge for {event.get('entity_id')}",
            "created_at": datetime.now().isoformat(),
        }
        nudges.append(nudge)
        nudges_data["nudges"] = nudges
        with open(nudges_file, "w", encoding="utf-8") as f:
            json.dump(nudges_data, f, indent=2, ensure_ascii=False)
        return True

    def _action_suggest_reschedule(self, data: dict) -> bool:
        return True

    def _action_suggest_campaign(self, data: dict) -> bool:
        return True

    def _action_generate_contract(self, data: dict) -> bool:
        return True

    def _action_register_income(self, data: dict) -> bool:
        return True

    def _action_review_deadlines(self, data: dict) -> bool:
        return True

    def _action_alert_behind(self, data: dict) -> bool:
        return True

    def _action_register_client(self, data: dict) -> bool:
        clients_file = self.data_dir / "clients.json"
        clients_data = self._load_json("clients.json")
        clients = clients_data.get("clients", [])
        next_id = len(clients) + 1
        client = {
            "id": f"CLI-{next_id:03d}",
            "name": data.get("name", "New Client"),
            "email": data.get("email", ""),
            "phone": data.get("phone", ""),
            "status": "lead",
            "registration_date": datetime.now().strftime("%Y-%m-%d"),
            "source": data.get("source", "unknown"),
        }
        clients.append(client)
        clients_data["clients"] = clients
        with open(clients_file, "w", encoding="utf-8") as f:
            json.dump(clients_data, f, indent=2, ensure_ascii=False)
        return True

    def _load_list(self, filename: str) -> list:
        try:
            with open(self.data_dir / filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_list(self, filename: str, items: list) -> None:
        with open(self.data_dir / filename, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)

    def _action_create_follow_up_task(self, data: dict) -> bool:
        missions = self._load_list("missions.json")
        mission = {
            "id": f"MISSION-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "profile": "partenon-diplomat",
            "title": f"Follow up with {data.get('name', 'new lead')}",
            "status": "to_do",
            "priority": "high",
            "description": "Auto-generated follow-up from workflow engine.",
            "due_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "workspace_id": "default",
        }
        missions.append(mission)
        self._save_list("missions.json", missions)
        return True

    def detect_automatic_events(self) -> List[dict]:
        """Scan data and detect events that should be emitted."""
        detected_events = []
        today = datetime.now()

        missions = self._load_list("missions.json")
        for task in missions:
            if task.get("status") in ["pending", "in_progress", "blocked", "to_do", "backlog"]:
                due_date = task.get("due_date")
                if due_date and due_date < today.strftime("%Y-%m-%d"):
                    detected_events.append(
                        self.emit_event(
                            type="task_overdue",
                            source="workflow_engine",
                            entity_id=task["id"],
                            entity_type="task",
                            data={
                                "title": task["title"],
                                "days_overdue": (
                                    today - datetime.strptime(due_date, "%Y-%m-%d")
                                ).days,
                            },
                        )
                    )

        pipeline_data = self._load_json("pipeline.json")
        entries = pipeline_data.get("entries", [])
        if entries:
            cutoff = (today - timedelta(days=3)).strftime("%Y-%m-%d")
            stalled = all(
                (entry.get("updated_at") or entry.get("created_at", "")) < cutoff
                for entry in entries
            )
            if stalled:
                detected_events.append(
                    self.emit_event(
                        type="pipeline_stalled",
                        source="workflow_engine",
                        entity_id="pipeline",
                        entity_type="pipeline",
                        data={"days_without_movement": 3},
                    )
                )

        return detected_events


def main() -> int:
    """CLI entry point for the workflow engine."""
    engine = WorkflowEngine()
    event = engine.emit_event(
        type="client_contracted",
        source="hermes-sales",
        entity_id="CLI-001",
        entity_type="client",
        data={
            "client_id": "CLI-001",
            "client_name": "Acme Inc",
            "project_name": "Website Redesign",
            "amount": 25000,
            "delivery_date": "2026-10-15",
        },
    )
    print(f"Event emitted: {event['id']}")
    print(f"Actions executed: {event.get('actions_executed', [])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
