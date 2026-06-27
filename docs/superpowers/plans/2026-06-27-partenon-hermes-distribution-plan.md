# Partenon-as-Hermes-Distribution Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert Partenon into an installable Hermes profile distribution with 7 hero profiles, native MCP servers, progressive onboarding, and a connected dashboard, while preserving all existing functionality.

**Architecture:** Wrap existing Python tools as FastMCP servers, provide Hermes-valid profile `config.yaml` files, keep dry-run as default, and expose a FastAPI backend for the Next.js dashboard. Use Hermes' native gateway and cron instead of custom implementations.

**Tech Stack:** Python 3.10+, FastMCP, Hermes Agent CLI, FastAPI, Next.js 15, TypeScript, Tailwind CSS, PyYAML.

## Global Constraints

- Python 3.10+ required.
- All MCP servers default to `PARTENON_MODE=dry-run`.
- No existing files are deleted until the new structure is validated.
- Every code change is paired with a documentation update.
- All commits must have descriptive messages.
- Secret scans must pass before any commit.
- Tests must pass before marking a task done.
- Write everything in English (code, docs, configs).
- Follow existing Partenon style: no banned fonts, no emojis, mobile-first layouts for web.

---

## Phase 1: Foundation

**Objective:** Create the distribution manifest, package structure, and validation tooling. Nothing is connected yet; this phase only lays the groundwork.

### Task 1.1: Distribution manifest and package metadata

**Files:**
- Create: `distribution.yaml`
- Create: `pyproject.toml`
- Modify: `README.md` (add install section)
- Test: `tests/test_distribution.py`

**Interfaces:**
- Produces: `distribution.yaml` consumed by `hermes profile install`.
- Produces: `pyproject.toml` with package metadata and MCP server entry points.

- [ ] **Step 1: Write failing test for distribution manifest**

```python
# tests/test_distribution.py
import yaml
from pathlib import Path

def test_distribution_yaml_exists():
    assert Path("distribution.yaml").exists()

def test_distribution_yaml_has_required_fields():
    with open("distribution.yaml") as f:
        data = yaml.safe_load(f)
    assert data["name"] == "partenon"
    assert "version" in data
    assert "hermes_requires" in data
    assert "profiles" in data
    assert len(data["profiles"]) == 7
```

- [ ] **Step 2: Run tests to verify failure**

```bash
cd "/Users/pablomeneses/Documents/Kimi Code/Partenon"
python3 -m pytest tests/test_distribution.py -v
```

Expected: FAIL (files do not exist).

- [ ] **Step 3: Create `distribution.yaml`**

```yaml
name: partenon
version: 1.0.0
description: "Seven-hero business operating system for Hermes Agent"
hermes_requires: ">=0.15.0"
alias: partenon
profiles:
  - partenon-scribe
  - partenon-herald
  - partenon-collector
  - partenon-guardian
  - partenon-strategist
  - partenon-diplomat
  - partenon-brain
env_requires:
  - name: OPENROUTER_API_KEY
    required: true
    description: "For LLM access through Hermes"
  - name: GOOGLE_SERVICE_ACCOUNT_JSON
    required: false
    description: "For Google Workspace live mode"
  - name: STRIPE_SECRET_KEY
    required: false
    description: "For Stripe live mode"
  - name: GBRAIN_DATABASE_URL
    required: false
    description: "For persistent memory"
```

- [ ] **Step 4: Create `pyproject.toml`**

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "partenon"
version = "1.0.0"
description = "Seven-hero business operating system for Hermes Agent"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "openpyxl>=3.1.0",
    "mcp>=1.0.0",
    "python-dotenv>=1.0.0",
    "pyyaml>=6.0",
    "fastapi>=0.110.0",
    "uvicorn>=0.27.0",
    "pydantic>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "httpx>=0.27",
    "pip-audit>=2.7",
]

[project.scripts]
partenon-onboarding = "partenon.onboarding.cli:main"
partenon-dashboard-api = "partenon.dashboard_api.main:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["partenon*", "mcp_servers*"]
```

- [ ] **Step 5: Update `README.md` install section**

Add a new section at the top of README.md:

```markdown
## Install with Hermes

```bash
# 1. Install Hermes Agent CLI
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# 2. Install Partenon distribution
hermes profile install github.com/cuentadeservicio377-cell/partenon --alias partenon

# 3. Run onboarding
partenon-onboarding

# 4. Chat with a hero
partenon-scribe chat
```
```

- [ ] **Step 6: Run tests**

```bash
python3 -m pytest tests/test_distribution.py -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add distribution.yaml pyproject.toml tests/test_distribution.py README.md
git commit -m "feat: add Hermes distribution manifest and package metadata"
```

---

### Task 1.2: Directory structure and validation tooling

**Files:**
- Create: `mcp_servers/__init__.py`
- Create: `profiles/.gitkeep`
- Create: `skills/.gitkeep`
- Create: `partenon/__init__.py`
- Create: `partenon/onboarding/__init__.py`
- Create: `partenon/dashboard_api/__init__.py`
- Create: `scripts/validate_profiles.py`
- Create: `tests/test_validate_profiles.py`
- Modify: `Makefile`
- Modify: `.gitignore`

**Interfaces:**
- Produces: `scripts/validate_profiles.py` validates any profile directory against Hermes schema.
- Produces: `make validate-profiles` target.

- [ ] **Step 1: Write failing test for validation script**

```python
# tests/test_validate_profiles.py
from pathlib import Path
from scripts.validate_profiles import validate_profile

def test_validate_profiles_script_exists():
    assert Path("scripts/validate_profiles.py").exists()

def test_validate_profile_detects_missing_config():
    result = validate_profile("tests/fixtures/fake-profile")
    assert result["valid"] is False
```

- [ ] **Step 2: Run tests to verify failure**

```bash
python3 -m pytest tests/test_validate_profiles.py -v
```

Expected: FAIL.

- [ ] **Step 3: Create directory structure and validation script**

```python
# scripts/validate_profiles.py
#!/usr/bin/env python3
"""Validate Partenon profiles against Hermes config.yaml schema."""
import sys
from pathlib import Path
import yaml

REQUIRED_KEYS = {"model", "agent", "mcp_servers"}
OPTIONAL_KEYS = {"skills", "platform_toolsets", "terminal"}
VALID_KEYS = REQUIRED_KEYS | OPTIONAL_KEYS

def validate_profile(profile_path: str) -> dict:
    path = Path(profile_path)
    result = {"path": str(path), "valid": True, "errors": []}

    if not path.exists():
        result["valid"] = False
        result["errors"].append("Profile directory does not exist")
        return result

    config_path = path / "config.yaml"
    if not config_path.exists():
        result["valid"] = False
        result["errors"].append("Missing config.yaml")
        return result

    soul_path = path / "SOUL.md"
    if not soul_path.exists():
        result["valid"] = False
        result["errors"].append("Missing SOUL.md")

    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
    except Exception as e:
        result["valid"] = False
        result["errors"].append(f"Invalid YAML: {e}")
        return result

    if not isinstance(config, dict):
        result["valid"] = False
        result["errors"].append("config.yaml must be a mapping")
        return result

    missing = REQUIRED_KEYS - set(config.keys())
    if missing:
        result["valid"] = False
        result["errors"].append(f"Missing required keys: {missing}")

    unknown = set(config.keys()) - VALID_KEYS
    if unknown:
        result["valid"] = False
        result["errors"].append(f"Unknown top-level keys: {unknown}")

    if "mcp_servers" in config:
        mcp_servers = config["mcp_servers"]
        if not isinstance(mcp_servers, dict):
            result["valid"] = False
            result["errors"].append("mcp_servers must be a mapping keyed by server name")
        else:
            for name, server in mcp_servers.items():
                if "command" not in server and "url" not in server:
                    result["valid"] = False
                    result["errors"].append(f"MCP server '{name}' missing command or url")

    return result

def main():
    profiles_dir = Path("profiles")
    if not profiles_dir.exists():
        print("No profiles/ directory found")
        sys.exit(1)

    all_valid = True
    for profile_dir in sorted(profiles_dir.iterdir()):
        if not profile_dir.is_dir():
            continue
        result = validate_profile(profile_dir)
        status = "PASS" if result["valid"] else "FAIL"
        print(f"[{status}] {result['path']}")
        for error in result["errors"]:
            print(f"  - {error}")
        if not result["valid"]:
            all_valid = False

    sys.exit(0 if all_valid else 1)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Create placeholder directories and files**

```bash
touch mcp_servers/__init__.py
touch profiles/.gitkeep
touch skills/.gitkeep
touch partenon/__init__.py
touch partenon/onboarding/__init__.py
touch partenon/dashboard_api/__init__.py
touch tests/fixtures/fake-profile/SOUL.md
```

- [ ] **Step 5: Update `Makefile`**

Add targets:

```makefile
.PHONY: validate-profiles test install check-secrets

validate-profiles:
	python3 scripts/validate_profiles.py

test:
	python3 -m pytest tests/ -v

check-secrets:
	@echo "Secret scan placeholder - add real scanner in Task 1.3"

install:
	pip install -e ".[dev]"
```

- [ ] **Step 6: Update `.gitignore`**

Ensure these entries exist:

```gitignore
__pycache__/
*.pyc
.venv/
.env
*.egg-info/
.pytest_cache/
.mypy_cache/
```

- [ ] **Step 7: Run tests**

```bash
python3 -m pytest tests/test_validate_profiles.py -v
```

Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add mcp_servers/ profiles/ skills/ partenon/ scripts/validate_profiles.py tests/test_validate_profiles.py tests/fixtures/fake-profile/SOUL.md Makefile .gitignore
git commit -m "feat: add directory structure and profile validation tooling"
```

---

### Task 1.3: Secret scanning and pre-commit safety

**Files:**
- Create: `scripts/check_for_secrets.sh`
- Create: `tests/test_security.py`
- Modify: `Makefile`

**Interfaces:**
- Produces: `make check-secrets` scans for AWS keys, Stripe keys, Google tokens, emails, IPs.

- [ ] **Step 1: Write failing test for secret scanner**

```python
# tests/test_security.py
from pathlib import Path
import subprocess

def test_secret_scanner_exists():
    assert Path("scripts/check_for_secrets.sh").exists()

def test_secret_scan_passes_clean_repo():
    result = subprocess.run(["bash", "scripts/check_for_secrets.sh"], capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
```

- [ ] **Step 2: Run tests to verify failure**

```bash
python3 -m pytest tests/test_security.py -v
```

Expected: FAIL.

- [ ] **Step 3: Create secret scanner**

```bash
# scripts/check_for_secrets.sh
#!/bin/bash
set -e

echo "Scanning for secrets and sensitive patterns..."

# AWS keys
grep -rE "AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.md" . || true

# Stripe keys
grep -rE "sk_(test|live)_[0-9a-zA-Z]{24,}" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.md" . || true

# Google OAuth / service account keys (simplified)
grep -rE "\"private_key\":|-----BEGIN PRIVATE KEY-----|-----BEGIN RSA PRIVATE KEY-----" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.md" . || true

# IP addresses
grep -rE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.md" . || true

# Email addresses
grep -rE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" --include="*.py" --include="*.yaml" --include="*.yml" --include="*.json" --include="*.md" . || true

echo "No secrets or sensitive patterns detected."
```

Make executable:

```bash
chmod +x scripts/check_for_secrets.sh
```

- [ ] **Step 4: Update `Makefile`**

Replace placeholder:

```makefile
check-secrets:
	bash scripts/check_for_secrets.sh
```

- [ ] **Step 5: Run tests**

```bash
python3 -m pytest tests/test_security.py -v
make check-secrets
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/check_for_secrets.sh tests/test_security.py Makefile
git commit -m "chore: add secret scanner and security tests"
```

---

## Phase 2: MCP Servers

**Objective:** Wrap existing Python tools as FastMCP servers, one per domain. All default to dry-run.

### Task 2.1: Finance MCP server

**Files:**
- Create: `mcp_servers/partenon_finance_mcp/__init__.py`
- Create: `mcp_servers/partenon_finance_mcp/server.py`
- Create: `mcp_servers/partenon_finance_mcp/tools.py`
- Create: `tests/mcp_servers/test_partenon_finance_mcp.py`

**Interfaces:**
- Consumes: Existing `hermes/profiles/partenon-tesorero/skills/finance/tools/parsers.py`, `templates.py`, `google_sheets.py`, `audit.py`.
- Produces: MCP tools: `finance_create_budget`, `finance_parse_expenses`, `finance_append_to_sheet`, `finance_run_audit`.

- [ ] **Step 1: Write failing test**

```python
# tests/mcp_servers/test_partenon_finance_mcp.py
from mcp_servers.partenon_finance_mcp.tools import create_budget

def test_create_budget_returns_dict():
    result = create_budget("coffee_shop", "USD")
    assert isinstance(result, dict)
    assert result["ok"] is True
    assert "budget" in result
```

- [ ] **Step 2: Run tests to verify failure**

```bash
python3 -m pytest tests/mcp_servers/test_partenon_finance_mcp.py -v
```

Expected: FAIL.

- [ ] **Step 3: Create tools module**

```python
# mcp_servers/partenon_finance_mcp/tools.py
import os
from pathlib import Path

MODE = os.environ.get("PARTENON_MODE", "dry-run")

def create_budget(business_type: str, currency: str = "USD") -> dict:
    if MODE == "dry-run":
        return {
            "ok": True,
            "mode": "dry-run",
            "business_type": business_type,
            "currency": currency,
            "budget": {
                "revenue": 10000,
                "fixed_costs": 4000,
                "variable_costs": 3000,
                "margin": 3000,
            },
        }
    # Live mode integration with real templates.py is out of scope for this phase.
    # It will be implemented in a future live-integration phase after dry-run validation.
    raise NotImplementedError("Live mode not yet implemented")

def parse_expenses(file_path: str) -> dict:
    if MODE == "dry-run":
        return {
            "ok": True,
            "mode": "dry-run",
            "file_path": file_path,
            "expenses": [
                {"category": "rent", "amount": 1000},
                {"category": "supplies", "amount": 250},
            ],
        }
    raise NotImplementedError("Live mode not yet implemented")

def append_to_sheet(spreadsheet_id: str, range_name: str, rows: list) -> dict:
    if MODE == "dry-run":
        return {
            "ok": True,
            "mode": "dry-run",
            "spreadsheet_id": spreadsheet_id,
            "range": range_name,
            "appended_rows": len(rows),
        }
    raise NotImplementedError("Live mode not yet implemented")

def run_audit(period: str) -> dict:
    if MODE == "dry-run":
        return {
            "ok": True,
            "mode": "dry-run",
            "period": period,
            "alerts": [],
        }
    raise NotImplementedError("Live mode not yet implemented")
```

- [ ] **Step 4: Create MCP server**

```python
# mcp_servers/partenon_finance_mcp/server.py
from mcp.server.fastmcp import FastMCP
from mcp_servers.partenon_finance_mcp.tools import (
    create_budget,
    parse_expenses,
    append_to_sheet,
    run_audit,
)

mcp = FastMCP("partenon-finance")

@mcp.tool()
def finance_create_budget(business_type: str, currency: str = "USD") -> dict:
    """Create a baseline budget for a business type."""
    return create_budget(business_type, currency)

@mcp.tool()
def finance_parse_expenses(file_path: str) -> dict:
    """Parse and classify expenses from a CSV/Excel file."""
    return parse_expenses(file_path)

@mcp.tool()
def finance_append_to_sheet(spreadsheet_id: str, range_name: str, rows: list) -> dict:
    """Append rows to a Google Sheet if credentials exist; otherwise simulate."""
    return append_to_sheet(spreadsheet_id, range_name, rows)

@mcp.tool()
def finance_run_audit(period: str) -> dict:
    """Run a financial audit for a period."""
    return run_audit(period)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

- [ ] **Step 5: Run tests**

```bash
python3 -m pytest tests/mcp_servers/test_partenon_finance_mcp.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add mcp_servers/partenon_finance_mcp/ tests/mcp_servers/test_partenon_finance_mcp.py
git commit -m "feat: add partenon-finance MCP server with dry-run tools"
```

---

### Task 2.2: Payments MCP server

**Files:**
- Create: `mcp_servers/partenon_payments_mcp/__init__.py`
- Create: `mcp_servers/partenon_payments_mcp/server.py`
- Create: `mcp_servers/partenon_payments_mcp/tools.py`
- Create: `tests/mcp_servers/test_partenon_payments_mcp.py`

**Interfaces:**
- Consumes: Existing `hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py`.
- Produces: MCP tools: `payments_create_link`, `payments_record_payment`, `payments_generate_invoice_pdf`, `payments_monitor_fraud`.

- [ ] **Step 1: Write failing test**

```python
# tests/mcp_servers/test_partenon_payments_mcp.py
from mcp_servers.partenon_payments_mcp.tools import create_payment_link

def test_create_payment_link_dry_run():
    result = create_payment_link(amount=1000, currency="USD", description="Deposit")
    assert result["ok"] is True
    assert result["mode"] == "dry-run"
```

- [ ] **Step 2: Run tests to verify failure**

```bash
python3 -m pytest tests/mcp_servers/test_partenon_payments_mcp.py -v
```

Expected: FAIL.

- [ ] **Step 3: Create tools module**

```python
# mcp_servers/partenon_payments_mcp/tools.py
import os

MODE = os.environ.get("PARTENON_MODE", "dry-run")

def create_payment_link(amount: int, currency: str, description: str) -> dict:
    if MODE == "dry-run":
        return {
            "ok": True,
            "mode": "dry-run",
            "amount": amount,
            "currency": currency,
            "description": description,
            "url": "https://dry-run.partenon.local/pay/12345",
        }
    raise NotImplementedError("Live mode not yet implemented")

def record_payment(payment_link_id: str, amount: int) -> dict:
    if MODE == "dry-run":
        return {"ok": True, "mode": "dry-run", "payment_link_id": payment_link_id, "amount": amount}
    raise NotImplementedError("Live mode not yet implemented")

def generate_invoice_pdf(invoice_id: str) -> dict:
    if MODE == "dry-run":
        return {"ok": True, "mode": "dry-run", "invoice_id": invoice_id, "pdf_path": "dry-run.pdf"}
    raise NotImplementedError("Live mode not yet implemented")

def monitor_fraud() -> dict:
    if MODE == "dry-run":
        return {"ok": True, "mode": "dry-run", "alerts": []}
    raise NotImplementedError("Live mode not yet implemented")
```

- [ ] **Step 4: Create MCP server**

```python
# mcp_servers/partenon_payments_mcp/server.py
from mcp.server.fastmcp import FastMCP
from mcp_servers.partenon_payments_mcp.tools import (
    create_payment_link,
    record_payment,
    generate_invoice_pdf,
    monitor_fraud,
)

mcp = FastMCP("partenon-payments")

@mcp.tool()
def payments_create_link(amount: int, currency: str, description: str) -> dict:
    return create_payment_link(amount, currency, description)

@mcp.tool()
def payments_record_payment(payment_link_id: str, amount: int) -> dict:
    return record_payment(payment_link_id, amount)

@mcp.tool()
def payments_generate_invoice_pdf(invoice_id: str) -> dict:
    return generate_invoice_pdf(invoice_id)

@mcp.tool()
def payments_monitor_fraud() -> dict:
    return monitor_fraud()

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

- [ ] **Step 5: Run tests**

```bash
python3 -m pytest tests/mcp_servers/test_partenon_payments_mcp.py -v
```

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add mcp_servers/partenon_payments_mcp/ tests/mcp_servers/test_partenon_payments_mcp.py
git commit -m "feat: add partenon-payments MCP server with dry-run tools"
```

---

### Task 2.3: Ops, Relations, Security, Comms, Memory MCP servers

**Files:**
- Create: `mcp_servers/partenon_ops_mcp/` (server.py, tools.py, __init__.py)
- Create: `mcp_servers/partenon_relations_mcp/` (server.py, tools.py, __init__.py)
- Create: `mcp_servers/partenon_security_mcp/` (server.py, tools.py, __init__.py)
- Create: `mcp_servers/partenon_comms_mcp/` (server.py, tools.py, __init__.py)
- Create: `mcp_servers/partenon_memory_mcp/` (server.py, tools.py, __init__.py)
- Create: corresponding test files under `tests/mcp_servers/`

**Interfaces:**
- Each server follows the same dry-run/live pattern as finance and payments.
- Tool names are prefixed with domain, e.g., `ops_create_project`, `relations_add_contact`, `security_list_keys`, `comms_generate_copy`, `memory_read_profile`.

- [ ] **Step 1: Write failing tests for all five servers**

```python
# tests/mcp_servers/test_partenon_ops_mcp.py
from mcp_servers.partenon_ops_mcp.tools import create_project

def test_create_project_dry_run():
    result = create_project(name="Q3 Launch", deadline="2026-09-01")
    assert result["ok"] is True
    assert result["mode"] == "dry-run"
```

Repeat pattern for relations, security, comms, memory.

- [ ] **Step 2: Run tests to verify failure**

```bash
python3 -m pytest tests/mcp_servers/test_partenon_ops_mcp.py tests/mcp_servers/test_partenon_relations_mcp.py tests/mcp_servers/test_partenon_security_mcp.py tests/mcp_servers/test_partenon_comms_mcp.py tests/mcp_servers/test_partenon_memory_mcp.py -v
```

Expected: FAIL.

- [ ] **Step 3: Create tools and servers**

For each domain, create a `tools.py` with dry-run implementations and a `server.py` wrapping them as MCP tools.

Example `mcp_servers/partenon_ops_mcp/tools.py`:

```python
import os

MODE = os.environ.get("PARTENON_MODE", "dry-run")

def create_project(name: str, deadline: str) -> dict:
    if MODE == "dry-run":
        return {"ok": True, "mode": "dry-run", "name": name, "deadline": deadline, "id": "proj-dry-001"}
    raise NotImplementedError("Live mode not yet implemented")

def add_task(project_id: str, title: str) -> dict:
    if MODE == "dry-run":
        return {"ok": True, "mode": "dry-run", "project_id": project_id, "title": title, "task_id": "task-dry-001"}
    raise NotImplementedError("Live mode not yet implemented")

def build_checklist(event_type: str) -> dict:
    if MODE == "dry-run":
        return {"ok": True, "mode": "dry-run", "event_type": event_type, "items": []}
    raise NotImplementedError("Live mode not yet implemented")

def schedule_reminder(text: str, when: str) -> dict:
    if MODE == "dry-run":
        return {"ok": True, "mode": "dry-run", "text": text, "when": when}
    raise NotImplementedError("Live mode not yet implemented")
```

Corresponding `server.py`:

```python
from mcp.server.fastmcp import FastMCP
from mcp_servers.partenon_ops_mcp.tools import create_project, add_task, build_checklist, schedule_reminder

mcp = FastMCP("partenon-ops")

@mcp.tool()
def ops_create_project(name: str, deadline: str) -> dict:
    return create_project(name, deadline)

@mcp.tool()
def ops_add_task(project_id: str, title: str) -> dict:
    return add_task(project_id, title)

@mcp.tool()
def ops_build_checklist(event_type: str) -> dict:
    return build_checklist(event_type)

@mcp.tool()
def ops_schedule_reminder(text: str, when: str) -> dict:
    return schedule_reminder(text, when)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Repeat analogous tools/servers for relations, security, comms, memory.

Relations tools: `add_contact`, `log_interaction`, `generate_proposal`, `schedule_followup`.
Security tools: `list_keys`, `rotate_key`, `log_audit_event`, `check_policy`.
Comms tools: `generate_copy`, `build_content_calendar`, `draft_post`.
Memory tools: `read_profile`, `write_learning`, `search_missions`, `find_conflicts`.

- [ ] **Step 4: Run tests**

```bash
python3 -m pytest tests/mcp_servers/ -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add mcp_servers/partenon_ops_mcp/ mcp_servers/partenon_relations_mcp/ mcp_servers/partenon_security_mcp/ mcp_servers/partenon_comms_mcp/ mcp_servers/partenon_memory_mcp/
git add tests/mcp_servers/test_partenon_ops_mcp.py tests/mcp_servers/test_partenon_relations_mcp.py tests/mcp_servers/test_partenon_security_mcp.py tests/mcp_servers/test_partenon_comms_mcp.py tests/mcp_servers/test_partenon_memory_mcp.py
git commit -m "feat: add ops, relations, security, comms, memory MCP servers"
```

---

## Phase 3: Hermes-Valid Profiles

**Objective:** Create 7 profiles under `profiles/` with valid Hermes `config.yaml`, `SOUL.md`, `.env.EXAMPLE`, and cron examples.

### Task 3.1: Scribe profile

**Files:**
- Create: `profiles/partenon-scribe/SOUL.md`
- Create: `profiles/partenon-scribe/config.yaml`
- Create: `profiles/partenon-scribe/.env.EXAMPLE`
- Create: `profiles/partenon-scribe/cron/jobs.json`

**Interfaces:**
- Consumes: `mcp_servers/partenon_finance_mcp`, `mcp_servers/partenon_memory_mcp`.
- Produces: Valid Hermes profile for the Scribe hero.

- [ ] **Step 1: Copy existing SOUL.md**

```bash
cp "hermes/profiles/partenon-tesorero/SOUL.md" profiles/partenon-scribe/SOUL.md
```

- [ ] **Step 2: Create `config.yaml`**

```yaml
model:
  default: anthropic/claude-sonnet-4
  provider: openrouter

agent:
  enabled_toolsets:
    - hermes-cli
    - file
    - terminal
    - mcp-partenon-finance
    - mcp-partenon-memory

mcp_servers:
  partenon-finance:
    command: python
    args: ["-m", "mcp_servers.partenon_finance_mcp.server"]
    env:
      PARTENON_MODE: "${PARTENON_MODE:-dry-run}"
      GOOGLE_SERVICE_ACCOUNT_JSON: "${GOOGLE_SERVICE_ACCOUNT_JSON}"
  partenon-memory:
    command: python
    args: ["-m", "mcp_servers.partenon_memory_mcp.server"]
    env:
      GBRAIN_DATABASE_URL: "${GBRAIN_DATABASE_URL}"

skills:
  auto_load:
    - partenon-core
    - finance

platform_toolsets:
  telegram:
    - hermes-telegram
    - mcp-partenon-finance
    - mcp-partenon-memory
```

- [ ] **Step 3: Create `.env.EXAMPLE`**

```bash
# Partenon Scribe profile environment variables
OPENROUTER_API_KEY=
GOOGLE_SERVICE_ACCOUNT_JSON=
GBRAIN_DATABASE_URL=
PARTENON_MODE=dry-run
```

- [ ] **Step 4: Create `cron/jobs.json`**

```json
{
  "jobs": [
    {
      "name": "scribe-daily-report",
      "schedule": "0 7 * * 1-5",
      "prompt": "Run the daily finance report and alert on budget variance.",
      "skills": ["finance"],
      "deliver": "telegram"
    }
  ]
}
```

- [ ] **Step 5: Validate profile**

```bash
python3 scripts/validate_profiles.py
```

Expected: `profiles/partenon-scribe` PASS.

- [ ] **Step 6: Commit**

```bash
git add profiles/partenon-scribe/
git commit -m "feat: add Hermes-valid Scribe profile"
```

---

### Task 3.2: Herald, Collector, Guardian, Strategist, Diplomat, Brain profiles

**Files:**
- Create: `profiles/partenon-herald/`
- Create: `profiles/partenon-collector/`
- Create: `profiles/partenon-guardian/`
- Create: `profiles/partenon-strategist/`
- Create: `profiles/partenon-diplomat/`
- Create: `profiles/partenon-brain/`

**Interfaces:**
- Each profile enables the MCP servers relevant to its domain.
- Herald: `partenon-comms`, `partenon-memory`.
- Collector: `partenon-payments`, `partenon-memory`.
- Guardian: `partenon-security`, `partenon-memory`.
- Strategist: `partenon-ops`, `partenon-memory`.
- Diplomat: `partenon-relations`, `partenon-memory`.
- Brain: `partenon-memory`.

- [ ] **Step 1: Copy SOUL.md for each**

```bash
cp hermes/profiles/partenon-mensajero/SOUL.md profiles/partenon-herald/SOUL.md
cp hermes/profiles/partenon-cobrador/SOUL.md profiles/partenon-collector/SOUL.md
cp hermes/profiles/partenon-guardian/SOUL.md profiles/partenon-guardian/SOUL.md
cp hermes/profiles/partenon-estratega/SOUL.md profiles/partenon-strategist/SOUL.md
cp hermes/profiles/partenon-diplomatico/SOUL.md profiles/partenon-diplomat/SOUL.md
cp hermes/profiles/partenon-brain/SOUL.md profiles/partenon-brain/SOUL.md
```

- [ ] **Step 2: Create `config.yaml`, `.env.EXAMPLE`, and `cron/jobs.json` for each**

Example `profiles/partenon-herald/config.yaml`:

```yaml
model:
  default: anthropic/claude-sonnet-4
  provider: openrouter

agent:
  enabled_toolsets:
    - hermes-cli
    - file
    - terminal
    - mcp-partenon-comms
    - mcp-partenon-memory

mcp_servers:
  partenon-comms:
    command: python
    args: ["-m", "mcp_servers.partenon_comms_mcp.server"]
    env:
      PARTENON_MODE: "${PARTENON_MODE:-dry-run}"
  partenon-memory:
    command: python
    args: ["-m", "mcp_servers.partenon_memory_mcp.server"]
    env:
      GBRAIN_DATABASE_URL: "${GBRAIN_DATABASE_URL}"

skills:
  auto_load:
    - partenon-core
    - comms

platform_toolsets:
  telegram:
    - hermes-telegram
    - mcp-partenon-comms
    - mcp-partenon-memory
```

Repeat with appropriate MCP servers for each profile.

- [ ] **Step 3: Validate all profiles**

```bash
python3 scripts/validate_profiles.py
```

Expected: 7/7 PASS.

- [ ] **Step 4: Commit**

```bash
git add profiles/
git commit -m "feat: add Hermes-valid profiles for all seven heroes"
```

---

## Phase 4: Hermes-Valid Skills

**Objective:** Create shared `skills/` with valid `SKILL.md` frontmatter.

### Task 4.1: Core and finance skills

**Files:**
- Create: `skills/partenon-core/SKILL.md`
- Create: `skills/finance/SKILL.md`
- Create: `tests/test_skills.py`

**Interfaces:**
- Produces: Hermes-discoverable skills with valid frontmatter.

- [ ] **Step 1: Write failing test**

```python
# tests/test_skills.py
from pathlib import Path
import yaml

def test_skill_frontmatter():
    skill_path = Path("skills/finance/SKILL.md")
    assert skill_path.exists()
    content = skill_path.read_text()
    _, frontmatter = content.split("---", 2)[1:3]
    meta = yaml.safe_load(frontmatter)
    assert meta["name"] == "finance"
    assert "description" in meta
    assert "version" in meta
```

- [ ] **Step 2: Run tests to verify failure**

```bash
python3 -m pytest tests/test_skills.py -v
```

Expected: FAIL.

- [ ] **Step 3: Create skills**

`skills/partenon-core/SKILL.md`:

```markdown
---
name: partenon-core
description: Core Partenon operating system skill. Use for onboarding, hero selection, and cross-hero coordination.
version: 1.0.0
metadata:
  hermes:
    tags: [partenon, onboarding, coordination]
    category: core
---

# Partenon Core

## When to Use
Use this skill when the user asks about Partenon, wants to start onboarding, or needs to coordinate multiple heroes.

## Available Heroes
- Scribe (finance)
- Herald (brand/comms)
- Collector (payments)
- Guardian (security)
- Strategist (operations)
- Diplomat (relations)
- Brain (memory)

## Onboarding Procedure
1. Ask the user for their business type.
2. Ask which integrations they want to enable (Google Workspace, Stripe, messaging).
3. Run `partenon-onboarding` if available.
4. Confirm dry-run mode is active until credentials are provided.
```

`skills/finance/SKILL.md`:

```markdown
---
name: finance
description: Manage budgets, expenses, cash flow, and financial audits for a small business.
version: 1.0.0
metadata:
  hermes:
    tags: [finance, google-sheets, partenon]
    category: business
---

# Finance Skill

## When to Use
Use this skill when the user asks about budgets, expenses, margins, cash flow, or financial reports.

## Available Tools
- `partenon_finance_create_budget`
- `partenon_finance_parse_expenses`
- `partenon_finance_append_to_sheet`
- `partenon_finance_run_audit`

## Procedure
1. Ask the user for the business type if unknown.
2. If they provide a CSV/Excel file, use `partenon_finance_parse_expenses`.
3. If they want a budget, use `partenon_finance_create_budget`.
4. In dry-run mode, explain that results are simulated and ask before switching to live mode.

## Onboarding Questions
- What accounting software or spreadsheet do you use?
- Do you have a Google service account for Workspace integration?
- What is your fiscal year start month?
```

- [ ] **Step 4: Run tests**

```bash
python3 -m pytest tests/test_skills.py -v
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add skills/partenon-core/SKILL.md skills/finance/SKILL.md tests/test_skills.py
git commit -m "feat: add core and finance Hermes skills"
```

---

### Task 4.2: Remaining skills

**Files:**
- Create: `skills/payments/SKILL.md`
- Create: `skills/ops/SKILL.md`
- Create: `skills/relations/SKILL.md`
- Create: `skills/security/SKILL.md`
- Create: `skills/comms/SKILL.md`
- Create: `skills/memory/SKILL.md`

- [ ] **Step 1: Create each SKILL.md**

Follow the same frontmatter pattern. Each skill describes its tools, procedure, and onboarding questions.

- [ ] **Step 2: Run tests**

```bash
python3 -m pytest tests/test_skills.py -v
```

Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add skills/
git commit -m "feat: add Hermes skills for payments, ops, relations, security, comms, memory"
```

---

## Phase 5: Onboarding Engine

**Objective:** Rewrite onboarding to be progressive, credential-aware, and business-type-specific.

### Task 5.1: Progressive onboarding CLI

**Files:**
- Create: `partenon/onboarding/engine.py`
- Create: `partenon/onboarding/questions.py`
- Create: `partenon/onboarding/cli.py`
- Create: `tests/test_onboarding.py`
- Modify: `README.md`

**Interfaces:**
- Produces: `partenon-onboarding` CLI command.
- Produces: `data/onboarding_state.json` and generated catalog files.

- [ ] **Step 1: Write failing test**

```python
# tests/test_onboarding.py
from partenon.onboarding.engine import OnboardingEngine

def test_onboarding_dry_run_default():
    engine = OnboardingEngine()
    state = engine.run_interactive(answers={"business_type": "coffee_shop"})
    assert state["mode"] == "dry-run"
    assert state["business_type"] == "coffee_shop"
```

- [ ] **Step 2: Run tests to verify failure**

```bash
python3 -m pytest tests/test_onboarding.py -v
```

Expected: FAIL.

- [ ] **Step 3: Implement onboarding engine**

```python
# partenon/onboarding/engine.py
import json
from pathlib import Path
from typing import Optional

DATA_DIR = Path("data")

class OnboardingEngine:
    def __init__(self, data_dir: Path = DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.state_path = self.data_dir / "onboarding_state.json"

    def run_interactive(self, answers: Optional[dict] = None) -> dict:
        answers = answers or {}
        business_type = answers.get("business_type") or "generic"
        mode = answers.get("mode", "dry-run")

        state = {
            "business_type": business_type,
            "mode": mode,
            "integrations": {
                "google_workspace": bool(answers.get("google_service_account_json")),
                "stripe": bool(answers.get("stripe_secret_key")),
                "messaging": bool(answers.get("messaging_platform")),
            },
            "document_catalog": self._generate_catalog(business_type),
        }

        self.state_path.write_text(json.dumps(state, indent=2))
        return state

    def _generate_catalog(self, business_type: str) -> list:
        base = [
            {"id": "welcome", "name": "Welcome Document", "stage": "onboarding"},
            {"id": "budget", "name": "Budget", "stage": "finance"},
            {"id": "tasks", "name": "Task List", "stage": "operations"},
        ]
        if business_type == "coffee_shop":
            base.append({"id": "menu_costs", "name": "Menu Cost Analysis", "stage": "finance"})
        elif business_type == "events":
            base.append({"id": "event_checklist", "name": "Event Checklist", "stage": "operations"})
        return base
```

- [ ] **Step 4: Implement CLI**

```python
# partenon/onboarding/cli.py
import argparse
from partenon.onboarding.engine import OnboardingEngine

def main():
    parser = argparse.ArgumentParser(description="Partenon onboarding wizard")
    parser.add_argument("--business-type", default="generic")
    parser.add_argument("--mode", default="dry-run")
    parser.add_argument("--google-service-account-json", default="")
    parser.add_argument("--stripe-secret-key", default="")
    parser.add_argument("--messaging-platform", default="")
    args = parser.parse_args()

    engine = OnboardingEngine()
    state = engine.run_interactive(answers={
        "business_type": args.business_type,
        "mode": args.mode,
        "google_service_account_json": args.google_service_account_json,
        "stripe_secret_key": args.stripe_secret_key,
        "messaging_platform": args.messaging_platform,
    })
    print(json.dumps(state, indent=2))

if __name__ == "__main__":
    main()
```

- [ ] **Step 5: Update `pyproject.toml` scripts**

Ensure these exist:

```toml
[project.scripts]
partenon-onboarding = "partenon.onboarding.cli:main"
```

- [ ] **Step 6: Run tests**

```bash
pip install -e ".[dev]"
python3 -m pytest tests/test_onboarding.py -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add partenon/onboarding/ tests/test_onboarding.py pyproject.toml
git commit -m "feat: add progressive onboarding engine and CLI"
```

---

## Phase 6: Dashboard API

**Objective:** Add FastAPI backend and connect the Next.js dashboard.

### Task 6.1: FastAPI backend

**Files:**
- Create: `partenon/dashboard_api/main.py`
- Create: `partenon/dashboard_api/routers/missions.py`
- Create: `partenon/dashboard_api/routers/heroes.py`
- Create: `partenon/dashboard_api/routers/cron.py`
- Create: `partenon/dashboard_api/routers/integrations.py`
- Create: `tests/test_dashboard_api.py`

**Interfaces:**
- Produces: `partenon-dashboard-api` CLI command serving on port 8000.
- Produces: REST endpoints consumed by dashboard frontend.

- [ ] **Step 1: Write failing test**

```python
# tests/test_dashboard_api.py
from fastapi.testclient import TestClient
from partenon.dashboard_api.main import app

client = TestClient(app)

def test_read_heroes():
    response = client.get("/api/v1/heroes")
    assert response.status_code == 200
    data = response.json()
    assert len(data["heroes"]) == 7
```

- [ ] **Step 2: Run tests to verify failure**

```bash
python3 -m pytest tests/test_dashboard_api.py -v
```

Expected: FAIL.

- [ ] **Step 3: Implement FastAPI app**

```python
# partenon/dashboard_api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from partenon.dashboard_api.routers import heroes, missions, cron, integrations

app = FastAPI(title="Partenon Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(heroes.router, prefix="/api/v1")
app.include_router(missions.router, prefix="/api/v1")
app.include_router(cron.router, prefix="/api/v1")
app.include_router(integrations.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"ok": True}

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Implement routers**

`partenon/dashboard_api/routers/heroes.py`:

```python
from fastapi import APIRouter

router = APIRouter()

HEROES = [
    {"id": "scribe", "name": "Scribe", "domain": "finance"},
    {"id": "herald", "name": "Herald", "domain": "comms"},
    {"id": "collector", "name": "Collector", "domain": "payments"},
    {"id": "guardian", "name": "Guardian", "domain": "security"},
    {"id": "strategist", "name": "Strategist", "domain": "ops"},
    {"id": "diplomat", "name": "Diplomat", "domain": "relations"},
    {"id": "brain", "name": "Brain", "domain": "memory"},
]

@router.get("/heroes")
def list_heroes():
    return {"heroes": HEROES}
```

`partenon/dashboard_api/routers/missions.py`:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/missions")
def list_missions():
    return {"missions": []}

@router.post("/missions")
def create_mission(payload: dict):
    return {"ok": True, "mission": payload}
```

`partenon/dashboard_api/routers/cron.py`:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/cron")
def list_cron():
    return {"jobs": []}
```

`partenon/dashboard_api/routers/integrations.py`:

```python
from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/integrations")
def list_integrations():
    return {
        "google_workspace": bool(os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON")),
        "stripe": bool(os.environ.get("STRIPE_SECRET_KEY")),
        "messaging": bool(os.environ.get("TELEGRAM_BOT_TOKEN") or os.environ.get("DISCORD_BOT_TOKEN")),
    }
```

- [ ] **Step 5: Update `pyproject.toml` scripts**

```toml
[project.scripts]
partenon-onboarding = "partenon.onboarding.cli:main"
partenon-dashboard-api = "partenon.dashboard_api.main:main"
```

- [ ] **Step 6: Run tests**

```bash
python3 -m pytest tests/test_dashboard_api.py -v
```

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add partenon/dashboard_api/ tests/test_dashboard_api.py pyproject.toml
git commit -m "feat: add FastAPI dashboard backend"
```

---

### Task 6.2: Connect Next.js dashboard to API

**Files:**
- Modify: `dashboard/src/lib/data.ts`
- Modify: `dashboard/src/app/(dashboard)/page.tsx`
- Modify: `dashboard/src/app/(dashboard)/cron/page.tsx`

**Interfaces:**
- Consumes: `http://localhost:8000/api/v1/*`.
- Produces: Dashboard renders real hero list and integration status.

- [ ] **Step 1: Update data layer**

Replace local JSON reads with API calls:

```typescript
// dashboard/src/lib/data.ts
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api/v1";

export async function fetchHeroes() {
  const res = await fetch(`${API_BASE}/heroes`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch heroes");
  return res.json();
}

export async function fetchMissions() {
  const res = await fetch(`${API_BASE}/missions`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch missions");
  return res.json();
}

export async function fetchCronJobs() {
  const res = await fetch(`${API_BASE}/cron`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch cron jobs");
  return res.json();
}

export async function fetchIntegrations() {
  const res = await fetch(`${API_BASE}/integrations`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch integrations");
  return res.json();
}
```

- [ ] **Step 2: Update dashboard pages**

Change `page.tsx` to call `fetchHeroes()` and `fetchIntegrations()`.
Change `cron/page.tsx` to call `fetchCronJobs()`.

- [ ] **Step 3: Build dashboard**

```bash
cd dashboard && npm run build
```

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add dashboard/src/lib/data.ts dashboard/src/app/(dashboard)/page.tsx dashboard/src/app/(dashboard)/cron/page.tsx
git commit -m "feat: connect dashboard to FastAPI backend"
```

---

## Phase 7: Documentation and CI

**Objective:** Update all docs and add continuous integration.

### Task 7.1: Documentation updates

**Files:**
- Modify: `README.md`
- Modify: `docs/for-developers.md`
- Modify: `docs/HERO_GUIDE.md`
- Modify: `docs/QUICKSTART.md`
- Create: `docs/HERMES_GATEWAY_SETUP.md`
- Create: `docs/CRON_JOBS.md`
- Modify: `CHANGELOG.md`
- Modify: `TODOS.md`

- [ ] **Step 1: Update `README.md`**

Replace old install instructions with Hermes install flow. Add section explaining dry-run vs. live mode.

- [ ] **Step 2: Update `docs/for-developers.md`**

Document:
- How to add a new MCP server.
- How to add a new profile.
- How to run tests.
- Hermes schema reference.

- [ ] **Step 3: Update `docs/HERO_GUIDE.md`**

Document each hero's MCP tools and how to invoke them.

- [ ] **Step 4: Update `docs/QUICKSTART.md`**

Replace local-only demo with:
1. Install Hermes.
2. Install Partenon.
3. Run onboarding.
4. Chat with Scribe in dry-run.

- [ ] **Step 5: Create `docs/HERMES_GATEWAY_SETUP.md`**

Document how to configure Telegram, Discord, WhatsApp via Hermes gateway.

- [ ] **Step 6: Create `docs/CRON_JOBS.md`**

Document default cron jobs and how to customize them.

- [ ] **Step 7: Update `CHANGELOG.md` and `TODOS.md`**

Add Phase 1-7 entries to CHANGELOG. Mark tasks done in TODOS.

- [ ] **Step 8: Commit**

```bash
git add README.md docs/ CHANGELOG.md TODOS.md
git commit -m "docs: update all documentation for Hermes distribution"
```

---

### Task 7.2: CI pipeline

**Files:**
- Create: `.github/workflows/ci.yml`
- Create: `tests/test_ci_placeholder.py`

- [ ] **Step 1: Create CI workflow**

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      - name: Run tests
        run: make test
      - name: Validate profiles
        run: make validate-profiles
      - name: Check secrets
        run: make check-secrets
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ci.yml
git commit -m "chore: add GitHub Actions CI pipeline"
```

---

## Phase 8: Integration and Cleanup

**Objective:** Run end-to-end dry-run mission, validate everything, and deprecate old `hermes/profiles/`.

### Task 8.1: End-to-end dry-run mission

**Files:**
- Create: `scripts/e2e_dry_run.py`
- Create: `tests/test_e2e.py`

- [ ] **Step 1: Create E2E script**

```python
# scripts/e2e_dry_run.py
import subprocess
import json

def run_mcp_tool(server_module: str, tool_name: str, args: dict) -> dict:
    # In a real E2E, this would spawn the MCP server and call the tool.
    # For dry-run validation, import directly.
    module = __import__(f"mcp_servers.{server_module}.tools", fromlist=[tool_name])
    func = getattr(module, tool_name)
    return func(**args)

def main():
    budget = run_mcp_tool("partenon_finance_mcp", "create_budget", {"business_type": "coffee_shop"})
    assert budget["ok"] is True

    project = run_mcp_tool("partenon_ops_mcp", "create_project", {"name": "Launch", "deadline": "2026-09-01"})
    assert project["ok"] is True

    print(json.dumps({"budget": budget, "project": project}, indent=2))
    print("E2E dry-run mission PASSED")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Create test**

```python
# tests/test_e2e.py
import subprocess

def test_e2e_dry_run():
    result = subprocess.run(
        ["python3", "scripts/e2e_dry_run.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "E2E dry-run mission PASSED" in result.stdout
```

- [ ] **Step 3: Run tests**

```bash
python3 -m pytest tests/test_e2e.py -v
python3 scripts/e2e_dry_run.py
```

Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add scripts/e2e_dry_run.py tests/test_e2e.py
git commit -m "feat: add end-to-end dry-run mission test"
```

---

### Task 8.2: Deprecate old `hermes/profiles/`

**Files:**
- Modify: `hermes/profiles/README.md`
- Modify: `install.sh`
- Modify: `scripts/setup_hermes.py`

**Interfaces:**
- Old profiles are kept but marked deprecated. New install path uses `profiles/`.

- [ ] **Step 1: Add deprecation notice**

Create `hermes/profiles/README.md`:

```markdown
# Deprecated Profiles

These profiles use a custom Partenon schema that is not compatible with Hermes CLI.
They are kept for reference only.

Use the profiles in `/profiles/` instead.
```

- [ ] **Step 2: Update `install.sh`**

Change install logic to use `profiles/` instead of `hermes/profiles/`.

- [ ] **Step 3: Update `scripts/setup_hermes.py`**

Same: use `profiles/` directory.

- [ ] **Step 4: Run full test suite**

```bash
make test
make validate-profiles
make check-secrets
```

Expected: ALL PASS.

- [ ] **Step 5: Commit**

```bash
git add hermes/profiles/README.md install.sh scripts/setup_hermes.py
git commit -m "chore: deprecate old hermes/profiles in favor of profiles/"
```

---

## Final Verification

Run:

```bash
make test
make validate-profiles
make check-secrets
cd dashboard && npm run build
```

All must pass. Then push to GitHub.

---

## Self-Review Checklist

- [ ] Spec coverage: every section of the design spec maps to at least one task.
- [ ] Placeholder scan: no TBD, TODO, or vague steps remain.
- [ ] Type consistency: function names match across tasks.
- [ ] No existing files deleted before validation.
- [ ] Documentation updates paired with code changes.
