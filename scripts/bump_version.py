#!/usr/bin/env python3
"""Bump the Partenon version and prepare a release.

Usage:
    python3 scripts/bump_version.py patch
    python3 scripts/bump_version.py minor --tag
    python3 scripts/bump_version.py major --tag --push

The script updates `pyproject.toml`, prepends a new section to `CHANGELOG.md`,
and optionally creates a git tag. It does not push anything unless `--push` is
passed.
"""

import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT_PATH = REPO_ROOT / "pyproject.toml"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"


def read_version() -> str:
    text = PYPROJECT_PATH.read_text()
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if not match:
        raise RuntimeError("Could not find version in pyproject.toml")
    return match.group(1)


def bump(version: str, part: str) -> str:
    major, minor, patch = map(int, version.split("."))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:
        patch += 1
    return f"{major}.{minor}.{patch}"


def update_pyproject(new_version: str) -> None:
    text = PYPROJECT_PATH.read_text()
    updated = re.sub(
        r'^(version\s*=\s*")([^"]+)(")',
        rf"\g<1>{new_version}\g<3>",
        text,
        flags=re.MULTILINE,
        count=1,
    )
    if updated == text:
        raise RuntimeError("Version line in pyproject.toml was not changed")
    PYPROJECT_PATH.write_text(updated)


def update_changelog(new_version: str) -> None:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    header = f"## [{new_version}] - {today}"
    text = CHANGELOG_PATH.read_text()
    if "## [Unreleased]" not in text:
        raise RuntimeError("CHANGELOG.md is missing an [Unreleased] section")
    updated = text.replace(
        "## [Unreleased]\n",
        f"## [Unreleased]\n\n### Added\n- Placeholder entry.\n\n{header}\n",
        1,
    )
    CHANGELOG_PATH.write_text(updated)


def create_git_tag(version: str) -> None:
    tag = f"v{version}"
    subprocess.run(["git", "tag", "-a", tag, "-m", f"Release {tag}"], check=True)
    print(f"Created git tag {tag}")


def push_git_tag(version: str) -> None:
    tag = f"v{version}"
    subprocess.run(["git", "push", "origin", tag], check=True)
    print(f"Pushed git tag {tag}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bump Partenon version")
    parser.add_argument("part", choices=["major", "minor", "patch"])
    parser.add_argument("--tag", action="store_true", help="Create a git tag")
    parser.add_argument("--push", action="store_true", help="Push the git tag")
    parser.add_argument("--dry-run", action="store_true", help="Do not modify files")
    args = parser.parse_args(argv)

    current = read_version()
    new = bump(current, args.part)
    print(f"Bumping {current} -> {new}")

    if args.dry_run:
        print("Dry run: no files modified")
        return 0

    update_pyproject(new)
    update_changelog(new)
    print(f"Updated {PYPROJECT_PATH.name} and {CHANGELOG_PATH.name}")

    if args.tag:
        create_git_tag(new)
    if args.push:
        if not args.tag:
            create_git_tag(new)
        push_git_tag(new)

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
