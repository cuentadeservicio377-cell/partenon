#!/usr/bin/env python3
"""
Partenon Workshop Simulation Runner

Runs hero actions inside isolated per-company workspaces so that
simulations do not pollute partenon_core/data or profile .files.

Usage:
    python3 workshop/simulations/sim_runner.py route "organize my numbers"
    python3 workshop/simulations/sim_runner.py design --name "Example Coffee" --industry coffee
    python3 workshop/simulations/sim_runner.py project --company example --title "Launch cold brew"
    python3 workshop/simulations/sim_runner.py task --company example --project-id PROJ-001 --title "Call roaster"
    python3 workshop/simulations/sim_runner.py checklist --company example --project-id PROJ-001 --industry food
    python3 workshop/simulations/sim_runner.py client --company example --name "Example Client" --email contact@example.test
    python3 workshop/simulations/sim_runner.py vendor --company example --name "Example Vendor" --service packaging
    python3 workshop/simulations/sim_runner.py milestone --company example --entity-id CLI-001 --description "Sign deal"
    python3 workshop/simulations/sim_runner.py followups --company example
    python3 workshop/simulations/sim_runner.py payment-link --company example --product "Sub" --amount 2800
    python3 workshop/simulations/sim_runner.py invoice --company example --email "client@example.test" --items '[{"description":"X","amount":1000}]'
    python3 workshop/simulations/sim_runner.py keys --company example
    python3 workshop/simulations/sim_runner.py briefing --company example
    python3 workshop/simulations/sim_runner.py calendar --company example --topic "automation"
"""

import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKSPACES = REPO_ROOT / "workshop" / "simulations" / "workspaces"


def _load_module(module_name: str, relative_path: str):
    path = REPO_ROOT / relative_path
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


# Load core and hero tool modules.
router = _load_module("router", "partenon_core/tools/router.py")
brand_intake = _load_module("brand_intake", "hermes/profiles/partenon-herald/skills/comms/tools/brand_intake.py")
content_calendar = _load_module("content_calendar", "hermes/profiles/partenon-herald/skills/comms/tools/content_calendar.py")
projects_mod = _load_module("projects", "hermes/profiles/partenon-strategist/skills/ops/tools/projects.py")
tasks_mod = _load_module("tasks", "hermes/profiles/partenon-strategist/skills/ops/tools/tasks.py")
checklists_mod = _load_module("checklists", "hermes/profiles/partenon-strategist/skills/ops/tools/checklists.py")
briefings_mod = _load_module("briefings", "hermes/profiles/partenon-strategist/skills/ops/tools/briefings.py")
crm_mod = _load_module("crm", "hermes/profiles/partenon-diplomat/skills/relations/tools/crm.py")
followups_mod = _load_module("followups", "hermes/profiles/partenon-diplomat/skills/relations/tools/followups.py")
stripe_mod = _load_module("stripe_tools", "hermes/profiles/partenon-collector/skills/payments/tools/stripe_tools.py")
key_manager = _load_module("key_manager", "hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py")


def _workspace(company: str) -> Path:
    ws = WORKSPACES / company
    ws.mkdir(parents=True, exist_ok=True)
    return ws


def _data_dir(company: str) -> Path:
    d = _workspace(company) / "data"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _patch_data_dir(company: str):
    """Force Strategist tools to write into the isolated workspace."""
    data_dir = _data_dir(company)

    def resolver():
        return data_dir

    projects_mod._resolve_data_dir = resolver
    tasks_mod._resolve_data_dir = resolver
    checklists_mod._resolve_data_dir = resolver
    briefings_mod._resolve_data_dir = resolver


def _patch_payments_file(company: str):
    """Force Collector tools to write into the isolated workspace."""
    payments_file = _workspace(company) / ".payments"

    def payments_path(profile_dir=None):
        return payments_file

    stripe_mod._payments_file = payments_path


def _setup_env(company: str):
    ws = _workspace(company)
    os.environ["PARTENON_DATA_DIR"] = str(_data_dir(company))
    os.environ["PARTENON_RELATIONS_FILE"] = str(ws / ".relations")
    os.chdir(ws)


def _json_out(result: Any):
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

def action_route(args):
    profile = router.route_intent(" ".join(args.message))
    _json_out({"profile": profile})


def action_design(args):
    _workspace(args.company)
    _setup_env(args.company)
    answers = {
        "brand_name": args.name,
        "what_you_sell": args.sell or f"Products and services for the {args.industry} industry",
        "who_you_help": args.who or "Small business owners and operators",
        "how_you_do_it": args.how or "Through a structured process and clear communication",
        "market": args.market or "Local / regional",
        "tone": args.tone or "direct",
        "addressing": args.addressing or "you informal",
        "final_approver": args.approver or "Founder",
        "channels": args.channels or "",
    }
    if args.industry:
        answers["industry"] = args.industry
    result = brand_intake.generate_design_from_dict(answers, Path(".design"))
    _json_out(result)


def action_project(args):
    _setup_env(args.company)
    _patch_data_dir(args.company)
    projects = projects_mod.Projects()
    result = projects.create_project(
        name=args.title,
        description=args.description or "",
        type=args.industry or "consulting",
        amount=args.amount or 0,
    )
    _json_out(result)


def action_task(args):
    _setup_env(args.company)
    _patch_data_dir(args.company)
    tasks = tasks_mod.Tasks()
    result = tasks.create_task(
        project_id=args.project_id,
        title=args.title,
        description=args.description or "",
        priority=args.priority or "medium",
        due_date=args.due_date or None,
    )
    _json_out(result)


def action_checklist(args):
    _setup_env(args.company)
    _patch_data_dir(args.company)
    checklists = checklists_mod.Checklists()
    result = checklists.create_project_checklist(
        project_id=args.project_id,
        industry=args.industry or "consulting",
    )
    _json_out(result)


def action_client(args):
    _setup_env(args.company)
    crm = crm_mod.RelationsCRM()
    result = crm.add_client(
        name=args.name,
        email=args.email or "",
        phone=args.phone or "",
        category=args.category or "",
        notes=args.notes or "",
    )
    _json_out(result)


def action_vendor(args):
    _setup_env(args.company)
    crm = crm_mod.RelationsCRM()
    result = crm.add_vendor(
        name=args.name,
        email=args.email or "",
        phone=args.phone or "",
        category=args.category or "",
        service=args.service or "",
        notes=args.notes or "",
    )
    _json_out(result)


def action_milestone(args):
    _setup_env(args.company)
    crm = crm_mod.RelationsCRM()
    result = crm.add_milestone(
        entity_id=args.entity_id,
        description=args.description,
        date=args.date,
        responsible=args.responsible or "Diplomat",
        next_step=args.next_step or "",
    )
    _json_out(result)


def action_followups(args):
    _setup_env(args.company)
    result = followups_mod.run_daily_followups()
    _json_out({"success": True, "report": result["report"], "total": result["total"]})


def action_payment_link(args):
    _setup_env(args.company)
    _patch_payments_file(args.company)
    result = stripe_mod.create_payment_link(
        product={"name": args.product, "description": args.description or ""},
        price={"amount": int(args.amount), "currency": args.currency or "mxn"},
    )
    _json_out(result)


def action_invoice(args):
    _setup_env(args.company)
    _patch_payments_file(args.company)
    items = json.loads(args.items)
    result = stripe_mod.create_invoice(
        customer={"email": args.email, "name": args.name or ""},
        items=items,
    )
    _json_out(result)


def action_keys(args):
    _setup_env(args.company)
    keys = key_manager.list_keys()
    profiles = [
        "partenon-guardian",
        "partenon-scribe",
        "partenon-herald",
        "partenon-collector",
        "partenon-strategist",
        "partenon-diplomat",
        "partenon-brain",
    ]
    audits = {p: key_manager.audit_access(p) for p in profiles}
    _json_out({"keys": keys, "audits": audits})


def action_briefing(args):
    _setup_env(args.company)
    _patch_data_dir(args.company)
    briefings = briefings_mod.Briefings()
    text = briefings.generate_morning_briefing(user_name=args.user or "Boss")
    _json_out({"briefing": text})


def action_calendar(args):
    _setup_env(args.company)
    design = content_calendar.load_design(Path(".design"))
    channels = [c.strip() for c in args.channels.split(",")] if args.channels else ["linkedin", "instagram"]
    calendar = content_calendar.generate_calendar(
        topic=args.topic,
        channels=channels,
        days=args.days or 7,
        brand_context=design,
    )
    _json_out({
        "campaign_id": calendar["campaign_id"],
        "days": calendar["duration_days"],
        "channels": calendar["channels"],
        "sample_day": calendar["calendar"][0] if calendar["calendar"] else None,
    })


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
}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Partenon workshop simulation runner")
    subparsers = parser.add_subparsers(dest="action", required=True)

    p_route = subparsers.add_parser("route", help="Route a message to a hero")
    p_route.add_argument("message", nargs="+", help="User message")

    p_design = subparsers.add_parser("design", help="Run Herald brand interview")
    p_design.add_argument("--company", default="default", help="Workspace name")
    p_design.add_argument("--name", required=True)
    p_design.add_argument("--industry", default="")
    p_design.add_argument("--sell", default="")
    p_design.add_argument("--who", default="")
    p_design.add_argument("--how", default="")
    p_design.add_argument("--market", default="")
    p_design.add_argument("--tone", default="")
    p_design.add_argument("--addressing", default="")
    p_design.add_argument("--approver", default="")
    p_design.add_argument("--channels", default="")

    p_project = subparsers.add_parser("project", help="Create a Strategist project")
    p_project.add_argument("--company", required=True)
    p_project.add_argument("--title", required=True)
    p_project.add_argument("--description", default="")
    p_project.add_argument("--industry", default="consulting")
    p_project.add_argument("--amount", type=float, default=0)

    p_task = subparsers.add_parser("task", help="Create a task")
    p_task.add_argument("--company", required=True)
    p_task.add_argument("--project-id", required=True)
    p_task.add_argument("--title", required=True)
    p_task.add_argument("--description", default="")
    p_task.add_argument("--priority", default="medium")
    p_task.add_argument("--due-date", default=None)

    p_checklist = subparsers.add_parser("checklist", help="Create a project checklist")
    p_checklist.add_argument("--company", required=True)
    p_checklist.add_argument("--project-id", required=True)
    p_checklist.add_argument("--industry", default="consulting")

    for name in ("client", "vendor"):
        p = subparsers.add_parser(name, help=f"Add a {name}")
        p.add_argument("--company", required=True)
        p.add_argument("--name", required=True)
        p.add_argument("--email", default="")
        p.add_argument("--phone", default="")
        p.add_argument("--category", default="")
        p.add_argument("--service", default="")
        p.add_argument("--notes", default="")

    p_milestone = subparsers.add_parser("milestone", help="Add a milestone")
    p_milestone.add_argument("--company", required=True)
    p_milestone.add_argument("--entity-id", required=True)
    p_milestone.add_argument("--description", required=True)
    p_milestone.add_argument("--date", required=True)
    p_milestone.add_argument("--responsible", default="Diplomat")
    p_milestone.add_argument("--next-step", default="")

    p_followups = subparsers.add_parser("followups", help="Run daily follow-ups")
    p_followups.add_argument("--company", required=True)

    p_plink = subparsers.add_parser("payment-link", help="Create a Stripe payment link")
    p_plink.add_argument("--company", required=True)
    p_plink.add_argument("--product", required=True)
    p_plink.add_argument("--amount", type=int, required=True)
    p_plink.add_argument("--description", default="")
    p_plink.add_argument("--currency", default="mxn")

    p_inv = subparsers.add_parser("invoice", help="Create an invoice")
    p_inv.add_argument("--company", required=True)
    p_inv.add_argument("--email", required=True)
    p_inv.add_argument("--items", required=True, help="JSON array of items")
    p_inv.add_argument("--name", default="")

    p_keys = subparsers.add_parser("keys", help="Audit API keys")
    p_keys.add_argument("--company", required=True)

    p_briefing = subparsers.add_parser("briefing", help="Generate morning briefing")
    p_briefing.add_argument("--company", required=True)
    p_briefing.add_argument("--user", default="Boss")

    p_cal = subparsers.add_parser("calendar", help="Generate content calendar")
    p_cal.add_argument("--company", required=True)
    p_cal.add_argument("--topic", required=True)
    p_cal.add_argument("--channels", default="")
    p_cal.add_argument("--days", type=int, default=7)

    args = parser.parse_args(argv)
    ACTIONS[args.action](args)


if __name__ == "__main__":
    main()
