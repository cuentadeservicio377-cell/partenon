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
- **Reality**: `partenon-core/tools/router.py` is implemented in English with keyword/pattern dictionaries for all 7 profiles, but it does not load profile metadata dynamically and uses simple scoring.
- **Severity**: MEDIUM
- **Status**: PARTIAL
- **Files**: `partenon-core/tools/router.py`
- **Suggested fix**: Load profile metadata from `hermes/profiles/*/config.yaml` and expose a `classify_intent(text)` API that returns a ranked list of profiles.

### 1.3 Workflow engine
- **Promise**: Multi-hero missions are orchestrated by a workflow engine.
- **Reality**: `partenon-core/tools/workflow_engine.py` contains hard-coded event/action workflows and can emit/process events locally. It does not dispatch to heroes or external systems.
- **Severity**: HIGH
- **Status**: PARTIAL
- **Files**: `partenon-core/tools/workflow_engine.py`
- **Suggested fix**: Wire action handlers to the corresponding hero tools and persist workflows in G-Brain.

### 1.4 Onboarding engine
- **Promise**: New heroes learn company context from a structured onboarding flow.
- **Reality**: `partenon-core/tools/onboarding_engine.py` and `onboarding_flow.py` exist and can create local data files, industry catalogs, sample data, and welcome documents. They do not yet read all profile files or pass context to heroes at runtime.
- **Severity**: MEDIUM
- **Status**: PARTIAL
- **Files**: `partenon-core/tools/onboarding_engine.py`, `partenon-core/tools/onboarding_flow.py`
- **Suggested fix**: Read `.brain`, `.finance`, `.design`, `.relations`, `.payments`, and `.security` files and produce a context summary that is passed to the hero at runtime.

---

## 2. Hero profiles

### 2.1 Scribe (finance) — `partenon-scribe`
- **Status**: PARTIAL
- **Done**: SOUL, config, SKILL, templates, cron, and finance tools translated to English. `google_sheets.py` can create a spreadsheet and seed headers. `parsers.py` can read Excel/CSV expenses. `templates.py` generates local Excel templates.
- **Gaps**:
  - No end-to-end demo that parses an uploaded file and writes to Google Sheets.
  - `CATEGORY_KEYWORDS` in `parsers.py` are English-only; historic Spanish transaction descriptions are accepted as aliases but inferred categories will be English words. This is intentional but must be documented.
  - No automated tests.
- **Files**: `hermes/profiles/partenon-scribe/skills/finance/tools/*.py`

### 2.2 Herald (communications) — `partenon-herald`
- **Status**: PARTIAL
- **Done**: SOUL, config, SKILL, `.design` template, `.env.example`, cron, and comms tools are in English. `brand_intake.py`, `copy_generator.py`, and `content_calendar.py` are functional.
- **Gaps**:
  - No actual publishing integration (LinkedIn, Instagram, WordPress, etc.).
  - `config.yaml` references `wordpress` and `ssh` tools but no implementation exists.
  - No Gmail MCP integration for sending newsletters.
- **Files**: `hermes/profiles/partenon-herald/`

### 2.3 Collector (payments) — `partenon-collector`
- **Status**: PARTIAL
- **Done**: SOUL, config, SKILL, `.env.example`, `.payments` template, cron, and Stripe tools are in English. `stripe_tools.py` can create payment links, subscriptions, reminders, and record payments in local mode or via the Stripe library.
- **Gaps**:
  - No end-to-end Stripe MCP wiring.
  - No invoice generation or PDF receipt creation.
  - Collections rely on local JSON; no real Gmail/WhatsApp reminder dispatch.
- **Files**: `hermes/profiles/partenon-collector/`

### 2.4 Guardian (security / NVIDIA) — `partenon-guardian`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.env.example`, `.security` template, cron, and `key_manager.py` are in English. `key_manager.py` can list keys, rotate placeholders, audit access, validate access, and recommend models.
- **Gaps**:
  - No real secrets-manager integration (only environment variables).
  - No NVIDIA NeMo / OpenShell integration.
  - No automated audit log persistence.
- **Files**: `hermes/profiles/partenon-guardian/`

### 2.5 Strategist (operations) — `partenon-strategist`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.ops`, template, cron, SKILL.md, and ops tools translated to English. `projects.py`, `tasks.py`, `checklists.py`, `goals.py`, and `briefings.py` are functional with English field names.
- **Gaps**:
  - No Google Calendar or Gmail MCP integration is wired; tools read local JSON only.
  - No automated tests.
- **Files**: `hermes/profiles/partenon-strategist/skills/ops/tools/*.py`

### 2.6 Diplomat (relations) — `partenon-diplomat`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.relations` template, cron, SKILL.md, and relations tools translated to English. `crm.py` and `followups.py` use English field names and match the translated `.relations` template.
- **Gaps**:
  - No actual Google Contacts or Gmail integration.
  - No handoff automation with Strategist beyond documentation.
  - No automated tests.
- **Files**: `hermes/profiles/partenon-diplomat/skills/relations/tools/*.py`

### 2.7 Brain (intelligence / memory) — `partenon-brain`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.env.example`, `.brain` template, cron, SKILL.md, and `gbrain_client.py` are translated to English. `gbrain_client.py` now sends `stdin` as text to the `gbrain` subprocess and works with a locally installed binary.
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
- **Gap**: Originally pointed to non-existent `partenon.*` modules.
- **Impact**: Cron entries are now mapped to real scripts and tools.
- **Status**: PARTIAL
- **Fix**: Entries now reference `scripts/demo_scribe.py`, the Herald content-calendar tool, and the Guardian key-manager tool. The Guardian entry is enabled now that `key_manager.py` has a CLI entry point.
- **Suggested next step**: Add a lightweight cron runner or document how to wire `data/cron.json` into the host system's cron / systemd / scheduler.
- **Files**: `data/cron.json`, `hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py`

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
- **Reality**: `gbrain/server.py` originally used `GBrain_DATABASE_URL`; `partenon-core/config/mcp/servers.yaml` passed the value as `DATABASE_URL`.
- **Severity**: MEDIUM
- **Status**: DONE
- **Fix**: `gbrain/server.py` now reads `GBRAIN_DATABASE_URL` (with fallbacks to `GBrain_DATABASE_URL` and `DATABASE_URL` for compatibility); `partenon-core/config/mcp/servers.yaml` now passes `GBRAIN_DATABASE_URL`.
- **Files**: `gbrain/server.py`, `partenon-core/config/mcp/servers.yaml`

### 4.3 Demo output filenames
- **Promise**: `README.md` says the demo creates `data/sample_expenses.xlsx` with a "Vendors" sheet.
- **Reality**: The sheet is named "Suppliers".
- **Severity**: LOW
- **Status**: DONE (README fixed in this pass)

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

### 6.1 Automated tests
- **Gap**: There was no `tests/` directory or CI workflow.
- **Impact**: Refactors and translations cannot be verified automatically.
- **Severity**: HIGH
- **Status**: PARTIAL
- **Fix**: Added `tests/test_scribe_demo.py` and `tests/test_onboarding_engine.py` using the standard library `unittest`. These verify the finance demo output and onboarding-engine data/file creation.
- **Suggested next step**: Add tests for `router.py`, `workflow_engine.py`, `eval_loop.py`, and each hero skill tool.
- **Files**: `tests/test_scribe_demo.py`, `tests/test_onboarding_engine.py`

### 6.2 No linting or formatting config
- **Gap**: No `pyproject.toml`, `ruff.toml`, or GitHub Actions.
- **Severity**: LOW
- **Status**: NOT_STARTED
- **Suggested fix**: Add a minimal Python formatter/linter and a pre-commit hook.

---

## 7. Workshop and production-readiness findings

A production-readiness test was run using five real small-business company cards and simulated onboardings (see `workshop/`). The exercise surfaced the following additional gaps:

### 7.1 No reusable company onboarding simulations
- **Promise:** Partenon can be taught to entrepreneurs and operators through workshops.
- **Reality:** Before this pass, no company cards, simulations, or facilitator materials existed.
- **Severity:** MEDIUM
- **Status:** DONE (added `workshop/companies/`, `workshop/simulations/`, `workshop/guides/HERMES_ONBOARDING.md`, `workshop/README.md`, `workshop/AGENDA.md`, `workshop/SLIDES.md`, `workshop/HANDOUT.md`, `workshop/checklists/PRODUCTION_READINESS.md`).

### 7.2 No Hermes onboarding guide
- **Promise:** Hermes should guide a new company through setup.
- **Reality:** No step-by-step guide existed for how Hermes asks questions, selects heroes, runs smoke tests, and hands off to the dashboard.
- **Severity:** MEDIUM
- **Status:** DONE (`workshop/guides/HERMES_ONBOARDING.md`).

### 7.3 POS / bank-export to Google Sheets flow missing
- **Promise:** The Scribe parses expenses and writes them into Google Sheets.
- **Reality:** `parsers.py` reads Excel/CSV and `google_sheets.py` can create a spreadsheet, but no end-to-end script combines upload → classification → publish.
- **Severity:** HIGH
- **Status:** NOT_STARTED
- **Suggested fix:** Add a script that takes a bank/CSV export path and a sheet title, classifies rows, and appends them via `google_sheets.py`.

### 7.4 Retail platform integrations absent
- **Promise:** Retail use cases (inventory, Shopify, Klaviyo) are referenced in docs.
- **Reality:** No Shopify order export, inventory, or email-dispatch integration exists.
- **Severity:** HIGH
- **Status:** NOT_STARTED
- **Suggested fix:** Add MCP stubs or CSV importers for Shopify orders and a simple inventory tracker.

### 7.5 SaaS cost and support integrations absent
- **Promise:** SaaS startups can track runway and churn.
- **Reality:** No AWS cost import, support-ticket churn signals, or investor-update generator exists.
- **Severity:** HIGH
- **Status:** NOT_STARTED
- **Suggested fix:** Add AWS cost CSV importer, churn-signal worksheet, and an investor-update template for the Strategist.

### 7.6 Invoice / receipt PDF generation missing
- **Promise:** The Collector handles invoices and payments.
- **Reality:** `stripe_tools.py` records invoices but does not generate PDF receipts or invoices.
- **Severity:** MEDIUM
- **Status:** NOT_STARTED
- **Suggested fix:** Add a PDF receipt tool using WeasyPrint or Google Docs templates.

### 7.7 Production support and incident runbooks missing
- **Promise:** Partenon is production-ready for real companies.
- **Reality:** No incident-response runbook or public support channel is configured.
- **Severity:** LOW
- **Status:** NOT_STARTED
- **Suggested fix:** Create `docs/RUNBOOK.md` and a public issue tracker or support email.

### 7.8 Workshop package deliverables
- **Promise:** The workshop package should be reusable for accelerators, universities, and chambers of commerce.
- **Reality:** Reusable README, agenda, slides, handout, and production-readiness checklist are now included.
- **Severity:** MEDIUM
- **Status:** DONE (`workshop/README.md`, `workshop/AGENDA.md`, `workshop/SLIDES.md`, `workshop/HANDOUT.md`, `workshop/checklists/PRODUCTION_READINESS.md`).

### 7.9 PyYAML dependency not declared
- **Promise:** Profile tools and the workshop simulation runner can load YAML configs and skill cards.
- **Reality:** Several `partenon-core` tools import `yaml`, but `pyyaml` is not listed in `requirements.txt`. The `.venv` installed it manually during this pass.
- **Severity:** MEDIUM
- **Status:** NOT_STARTED
- **Suggested fix:** Add `pyyaml>=6.0` to `requirements.txt` and document Python version constraints.
- **Files:** `requirements.txt`

### 7.10 G-Brain client stdin handling
- **Promise:** The Brain can write pages to G-Brain from any Python runtime.
- **Reality:** `gbrain_client.py` passed `stdin.encode()` to `subprocess.run(text=True)`, which failed on Python 3.9/3.12 with `AttributeError: 'bytes' object has no attribute 'encode'`.
- **Severity:** HIGH
- **Status:** DONE — fixed by passing `stdin` directly; smoke test with a local `gbrain` binary returned `status: created_or_updated`.
- **Files**: `hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py`

### 7.11 Public support channel / issue templates
- **Promise:** Partenon is production-ready for real companies.
- **Reality:** No GitHub issue templates, support email, or public help channel are configured.
- **Severity:** LOW
- **Status:** NOT_STARTED
- **Suggested fix:** Add `.github/ISSUE_TEMPLATE.md` and a support email to `README.md`.

### 7.12 `install.sh` does not validate the existing venv Python version
- **Promise:** Running `./install.sh` prepares a working local environment.
- **Reality:** If an existing `.venv` was created with Python 3.9, the script detects a system Python 3.10+ but still calls `.venv/bin/pip`, which fails to install `mcp>=1.0.0`.
- **Severity:** HIGH
- **Status:** NOT_STARTED
- **Suggested fix:** Before installing packages, compare `.venv/bin/python` version to 3.10. Recreate the venv if it is below the minimum.
- **Evidence:** `workshop/PRODUCTION_READINESS_RESEARCH.md`, section 2.

### 7.13 `workshop/simulations/sim_runner.py` is missing
- **Promise:** The workshop has a runnable simulation runner and the checklist marks it green.
- **Reality:** `sim_runner.py` does not exist. The simulation markdowns also reference CLI flags that the underlying tools do not support.
- **Severity:** HIGH
- **Status:** NOT_STARTED
- **Suggested fix:** Implement `sim_runner.py`, or update the README/checklist to reflect that simulations are documentation-only and add CLI entry points to the Strategist/Scribe tools.
- **Evidence:** `workshop/PRODUCTION_READINESS_RESEARCH.md`, sections 3 and 4.

### 7.14 Construction checklist template is missing
- **Promise:** The Strategist can generate industry-specific checklists.
- **Reality:** `checklists.py` has templates for events, legal, consulting, and retail, but not construction. Construction simulations fall back to consulting.
- **Severity:** MEDIUM
- **Status:** NOT_STARTED
- **Suggested fix:** Add a construction checklist template with phases such as pre-construction, construction, and closeout.
- **Evidence:** `workshop/PRODUCTION_READINESS_RESEARCH.md`, section 3.

### 7.15 Simulation markdowns link to missing company cards
- **Promise:** Each simulation points to a matching company card.
- **Reality:** `construction.md`, `retail.md`, and `saas.md` reference `D&M Construction`, `Brookline Booksmith`, and `WP Umbrella` cards that do not exist. The existing cards are `SpawGlass`, `Tracksmith`, and `Buffer`.
- **Severity:** LOW
- **Status:** NOT_STARTED
- **Suggested fix:** Align the simulation names with the existing company cards, or create the three missing cards.
- **Evidence:** `workshop/PRODUCTION_READINESS_RESEARCH.md`, section 4.

---

## 8. Suggested priority order

1. Add automated tests for `partenon-core` and hero tools.
2. Build an end-to-end bank/CSV → classification → Google Sheets script for the Scribe.
3. Implement the workflow engine runtime so heroes can dispatch to one another.
4. Add Shopify/order import and inventory tracking for retail.
5. Add AWS cost import and churn-signal worksheet for SaaS.
6. Bundle or replace the external `gbrain` binary with a local SQLite/PGLite fallback.
7. Add invoice/receipt PDF generation to the Collector.
8. Wire live Google Calendar/Gmail MCP for Strategist and Diplomat.
9. Standardize `GBRAIN_DATABASE_URL` naming.
10. Add CI/linting and a production runbook.

---

## 9. Files changed in this audit/fix pass

- `README.md` — updated demo sheet name (Suppliers), badges, install note.
- `data/tasks.json` — translated mission titles and descriptions to English.
- `hermes/profiles/partenon-scribe/` — fully translated (SOUL, config, SKILL, `.env.example`, cron, templates, finance tools).
- `hermes/profiles/partenon-strategist/` — SOUL, config, `.ops`, template, cron, SKILL.md, and ops tools translated to English; `metas.py` renamed to `goals.py`.
- `hermes/profiles/partenon-diplomat/` — SOUL, config, `.relations` template, cron, SKILL.md, and relations tools translated to English.
- `hermes/profiles/partenon-brain/` — SOUL, config, `.brain`, `.env.example`, cron, SKILL.md translated to English; `gbrain_client.py` stdin bug fixed.
- `partenon-core/SKILL.md` and `partenon-core/README.md` — updated to reference 7 heroes and include Brain.
- `partenon-core/tools/onboarding_flow.py` — added Brain (`.brain`) to `PROFILE_FILES`.
- `workshop/` — new workshop package: five real company cards, five simulated onboardings, `HERMES_ONBOARDING.md`, `README.md`, `AGENDA.md`, `SLIDES.md`, `HANDOUT.md`, and `PRODUCTION_READINESS.md`.
- `MISSING_IMPLEMENTATION.md` — this file, updated with production-readiness findings.
- `README.md` — already linked to `workshop/README.md` in the documentation section.
- `docs/ENTREPRENEUR_PLAYBOOK.md` — already references the workshop simulations in Section 7.
- `requirements.txt` — added `pyyaml>=6.0` to declare the dependency used by `partenon-core` and the simulation runner.
- Verification run in this pass:
  - `python3 scripts/demo_scribe.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `bash -n install.sh` PASS (syntax only; runtime fails with a stale Python 3.9 venv).
  - `python3 -m py_compile` on all profile Python tools PASS.
  - `python3 partenon-core/tools/router.py` PASS.
  - `python3 -m unittest discover tests` PASS (4 tests).
  - `python3 workshop/simulations/sim_runner.py` does not exist; this previous claim was incorrect.
  - Brain `GBrainClient().put_page('test/smoke', ...)` PASS after stdin fix.
