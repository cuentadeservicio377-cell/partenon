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

### 2.1 Scribe (finance) — `partenon-tesorero`
- **Status**: PARTIAL
- **Done**: SOUL, config, SKILL, templates, cron, and finance tools translated to English. `google_sheets.py` can create a spreadsheet and seed headers. `parsers.py` can read Excel/CSV expenses. `templates.py` generates local Excel templates.
- **Gaps**:
  - No end-to-end demo that parses an uploaded file and writes to Google Sheets.
  - `CATEGORY_KEYWORDS` in `parsers.py` are English-only; historic Spanish transaction descriptions are accepted as aliases but inferred categories will be English words. This is intentional but must be documented.
  - No automated tests.
- **Files**: `hermes/profiles/partenon-tesorero/skills/finance/tools/*.py`

### 2.2 Herald (communications) — `partenon-mensajero`
- **Status**: PARTIAL
- **Done**: SOUL, config, SKILL, `.design` template, `.env.example`, cron, and comms tools are in English. `brand_intake.py`, `copy_generator.py`, and `content_calendar.py` are functional.
- **Gaps**:
  - No actual publishing integration (LinkedIn, Instagram, WordPress, etc.).
  - `config.yaml` references `wordpress` and `ssh` tools but no implementation exists.
  - No Gmail MCP integration for sending newsletters.
- **Files**: `hermes/profiles/partenon-mensajero/`

### 2.3 Collector (payments) — `partenon-cobrador`
- **Status**: PARTIAL
- **Done**: SOUL, config, SKILL, `.env.example`, `.payments` template, cron, and Stripe tools are in English. `stripe_tools.py` can create payment links, subscriptions, reminders, and record payments in local mode or via the Stripe library.
- **Gaps**:
  - No end-to-end Stripe MCP wiring.
  - No invoice generation or PDF receipt creation.
  - Collections rely on local JSON; no real Gmail/WhatsApp reminder dispatch.
- **Files**: `hermes/profiles/partenon-cobrador/`

### 2.4 Guardian (security / NVIDIA) — `partenon-guardian`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.env.example`, `.security` template, cron, and `key_manager.py` are in English. `key_manager.py` can list keys, rotate placeholders, audit access, validate access, and recommend models.
- **Gaps**:
  - No real secrets-manager integration (only environment variables).
  - No NVIDIA NeMo / OpenShell integration.
  - No automated audit log persistence.
- **Files**: `hermes/profiles/partenon-guardian/`

### 2.5 Strategist (operations) — `partenon-estratega`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.ops`, template, cron, SKILL.md, and ops tools translated to English. `projects.py`, `tasks.py`, `checklists.py`, `goals.py`, and `briefings.py` are functional with English field names.
- **Gaps**:
  - No Google Calendar or Gmail MCP integration is wired; tools read local JSON only.
  - No automated tests.
- **Files**: `hermes/profiles/partenon-estratega/skills/ops/tools/*.py`

### 2.6 Diplomat (relations) — `partenon-diplomatico`
- **Status**: PARTIAL
- **Done**: SOUL, config, `.relations` template, cron, SKILL.md, and relations tools translated to English. `crm.py` and `followups.py` use English field names and match the translated `.relations` template.
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
- **Gap**: Commands point to non-existent `partenon.*` modules.
- **Impact**: Cron entries are illustrative only.
- **Status**: STUB
- **Suggested fix**: Map each entry to an existing script or skill tool path, or remove until implemented.

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

### 6.1 No automated tests
- **Gap**: There is no `tests/` directory or CI workflow.
- **Impact**: Refactors and translations cannot be verified automatically.
- **Severity**: HIGH
- **Status**: NOT_STARTED
- **Suggested fix**: Add unit tests for `partenon-core` tools and at least one integration test for the Scribe parser/template flow.

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
- `hermes/profiles/partenon-tesorero/` — fully translated (SOUL, config, SKILL, `.env.example`, cron, templates, finance tools).
- `hermes/profiles/partenon-estratega/` — SOUL, config, `.ops`, template, cron, SKILL.md, and ops tools translated to English; `metas.py` renamed to `goals.py`.
- `hermes/profiles/partenon-diplomatico/` — SOUL, config, `.relations` template, cron, SKILL.md, and relations tools translated to English.
- `hermes/profiles/partenon-brain/` — SOUL, config, `.brain`, `.env.example`, cron, SKILL.md translated to English.
- `partenon-core/SKILL.md` and `partenon-core/README.md` — updated to reference 7 heroes and include Brain.
- `partenon-core/tools/onboarding_flow.py` — added Brain (`.brain`) to `PROFILE_FILES`.
- `workshop/` — new workshop package: five real company cards, five simulated onboardings, `HERMES_ONBOARDING.md`, `README.md`, `AGENDA.md`, `SLIDES.md`, `HANDOUT.md`, and `PRODUCTION_READINESS.md`.
- `MISSING_IMPLEMENTATION.md` — this file, updated with production-readiness findings.
- `README.md` — already linked to `workshop/README.md` in the documentation section.
- `docs/ENTREPRENEUR_PLAYBOOK.md` — already references the workshop simulations in Section 7.
- Verification run in this pass:
  - `python3 scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `python3 -m py_compile` on all profile Python tools PASS.
