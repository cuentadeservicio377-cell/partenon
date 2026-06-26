# Missing Implementation Audit

This document tracks gaps between what the Partenon website and documentation promise and what is currently implemented in the repository. It is written in English because the public repository targets an international audience.

## How to read this file

- **Severity**: `BLOCKER` means the feature cannot be used without it; `HIGH` means a core promise is unfulfilled; `MEDIUM` means quality or completeness is affected; `LOW` means cosmetic or nice-to-have.
- **Status**: `NOT_STARTED`, `PARTIAL`, `STUB`, `DONE`.

---

## 1. Core platform promises

### 1.1 Functional eval loop
- **Promise**: `web/developers.html` and `docs/architecture.md` describe a quality-measurement loop with a judge skill and configurable threshold.
- **Reality**: `partenon-core/tools/eval_loop.py` is implemented and can score mission outputs against completeness, format, safety, and context criteria. It is not yet wired into the router or hero runtime.
- **Severity**: MEDIUM
- **Status**: PARTIAL
- **Files**: `partenon-core/tools/eval_loop.py`, `partenon-core/SKILL.md`
- **Suggested fix**: Call `EvalLoop.evaluate()` from the mission router or a post-action hook, and persist scores in G-Brain.

### 1.2 Mission router
- **Promise**: `partenon-core` routes user intent to the correct hero.
- **Reality**: `partenon-core/tools/router.py` has Spanish keyword/pattern dictionaries and does not load hero configs dynamically. It classifies a handful of finance and operations keywords only.
- **Severity**: HIGH
- **Status**: PARTIAL
- **Files**: `partenon-core/tools/router.py`
- **Suggested fix**: Translate keywords to English, load profile metadata from `hermes/profiles/*/config.yaml`, and expose a `classify_intent(text)` API that returns a ranked list of profiles.

### 1.3 Workflow engine
- **Promise**: Multi-hero missions are orchestrated by a workflow engine.
- **Reality**: `partenon-core/tools/workflow_engine.py` contains hard-coded Spanish event/action placeholders and no execution runtime.
- **Severity**: HIGH
- **Status**: STUB
- **Files**: `partenon-core/tools/workflow_engine.py`
- **Suggested fix**: Define a minimal workflow schema (trigger, actions, handoffs), persist workflows in JSON, and execute them step by step with G-Brain state.

### 1.4 Onboarding engine
- **Promise**: New heroes learn company context from a structured onboarding flow.
- **Reality**: `partenon-core/tools/onboarding_engine.py` and `onboarding_flow.py` exist but are mostly skeletons.
- **Severity**: MEDIUM
- **Status**: STUB
- **Files**: `partenon-core/tools/onboarding_engine.py`, `partenon-core/tools/onboarding_flow.py`
- **Suggested fix**: Read `.brain`, `.finance`, `.design`, `.relations`, `.payments`, and `.security` files and produce a context summary that is passed to the hero at runtime.

---

## 2. Hero profiles

### 2.1 Treasurer (finance) — `partenon-tesorero`
- **Status**: PARTIAL
- **Done**: SOUL, config, SKILL, templates, cron, and finance tools have been translated to English. `google_sheets.py` can create a spreadsheet and seed headers. `parsers.py` can read Excel/CSV expenses. `templates.py` generates local Excel templates.
- **Gaps**:
  - No end-to-end demo that parses an uploaded file and writes to Google Sheets.
  - `CATEGORY_KEYWORDS` in `parsers.py` are English-only; historic Spanish transaction descriptions are accepted but inferred categories will be English words. This is intentional but must be documented.
  - No automated tests.
- **Files**: `hermes/profiles/partenon-tesorero/skills/finance/tools/*.py`

### 2.2 Messenger (communications) — `partenon-mensajero`
- **Status**: PARTIAL
- **Done**: SOUL, config, SKILL, `.design` template, `.env.example`, cron, and comms tools are translated to English. `brand_intake.py`, `copy_generator.py`, and `content_calendar.py` are functional.
- **Gaps**:
  - No actual publishing integration (LinkedIn, Instagram, WordPress, etc.).
  - `config.yaml` references `wordpress` and `ssh` tools but no implementation exists.
  - No Gmail MCP integration for sending newsletters.
- **Files**: `hermes/profiles/partenon-mensajero/`

### 2.3 Collector (payments) — `partenon-cobrador`
- **Status**: PARTIAL
- **Done**: SOUL, config, SKILL, `.env.example`, `.payments` template, cron, and Stripe tools are translated to English. `stripe_tools.py` can create payment links, subscriptions, reminders, and record payments in local mode or via the Stripe library.
- **Gaps**:
  - No end-to-end Stripe MCP wiring.
  - No invoice generation or PDF receipt creation.
  - Collections rely on local JSON; no real Gmail/WhatsApp reminder dispatch.
- **Files**: `hermes/profiles/partenon-cobrador/`

### 2.4 Guardian (security / NVIDIA) — `partenon-guardian`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.env.example`, `.security` template, cron, and `key_manager.py` are translated to English. `key_manager.py` can list keys, rotate placeholders, audit access, validate access, and recommend models.
- **Gaps**:
  - No real secrets-manager integration (only environment variables).
  - No NVIDIA NeMo / OpenShell integration.
  - No automated audit log persistence.
- **Files**: `hermes/profiles/partenon-guardian/`

### 2.5 Strategist (operations) — `partenon-estratega`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.ops`, template, cron, SKILL.md, and ops tools are translated to English. `projects.py`, `tasks.py`, `checklists.py`, `goals.py`, and `briefings.py` are functional with English field names.
- **Gaps**:
  - No Google Calendar or Gmail MCP integration is wired; tools read local JSON only.
  - No automated tests.
- **Files**: `hermes/profiles/partenon-estratega/skills/ops/tools/*.py`

### 2.6 Diplomat (relations) — `partenon-diplomatico`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.relations` template, cron, SKILL.md, and relations tools are translated to English. `crm.py` and `followups.py` use English field names and match the translated `.relations` template.
- **Gaps**:
  - No actual Google Contacts or Gmail integration.
  - No handoff automation with Strategist beyond documentation.
  - No automated tests.
- **Files**: `hermes/profiles/partenon-diplomatico/skills/relations/tools/*.py`

### 2.7 Brain (intelligence / memory) — `partenon-brain`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.env.example`, `.brain` template, cron, SKILL.md, and `gbrain_client.py` are translated to English.
- **Gaps**:
  - `gbrain_client.py` shells out to a `gbrain` binary that is not bundled in this repo.
  - No persistent G-Brain implementation beyond the separate `gbrain/` experiment.
  - The website promises collective memory, conflict detection, and onboarding context.
- **Files**: `hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py`, `gbrain/`

---

## 3. Data files

### 3.1 `data/tasks.json`
- **Gap**: Translated to English in this pass.
- **Impact**: Dashboard now shows English missions.
- **Status**: DONE

### 3.2 `data/cron.json`
- **Gap**: Commands now point to existing scripts/tools instead of non-existent `partenon.*` modules. Some entries are still illustrative.
- **Impact**: Cron entries are runnable placeholders.
- **Status**: PARTIAL
- **Suggested fix**: Replace Treasurer demo command with a real weekly report script; add Guardian CLI entry point.

---

## 4. Install and environment

### 4.1 Hermes CLI availability
- **Promise**: Website and docs imply a smooth install of Hermes profiles.
- **Reality**: Hermes Agent CLI is not bundled in this repo. `install.sh` and `scripts/setup_hermes.py` handle this gracefully by checking PATH and printing instructions.
- **Severity**: MEDIUM (handled, but public expectations need to be set)
- **Status**: PARTIAL
- **Suggested fix**: Keep the install note in `README.md` and `web/developers.html`.

### 4.2 `GBRAIN_DATABASE_URL` mismatch
- **Promise**: `.env.example` documents `GBRAIN_DATABASE_URL`.
- **Reality**: `gbrain/server.py` and `partenon-core/config/mcp/servers.yaml` use `GBrain_DATABASE_URL`.
- **Severity**: MEDIUM
- **Status**: DOCUMENTED
- **Suggested fix**: Standardize on one variable name across `.env.example`, `gbrain/server.py`, and `partenon-core/config/mcp/servers.yaml`.

### 4.3 Demo output filenames
- **Promise**: `README.md` and `docs/for-developers.md` say the demo creates `data/sample_gastos.xlsx` and `data/sample_gastos_report.json`.
- **Reality**: `scripts/demo_tesorero.py` creates `data/sample_expenses.xlsx` and `data/sample_expenses_report.json`.
- **Severity**: LOW
- **Status**: PARTIAL
- **Suggested fix**: Update docs to match the actual filenames.

---

## 5. Web pages vs repository

### 5.1 Live integrations
- **Promise**: `web/index.html` shows Google Workspace, Stripe, NVIDIA, and G-Brain as working integrations.
- **Reality**: Integrations are partially implemented as local tools that require real credentials to do anything live.
- **Severity**: HIGH
- **Status**: PARTIAL
- **Suggested fix**: Add a "current status" section to the site, or implement at least one sandboxed end-to-end flow (e.g., Stripe test payment link).

### 5.2 Counter and metrics
- **Promise**: `web/index.html` displays `10 -> 1M` growth milestones.
- **Reality**: Numbers are static HTML. No tracking or dynamic reporting exists.
- **Severity**: LOW (marketing page)
- **Status**: NOT_STARTED

### 5.3 Dashboard
- **Promise**: `web/developers.html` and `README.md` describe a working dashboard.
- **Reality**: The Next.js dashboard builds and runs, but it only reads/writes local JSON files (`data/tasks.json`, `data/cron.json`). It is not connected to heroes or G-Brain.
- **Severity**: MEDIUM
- **Status**: PARTIAL
- **Suggested fix**: Keep the dashboard as a local ops view and document it clearly.

---

## 6. Testing and quality

### 6.1 No automated tests
- **Gap**: There is no `tests/` directory or CI workflow.
- **Impact**: Refactors and translations cannot be verified automatically.
- **Severity**: HIGH
- **Status**: NOT_STARTED
- **Suggested fix**: Add unit tests for `partenon-core` tools and at least one integration test for the Treasurer parser/template flow.

### 6.2 No linting or formatting config
- **Gap**: No `pyproject.toml`, `ruff.toml`, or GitHub Actions.
- **Severity**: LOW
- **Status**: NOT_STARTED
- **Suggested fix**: Add a minimal Python formatter/linter and a pre-commit hook.

---

## 7. Suggested priority order

1. Implement a real intent router in `partenon-core`.
2. Implement the workflow engine runtime.
3. Wire the eval loop into the router.
4. Add publishing integrations for Messenger and dispatch integrations for Collector/Diplomat.
5. Add tests for Treasurer and core tools.
6. Standardize `GBRAIN_DATABASE_URL` naming.
7. Update README/demo output filenames if still inconsistent.
8. Add CI/linting.

---

## 8. Files changed in this audit/fix pass

- `README.md` — translated, badges, install note.
- `docs/for-founders.md` — translated.
- `docs/for-developers.md` — translated, install note, known gaps.
- `docs/architecture.md` — translated.
- `.env.example` — translated comments, added `HERMES_CLI_PATH` placeholder.
- `install.sh` / `scripts/setup_hermes.py` — safe installer, no fake URLs, demo run.
- `partenon-core/` — README, SKILL, and tools translated to English; `eval_loop.py` added.
- `gbrain/` — README, server, tools translated to English.
- `hermes/profiles/partenon-*/` — all seven hero profiles translated: SOUL, config, SKILL, `.env.example`, cron, templates, and Python tools.
- `data/cron.json` / `data/tasks.json` — translated and mapped to existing scripts.
- `MISSING_IMPLEMENTATION.md` — this file.
