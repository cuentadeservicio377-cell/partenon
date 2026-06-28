#!/usr/bin/env python3
"""Validate Partenon hero profile config.yaml files against the canonical schema."""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

PROFILES_DIR = Path(__file__).resolve().parent.parent / "hermes" / "profiles"

HEROES = {
    "partenon-scribe": {"hero": "finance", "file": ".finance"},
    "partenon-herald": {"hero": "design", "file": ".design"},
    "partenon-collector": {"hero": "payments", "file": ".payments"},
    "partenon-guardian": {"hero": "security", "file": ".security"},
    "partenon-strategist": {"hero": "ops", "file": ".ops"},
    "partenon-diplomat": {"hero": "relations", "file": ".relations"},
    "partenon-brain": {"hero": "memory", "file": ".brain"},
}

REQUIRED_TOP_LEVEL_KEYS = [
    "profile",
    "model",
    "skills",
    "mcp_servers",
    "files",
]

REQUIRED_PROFILE_KEYS = ["name", "display_name", "description", "version"]
REQUIRED_MODEL_KEYS = ["default", "fallback"]
REQUIRED_SKILLS_KEYS = ["auto_load"]


def validate_profile(profile_name: str) -> list[str]:
    """Validate a single profile directory and return a list of error messages."""
    errors: list[str] = []
    profile_dir = PROFILES_DIR / profile_name
    config_path = profile_dir / "config.yaml"
    info = HEROES[profile_name]

    # 1. Profile directory exists.
    if not profile_dir.is_dir():
        errors.append(f"{profile_name}: directory does not exist: {profile_dir}")
        return errors

    # 2. config.yaml is valid YAML.
    if not config_path.is_file():
        errors.append(f"{profile_name}: config.yaml not found: {config_path}")
        return errors

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        errors.append(f"{profile_name}: invalid YAML in config.yaml: {exc}")
        return errors
    except Exception as exc:
        errors.append(f"{profile_name}: error reading config.yaml: {exc}")
        return errors

    if not isinstance(data, dict):
        errors.append(f"{profile_name}: config.yaml root must be a mapping")
        return errors

    # 3. Required top-level keys.
    for key in REQUIRED_TOP_LEVEL_KEYS:
        if key not in data:
            errors.append(f"{profile_name}: missing top-level key '{key}'")

    profile = data.get("profile", {})
    if not isinstance(profile, dict):
        errors.append(f"{profile_name}: 'profile' must be a mapping")
    else:
        for key in REQUIRED_PROFILE_KEYS:
            if key not in profile:
                errors.append(f"{profile_name}: missing profile.{key}")
        if profile.get("name") != profile_name:
            errors.append(
                f"{profile_name}: profile.name is '{profile.get('name')}', expected '{profile_name}'"
            )

    model = data.get("model", {})
    if not isinstance(model, dict):
        errors.append(f"{profile_name}: 'model' must be a mapping")
    else:
        for key in REQUIRED_MODEL_KEYS:
            if key not in model:
                errors.append(f"{profile_name}: missing model.{key}")

    skills = data.get("skills", {})
    if not isinstance(skills, dict):
        errors.append(f"{profile_name}: 'skills' must be a mapping")
    else:
        for key in REQUIRED_SKILLS_KEYS:
            if key not in skills:
                errors.append(f"{profile_name}: missing skills.{key}")

    if "mcp_servers" not in data or not isinstance(data.get("mcp_servers"), dict):
        errors.append(f"{profile_name}: 'mcp_servers' must be a mapping")
    else:
        if "partenon-memory" not in data["mcp_servers"]:
            errors.append(f"{profile_name}: missing required mcp_servers.partenon-memory")

    files = data.get("files", [])
    if not isinstance(files, list):
        errors.append(f"{profile_name}: 'files' must be a list")
    else:
        expected_file = info["file"]
        if expected_file not in files:
            errors.append(
                f"{profile_name}: expected '{expected_file}' in files, got {files}"
            )

    # 4. Referenced cron files exist.
    cron_entries = data.get("cron", [])
    if isinstance(cron_entries, list):
        for entry in cron_entries:
            if not isinstance(entry, dict):
                errors.append(f"{profile_name}: cron entry must be a mapping")
                continue
            cron_file = entry.get("file")
            if not cron_file:
                errors.append(f"{profile_name}: cron entry missing 'file'")
                continue
            cron_path = profile_dir / cron_file
            if not cron_path.is_file():
                errors.append(
                    f"{profile_name}: referenced cron file does not exist: {cron_path}"
                )

    # 5. Referenced files in files: exist as templates.
    if isinstance(files, list):
        for fname in files:
            template_path = profile_dir / "templates" / f"{fname}.example"
            if not template_path.is_file():
                errors.append(
                    f"{profile_name}: missing template for file '{fname}': {template_path}"
                )

    return errors


def main() -> int:
    all_errors: list[str] = []
    checked = 0

    for profile_name in HEROES:
        checked += 1
        errors = validate_profile(profile_name)
        all_errors.extend(errors)

    print(f"Profiles checked: {checked}")
    if all_errors:
        print(f"Errors found: {len(all_errors)}")
        for error in all_errors:
            print(f"  - {error}")
        return 1

    print("All profile configs are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
