#!/usr/bin/env python3
"""
Hermes CLI stub — Partenon web promise placeholder.

This script demonstrates the `hermes` command-line interface documented on
`web/developers.html` and `web/heroes.html`. It is NOT a real Hermes Agent CLI;
it exists so visitors can see the intended command shape while the production
CLI is implemented by the `scripts-core-install` scope.

Supported commands (stubs):
  hermes init --name "Enterprise Name"
  hermes activate <hero>
  hermes deactivate <hero>
  hermes mission <hero> --type <mission-type> [options]
  hermes status [--verbose]
  hermes dashboard [--port 3000]
  hermes test [--all]
  hermes config --edit
  hermes backup --to google-drive

Usage:
  python examples/hermes-cli-stub.py init --name "Cafe Central"
  python examples/hermes-cli-stub.py activate scribe
  python examples/hermes-cli-stub.py mission scribe --type financial-model
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

HEROES = [
    "scribe",
    "herald",
    "collector",
    "guardian",
    "strategist",
    "diplomat",
    "brain",
]

MISSION_TEMPLATES = {
    "scribe": ["financial-model", "dashboard", "expense-audit"],
    "herald": ["brand-strategy", "content-calendar", "seo-audit"],
    "collector": ["payment-setup", "invoice", "subscription"],
    "guardian": ["security-audit", "key-rotation", "access-review"],
    "strategist": ["project-setup", "calendar-sync", "weekly-briefing"],
    "diplomat": ["client-onboard", "follow-up", "partnership"],
    "brain": ["cross-agent-analysis", "pattern-search", "insight"],
}


def load_state():
    state_path = DATA_DIR / "hermes_cli_state.json"
    if state_path.exists():
        return json.loads(state_path.read_text(encoding="utf-8"))
    return {"enterprise": None, "heroes": {h: "inactive" for h in HEROES}, "missions": []}


def save_state(state):
    state_path = DATA_DIR / "hermes_cli_state.json"
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_init(args):
    state = load_state()
    state["enterprise"] = {"name": args.name, "created_at": datetime.now(timezone.utc).isoformat()}
    save_state(state)
    print(f"Initialized enterprise: {args.name}")


def cmd_activate(args):
    state = load_state()
    hero = args.hero.lower()
    if hero not in HEROES:
        print(f"Unknown hero: {hero}", file=sys.stderr)
        return 1
    state["heroes"][hero] = "active"
    save_state(state)
    print(f"Activated {hero}")


def cmd_deactivate(args):
    state = load_state()
    hero = args.hero.lower()
    if hero not in HEROES:
        print(f"Unknown hero: {hero}", file=sys.stderr)
        return 1
    state["heroes"][hero] = "inactive"
    save_state(state)
    print(f"Deactivated {hero}")


def cmd_mission(args):
    state = load_state()
    hero = args.hero.lower()
    if hero not in HEROES:
        print(f"Unknown hero: {hero}", file=sys.stderr)
        return 1
    if state["heroes"].get(hero) != "active":
        print(f"Hero '{hero}' is not active. Run: hermes activate {hero}", file=sys.stderr)
        return 1
    mission = {
        "id": f"MISSION-{len(state['missions']) + 1:03d}",
        "hero": hero,
        "type": args.type,
        "status": "completed",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "output": f"Stub output for {hero}/{args.type}",
    }
    state["missions"].append(mission)
    save_state(state)
    print(f"Mission {mission['id']} ({hero}/{args.type}) completed.")
    print(json.dumps(mission, indent=2, ensure_ascii=False))


def cmd_status(args):
    state = load_state()
    payload = {
        "status": "healthy",
        "version": "0.1.0-stub",
        "enterprise": state.get("enterprise"),
        "heroes": state["heroes"],
        "missions_count": len(state["missions"]),
    }
    if args.verbose:
        payload["missions"] = state["missions"]
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def cmd_dashboard(args):
    print(f"Stub: open dashboard at http://localhost:{args.port}")
    print("Run the real dashboard with: cd dashboard && npm install && npm run dev")


def cmd_test(args):
    print("Running stub integration tests...")
    print("OK (stubs always pass)")


def cmd_config(args):
    env_file = REPO_ROOT / ".env"
    print(f"Edit configuration in: {env_file}")
    if env_file.exists():
        print(env_file.read_text(encoding="utf-8"))


def cmd_backup(args):
    print(f"Stub: backup enterprise data to {args.to}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="hermes", description="Hermes CLI stub for Partenon")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init", help="Initialize a new enterprise")
    p_init.add_argument("--name", required=True, help="Enterprise name")
    p_init.set_defaults(func=cmd_init)

    p_activate = subparsers.add_parser("activate", help="Activate a hero")
    p_activate.add_argument("hero", help="Hero name (scribe, herald, collector, ...)")
    p_activate.set_defaults(func=cmd_activate)

    p_deactivate = subparsers.add_parser("deactivate", help="Deactivate a hero")
    p_deactivate.add_argument("hero", help="Hero name")
    p_deactivate.set_defaults(func=cmd_deactivate)

    p_mission = subparsers.add_parser("mission", help="Start a hero mission")
    p_mission.add_argument("hero", help="Hero name")
    p_mission.add_argument("--type", required=True, help="Mission type")
    p_mission.set_defaults(func=cmd_mission)

    p_status = subparsers.add_parser("status", help="Check system status")
    p_status.add_argument("--verbose", action="store_true", help="Include mission details")
    p_status.set_defaults(func=cmd_status)

    p_dashboard = subparsers.add_parser("dashboard", help="Open web dashboard")
    p_dashboard.add_argument("--port", type=int, default=3000, help="Dashboard port")
    p_dashboard.set_defaults(func=cmd_dashboard)

    p_test = subparsers.add_parser("test", help="Run integration tests")
    p_test.add_argument("--all", action="store_true", help="Run all tests")
    p_test.set_defaults(func=cmd_test)

    p_config = subparsers.add_parser("config", help="Edit configuration")
    p_config.add_argument("--edit", action="store_true", help="Show .env file")
    p_config.set_defaults(func=cmd_config)

    p_backup = subparsers.add_parser("backup", help="Backup enterprise data")
    p_backup.add_argument("--to", default="google-drive", help="Backup target")
    p_backup.set_defaults(func=cmd_backup)

    args = parser.parse_args(argv)
    return args.func(args) or 0


if __name__ == "__main__":
    sys.exit(main())
