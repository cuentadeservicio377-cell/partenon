# Partenon API and CLI Reference

This document describes the programmable interfaces that exist in the repository today. It covers the Python core, scripts, and example stubs. For the Hermes Agent natural-language interface, see [`docs/HERO_GUIDE.md`](HERO_GUIDE.md).

---

## 1. `partenon-core` Python tools

All files are under [`partenon-core/tools/`](../partenon-core/tools/).

### `router.py` — Intent Router

Routes natural-language messages to the correct hero profile.

```python
from partenon_core.tools.router import route_intent, get_router

profile = route_intent("Organize my numbers")
print(profile)  # "partenon-tesorero"
```

**Functions**

| Function | Args | Returns |
|----------|------|---------|
| `route_intent(message)` | `message: str` | `str | None` — profile name or `None` if no match |
| `IntentRouter.route(message)` | `message: str` | `str | None` |
| `IntentRouter.route_with_context(message, last_profile, last_entity)` | same + context | `dict` with `profile`, `entity`, `confidence` |
| `get_router()` | none | singleton `IntentRouter` |

**Confidence values**

- `0.8` — direct route
- `0.5` — fallback to `last_profile`
- `0.0` — no route found

**Example**

```bash
python partenon-core/tools/router.py
```

---

### `onboarding_engine.py` — Installation Wizard

Creates local data files, industry catalog, sample client/project, and Google Workspace structure.

```python
from partenon_core.tools.onboarding_engine import OnboardingEngine

engine = OnboardingEngine("config/company.yaml")
result = engine.run_full_onboarding()
print(result["success"])   # True or False
print(result["steps"])     # list of step dicts
print(result["errors"])    # list of error strings
```

**Functions**

| Function | Args | Returns |
|----------|------|---------|
| `OnboardingEngine(config_path)` | `config_path: str` (optional) | engine instance |
| `run_full_onboarding()` | none | `dict` with `success`, `steps`, `errors` |
| `get_onboarding_status()` | none | `dict` with config existence, active profiles, etc. |
| `get_onboarding_engine()` | none | singleton `OnboardingEngine` |

**Example**

```bash
python partenon-core/tools/onboarding_engine.py
```

---

### `workflow_engine.py` — Event-Driven Workflows

Emits events and runs hard-coded multi-step workflows. Used for hero handoffs.

```python
from partenon_core.tools.workflow_engine import WorkflowEngine

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

**Functions**

| Function | Args | Returns |
|----------|------|---------|
| `WorkflowEngine(data_dir)` | `data_dir: str` (optional) | engine instance |
| `emit_event(type, source, entity_id, entity_type, data)` | event fields | `dict` representing the event |
| `process_event(event)` | `event: dict` | `list[str]` of executed actions |
| `detect_automatic_events()` | none | `list[dict]` of emitted overdue/pipeline events |

**Built-in workflows**

| Trigger | Actions |
|---------|---------|
| `client_contracted` | create project, create goal, generate checklist, notify |
| `task_overdue` | urgent nudge, suggest reschedule |
| `pipeline_stalled` | nudge pipeline, suggest campaign |
| `quote_approved` | generate contract, register expected income, create project |
| `project_progress_50` | review deadlines, alert if behind |
| `new_client` | register client, create follow-up task, welcome nudge |

---

### `eval_loop.py` — Output Quality Judge

Scores a hero mission output against completeness, format, safety, and context.

```python
from partenon_core.tools.eval_loop import EvalLoop

loop = EvalLoop()
result = loop.evaluate(
    mission_id="mission-001",
    profile="partenon-tesorero",
    output={
        "mission_id": "mission-001",
        "profile": "partenon-tesorero",
        "status": "completed",
        "output": {"income": 4000, "margin": 2361},
    },
    company_context={"name": "Acme Coffee", "industry": "food"},
)
print(result.score, result.passed)
```

**Functions**

| Function | Args | Returns |
|----------|------|---------|
| `EvalLoop(eval_dir)` | `eval_dir: Path` (optional) | evaluator instance |
| `evaluate(mission_id, profile, output, company_context)` | mission output | `EvalResult` dataclass |
| `list_results()` | none | `list[dict]` |
| `summary()` | none | `dict` with `total`, `passed`, `average_score` |

**Pass threshold**: `7.0 / 10.0`

**Criteria weights**

| Criterion | Weight |
|-----------|--------|
| completeness | 0.35 |
| format | 0.25 |
| safety | 0.25 |
| context | 0.15 |

---

### `config_loader.py` — Company Configuration

Reads `config/company.yaml`.

```python
from partenon_core.tools.config_loader import ConfigLoader, get_config

config = get_config()
print(config.name)       # "My Company"
print(config.industry)   # "services"
print(config.currency)   # "USD"
print(config.language)   # "en"
print(config.timezone)   # "UTC"
print(config.integration_active("google_workspace"))
print(config.department_active("treasurer"))
```

**Properties / functions**

| Name | Returns |
|------|---------|
| `name` | company name or `"My Company"` |
| `industry` | industry or `"services"` |
| `currency` | currency or `"USD"` |
| `language` | language or `"en"` |
| `timezone` | timezone or `"UTC"` |
| `integration_active(name)` | `bool` |
| `department_active(name)` | `bool` |
| `get_config()` | singleton `ConfigLoader` |

---

## 2. Scripts

All scripts are under [`scripts/`](../scripts/).

### `demo_tesorero.py`

Generates a sample finance workbook and JSON report.

```bash
python scripts/demo_tesorero.py
```

**Outputs**

- `data/sample_expenses.xlsx` — workbook with Dashboard, Income, Fixed Expenses, Variable Expenses, Suppliers sheets.
- `data/sample_expenses_report.json` — report with `income`, `fixed_expenses`, `variable_expenses`, `margin`, `margin_pct`, `alerts`.

**Return shape**

```json
{
  "timestamp": "2026-06-26T21:00:00Z",
  "income": 4000.0,
  "fixed_expenses": 609.0,
  "variable_expenses": 1030.0,
  "margin": 2361.0,
  "margin_pct": 59.02,
  "alerts": []
}
```

---

### `setup_hermes.py`

Alternative installer to `install.sh`.

```bash
python scripts/setup_hermes.py
```

**What it does**

1. Creates `.venv` if missing.
2. Installs `requirements.txt`.
3. Checks for `hermes` CLI in PATH.
4. Copies `partenon-core/SKILL.md` to `~/.hermes/skills/partenon-core`.
5. Installs the seven profiles if `hermes` is available.
6. Copies `.env.example` to `.env`.
7. Creates `data/` and `logs/`.
8. Runs `scripts/demo_tesorero.py`.

**Return code**: `0` on success.

---

### `capture.py`

Captures desktop and mobile screenshots of the static web pages using Playwright.

```bash
# Start a local server on port 8080 first, e.g.:
# python -m http.server 8080 --directory web
python scripts/capture.py
```

**Outputs**

- `screenshots/index-desktop.png`
- `screenshots/index-mobile.png`
- `screenshots/heroes-desktop.png`
- `screenshots/heroes-mobile.png`
- `screenshots/developers-desktop.png`
- `screenshots/developers-mobile.png`

---

## 3. Example stubs

These files are placeholders that document the intended API shapes. They are not production backends.

### `examples/api-server-stub.py`

A FastAPI stub with the endpoints documented on `web/developers.html`.

```bash
pip install fastapi uvicorn
uvicorn examples.api-server-stub:app --reload --port 8000
```

**Endpoints**

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/heroes` | List heroes |
| GET | `/api/v1/heroes/{hero_id}` | Get one hero |
| POST | `/api/v1/missions` | Create a stub mission |
| GET | `/api/v1/missions/{mission_id}` | Get mission |
| GET | `/api/v1/mcp/tools` | List MCP tools |
| POST | `/api/v1/mcp/call` | Stub tool call |
| GET | `/api/v1/status` | System status |

**Example**

```bash
curl -X POST http://localhost:8000/api/v1/missions \
  -H "Content-Type: application/json" \
  -d '{"hero": "scribe", "type": "expense-audit"}'
```

---

### `examples/hermes-cli-stub.py`

Demonstrates the intended `hermes` CLI shape.

```bash
python examples/hermes-cli-stub.py init --name "Acme Coffee"
python examples/hermes-cli-stub.py activate scribe
python examples/hermes-cli-stub.py mission scribe --type financial-model
python examples/hermes-cli-stub.py status --verbose
```

**Commands**

| Command | Args |
|---------|------|
| `init --name` | company name |
| `activate <hero>` | hero id |
| `deactivate <hero>` | hero id |
| `mission <hero> --type <type>` | hero + mission type |
| `status [--verbose]` | show state |
| `dashboard [--port]` | stub dashboard pointer |
| `test [--all]` | stub tests |
| `config --edit` | show `.env` |
| `backup --to` | stub backup |

**State file**: `data/hermes_cli_state.json`

---

### `examples/mcp-client-example.py`

Demonstrates calling the G-Brain MCP server.

```bash
pip install mcp
python examples/mcp-client-example.py
```

It launches `gbrain.server` over stdio with `GBrain_DATABASE_URL=sqlite:///data/gbrain_example.db`, lists tools, stores a learning, and searches missions.

---

## 4. G-Brain MCP tools

The local MCP server is [`gbrain/server.py`](../gbrain/server.py). Tools are defined in [`gbrain/tools.py`](../gbrain/tools.py).

| Tool name | Args | Returns |
|-----------|------|---------|
| `gbrain_read_profile` | `profile: str`, `scope: str = "default"` | JSON string of profile scope |
| `gbrain_write_profile` | `profile: str`, `scope: str`, `content: str` | `"ok"` or error |
| `gbrain_write_mission` | `mission_id`, `profile`, `title`, `status`, `input_data`, `output_data`, `learnings` | `"ok"` |
| `gbrain_search_missions` | `profile: str` (optional), `status: str` (optional) | JSON list of missions |
| `gbrain_search_entities` | `query: str`, `kind: str` (optional) | JSON list of entities |
| `gbrain_store_learning` | `profile: str`, `insight: str` | `"ok"` |

---

## 5. Hero profile tools

Each hero exposes Python tools under `hermes/profiles/<profile>/skills/<skill>/tools/`. They are documented per hero in [`docs/HERO_GUIDE.md`](HERO_GUIDE.md) and can be run directly when they include a `main()` function.

```bash
python hermes/profiles/partenon-mensajero/skills/comms/tools/content_calendar.py "topic" linkedin 7
python hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py
python hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py
```
