# Partenon API and CLI Reference

This document lists the commands, scripts, and API endpoints that exist in the repository today. Some are fully functional Python tools; others are stubs that document the intended interface while backend integrations are completed.

## Terminology

- **Hero** — one of the 7 Partenon profiles.
- **Mission** — a single task assigned to a hero.
- **Profile file** — `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations`, or `.brain`.
- **MCP** — Model Context Protocol server used by Hermes Agent.

---

## Installation and setup commands

### Bash installer

```bash
./install.sh
```

Creates `.venv`, installs dependencies, checks for Hermes CLI, installs the `partenon-core` skill reference, copies `.env.example` to `.env`, and runs the Scribe demo.

### Python setup helper

```bash
python scripts/setup_hermes.py
```

Same steps as `install.sh`, implemented in Python.

### Environment file

```bash
cp .env.example .env
```

Edit `.env` with your credentials. See [`SECURITY.md`](SECURITY.md) for safe handling.

---

## Demo scripts

### Scribe demo

```bash
python scripts/demo_tesorero.py
```

Creates:

- `data/sample_expenses.xlsx` — workbook with Dashboard, Income, Fixed Expenses, Variable Expenses, and Suppliers sheets.
- `data/sample_expenses_report.json` — income, fixed expenses, variable expenses, margin, margin percentage, and alerts.

Return value: prints the JSON report to stdout and writes it to disk.

---

## Core Python modules

All paths are relative to the repository root.

### Config loader

```python
from partenon-core.tools.config_loader import get_config

config = get_config()
print(config.name)               # company name
print(config.industry)           # industry
print(config.currency)           # base currency
print(config.integration_active("google_workspace"))
print(config.department_active("treasurer"))
```

### Intent router

```python
from partenon-core.tools.router import get_router

router = get_router()
profile = router.route("Organize my numbers")   # -> "partenon-tesorero"
result = router.route_with_context("Follow up with Acme", last_profile="partenon-diplomatico")
# result -> {"profile": "partenon-diplomatico", "entity": "Acme Inc", "confidence": 0.5}
```

### Workflow engine

```python
from partenon-core.tools.workflow_engine import WorkflowEngine

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
print(event["actions_executed"])
```

Actions executed may include `create_operations_project`, `create_initiative_goal`, `generate_checklist`, and `notify_user`.

### Onboarding engine

```python
from partenon-core.tools.onboarding_engine import OnboardingEngine

engine = OnboardingEngine()
result = engine.run_full_onboarding()
print(result["success"])   # False until config/company.yaml is completed
```

### Eval loop

```python
from partenon-core.tools.eval_loop import EvalLoop

loop = EvalLoop()
result = loop.evaluate(
    mission_id="mission-001",
    profile="partenon-tesorero",
    output={"mission_id": "mission-001", "profile": "partenon-tesorero", "status": "completed", "output": {"margin": 2361.0}},
    company_context={"name": "Aurora Coffee", "industry": "food", "currency": "USD"},
)
print(result.score)    # 0.0 - 10.0
print(result.passed)   # True if score >= 7.0
```

> The eval loop is a functional stub. It scores completeness, format, safety, and context, but is not yet wired into every hero runtime.

---

## Hermes CLI

The real Hermes CLI is distributed separately by Nous Research. If you have it installed, Partenon profiles can be used like this:

```bash
hermes profile install hermes/profiles/partenon-tesorero --alias partenon-tesorero
hermes profile use partenon-tesorero
hermes run "Record a $500 advertising expense"
```

### CLI stub

A stub implementation is provided in `examples/hermes-cli-stub.py` for interface exploration:

```bash
python examples/hermes-cli-stub.py init --name "Cafe Central"
python examples/hermes-cli-stub.py activate scribe
python examples/hermes-cli-stub.py mission scribe --type financial-model
python examples/hermes-cli-stub.py status --verbose
python examples/hermes-cli-stub.py config --edit
```

Available subcommands: `init`, `activate`, `deactivate`, `mission`, `status`, `dashboard`, `test`, `config`, `backup`.

State is stored in `data/hermes_cli_state.json`.

---

## REST API stub

`examples/api-server-stub.py` is a FastAPI application that returns the documented JSON shapes.

### Run

```bash
pip install fastapi uvicorn pydantic
uvicorn examples.api-server-stub:app --reload --port 8000
```

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/heroes` | List all heroes. |
| GET | `/api/v1/heroes/{hero_id}` | Get a single hero. |
| POST | `/api/v1/missions` | Create a mission. Body: `{"hero": "scribe", "type": "financial-model", "input_data": {}}` |
| GET | `/api/v1/missions/{mission_id}` | Get mission result. |
| GET | `/api/v1/mcp/tools` | List available MCP tools. |
| POST | `/api/v1/mcp/call` | Call an MCP tool. Body: `{"name": "create_spreadsheet", "arguments": {"title": "Finances"}}` |
| GET | `/api/v1/status` | System status and integration health. |

### Example calls

```bash
curl http://localhost:8000/api/v1/heroes
curl http://localhost:8000/api/v1/heroes/scribe

curl -X POST http://localhost:8000/api/v1/missions \
  -H "Content-Type: application/json" \
  -d '{"hero": "scribe", "type": "expense-audit"}'

curl http://localhost:8000/api/v1/mcp/tools

curl -X POST http://localhost:8000/api/v1/mcp/call \
  -H "Content-Type: application/json" \
  -d '{"name": "create_spreadsheet", "arguments": {"title": "Partenon Finances"}}'

curl http://localhost:8000/api/v1/status
```

> This is a stub. It returns static shapes and does not execute real hero missions.

---

## G-Brain MCP API

The G-Brain MCP server exposes shared memory tools. It is implemented in `gbrain/server.py` and backed by SQLite or PostgreSQL via `gbrain/tools.py`.

### Run the server

```bash
python -m gbrain.server
```

Environment: `GBrain_DATABASE_URL=sqlite:///data/gbrain.db` or `postgresql://localhost:5432/gbrain`.

### Tools

| Tool | Arguments | Returns |
|------|-----------|---------|
| `gbrain_read_profile` | `profile`, `scope="default"` | JSON string with profile scope content. |
| `gbrain_write_profile` | `profile`, `scope`, `content` (JSON string) | `"ok"` or error. |
| `gbrain_write_mission` | `mission_id`, `profile`, `title`, `status`, `input_data`, `output_data`, `learnings` | `"ok"` or error. |
| `gbrain_search_missions` | `profile` (optional), `status` (optional) | JSON array of missions. |
| `gbrain_search_entities` | `query`, `kind` (optional) | JSON array of entities. |
| `gbrain_store_learning` | `profile`, `insight` | `"ok"` or error. |

### Python client example

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(
        command="python",
        args=["-m", "gbrain.server"],
        env={"GBrain_DATABASE_URL": "sqlite:///data/gbrain.db"},
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "gbrain_store_learning",
                {"profile": "scribe", "insight": "Coffee expenses spiked 20% in June."}
            )
            print(result)

asyncio.run(main())
```

A full example is in `examples/mcp-client-example.py`.

---

## Profile tool APIs

### Scribe

```python
from hermes.profiles.partenon-tesorero.skills.finance.tools.audit import get_audit
from hermes.profiles.partenon-tesorero.skills.finance.tools.templates import get_templates
from hermes.profiles.partenon-tesorero.skills.finance.tools.google_sheets import get_google_sheets

audit = get_audit()
audit.run_daily_report("output/daily_report.json")

get_templates().create_budget("budget.xlsx")
get_templates().create_vendors("vendors.xlsx")
get_templates().create_cash_flow("cash_flow.xlsx", months=6)

sheets = get_google_sheets()
sheet_id = sheets.create_dashboard("Partenon Finances")
```

### Herald

```python
from hermes.profiles.partenon-mensajero.skills.comms.tools.content_calendar import generate_calendar, save_calendar
from hermes.profiles.partenon-mensajero.skills.comms.tools.copy_generator import generate_copy
from hermes.profiles.partenon-mensajero.skills.comms.tools.seo_geo_optimizer import analyze

calendar = generate_calendar("automation for SMBs", ["linkedin", "instagram"], 14)
save_calendar(calendar)

copy = generate_copy("post", "payment automation", "linkedin")
seo = analyze("payment automation for SMEs")
```

### Collector

```python
from hermes.profiles.partenon-cobrador.skills.payments.tools.stripe_tools import (
    create_payment_link, create_subscription, create_invoice,
    send_payment_reminder, record_payment, list_charges,
    generate_income_report, monitor_fraud
)

create_payment_link({"name": "Consultation"}, {"amount": 15000, "currency": "mxn"})
create_subscription({"email": "client@example.com"}, {"amount": 5000, "interval": "month"})
create_invoice({"email": "client@example.com"}, [{"description": "Service", "amount": 10000}])
list_charges("2026-06-01", "2026-06-30")
generate_income_report("2026-06-01", "2026-06-30")
monitor_fraud()
```

### Guardian

```python
from hermes.profiles.partenon-guardian.skills.security.tools.key_manager import list_keys, rotate_key, audit_access
from hermes.profiles.partenon-guardian.skills.security.tools.audit_logger import audit_log, get_audit_logs

list_keys()
rotate_key("stripe")
audit_access("partenon-tesorero")
audit_log("access", "partenon-tesorero", "google_sheets", "read", "allowed")
get_audit_logs(profile="partenon-tesorero", limit=10)
```

### Strategist

```python
from hermes.profiles.partenon-estratega.skills.ops.tools.projects import get_projects
from hermes.profiles.partenon-estratega.skills.ops.tools.tasks import get_tasks
from hermes.profiles.partenon-estratega.skills.ops.tools.briefings import generate_morning_briefing

projects = get_projects()
projects.create_project("Q3 launch", client_name="Acme", amount=10000, delivery_date="2026-09-30")
projects.get_projects_summary()

tasks = get_tasks()
tasks.create_task("PROJ-001", "Draft copy", assignee="Herald", due_date="2026-07-10")
tasks.get_overdue_tasks()

generate_morning_briefing(user_name="Alex")
```

### Diplomat

```python
from hermes.profiles.partenon-diplomatico.skills.relations.tools.crm import get_relations_crm
from hermes.profiles.partenon-diplomatico.skills.relations.tools.followups import run_daily_followups
from hermes.profiles.partenon-diplomatico.skills.relations.tools.generate_proposal import generate_proposal

crm = get_relations_crm()
crm.add_client("Acme Inc", email="hello@acme.test")
crm.add_milestone("CLI-001", "Sign contract", "2026-07-15")
crm.confirm_milestone("MIL-CLI-001-01")

run_daily_followups()
generate_proposal("CLI-001", "Operations Package", amount=50000, duration_days=45)
```

### Brain

```python
from hermes.profiles.partenon-brain.skills.memory.tools.gbrain_client import GBrainClient

client = GBrainClient()
client.put_page("memory/payment-terms", "50% upfront for projects over $5,000.", tags=["decision", "scribe"])
client.get_page("memory/payment-terms")
client.search("payment terms")
client.conflicts("scribe")
```

---

## Dashboard

The dashboard is a Next.js app in `dashboard/`.

```bash
cd dashboard
npm install
npm run dev      # http://localhost:3000
npm run build    # production build
npm run start    # production server
```

Default login: `admin` / `partenon`. Change via `DASHBOARD_APP_USERNAME` and `DASHBOARD_APP_PASSWORD` in `.env`.

The dashboard reads and writes:

- `data/tasks.json` — mission kanban.
- `data/cron.json` — cron job manager.

---

## Docker

```bash
docker-compose up --build
```

Services:

- `gbrain` — PostgreSQL 16 on port 5432.
- `dashboard` — Next.js dashboard on port 3000.

The dashboard container mounts `./data:/app/data:rw`.

---

## Known limitations

- The REST API stub does not run real hero missions.
- The Hermes CLI stub is for interface exploration only.
- Live Google Workspace, Stripe, and G-Brain integrations require real credentials.
- The eval loop is not yet enforced automatically on every mission.
