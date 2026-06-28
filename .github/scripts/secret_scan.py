#!/usr/bin/env python3
"""Scan the repository for likely hardcoded secrets.

This is a lightweight static check run in CI. It flags common secret patterns and
ignores explicit placeholders/example values. It is NOT a replacement for a
secrets manager or pre-commit hooks such as detect-secrets / git-secrets.
"""

import os
import re
import sys

ROOT = "."

SEVERITY = {"critical": [], "high": [], "medium": [], "low": []}

SECRET_PATTERNS = [
    ("OpenAI API key", r"sk-[a-zA-Z0-9]{48}", "critical"),
    ("OpenRouter API key", r"sk-or-v1-[a-zA-Z0-9]{32,}", "critical"),
    ("Stripe secret key", r"sk_(test|live)_[a-zA-Z0-9]{24,}", "critical"),
    ("AWS access key", r"AKIA[0-9A-Z]{16}", "critical"),
    ("GitHub personal access token", r"ghp_[a-zA-Z0-9]{36}", "critical"),
    ("Generic private key", r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "critical"),
    ("Hardcoded password assignment", r"(?i)(password|passwd|pwd)\s*=\s*['\"][^'\"]{6,}['\"]", "high"),
    ("Hardcoded secret assignment", r"(?i)(secret|token|api_key)\s*=\s*['\"][^'\"]{8,}['\"]", "high"),
    ("NVIDIA API key", r"nvapi-[a-zA-Z0-9]{32,}", "critical"),
]

SKIP_DIRS = {".git", ".venv", "node_modules", ".next", "__pycache__", ".kimi", ".kimi-code"}
SKIP_FILES = {"install.sh"}  # installer reads/generates secrets at runtime

PLACEHOLDER_MARKERS = [
    "replace_me",
    "replace_with",
    "example",
    "placeholder",
    "changeme",
    "your_",
    "xxxx",
    "0000000000",
]


def should_skip(path):
    parts = path.split(os.sep)
    if any(p in SKIP_DIRS for p in parts):
        return True
    if os.path.basename(path) in SKIP_FILES:
        return True
    return False


def is_placeholder(line):
    return any(marker in line.lower() for marker in PLACEHOLDER_MARKERS)


def main():
    for dirpath, _dirnames, filenames in os.walk(ROOT):
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            if should_skip(path):
                continue
            if path.endswith(
                (
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".gif",
                    ".ico",
                    ".xlsx",
                    ".xls",
                    ".zip",
                    ".tar.gz",
                )
            ):
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
            except Exception:
                continue
            lines = text.splitlines()
            for pat_name, pat, severity in SECRET_PATTERNS:
                for i, line in enumerate(lines, 1):
                    if re.search(pat, line) and not is_placeholder(line):
                        SEVERITY[severity].append(
                            f"{path}:{i}: {pat_name}: {line.strip()}"
                        )

    exit_code = 0
    for sev in ["critical", "high", "medium", "low"]:
        findings = SEVERITY[sev]
        if findings:
            print(f"\n{sev.upper()} findings ({len(findings)}):")
            for finding in findings:
                print("  " + finding)
            if sev in ("critical", "high"):
                exit_code = 1

    if exit_code == 0:
        print("No hardcoded secrets detected above placeholder threshold.")
    else:
        print("\nSecret scan failed. Remove or templatize the values above.")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
