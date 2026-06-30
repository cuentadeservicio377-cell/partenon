# Progress

## Session History

### 2026-06-30 — Save finalized article `THE PARTENON`
- Saved the user's finalized article verbatim as `ARTICLE.md` at the repository root for use in the next phase.
- Committed as `743d19e`.

### 2026-06-30 — README update after Phase 7 website reality
- Updated `README.md` to reflect the four-page static site (`index.html`, `heroes.html`, `developers.html`, `workshop.html`).
- Added workshop badge and public mission statement: install 1 million Hermes profiles.
- Added new "Website" and "Installation Workshop" sections with links to `web/workshop.html` and the live workshop landing.
- Clarified honest capability framing: local install and SQLite memory are `live`; Google Workspace and Stripe require credentials; NVIDIA/OpenRouter items remain roadmap.
- Updated Roadmap: Phase 7 website reality marked done; Phase 7b (capabilities page + screenshots) remains pending.
- Updated `TODOS.md` to mark README update complete and keep `web/capabilities.html` and screenshots as remaining Phase 7 tasks.
- Verified:
  - `README.md` renders without broken Mermaid or markdown issues.
  - Internal links to `DESIGN.md`, `docs/CAPABILITIES.md`, `workshop/README.md`, and `web/*.html` are consistent.

### 2026-06-30 — Phase 7 Website Reality: workshop landing page
- Created `web/workshop.html` as the third main page of the site.
- Wrote and committed the design spec (`docs/superpowers/specs/2026-06-30-workshop-landing-design.md`) and implementation plan (`docs/superpowers/plans/2026-06-30-workshop-landing-phase1.md`).
- Sections built: hero with 1M-installation storytelling and impact counters, value bento, Local/VPS install tabs, 90-minute agenda, per-hero preparation accordions with AI prompts, Brain and automations, custom workshops, Workshop 2.0 follow-up.
- Updated navigation in `web/index.html`, `web/heroes.html`, and `web/developers.html` to include the Workshop page.
- Applied `kimi-design-system` anti-slop rules: asymmetric bento, direct copy, one `<h1>`, no emojis, no em-dashes, no filler verbs.
- Verified:
  - `pytest tests/` PASS (184 passed).
  - `bash -n install.sh` PASS.
  - `cd dashboard && npm run build` PASS.
  - HTML parse check PASS for all four pages.
  - Chrome opened for visual review at `http://localhost:8080/workshop.html`.

### 2026-06-30 — Phase 7 Website Reality: copy rewrite and honest capability labels
- Reframed `web/index.html` foundation, process steps, `1 → 1M` counter, hackathon-partner framing, and "Install the Partenon" CTA.
- Updated `web/heroes.html` per-hero status tags (live / connect / roadmap), reworked remaining hero profiles, and rewrote the workflow timeline to four steps: Install → Assemble → Operate → Orchestrate.
- Repositioned `web/developers.html` as a judge-facing technical brief for Nous Research, NVIDIA, and Stripe teams; replaced per-hero config accordions with "Capabilities / Live now / To connect" tabs; fixed live-vs-roadmap MCP labels; corrected SVG structure and tab JavaScript.
- Synced `docs/CAPABILITIES.md` with website claims: install from source, optional Hermes CLI, Guardian live/roadmap tools, OpenRouter and NVIDIA status.
- Verified:
  - `pytest tests/` PASS (184 passed).
  - `bash -n install.sh` PASS.
  - `cd dashboard && npm run build` PASS.
  - HTML parse check PASS for `web/index.html`, `web/heroes.html`, `web/developers.html`.
  - Chrome opened for visual review at `http://localhost:8080`.

### 2026-06-29 — Pre-push audit and blocker fixes
- Ran a 5-agent swarm to audit release readiness.
- Fixed `TODOS.md` stale "Current Phase: Phase 0" header to reflect Phase 6 closed / Phase 7 pending.
- Fixed broken `workshop/checklists/PRODUCTION_READINESS.md` links to the real `workshop/checklists/production-readiness.md` in `README.md`.
- Updated `docs/CAPABILITIES.md` date and removed references to non-existent `scripts/generate_status.py` and `web/capabilities.html`.
- Reverted demo-generated `data/sample_expenses.xlsx` and `data/sample_expenses_report.json` artifacts before committing.
- Created `audits/AUDIT_INDEX.md` consolidating all website-claims and release-readiness reports.
- Verified:
  - `pytest tests/` PASS (184 passed).
  - `ruff check` PASS.
  - `cd dashboard && npm run build` PASS.
  - `bash -n install.sh` PASS.
  - `python3 -m py_compile scripts/bump_version.py` PASS.
  - `python3 .github/scripts/secret_scan.py` PASS.
  - Working tree clean and ready for push.
- Committed as `c88accb`.

### 2026-06-29 — Phase 6 Deployment World: production Docker stack, CI/CD, metrics, and release process
- Added production `Dockerfile` for the FastAPI backend with multi-stage build, non-root `partenon` user, and health check.
- Added `.dockerignore` to keep images small and avoid leaking secrets.
- Rewrote `docker-compose.yml` to run `gbrain` Postgres, `api`, and `dashboard` services with health checks and shared network.
- Added `docker-compose.override.yml` for live-reload local development.
- Updated `dashboard/Dockerfile` with curl and a health check.
- Added `prometheus-fastapi-instrumentator` and `structlog` dependencies; created `partenon_api/observability.py`.
- Extended health endpoints in `partenon_api/main.py` to `/health/live` and `/health/ready`; `/metrics` exposes Prometheus metrics.
- Expanded test suite with `tests/test_config.py`, `tests/test_observability.py`, and `tests/test_mcp_client.py` (26 new tests).
- Expanded `.github/workflows/ci.yml` with Python lint, install-script syntax check, Docker image builds, and Docker Compose integration smoke tests.
- Added `.github/workflows/release.yml` to publish `api` and `dashboard` images to GHCR on version tags.
- Added `scripts/bump_version.py` and `docs/RELEASE.md` for SemVer releases.
- Added `docs/DEPLOYMENT.md` and Docker section in `README.md`; updated `CHANGELOG.md`.
- Verified:
  - `pytest tests/` PASS (184 passed, target ≥180).
  - `ruff check partenon_api tests partenon_core/tools/intent_router.py partenon_core/tools/router.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `bash -n install.sh` PASS.
  - `python3 -m py_compile scripts/bump_version.py` PASS.
  - `python3 .github/scripts/secret_scan.py` PASS.
  - `docker build` could not run locally because the Docker daemon is not active, but the Dockerfile syntax and build steps were validated.
- Phase 6 closed; repository is ready for Phase 7 — Website Reality.

### 2026-06-29 — Phase 5 Gateway Messaging: closure and functional verification
- Finalized Phase 5 implementation after the gateway skill swarm:
  - Added FastAPI smoke-test router `partenon_api/routers/gateway.py` with `POST /api/v1/gateway/dry_run`.
  - Fixed cross-package import problem: Hermes profile directories use hyphens (`partenon-scribe`), so the API now loads gateway tools via `importlib.util.spec_from_file_location`.
  - Added `tests/test_api_gateway.py` (6 tests) covering command parsing, aliases, intent fallback, attachment routing, guard allow/deny, and group rules.
- Verified the full stack:
  - `pytest tests/` PASS (158 passed, target ≥130).
  - `ruff check partenon_api tests partenon_core/tools/intent_router.py partenon_core/tools/router.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `bash -n install.sh` PASS.
  - `python3 .github/scripts/secret_scan.py` PASS.
- Updated `TODOS.md` to mark Phase 5 as closed with all subtasks completed.
- Phase 5 is now complete; repository is ready for Phase 6 — Deployment World.

### 2026-06-29 — Phase 5 Gateway Messaging: config template and setup docs
- Created reusable `partenon_core/tools/intent_router.py` and refactored `partenon_core/tools/router.py` to import from it.
- Added shared `gateway` skill under `hermes/profiles/partenon-scribe/skills/gateway/` with `SKILL.md` and tools:
  - `parse_command.py` — slash prefixes, aliases, and intent-router fallback.
  - `route_attachment.py` — file-type routing to the right hero.
  - `check_guard.py` — allowlists, group-mention rules, and per-user rate limits.
  - `onboarding_reply.py` — progressive onboarding state machine backed by `partenon-memory`.
- Mirrored the gateway skill into the other six profiles via symlinks.
- Added `gateway` to `skills.auto_load` in all seven profile `config.yaml` files.
- Created `config/hermes_gateway.yaml` template with Telegram and Email adapter declarations using env var references.
- Created `docs/GATEWAY_SETUP.md` with step-by-step setup instructions.
- Updated `.env.example` with `TELEGRAM_BOT_TOKEN`, `TELEGRAM_ALLOWED_USERS`, `EMAIL_ACCOUNT`, `EMAIL_PASSWORD`, `GATEWAY_ALLOWED_USERS`, and `GATEWAY_RATE_LIMIT_PER_MINUTE`.
- Verification:
  - `pytest tests/` PASS (152 tests, target ≥130).
  - `ruff check` PASS on controllable files.
  - `python -m py_compile` PASS for gateway tools.
  - `cd dashboard && npm run build` PASS.
- Note: the gateway tool files created by a previous process carry `com.apple.provenance` extended attributes, preventing in-place edits; tests pass and the only outstanding lint item is an import-sort warning in `check_guard.py` (I001) that cannot be edited away without replacing the protected file.

### 2026-06-29 — Repair sprint closure: Hermes-Partenon unification complete
- Committed packaging repair: `fabd2b1`.
- Committed runtime MCP unification: `653f471`.
- Committed README update: `5519ebf`.
- Final verification:
  - `pytest tests/` PASS (117 passed).
  - `ruff check partenon_api tests partenon_core/tools/workflow_engine.py` PASS.
  - `cd dashboard && npm run lint` PASS.
  - `cd dashboard && npm run build` PASS.
  - `bash -n install.sh` PASS.
  - `python3 .github/scripts/secret_scan.py` PASS.
- Repository is now ready for Phase 5 Gateway Messaging.

### 2026-06-29 — Repair sprint: workflow engine + integrations MCP runtime
- Migrated `partenon_core/tools/workflow_engine.py` from direct JSON writes and Python imports to the Hermes MCP runtime:
  - `_action_create_follow_up_task` now writes to `partenon-memory` via `sync_call("memory_put_page", slug="workspace/default/missions/{id}", tags="mission,workspace:default,follow-up")`.
  - `_action_handoff_nudge` and `_action_nudge` now write to `partenon-memory` via `sync_call("memory_put_page", slug="workspace/default/nudges/{id}", tags="nudge,workspace:default")`.
  - `_action_notify_slack` now calls `mcp_servers.notifications.server` via `sync_call("slack_notify_task_overdue", server_module=...)` instead of importing the Slack module directly.
  - JSON fallback is preserved when `PARTENON_STORE_MODE=json` is set (tests).
- Extended `partenon_api/mcp_client.py`:
  - Added `AsyncDomainClient(module_path, env=None)` context manager for arbitrary domain MCP servers.
  - Promoted `_call_tool` to public `call_tool` on both `AsyncMemoryClient` and `AsyncDomainClient`.
  - Extended `sync_call(..., server_module=None)` so synchronous callers can target domain servers.
- Rewrote `partenon_api/routers/integrations.py`:
  - Removed all direct `mcp_servers.*` Python imports.
  - `GET /api/v1/integrations` remains status-based.
  - `POST /api/v1/integrations/{domain}/{action}` maps domains to MCP server modules and tool name prefixes, short-circuits unconfigured domains to dry-run/live-error responses, and invokes the tool via `AsyncDomainClient`.
  - Normalizes non-dict MCP results to a consistent JSON shape.
- Added `tests/test_api_integrations.py` with coverage for list, unknown domain, dry-run short-circuit, memory invocation, and forced-live error paths.
- Added a session-scoped `PARTENON_STORE_MODE=json` fixture in `tests/conftest.py` so all tests (including unittest-based `test_handoffs.py`) use the JSON fallback by default.
- Updated `TODOS.md` (repo root and `.kimi-code/memory/`) with the repair sprint tasks.
- Verified:
  - `pytest tests/` PASS (117 passed).
  - `ruff check partenon_api tests partenon_core/tools/workflow_engine.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - Manual smoke test: `python -m partenon_core.tools.workflow_engine` and `new_client` event emit with MCP-backed follow-up mission and nudge creation PASS.

### 2026-06-28 — Phase 0 contaminants cleanup
- Deleted dead code and stale artifacts: `Kimi_Agent_10 Storytelling Web Sites/`, `examples/*-stub.py`, `docs/PARTENON_GUIDE.html`, `docs/HERMES_GATEWAY_AUDIT.md`, and old superpowers plans/specs.
- Anonymized sample data across `partenon-core/tools/onboarding_engine.py`, profile tools, `data/clients.json`, `docs/HERO_GUIDE.md`, `docs/ENTREPRENEUR_PLAYBOOK.md`, `workshop/simulations/*.md`, and `workshop/simulations/sim_runner.py`.
- Hardened dashboard auth in `.env.example` and `dashboard/src/lib/auth.ts`: removed default `admin`/`partenon` credentials, added required `DASHBOARD_AUTH_SECRET`, and made missing env vars throw at runtime.
- Replaced external `gbrain` binary calls in `hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py` with direct `GBrainStore` usage.
- Added legal docs at repo root: `LICENSE` (Apache-2.0), `CONTRIBUTING.md`, `SECURITY.md`, and `NOTICE.md`.
- Removed temporary `.tmp_anonymize.py` script.
- Verified:
  - `cd dashboard && npx tsc --noEmit` PASS.
  - `cd dashboard && npm run build` PASS.
  - `python3 -m unittest discover tests` PASS.
  - `python3 scripts/demo_tesorero.py` PASS.
  - `bash -n install.sh` PASS.
  - `python3 -m py_compile` on modified Python tools PASS.
  - `GBrainClient` import via `importlib` PASS.
  - Grep verification: no obvious real emails remain in listed files.

### 2026-06-27 — Final production-readiness verification and sim_runner restore
- Restored `workshop/simulations/sim_runner.py` so the workshop docs (`AGENDA.md`, `SLIDES.md`, `HANDOUT.md`) have a working command runner again.
- Rewrote `workshop/checklists/PRODUCTION_READINESS.md` from green/yellow/red into PASS/FAIL/PARTIAL evidence with a verification log and summary totals.
- Cleaned duplicate/stray files: removed `docs/HERMES_ONBOARDING.md`, extra company cards, old simulation markdown files, `run_all_sims.sh`, and generated `workspaces/`.
- Verified the final package:
  - `python3 scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `python3 -m unittest discover tests` PASS (4 tests).
  - `bash -n install.sh` PASS.
  - `python3 -m py_compile` on all profile Python tools PASS.
  - `python3 workshop/simulations/sim_runner.py route/project/checklist/client/payment-link/calendar` PASS.
  - Brain `GBrainClient().put_page('test/smoke', 'Smoke test page')` PASS.
- Committed: production-readiness checklist rewrite and restored `sim_runner.py`.

### 2026-06-27 — Workshop cleanup, onboarding guide rewrite, and final commit
- Rewrote `workshop/guides/HERMES_ONBOARDING.md` to remove stale `sim_runner.py` and Oblique Coffee Roasters references.
- Replaced the simulation-runner section with direct Python smoke-test commands for each hero and a pre-flight checklist grounded in actual files.
- Added generated-artifact patterns to `.gitignore` to keep demo workbooks, JSON data files, `docs/WELCOME.md`, and tool outputs out of commits.
- Committed the production-readiness pass: workshop package, company cards, simulations, onboarding guide, production-readiness checklist, tests, G-Brain URL standardization, Guardian key-manager CLI, and `pyyaml` dependency.
- Verified:
  - `python3 scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `python3 -m unittest discover tests` PASS (4 tests).
  - `bash -n install.sh` PASS.
  - `python3 -m py_compile` on referenced profile Python tools PASS.
- Commit: `2897ea9 feat(workshop): finalize production-readiness pass, add tests, remove sim_runner`.

### 2026-06-27 — Final close: G-Brain URL standardization, Guardian cron, tests, and commit
- Standardized `GBRAIN_DATABASE_URL` across `.env.example`, `gbrain/server.py`, and `partenon-core/config/mcp/servers.yaml`; removed the `GBrain_DATABASE_URL` inconsistency from the README known gaps.
- Added a runnable CLI entry point to `hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py` and enabled the Guardian cron entry in `data/cron.json`.
- Added initial automated tests in `tests/`: `test_scribe_demo.py` verifies the finance demo output, and `test_onboarding_engine.py` verifies onboarding data-file and welcome-doc creation.
- Updated `README.md` to mark the `GBRAIN_DATABASE_URL` roadmap item as done, refresh known gaps, and list the new test suite.
- Updated `TODOS.md` to mark the G-Brain naming, initial tests, and Guardian cron entry as completed.
- Verified:
  - `python3 scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `python3 -m unittest discover tests` PASS (4 tests).
- Committed all production-readiness changes locally.

### 2026-06-27 — Production-readiness verification and close
- Completed the production-readiness test under the `company-research` scope.
- Updated `workshop/checklists/PRODUCTION_READINESS.md` with the latest verification evidence: all seven heroes smoke-tested, `sim_runner.py` actions verified, Brain `put_page` fixed and working.
- Fixed `hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py` stdin handling so `GBrainClient.put_page` works on Python 3.9/3.12 when a local `gbrain` binary is installed.
- Updated `MISSING_IMPLEMENTATION.md` with the G-Brain client fix and a new public-support-channel gap.
- Linked `README.md` and `docs/ENTREPRENEUR_PLAYBOOK.md` to `workshop/guides/HERMES_ONBOARDING.md` and `workshop/checklists/PRODUCTION_READINESS.md`.
- Verified:
  - `python3 scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `bash -n install.sh` PASS.
  - `python3 -m py_compile` on all profile Python tools PASS.
  - `python3 workshop/simulations/sim_runner.py route/project/checklist/client/payment-link/calendar` PASS.
  - Brain `GBrainClient().put_page('test/smoke', 'Smoke test page')` PASS.
- Updated `TODOS.md` and committed the production-readiness pass.

### 2026-06-27 — Workshop package and production-readiness test
- Ran a production-readiness test by researching five real small businesses and creating one-page company cards in `workshop/companies/`.
- Created simulated Partenon onboardings in `workshop/simulations/` for coffee shop, agency, construction, retail, and SaaS.
- Created `workshop/guides/HERMES_ONBOARDING.md` with a pre-flight checklist, five-step setup flow, example prompts, and failure responses.
- Created a complete workshop package: `workshop/README.md`, `workshop/AGENDA.md` (90-minute and 3-hour), `workshop/SLIDES.md`, and `workshop/HANDOUT.md`.
- Created `workshop/checklists/PRODUCTION_READINESS.md` with PASS/FAIL/PARTIAL ratings and consolidated gap priorities.
- Updated `MISSING_IMPLEMENTATION.md` with workshop findings and a revised priority order.
- Updated `README.md` and `docs/ENTREPRENEUR_PLAYBOOK.md` to reference the new workshop materials.
- Added generated-artifact patterns to `.gitignore` to keep demo and tool outputs out of commits.
- Verified:
  - `python3 scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `python3 -m py_compile` on all simulation-referenced tools PASS.
- Updated `TODOS.md`.

### 2026-06-26 — Final python3 normalization and session close
- Normalized every Python command example from `python` to `python3` across `README.md`, all new docs (`docs/ENTREPRENEUR_PLAYBOOK.md`, `docs/HERO_GUIDE.md`, `docs/QUICKSTART.md`, `docs/SECURITY.md`, `docs/API.md`, `docs/FAQ.md`, `docs/for-developers.md`, `docs/assets/hero-matrix.md`), existing docs (`docs/superpowers/plans/2026-06-26-partenon-system-build.md`), scripts (`scripts/demo_tesorero.py`, `scripts/setup_hermes.py`), examples (`examples/hermes-cli-stub.py`, `examples/mcp-client-example.py`, `examples/README.md`), `install.sh`, `partenon-core/tools/onboarding_engine.py`, `hermes/profiles/partenon-tesorero/SKILL.md`, `web/developers.html`, and `TODOS.md`.
- Updated Python badge in `README.md` to 3.12+.
- Updated `CHANGELOG.md` with the command-normalization change.
- Verified:
  - `python3 scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
- Working tree clean; no additional commit needed because all changes were already committed in this session.

### 2026-06-26 — Documentation polish and final commit
- Finalized working-directory revisions to `README.md`, `docs/API.md`, `docs/FAQ.md`, `docs/SECURITY.md`, and `docs/assets/hero-matrix.md`.
- Reverted timestamp-only changes to demo artifacts (`data/sample_expenses.xlsx`, `data/sample_expenses_report.json`).
- Cross-checked all internal documentation links; fixed `docs/FAQ.md` relative link to `MISSING_IMPLEMENTATION.md`.
- Updated `CHANGELOG.md`.
- Committed: `425d467 docs: polish README, API, FAQ, SECURITY, and hero-matrix`.

### 2026-06-26 — Documentation package: README rewrite + hero guides + quickstart + security/API/FAQ
- Rewrote `README.md` from scratch with ASCII banner, badges, one-liner, value prop, Mermaid diagrams, three concrete use cases, quick install block, hero feature matrix, architecture section, roadmap, and known gaps.
- Created `docs/ENTREPRENEUR_PLAYBOOK.md` with business-type hero selection (coffee shop, agency, construction, SaaS, retail), copy-paste mission prompts, 30-60-90 day rollout checklist, and example `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations`, `.brain` configurations.
- Created `docs/HERO_GUIDE.md` with per-hero real tools, MCP servers, env vars, cron jobs, example prompts, and integration points for all seven profiles.
- Created `docs/QUICKSTART.md` with 15-minute step-by-step commands, expected outputs, and screenshot placeholders.
- Created `docs/SECURITY.md` covering `.env` handling, Google service accounts, Stripe key rotation, Guardian responsibilities, audit logging, and Docker Compose security notes.
- Created `docs/API.md` documenting `partenon-core/tools/`, `scripts/`, `examples/`, `gbrain/server.py`, and the Next.js dashboard.
- Created `docs/FAQ.md` with 20 honest questions and answers for entrepreneurs and developers.
- Created `docs/assets/architecture-diagram.mmd`, `docs/assets/hero-matrix.md`, and `docs/assets/partenon-logo.svg`.
- Cross-checked all internal documentation links and verified content is in English.
- Verification:
  - `python scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
- Updated `TODOS.md`.

### 2026-06-26 — Collector (partenon-cobrador) i18n audit and gap-fix
- Audited `hermes/profiles/partenon-cobrador` against `web/heroes.html`, `web/developers.html`, and `web/index.html`.
- Verified all profile files are in English; no Spanish prose remains.
- Added missing capabilities and MCP-aligned tools:
  - `create_invoice` for the Invoicing capability.
  - `list_charges` for Revenue Tracking.
  - `monitor_fraud` for Fraud Monitoring.
  - `read_pending_payments`, `read_overdue_payments`, `classify_risk`, `schedule_followup`, and `notify` for collection workflows.
  - `get_upcoming_payments` and `get_failed_subscriptions` for daily cron jobs.
- Fixed broken/inconsistent logic:
  - `record_payment` now stores `synced_with_treasurer` (aligned with `.payments.example`) and reports sync to Treasurer.
  - `generate_income_report` now populates `by_product` using the price-product lookup.
  - Cron JSON files now reference tools that actually exist.
- Updated `config.yaml` with new permissions, an invoice workflow, and a fraud-review workflow.
- Updated `SOUL.md` and `SKILL.md` to document the full capability set.
- Aligned `.payments.example` field names with the tool implementation (`customer_email`, `stripe_commission`, `synced_with_treasurer`, invoices section).
- Added `skills/payments/tools/__init__.py` for package consistency.
- Verification:
  - `python3 -m py_compile hermes/profiles/partenon-cobrador/skills/payments/tools/*.py` PASS.
  - `stripe_tools.py` smoke test PASS.
  - JSON cron files validated PASS.
  - YAML config validated PASS.
- Committed: `8a888d9 i18n(audit): complete Collector (partenon-cobrador) i18n gap-fix`.

### 2026-06-26 — Final i18n pass: AGENTS/DESIGN/SPEC, dashboard UI, profile tooling
- Translated remaining Spanish source files to English:
  - `AGENTS.md`, `DESIGN.md`, `SPEC.md`, and remaining Spanish snippets in `docs/superpowers/plans/2026-06-26-partenon-system-build.md`.
  - Next.js dashboard `dashboard/src/app/(dashboard)/page.tsx`: labels, status (`done`), and priority (`high`, `medium`, `low`) strings.
- Continued profile i18n from earlier in the session:
  - Translated all profile config templates (`.finance.example`, `.design.example`, `.payments.example`, `.relations.example`, `.brain.example`) to English.
  - Translated all profile cron JSON files to English.
  - Translated Strategist `tasks.py`, Diplomat `crm.py` and `followups.py`, and Brain `gbrain_client.py` to English.
- Translated `data/cron.json` and `data/tasks.json` to English with runnable command placeholders.
- Updated `MISSING_IMPLEMENTATION.md` with current implementation state and gaps.
- Verification:
  - `python3 -m py_compile` on all profile Python files PASS.
  - `python3 scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - Diplomat CRM and follow-up scripts run without errors PASS.
- Updated `TODOS.md`.

### 2026-06-26 — scripts-core-install audit and English translation
- Audited `install.sh`, `scripts/setup_hermes.py`, `scripts/demo_tesorero.py`, `.env.example`, and `partenon-core/` against `web/developers.html` promises.
- Translated all touched files to English: `.env.example`, `install.sh`, `scripts/setup_hermes.py`, `scripts/demo_tesorero.py`, `templates/google-sheet-base/finance_sheet.py`, and all `partenon-core/` files.
- Made `install.sh` and `scripts/setup_hermes.py` safe and functional: removed fake Hermes CLI install URL, added clear placeholders and instructions, and made Hermes CLI detection graceful.
- Updated `demo_tesorero.py` to use English sheet names and report keys; renamed generated artifacts to `sample_expenses.*`.
- Added missing core stubs: `partenon-core/tools/config_loader.py` and `partenon-core/tools/eval_loop.py`.
- Extended `router.py` to route to the 7th hero profile (`partenon-brain`) and translated all intent patterns to English.
- Hardened `workflow_engine.py` and `onboarding_engine.py` so they no longer depend on non-existent HBOS modules.
- Verified: `python scripts/demo_tesorero.py` PASS, `python partenon-core/tools/router.py` PASS, `python partenon-core/tools/workflow_engine.py` PASS, `python partenon-core/tools/eval_loop.py` PASS, `python partenon-core/tools/onboarding_engine.py` PASS, `python3 -m py_compile` PASS, `bash -n install.sh` PASS.
- Created `docs/WELCOME.md` via onboarding engine.
- Updated `.kimi-code/memory/TODOS.md` and `.brain/MEMORY.md`.

### 2026-06-26 — docs-and-readme audit and English translation
- Audited `README.md` and `docs/` against `web/index.html`, `web/heroes.html` and `web/developers.html`.
- Translated `README.md`, `docs/for-founders.md`, `docs/for-developers.md` and `docs/architecture.md` to English.
- Translated `partenon-core/README.md`, `partenon-core/SKILL.md`, `gbrain/README.md`, `CHANGELOG.md` and `TODOS.md` to English.
- Updated `README.md` to accurately reflect repository contents: live site, GitHub URL, installation options, hero profiles, stack, demo, dashboard and known gaps.
- Removed the non-working `curl https://www.nvidia.com/nemoclaw.sh` command from installation instructions and pointed users to official NVIDIA instructions.
- Documented known gaps: eval-loop stub not implemented; live Google Workspace/Stripe/G-Brain integrations require real credentials; `GBRAIN_DATABASE_URL` vs `GBrain_DATABASE_URL` naming inconsistency.
- Verified that no Spanish remains in the modified files.
- Committed changes locally.

### 2026-06-26 — Public GitHub repository created with loop-engineering
- Activated loop-engineering to build the Partenon GitHub repository end-to-end.
- Created public repo `cuentadeservicio377-cell/partenon` and pushed the `main` branch.
- Resolved GitHub Push Protection block: placeholder `sk_test_[REDACTED]` in `.env.example` was detected as a secret; history was rewritten with `git filter-repo` to remove the pattern.
- Completed repository structure:
  - Global `.env.example` with safe placeholders.
  - Complete `partenon-brain` profile: `SOUL.md`, `config.yaml`, `.env.example`, `.brain`, `memory` skill with `gbrain_client.py`, daily cron and template.
  - Updated `install.sh` to install the 7 profiles.
  - `scripts/setup_hermes.py` as an alternative install helper.
  - Cleaned up `__pycache__`.
- Added complete documentation:
  - `docs/for-founders.md` based on `web/index.html`.
  - `docs/for-developers.md` based on `web/developers.html`.
  - `docs/architecture.md` with system overview.
  - Updated `README.md` with repo URL, live badge, doc links and current status.
- Verification:
  - `python scripts/demo_tesorero.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - `python3 -m py_compile` on scripts and Brain profile PASS.
  - Regenerated `web-deploy.zip` (27 MB).
  - Live site `https://hermespartenon.online/` responds HTTP 200 on `/`, `/heroes.html` and `/developers.html`.
- Loop completed in 4 iterations. All gates ≥ 7/10.
- Updated `TODOS.md`, `PROGRESS.md`, `MEMORY.md`, brain central and gbrain.

### 2026-06-26 — Migrated `Developers.tsx` to `web/developers.html` + deployed to hermespartenon.online
- Replaced the previous `web/developers.html` with a static version based EXACTLY on `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Developers.tsx`.
- Stack: static HTML5 + Tailwind CSS CDN + custom CSS; Cinzel, Inter, JetBrains Mono fonts; Material Symbols Sharp and inline SVG icons.
- Migrated sections: technical hero "THE ARCHITECTURE OF HEROES", interactive SVG architecture diagram, technical specifications for the 7 heroes (Scribe, Herald, Collector, Guardian, Strategist, Diplomat, Brain) with capabilities/MCP tools tables and CLI examples, Model Context Protocol section with SVG diagram and methods table, Integration Patterns with 3 sequence diagrams, Google Workspace file structure, Workshop Protocol with visual timeline, materials and formats, Install tabs (Quick Start / Manual / Docker), repository structure, environment variables, API Reference with CLI commands and REST endpoints.
- Preserved interactivity: scroll reveal via IntersectionObserver, floating navbar with light/dark theme per section, mobile hamburger nav, copy-to-clipboard with toast, install tabs, per-hero configuration accordions, hover on architecture diagram nodes, smooth scroll.
- Applied corrections across ALL content:
  - "Nose Research" → "Nous Research".
  - "Envidia" → "NVIDIA".
  - Invented MCP tools replaced with generic names/descriptions or real tools (`create_spreadsheet`, `append_rows`, `create_payment_link`, etc.).
  - "Kimi Coding" → "Kimi / Moonshot" in environment variables.
  - Footer with correct credits: Nous Research, NVIDIA, Stripe.
- Basic HTML validation: OK.
- Deployed to Hostinger: uploaded `web-deploy.zip` (27 MB) to `public_html` via File Manager and extracted.
- Verified on real domain: `http://hermespartenon.online/`, `/heroes.html` and `/developers.html` respond HTTP 200; assets load; no forbidden terms.
- Updated `TODOS.md`, `PROGRESS.md`, `MEMORY.md`, `README.md` and brain central.

### 2026-06-26 — Migrated `Heroes.tsx` to `web/heroes.html`
- Created `web/heroes.html` as a static version based EXACTLY on `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Heroes.tsx`.
- Stack: static HTML5 + Tailwind CSS CDN + custom CSS; Cinzel, Inter, JetBrains Mono fonts; Material Symbols Sharp and inline SVG icons.
- Migrated sections: Hero "Meet Your Heroes" with quick nav of 7 icons, 7 detailed hero profiles (Scribe, Herald, Collector, Guardian, Strategist, Diplomat, Brain), Comparison Matrix, 7-step product-launch Workflow Timeline, CTA with copy-to-clipboard.
- Preserved interactivity: scroll reveal via IntersectionObserver, card/badge hover, copy-to-clipboard with toast, smooth scroll, mobile hamburger nav, floating navbar switching light/dark theme per section.
- Applied corrections across ALL content:
  - "Nose Research" → "Nous Research".
  - "Envidia" → "NVIDIA".
  - MCP connections presented as generic integrations/descriptions (Google Workspace, Stripe, NVIDIA, CRM, Email, Calendar, Social media APIs) instead of invented tool names.
  - Footer with correct credits: Nous Research, NVIDIA, Stripe.
- Basic HTML validation: OK.
- Updated `TODOS.md` and `PROGRESS.md`.

### 2026-06-26 — Migrated `Home.tsx` to `web/index.html`
- Replaced the previous `web/index.html` with a static version based EXACTLY on `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Home.tsx`.
- Stack: static HTML5 + Tailwind CSS CDN + custom CSS; Cinzel, Inter, JetBrains Mono fonts; Material Symbols Sharp and inline SVG icons.
- Migrated sections: Hero Gateway (two panels), The Myth, The Heroes (7 cards: Scribe, Herald, Collector, Guardian, Strategist, Diplomat, Brain), How It Works (4 steps), Impact Counter with milestone bar, Growth Plan (4 channels), Partners, CTA with typing effect.
- Preserved interactivity: scroll reveal, panel/card hover, animated counters via IntersectionObserver, typewriter effect, copy-to-clipboard with toast, smooth scroll, mobile nav.
- Applied corrections across ALL content:
  - "Nose Research" → "Nous Research".
  - "Envidia" → "NVIDIA".
  - Invented metrics labeled as design objectives, hypotheses or adoption projections.
  - No invented MCP tools; generic descriptions or real Stripe / Google Workspace tools used.
  - Alpha / early preview qualifier for NemoClaw / OpenShell.
  - "Kimi Coding" → "Kimi / Moonshot" in inherited content.
  - NVIDIA agent skills described correctly.
  - Stripe Skills presented as optional Hermes skills, not Stripe products.
  - Footer with correct credits and no-official-affiliation disclaimer.
- Basic HTML validation: OK.
- Updated `TODOS.md` and `PROGRESS.md`.

### 2026-06-26 — Recovered storytelling from `Kimi_Agent_10 Storytelling Web Sites/`
- Full audit of `Kimi_Agent_10 Storytelling Web Sites/` with AgentSwarm. Recovered narrative and information patterns; discarded classic aesthetic (Cinzel, marble, figurative icons), brand errors ("Nose Research" → Nous Research) and the seventh hero "The Brain".
- Enriched `web/index.html`: 4-step process section (intent → heroes → missions → delivery), animated counters with 10 → 1M milestone bar, secondary impact metrics, 4-channel growth plan (workshops, pilot companies, technical partners, profile marketplace), typing CTA with writing effect and copy toast.
- Enriched `web/developers.html`: technical badges and per-hero spec tables (role, I/O, permissions, connections, Pegaso/toolkit, eval, MCP), G-Brain API reference with methods table and code examples, visual 4-phase workshop timeline, install tabs (Local / NemoClaw / Stripe / Variables) with copy feedback, "Hermes harness" badge on NVIDIA NemoClaw.
- Updated `scripts/capture.py` to force `.stat-value` and regenerate screenshots.
- Updated `README.md` and `TODOS.md`.
- Regenerated desktop/mobile screenshots in `screenshots/`.
- Validated HTML of both pages.
- Commit performed.

### 2026-06-26 — Full repair loop (3 phases)
- Rewrote `web/index.html` as master marketing spec with archetype narrative, Hermes=company, 6 heroes with Pegasus, construction/cafe examples, 10→1M counter, intent letter from Pablo (PlayStation/LATAM/wsc.lat) and detailed go-to-market.
- Rewrote `web/developers.html` as technical mirror with Mermaid architecture, mission sequence, per-hero technical cards, connection diagrams per profile, 90-min workshop, repo structure and roadmap.
- Updated desktop/mobile screenshots in `screenshots/`.
- Updated `README.md` with new narrative, Pegasus, flow and status.
- Updated `TODOS.md`.
- Updated 6 SOUL.md files with "Pegaso" section.
- Verified `python scripts/demo_tesorero.py` PASS.
- Verified `cd dashboard && npm run build` PASS.
- Final loop commit performed.

### 2026-06-26 — Completed `partenon-estratega` profile
- Created `hermes/profiles/partenon-estratega/` as a Hermes Agent distribution.
- Files: `SOUL.md`, `config.yaml`, `.env.example`, `.ops`, `templates/.ops.example`, `cron/morning-briefing.json`, `cron/midday-pulse.json`, `cron/weekly-planning.json`, `cron/weekly-retro.json`.
- `ops` skill with `SKILL.md` and five Python tools.
- Tools verified with `python3 -m py_compile` and test run.
- Updated `TODOS.md`, `CHANGELOG.md` and `README.md`.

### 2026-06-26 — Completed `partenon-diplomatico` profile
- Completed `hermes/profiles/partenon-diplomatico/` as a Hermes Agent distribution.
- New files: `skills/relations/tools/crm.py`, `skills/relations/tools/followups.py`.
- Tools verified.
- Updated `TODOS.md` and `CHANGELOG.md`.

### 2026-06-26 — Created `partenon-tesorero`, `partenon-mensajero`, `partenon-cobrador`, `partenon-guardian` profiles
- Each with SOUL.md, config.yaml, .env.example, templates and cron.
- Skills finance, comms, payments, security with Python tools.
- Tools verified with `python3 -m py_compile`.

### 2026-06-24 — Nous-style redesign of web pages
- Approved plan to restructure `web/index.html` and `web/developers.html`.
- Updated `DESIGN.md` with visual tokens and anti-slop copy rules.
- Commit `e786b18`.

### 2026-06-26 — Profile templates, cron, and tool translation to English
- Translated all profile configuration templates to English: `.finance.example`, `.design.example`, `.payments.example`, `.relations.example`, `.brain.example`.
- Translated all profile cron JSON files under `hermes/profiles/*/cron/` to English.
- Translated remaining Python tools to English and aligned JSON keys:
  - `hermes/profiles/partenon-estratega/skills/ops/tools/tasks.py`
  - `hermes/profiles/partenon-diplomatico/skills/relations/tools/crm.py`
  - `hermes/profiles/partenon-diplomatico/skills/relations/tools/followups.py`
  - `hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py`
- Translated `data/cron.json` and `data/tasks.json` to English with runnable command placeholders.
- Updated `MISSING_IMPLEMENTATION.md` to reflect the current implementation state.
- Verified syntax for all profile Python tools via `python3 -m py_compile`.
- Verified `python3 scripts/demo_tesorero.py` runs successfully.
- Verified `cd dashboard && npm run build` succeeds.
- Cleaned generated test artifacts (`.payments`, `output/`, cache files, temporary goals JSON).
- Updated `TODOS.md` with completed translation and verification tasks.

### 2026-06-26 — Brain profile i18n audit and gap-fix
- Audited `web/heroes.html` and `web/developers.html` promises for The Brain (MCP orchestration, context sharing, pattern analysis, insight generation).
- Verified all `partenon-brain` profile files are in English (`SOUL.md`, `config.yaml`, `.env.example`, `SKILL.md`, cron JSON, templates).
- Added missing MCP tools in `hermes/profiles/partenon-brain/skills/memory/tools/`:
  - `mcp_hub.py` — `share_context`, `find_patterns`, `orchestrate_agents`, `register_agent`, `generate_insight`
  - `sync.py` — `collect_learnings`, `collect_decisions`, `index_in_gbrain`, `notify`
  - `__init__.py` — exports all tool functions
- Fixed `gbrain_client.py` `put_page` to send content via `stdin` instead of a broken shell-redirection argument.
- Updated `SKILL.md` to document the new tools and bumped `config.yaml` version to `0.2.0`.
- Verified all Brain Python tools compile with `python3 -m py_compile`.
- Fixed Python 3.9 compatibility by replacing `str | None` union syntax with `Optional[str]`.
- Committed changes: `aa910c5`, `54ef785`.

### 2026-06-26 — Diplomat profile i18n audit and gap-fix
- Audited `web/heroes.html` and `web/developers.html` promises for The Diplomat (client/vendor relationships, CRM operations, meeting scheduler, follow-ups, proposals).
- Verified all `partenon-diplomatico` profile files are in English (`SOUL.md`, `config.yaml`, `.env.example`, `SKILL.md`, cron JSON, templates).
- Translated Spanish placeholder names in `templates/.relations.example` to English.
- Restructured `config.yaml` with explicit MCP server definitions, model fallback, and Diplomat role.
- Expanded `.env.example` with CRM provider and meeting scheduler variables.
- Added profile-level `SKILL.md`.
- Added `tools/__init__.py` to the relations skill package.
- Added missing MCP-aligned tools in `hermes/profiles/partenon-diplomatico/skills/relations/tools/`:
  - `sync_contacts.py` — export/import `.relations` contacts to HubSpot/Salesforce/custom CRM payloads.
  - `schedule_meeting.py` — create meeting records and calendar event payloads.
  - `log_interaction.py` — wrapper for logging communications/calls/emails.
  - `auto_followup.py` — daily follow-up report entry point.
  - `generate_proposal.py` — draft client proposals from `.relations` context.
- Updated `skills/relations/SKILL.md` to document all tools and commands.
- Verified all Diplomat Python tools compile with `python3 -m py_compile` and run basic smoke tests.
- Committed changes: `9faf8a1`.

## Completed Features
- Master web pages rebuilt and committed.
- Six Hermes profiles with updated SOUL.md (including Pegasus).
- Functional Scribe demo.
- Next.js dashboard with kanban and cron.
- Nous-style visual system applied.
- Project documentation synchronized.
- English translation of README and docs completed.

### 2026-06-26 — Herald profile i18n audit and gap-fix
- Audited `web/heroes.html` and `web/developers.html` promises for The Herald (brand strategy, social media, SEO/GEO, campaign management, content calendar, presentations).
- Verified all `partenon-mensajero` profile files are translated to English (`SOUL.md`, `config.yaml`, `.env.example`, `SKILL.md`, cron JSON, templates, tools).
- Aligned `.design.example` keys with tool logic (`positioning`, `addressing`, `claims_to_avoid`) and added a `visual` section.
- Restructured `config.yaml` with Herald role, MCP servers, and optional social/WordPress tools.
- Expanded `.env.example` with social media API and WordPress/SSH variables.
- Added missing MCP-aligned tools in `hermes/profiles/partenon-mensajero/skills/comms/tools/`:
  - `publish_post.py` — validate and record social posts with approval gating.
  - `schedule_content.py` — build a post schedule from a content calendar.
  - `seo_geo_optimizer.py` — keyword analysis and SEO/GEO recommendations.
  - `analyze_engagement.py` — engagement report and opportunity detection.
  - `presentation_builder.py` — generate slide deck outlines.
  - `read_brand_config.py`, `read_content_calendar.py`, `generate_post_ideas.py` — cron workflow helpers.
  - `read_social_metrics.py`, `detect_opportunities.py`, `notify.py` — midday pulse helpers.
  - `__init__.py` for the comms skill package.
- Added `templates/pitch-deck/base.md` for presentation structure.
- Updated cron JSON files to use Herald identifiers and English descriptions.
- Verified all Herald Python tools compile with `python3 -m py_compile`.

## Resolved Blockers
- None.

## Remaining Gaps
- The profile directory remains named `partenon-mensajero` because external files (e.g., `data/cron.json`, `scripts/setup_hermes.py`) reference that path. Only internal file contents were translated.

### 2026-06-28 — Phase 0 contaminants cleanup
- Removed dead code: `Kimi_Agent_10 Storytelling Web Sites/`, `examples/*-stub.py`, `docs/PARTENON_GUIDE.html`, `docs/HERMES_GATEWAY_AUDIT.md`, and stale `docs/superpowers/plans/specs` files.
- Replaced `examples/README.md` with a note that the directory is reserved for real examples.
- Anonymized sample data across `partenon-core/tools/onboarding_engine.py`, Diplomat and Treasurer tools, `data/clients.json`, `docs/HERO_GUIDE.md`, `docs/ENTREPRENEUR_PLAYBOOK.md`, and all `workshop/simulations/*.md` files.
- Hardened dashboard auth: removed fallback credentials/secret in `.env.example` and `dashboard/src/lib/auth.ts`; missing env vars now throw.
- Replaced external `gbrain` binary dependency in `gbrain_client.py` with direct `GBrainStore` usage.
- Added `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, and `NOTICE.md`.
- Verified: `npx tsc --noEmit` PASS, `npm run build` PASS, `python3 -m py_compile` on Brain tools PASS, `GBrainClient` import and functional smoke test PASS.

### 2026-06-28 — Standardize hero profile configs to canonical schema
- Rewrote `config.yaml` for all 7 profiles: `partenon-scribe`, `partenon-herald`, `partenon-collector`, `partenon-guardian`, `partenon-strategist`, `partenon-diplomat`, `partenon-brain`.
- Applied canonical schema: `profile`, `model`, `skills.auto_load`, `mcp_servers`, `files`, `permissions`, `workflows`, `handoffs`, `cron`, `behavior`.
- Added `partenon-memory` MCP server (`python -m gbrain.server`) to every profile.
- Added `google_workspace`, `gmail`, and `stripe` MCP servers only for profiles that already referenced them in config or SKILL.md.
- Preserved meaningful existing data: descriptions, models, permissions, workflows, handoffs, and cron jobs.
- Removed non-canonical fields: `alias`, `role`, `hermes_agent`, `metadata.partenon`, `logging`, `agent.max_iterations`, `memory`, `tools`.
- Created `scripts/validate_profiles.py` to enforce directory existence, YAML validity, required keys, cron file references, and template existence.
- Verified: `python3 -c "import yaml; yaml.safe_load(...)"` for each config PASS; `python3 scripts/validate_profiles.py` PASS (7/7 profiles valid).
- Committed changes: `803551d`.

### 2026-06-28 — Phase 4: Real-Time Dashboard + API
- Created `partenon_api/` FastAPI backend as the single source of truth for missions, cron jobs, hero status, workflow events, and integrations.
- Added atomic JSON store (`partenon_api/store.py`) with advisory locking and migration from legacy `data/tasks.json` to `data/missions.json`.
- Implemented JWT auth shared between dashboard and API; login endpoint `/api/v1/auth/token` issues tokens signed with `PARTENON_API_SECRET`/`DASHBOARD_AUTH_SECRET`.
- Built domain routes: `/api/v1/missions`, `/api/v1/cron`, `/api/v1/heroes`, `/api/v1/events`, `/api/v1/integrations`, plus `/api/v1/memory/search`.
- Added Server-Sent Events endpoint `/api/v1/stream` with in-memory broadcast bus; dashboard `LiveEvents` component reconnects and refreshes on mission/cron/event changes.
- Refactored Next.js dashboard to consume the API via server actions (`dashboard/src/lib/api.ts`, `dashboard/src/lib/data.ts`, `dashboard/src/lib/auth.ts`).
- Added workspace isolation foundation: every entity carries `workspace_id` and API routes filter by the JWT workspace.
- Added integration bridge over existing MCP servers (Google Workspace, Slack, Payments, Memory).
- Added 23 new tests covering auth, missions, cron, events, and store; total suite now 82 tests.
- Updated `.env.example`, `README.md`, `install.sh`, `TODOS.md`, and `PLAN.md` for the new API backend.
- Verified: `pytest tests/` PASS (82), `ruff check` PASS, `cd dashboard && npm run lint` PASS, `cd dashboard && npm run build` PASS, `bash -n install.sh` PASS, `python3 .github/scripts/secret_scan.py` PASS.

### 2026-06-29 — Repair sprint: migrate API store to partenon-memory MCP server
- Created `partenon_api/mcp_client.py` with `AsyncMemoryClient` (stdio MCP context manager) and `sync_call` helper for non-async callers.
- Rewrote `partenon_api/store.py`: replaced direct JSON file access with `MemoryStore` backed by the `partenon-memory` MCP server.
- Entities stored as G-Brain pages with slugs like `workspace/{workspace_id}/missions/{id}` and tags (`mission`, `workspace:default`, profile).
- Implemented async CRUD methods for missions, cron jobs, events, and nudges; deletes use tombstone pages because the MCP server has no delete tool.
- Added `migrate_legacy_json_to_memory()` one-time helper that imports existing `data/missions.json`, `data/cron.json`, and `data/nudges.json` into G-Brain pages and renames the JSON files to `*.migrated`.
- Updated `partenon_api/main.py` lifespan to open `AsyncMemoryClient`, store it in `app.state.memory_client`, run migration, and close on shutdown.
- Updated `partenon_api/routers/missions.py`, `cron.py`, `heroes.py`, and `events.py` to read/write via `MemoryStore(request.app.state.memory_client)`.
- Added `get_gbrain_database_url()` to `partenon_api/config.py`.
- Added a synchronous JSON-file fallback in `MemoryStore` selected by `PARTENON_STORE_MODE=json` so tests can run without spawning an MCP subprocess.
- Updated `tests/conftest.py` to use the JSON fallback and point `GBRAIN_DATABASE_URL` to a temporary SQLite file per test.
- Verified:
  - `pytest tests/test_api_missions.py tests/test_api_cron.py tests/test_api_events.py tests/test_store.py -q` PASS (17 tests).
  - `pytest tests/` PASS (110 tests).
  - `ruff check partenon_api tests partenon_core/tools/workflow_engine.py` PASS.
  - `cd dashboard && npm run build` PASS.
  - Manual MCP smoke test (create/list missions and heroes) PASS.
