#!/usr/bin/env python3
"""
Simulation runner for Partenon workshop scenarios.

Usage:
    python3 workshop/simulations/sim_runner.py <action> [args...]

Each action works inside a workspace directory so different case studies do
not overwrite the main project data files.
"""

import importlib.util
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACES = Path(__file__).resolve().parent / "workspaces"


def _load_module(module_name: str, relative_path: str):
    """Load a tool module by path without requiring package __init__ files."""
    path = REPO_ROOT / relative_path
    if not path.exists():
        raise FileNotFoundError(f"Tool not found: {path}")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    # Add the tool's own directory to sys.path so its fallback imports work.
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def _workspace_path(name: str) -> Path:
    ws = WORKSPACES / name
    ws.mkdir(parents=True, exist_ok=True)
    config = ws / "config"
    config.mkdir(parents=True, exist_ok=True)
    company_yaml = config / "company.yaml"
    if not company_yaml.exists():
        company_yaml.write_text(
            f"company:\n  name: {name}\n  industry: services\n  currency: USD\n  timezone: America/Los_Angeles\n",
            encoding="utf-8",
        )
    return ws


def _data_dir(workspace: Path) -> Path:
    d = workspace / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _init_json(path: Path, default: Dict[str, Any]):
    if not path.exists():
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")


def _prepare_data_dir(workspace: Path):
    d = _data_dir(workspace)
    defaults = {
        "projects.json": {"projects": [], "next_id": 1},
        "tasks.json": {"tasks": [], "next_id": 1},
        "checklists.json": {},
        "clients.json": {"clients": [], "next_id": 1},
        "projects.json": {"projects": [], "next_id": 1},
        "tasks.json": {"tasks": [], "next_id": 1},
        "quotes.json": {"quotes": [], "next_num": 1},
        "pipeline.json": {"entries": []},
        "events.json": {"events": []},
        "nudges.json": {"nudges": []},
        "goals.json": {"goals": []},
    }
    for filename, default in defaults.items():
        _init_json(d / filename, default)
    return d


def _projects(workspace: Path):
    d = _prepare_data_dir(workspace)
    module = _load_module("projects_tool", "hermes/profiles/partenon-estratega/skills/ops/tools/projects.py")
    inst = module.Projects()
    inst.data_dir = d
    inst.projects_file = d / "projects.json"
    inst._projects = None
    return inst


def _tasks(workspace: Path):
    d = _prepare_data_dir(workspace)
    module = _load_module("tasks_tool", "hermes/profiles/partenon-estratega/skills/ops/tools/tasks.py")
    inst = module.Tasks()
    inst.data_dir = d
    inst.tasks_file = d / "tasks.json"
    inst._tasks = None
    return inst


def _checklists(workspace: Path):
    d = _prepare_data_dir(workspace)
    module = _load_module("checklists_tool", "hermes/profiles/partenon-estratega/skills/ops/tools/checklists.py")
    inst = module.Checklists()
    inst.data_dir = d
    inst.checklists_file = d / "checklists.json"
    inst._checklists = None
    return inst


def _relations(workspace: Path):
    d = _prepare_data_dir(workspace)
    relations_file = workspace / ".relations"
    if not relations_file.exists():
        relations_file.write_text(
            json.dumps(
                {
                    "company": workspace.name,
                    "updated": datetime.now().isoformat(),
                    "clients": [],
                    "vendors": [],
                    "contracts": [],
                    "communications": [],
                    "reminders": [],
                }
            ),
            encoding="utf-8",
        )
    module = _load_module("crm_tool", "hermes/profiles/partenon-diplomatico/skills/relations/tools/crm.py")
    crm = module.RelationsCRM(relations_file=relations_file)
    crm.data_dir = d
    crm.cache_file = d / "relations_cache.json"

    def _persist_relations():
        crm._sync_cache(crm._cache)
        if crm.relations_file:
            crm.relations_file.write_text(
                json.dumps(crm._cache, ensure_ascii=False, indent=2), encoding="utf-8"
            )

    crm._save = _persist_relations
    return crm


def _stripe_tools(workspace: Path):
    module = _load_module("stripe_tools", "hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py")
    payments_file = workspace / ".payments"
    if not payments_file.exists():
        payments_file.write_text(
            json.dumps(
                {
                    "metadata": {"currency": "USD"},
                    "products": [],
                    "prices": [],
                    "links": [],
                    "subscriptions": [],
                    "customers": [],
                    "payments": [],
                    "invoices": [],
                    "reminders": [],
                }
            ),
            encoding="utf-8",
        )

    def _payments_file(profile_dir=None):
        return payments_file

    module._payments_file = _payments_file
    return module


def _brand_intake(workspace: Path):
    module = _load_module("brand_intake", "hermes/profiles/partenon-mensajero/skills/comms/tools/brand_intake.py")
    return module


def _content_calendar(workspace: Path):
    module = _load_module("content_calendar", "hermes/profiles/partenon-mensajero/skills/comms/tools/content_calendar.py")
    return module


def _workspace_currency(workspace: Path) -> str:
    config = workspace / "config" / "company.yaml"
    if config.exists():
        try:
            import yaml
            data = yaml.safe_load(config.read_text(encoding="utf-8")) or {}
            return data.get("company", {}).get("currency", "USD")
        except Exception:
            pass
    return "USD"


def _briefings(workspace: Path):
    d = _prepare_data_dir(workspace)
    module = _load_module("briefings", "hermes/profiles/partenon-estratega/skills/ops/tools/briefings.py")
    currency = _workspace_currency(workspace)
    module._default_currency = lambda data_dir: currency
    return module.Briefings(data_dir=str(d))


def _guardian():
    return _load_module("key_manager", "hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py")


def _router():
    return _load_module("router", "partenon-core/tools/router.py")


def action_route(args):
    message = " ".join(args)
    module = _router()
    result = module.route_intent(message)
    print(json.dumps({"message": message, "profile": result}, ensure_ascii=False, indent=2))


def action_design(args):
    workspace = _workspace_path(args[0])
    module = _brand_intake(workspace)
    answers = {
        "brand_name": args[1],
        "industry": args[2],
        "market": args[3],
        "what_you_sell": args[4],
        "who_you_help": args[5],
        "how_you_do_it": args[6],
        "tone": args[7],
        "addressing": args[8],
        "final_approver": args[9],
    }
    if len(args) > 10:
        answers["channels"] = args[10]
    design_path = workspace / ".design"
    result = module.generate_design_from_dict(answers, design_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_project(args):
    workspace = _workspace_path(args[0])
    name, client_name, delivery_date, amount = args[1], args[2], args[3], float(args[4])
    industry = args[5] if len(args) > 5 else "consulting"
    p = _projects(workspace)
    result = p.create_project(
        name=name,
        client_name=client_name,
        delivery_date=delivery_date,
        amount=amount,
        type=industry,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_task(args):
    workspace = _workspace_path(args[0])
    project_id, title, assignee, due_date = args[1], args[2], args[3], args[4]
    priority = args[5] if len(args) > 5 else "medium"
    t = _tasks(workspace)
    result = t.create_task(project_id=project_id, title=title, assignee=assignee, due_date=due_date, priority=priority)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_checklist(args):
    workspace = _workspace_path(args[0])
    project_id = args[1]
    industry = args[2] if len(args) > 2 else None
    c = _checklists(workspace)
    result = c.create_project_checklist(project_id, industry=industry)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_client(args):
    workspace = _workspace_path(args[0])
    name, email = args[1], args[2]
    category = args[3] if len(args) > 3 else "client"
    crm = _relations(workspace)
    result = crm.add_client(name, email=email, category=category)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_vendor(args):
    workspace = _workspace_path(args[0])
    name = args[1]
    category = args[2] if len(args) > 2 else "supplier"
    crm = _relations(workspace)
    result = crm.add_vendor(name, category=category)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_milestone(args):
    workspace = _workspace_path(args[0])
    entity_id, description, date = args[1], args[2], args[3]
    crm = _relations(workspace)
    result = crm.add_milestone(entity_id, description, date)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_followups(args):
    workspace = _workspace_path(args[0])
    crm_module = _load_module("followups", "hermes/profiles/partenon-diplomatico/skills/relations/tools/followups.py")
    crm = _relations(workspace)
    result = crm_module.run_daily_followups(crm=crm)
    print(json.dumps({"total": result["total"], "report": result["report"]}, ensure_ascii=False, indent=2))


def action_payment_link(args):
    workspace = _workspace_path(args[0])
    product_name = args[1]
    amount = int(args[2])
    currency = args[3] if len(args) > 3 else "usd"
    module = _stripe_tools(workspace)
    result = module.create_payment_link({"name": product_name}, {"amount": amount, "currency": currency})
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_invoice(args):
    workspace = _workspace_path(args[0])
    email = args[1]
    description = args[2]
    amount = int(args[3])
    currency = args[4] if len(args) > 4 else "usd"
    module = _stripe_tools(workspace)
    result = module.create_invoice({"email": email}, [{"description": description, "amount": amount, "currency": currency}])
    print(json.dumps(result, ensure_ascii=False, indent=2))


def action_keys(args):
    module = _guardian()
    print(json.dumps(module.list_keys(), ensure_ascii=False, indent=2))


def action_briefing(args):
    workspace = _workspace_path(args[0])
    kind = args[1] if len(args) > 1 else "morning"
    b = _briefings(workspace)
    method = {
        "morning": b.generate_morning_briefing,
        "midday": b.generate_midday_pulse,
        "evening": b.generate_evening_wrap,
        "weekly_planning": b.generate_weekly_planning,
        "weekly_retro": b.generate_weekly_retro,
    }.get(kind)
    if not method:
        raise SystemExit(f"Unknown briefing kind: {kind}")
    print(method("Owner"))


def action_calendar(args):
    workspace = _workspace_path(args[0])
    topic = args[1]
    channels = args[2].split(",")
    days = int(args[3])
    module = _content_calendar(workspace)
    design_path = workspace / ".design"
    brand_context = module.load_design(design_path)
    calendar = module.generate_calendar(topic, channels, days, brand_context)
    out_dir = workspace / "output" / "campaigns"
    path = module.save_calendar(calendar, out_dir)
    print(
        json.dumps(
            {
                "campaign_id": calendar["campaign_id"],
                "calendar_path": str(path),
                "days": days,
                "channels": channels,
                "sample_day": calendar["calendar"][0] if calendar["calendar"] else None,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def action_summary(args):
    workspace = _workspace_path(args[0])
    p = _projects(workspace)
    t = _tasks(workspace)
    print(
        json.dumps(
            {
                "projects": p.get_projects_summary(),
                "tasks": t.get_tasks_summary(),
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )


ACTIONS = {
    "route": action_route,
    "design": action_design,
    "project": action_project,
    "task": action_task,
    "checklist": action_checklist,
    "client": action_client,
    "vendor": action_vendor,
    "milestone": action_milestone,
    "followups": action_followups,
    "payment-link": action_payment_link,
    "invoice": action_invoice,
    "keys": action_keys,
    "briefing": action_briefing,
    "calendar": action_calendar,
    "summary": action_summary,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Actions:", ", ".join(sorted(ACTIONS)))
        sys.exit(0)

    action = sys.argv[1]
    args = sys.argv[2:]
    fn = ACTIONS.get(action)
    if not fn:
        print(f"Unknown action: {action}", file=sys.stderr)
        print("Available:", ", ".join(sorted(ACTIONS)), file=sys.stderr)
        sys.exit(1)

    try:
        fn(args)
    except Exception as exc:
        print(json.dumps({"success": False, "error": str(exc)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
