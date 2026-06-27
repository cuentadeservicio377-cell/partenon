# Design: Partenon as a Hermes Profile Distribution

**Date:** 2026-06-27  
**Status:** Approved for spec  
**Owner:** Kimi Code session  
**Related:** Partenon original repo (`/Users/pablomeneses/Documents/Kimi Code/Partenon/`)

---

## 1. Executive Summary

Partenon is currently a well-documented prototype with static marketing pages, local Python tools, and a Next.js dashboard that reads local JSON. It is **not compatible with Hermes CLI**, the open-source agent runtime from Nous Research. The website and docs promise a multi-agent operating system with live Google Workspace, Stripe, and messaging integrations, but those capabilities are mostly stubs or require manual wiring.

This design converts Partenon into a **Hermes profile distribution**: a single installable package that provides 7 hero profiles, native MCP servers, and progressive onboarding. It preserves all existing content (SOULs, tools, dashboard, website, workshop) and adds the missing runtime layer that connects everything through Hermes.

The result: a user can run:

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
hermes profile install github.com/cuentadeservicio377-cell/partenon --alias partenon
partenon-scribe chat
```

and get a working hero that can evolve from dry-run to live integrations as the user completes onboarding.

---

## 2. Context and Motivation

### 2.1 What we learned from the Paola attempt

A recent adaptation attempt for Paola Meneses revealed that Partenon's value is conceptual, not operational. The code did not connect to Hermes' real messaging gateway, did not use Google Workspace end-to-end, and did not provide a runtime. The attempt was abandoned and its artifacts deleted so Partenon itself can be fixed first.

### 2.2 What Hermes actually provides

Hermes Agent (Nous Research, MIT license) provides:

- `hermes` CLI with profile, skill, gateway, cron, and MCP management.
- A built-in messaging gateway for Telegram, Discord, Slack, WhatsApp, Signal, SMS, Email, iMessage (BlueBubbles), Teams, LINE, and others.
- Profile distributions installable via `hermes profile install <git-url>`.
- Skill discovery based on `SKILL.md` files with YAML frontmatter.
- Native MCP client support (`mcp_servers:` in `config.yaml`).
- Cron jobs via `hermes cron create` or `cron/jobs.json`.

### 2.3 Why this is the right path

Instead of building a custom runtime from scratch, Partenon can become a **content layer on top of Hermes**. Hermes provides the engine; Partenon provides the business logic, personalities, and integrations. This matches the project's marketing and makes it actually usable.

---

## 3. Goals

1. Make Partenon installable as a Hermes profile distribution with one command.
2. Provide 7 working hero profiles that follow the Hermes `config.yaml` schema.
3. Expose existing Python tools as native MCP servers so Hermes can discover and invoke them.
4. Enable messaging through Hermes' native gateway (Telegram, Discord, WhatsApp, etc.) without building custom bots.
5. Run cron jobs through Hermes' native scheduler.
6. Keep dry-run/test mode as the default so the system works immediately without credentials.
7. Add progressive onboarding that asks for credentials and business type only when the user is ready.
8. Preserve all existing files, docs, website, dashboard, and workshop materials.
9. Update documentation in parallel with every code change.
10. Add tests for MCP servers, profile validation, and onboarding.

---

## 4. Non-Goals

1. Replace or fork Hermes CLI. We depend on the official Hermes Agent runtime.
2. Build a custom messaging gateway. We use Hermes' gateway.
3. Build a custom scheduler. We use Hermes' cron.
4. Add new LLM providers. We use Hermes' model configuration.
5. Remove the static marketing site or dashboard. Both are preserved and improved.
6. Support every business type out of the box. We provide templates; customization happens during onboarding.

---

## 5. Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                         User                                    │
│  CLI  │  Telegram  │  Discord  │  WhatsApp  │  Dashboard       │
└───────┴────────────┴───────────┴────────────┴───────────────────┘
                              │
                         Hermes Gateway
                         (provided by Hermes CLI)
                              │
┌─────────────────────────────────────────────────────────────────┐
│                     Hermes Agent Runtime                        │
│  - Intent routing                                               │
│  - Tool selection                                               │
│  - Memory / SOUL.md loading                                     │
│  - Skill invocation                                             │
│  - Cron execution                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
  ┌─────────────┐    ┌─────────────────┐   ┌─────────────────┐
  │  Partenon   │    │  Partenon MCP   │   │  Partenon       │
  │  Skills     │    │  Servers        │   │  Dashboard API  │
  │  (SKILL.md) │    │  (Python tools) │   │  (FastAPI)      │
  └─────────────┘    └─────────────────┘   └─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   Google Workspace      Stripe               G-Brain / Memory
   (Sheets/Docs/         (payment links,      (SQLite/Postgres)
    Slides/Drive/         invoices)
    Calendar/Gmail)
```

---

## 6. Detailed Design

### 6.1 Repo structure changes

Current structure is preserved. New directories are added:

```
partenon/
├── distribution.yaml                 # Hermes distribution manifest
├── pyproject.toml                    # Package for MCP servers
├── mcp_servers/                      # Native Hermes MCP servers
│   ├── partenon_finance_mcp/
│   ├── partenon_payments_mcp/
│   ├── partenon_ops_mcp/
│   ├── partenon_relations_mcp/
│   ├── partenon_security_mcp/
│   ├── partenon_comms_mcp/
│   └── partenon_memory_mcp/
├── profiles/                         # Hermes-valid profiles
│   ├── partenon-scribe/
│   ├── partenon-herald/
│   ├── partenon-collector/
│   ├── partenon-guardian/
│   ├── partenon-strategist/
│   ├── partenon-diplomat/
│   └── partenon-brain/
├── skills/                           # Hermes-valid shared skills
│   ├── partenon-core/
│   ├── finance/
│   ├── payments/
│   ├── ops/
│   ├── relations/
│   ├── security/
│   ├── comms/
│   └── memory/
├── onboarding/                       # Progressive onboarding scripts
│   ├── __init__.py
│   ├── engine.py
│   └── questions/
├── dashboard_api/                    # FastAPI backend for dashboard
│   ├── main.py
│   └── routers/
├── web/                              # Existing static site
├── dashboard/                        # Existing Next.js dashboard
├── workshop/                         # Existing workshop materials
├── tests/                            # Expanded test suite
└── docs/                             # Updated documentation
```

Existing `hermes/profiles/` is **deprecated but kept** during migration, then removed in a later phase after validation. No files are deleted until the new structure is proven.

### 6.2 Profile distribution

`distribution.yaml`:

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

### 6.3 Per-profile `config.yaml`

Example `profiles/partenon-scribe/config.yaml`:

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
    args: ["-m", "partenon_finance_mcp.server"]
    env:
      PARTENON_MODE: "${PARTENON_MODE:-dry-run}"
      GOOGLE_SERVICE_ACCOUNT_JSON: "${GOOGLE_SERVICE_ACCOUNT_JSON}"
  partenon-memory:
    command: python
    args: ["-m", "partenon_memory_mcp.server"]
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

Each profile enables the MCP servers relevant to its domain. All MCP servers default to `PARTENON_MODE=dry-run`.

### 6.4 MCP servers

Each MCP server is a Python package using the FastMCP library. They expose existing tool functions as MCP tools.

`mcp_servers/partenon_finance_mcp/server.py` example:

```python
from mcp.server.fastmcp import FastMCP
from partenon_finance_mcp.tools import (
    create_budget,
    parse_expenses,
    append_to_sheet,
    run_audit,
)

mcp = FastMCP("partenon-finance")

@mcp.tool()
def create_budget_tool(business_type: str, currency: str = "USD") -> dict:
    """Create a baseline budget for a business type."""
    return create_budget(business_type, currency)

@mcp.tool()
def parse_expenses_tool(file_path: str) -> dict:
    """Parse and classify expenses from a CSV/Excel file."""
    return parse_expenses(file_path)

@mcp.tool()
def append_to_sheet_tool(spreadsheet_id: str, range_name: str, rows: list) -> dict:
    """Append rows to a Google Sheet if credentials exist; otherwise simulate."""
    return append_to_sheet(spreadsheet_id, range_name, rows)

@mcp.tool()
def run_audit_tool(period: str) -> dict:
    """Run a financial audit for a period."""
    return run_audit(period)

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Each server:
- Reads `PARTENON_MODE` env var (`dry-run` or `live`).
- In dry-run mode, returns simulated results and never calls external APIs.
- In live mode, calls real APIs using credentials from env vars.
- Logs every call to a structured log file.

### 6.5 Skills

All `SKILL.md` files follow the Hermes format:

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
- `partenon_finance_create_budget_tool`
- `partenon_finance_parse_expenses_tool`
- `partenon_finance_append_to_sheet_tool`
- `partenon_finance_run_audit_tool`

## Procedure
1. Ask the user for the business type if unknown.
2. If they provide a CSV/Excel file, use `parse_expenses_tool`.
3. If they want a budget, use `create_budget_tool`.
4. In dry-run mode, explain that results are simulated and ask before switching to live mode.

## Examples
User: "Create a budget for a coffee shop."
→ Use `create_budget_tool(business_type="coffee_shop")`

## Onboarding Questions
- What accounting software or spreadsheet do you use?
- Do you have a Google service account for Workspace integration?
- What is your fiscal year start month?
```

### 6.6 Messaging gateway

No custom bot code. Users run:

```bash
hermes gateway setup
hermes gateway start
```

Partenon provides:
- `docs/HERMES_GATEWAY_SETUP.md` with per-platform instructions.
- Recommended `platform_toolsets` blocks in each profile `config.yaml`.
- A `gateway/` directory with example `.env` snippets.

### 6.7 Cron

No custom scheduler. Users run:

```bash
hermes cron create "0 8 * * 1-5" "Run daily finance report" --profile partenon-scribe --deliver telegram
```

Partenon provides:
- `scripts/setup_default_crons.py` that creates recommended cron jobs.
- `docs/CRON_JOBS.md` explaining each job.
- Cron definitions stored in Hermes-native format.

### 6.8 Onboarding engine

The onboarding engine is rewritten to be progressive and credential-aware:

```python
class OnboardingEngine:
    def run(self):
        self.check_hermes_cli()
        self.install_profile_distribution()
        business_type = self.ask_business_type()
        self.generate_document_catalog(business_type)
        self.ask_optional_integrations()  # Google, Stripe, messaging
        self.generate_welcome_docs()
```

Key behaviors:
- Dry-run is the default. The system works immediately.
- Google Workspace, Stripe, and messaging are opt-in.
- Each integration has a small wizard that validates credentials in test mode.
- Business type determines default document catalog and hero objectives.
- Generated artifacts go to `data/` and are loaded by hero profiles.

### 6.9 Dashboard API

A small FastAPI backend is added in `dashboard_api/main.py`. It exposes:

- `GET /api/v1/missions` — list recent missions.
- `GET /api/v1/heroes` — hero status and enabled tools.
- `GET /api/v1/cron` — cron jobs.
- `POST /api/v1/missions` — create a mission (routes through Hermes).
- `GET /api/v1/integrations` — status of Google/Stripe/messaging.

The existing Next.js dashboard is updated to consume this API instead of reading local JSON directly.

### 6.10 Documentation updates

Every code change is paired with a doc update:

| Code change | Doc update |
|---|---|
| Add `distribution.yaml` | `README.md` install section |
| Rewrite profiles | `docs/HERO_GUIDE.md`, `docs/for-developers.md` |
| Add MCP servers | `docs/API.md`, `docs/for-developers.md` |
| Add onboarding | `docs/QUICKSTART.md`, `docs/ENTREPRENEUR_PLAYBOOK.md` |
| Gateway setup | New `docs/HERMES_GATEWAY_SETUP.md` |
| Cron setup | New `docs/CRON_JOBS.md` |
| Dashboard API | `docs/API.md`, `dashboard/README.md` |
| All changes | `CHANGELOG.md`, `TODOS.md` |

---

## 7. Migration Strategy

1. **Phase 0 — Foundation**
   - Add `distribution.yaml`.
   - Create `mcp_servers/` with wrappers for existing tools.
   - Create `profiles/` with valid Hermes `config.yaml` files.
   - Keep existing `hermes/profiles/` untouched for reference.

2. **Phase 1 — Validation**
   - Install Partenon locally via `hermes profile install`.
   - Run each hero in dry-run mode.
   - Validate MCP servers with `hermes mcp test`.
   - Fix schema issues.

3. **Phase 2 — Onboarding**
   - Rewrite onboarding engine.
   - Add progressive credential wizards.
   - Generate business-type-specific catalogs.

4. **Phase 3 — Dashboard and Gateway**
   - Add dashboard API.
   - Update dashboard frontend.
   - Document gateway setup.

5. **Phase 4 — Cleanup**
   - Remove deprecated `hermes/profiles/` after validation.
   - Expand tests.
   - Add CI.

---

## 8. Testing

| Test type | Coverage |
|---|---|
| MCP server tests | Each server has tests for dry-run and live modes |
| Profile validation | Script checks all 7 profiles against Hermes schema |
| Onboarding tests | Simulate user inputs and verify generated artifacts |
| Router tests | Verify intent routing still works |
| Dashboard API tests | Test FastAPI endpoints |
| Integration tests | End-to-end dry-run mission with multiple heroes |

Command to run all tests:

```bash
make test
```

---

## 9. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Hermes CLI changes its schema | Pin `hermes_requires` and validate against installed version |
| MCP servers are too slow | Add caching and async handlers |
| Users struggle with Hermes install | Document fallback to PyPI `pip install hermes-agent` |
| Credential setup is confusing | Progressive onboarding with validation at each step |
| Existing tools break during wrapping | Keep original scripts and run both old and new tests during migration |
| Website still over-promises | Update website copy to distinguish dry-run vs. live mode |

---

## 10. Success Criteria

1. `hermes profile install github.com/cuentadeservicio377-cell/partenon` completes without errors.
2. `partenon-scribe chat` responds to "create a budget" in dry-run mode.
3. `make test` passes with at least 50 tests.
4. All 7 profiles validate against Hermes schema.
5. At least one end-to-end dry-run mission runs across 2+ heroes.
6. Documentation is updated and consistent.
7. No existing functionality is removed.

---

## 11. Open Questions

1. Should we publish MCP servers as separate PyPI packages or keep them in-repo?
2. Which OpenRouter model should be the default for each profile?
3. Do we need a separate `partenon` CLI wrapper, or do we rely entirely on `hermes` commands?
4. Should the dashboard API be bundled in the same Docker Compose as the dashboard?
