# Changelog — Partenon

> Format: type(scope): description

## [Unreleased]

### Added
- feat(phase-3): add `mcp_servers/google_workspace/` adapter with Sheets, Docs, Slides, Calendar, and Gmail tools; wire Scribe, Herald, Strategist, and Diplomat to it.
- feat(phase-3): implement Stripe live mode in `mcp_servers/payments/server.py` (payment links, invoices, subscriptions, charges, income report, fraud, pending/overdue tracking).
- feat(phase-3): add Stripe webhook handler at `mcp_servers/payments/webhook.py` that emits `payment_confirmed` to the workflow engine.
- feat(phase-3): add `mcp_servers/notifications/slack.py` adapter and `partenon-slack` MCP server for Strategist notifications.
- feat(phase-3): add Guardian key audit (`security_audit_key_strength`, `security_detect_key_provider`) and model recommendation (`security_recommend_model`) tools.
- feat(phase-3): extend workflow engine to notify Slack on `task_overdue` events.
- test(phase-3): add `tests/test_google_workspace_adapter.py`, `tests/test_stripe_live.py`, `tests/test_stripe_webhook.py`, `tests/test_slack_adapter.py`, `tests/test_guardian_key_manager.py`, and extend `tests/test_handoffs.py` for Slack notification.
- build(deps): add `fastapi`, `uvicorn`, `gspread`, `google-api-python-client`, `stripe`, `slack-sdk`, and `httpx` to dependencies.
- feat(phase-2): finalize dry-run/live tool lists for all 7 heroes and rewrite `SOUL.md`/`SKILL.md` with operating modes, MCP catalogs, and dry-run/live tables.
- feat(phase-2): implement dry-run wrappers in every MCP server (`memory`, `finance`, `payments`, `comms`, `security`, `ops`, `relations`).
- feat(phase-2): add 6 collaboration handoff workflows to `workflow_engine.py` for payment→scribe, budget→scribe, agreement→ops/strategist, milestone→diplomat, key rotation→all, and learning→target hero.
- test(phase-2): add `tests/test_mcp_servers.py` and `tests/test_handoffs.py` covering all domain tools and handoff events (27 tests).
- feat(phase-1): add root `distribution.yaml` and `pyproject.toml`; package `partenon_core` with `partenon-core`, `partenon-judge`, and `partenon-workflows` skills.
- feat(phase-1): create `mcp_servers/` wrappers for memory, finance, payments, comms, security, ops, and relations (dry-run defaults).
- feat(phase-1): bundle G-Brain as `mcp_servers.memory` (`partenon-memory`) and wire all profiles to it.
- feat(phase-1): add per-profile `distribution.yaml` files and verify `hermes profile install` end-to-end for all 7 heroes.
- ci(github): add `.github/workflows/ci.yml` with Python tests, dashboard lint/build, and secret scan jobs.
- ci(scripts): add `.github/scripts/secret_scan.py` for lightweight hardcoded-secret detection in CI.
- build(dashboard): configure ESLint with `eslint-config-next` and add lint script.
- build(installer): make `install.sh` idempotent, space-safe, and secret-generating on first run.
- docs(workshop): add `workshop/PRODUCTION_READINESS_RESEARCH.md` with base-system verification, hero smoke tests, five real small-business case studies, and production-readiness scoring for construction/retail/SaaS simulations.
- docs(workshop): add production-readiness findings to `MISSING_IMPLEMENTATION.md` (stale venv blocker, missing `sim_runner.py`, missing construction checklist, mismatched simulation company cards).
- feat(profiles): create `partenon-diplomat` profile with relations skill, CRM and follow-ups.
- feat(profiles): create `partenon-strategist` profile with ops skill (projects, tasks, checklists, goals, briefings), `.ops` template and morning/midday/planning/retro cron jobs.
- docs(playbook): add `docs/ENTREPRENEUR_PLAYBOOK.md` with hero selection by business type, prompts, and rollout checklist.
- docs(guides): add `docs/HERO_GUIDE.md` and `docs/QUICKSTART.md`.
- docs(reference): add `docs/SECURITY.md`, `docs/API.md`, and `docs/FAQ.md`.
- docs(assets): add `docs/assets/architecture-diagram.mmd`, `docs/assets/hero-matrix.md`, and `docs/assets/partenon-logo.svg`.

### Changed
- docs(readme): translate README and docs to English; align repository description with live site and GitHub URL.
- docs(architecture): document current `partenon-core` components and mark eval-loop stub as not yet implemented.
- docs(polish): revise README banner, API reference, FAQ, security guide, and hero capability matrix for consistency and grounded detail.
- docs(commands): normalize all Python command examples to `python3` across README, docs, scripts, examples, install output, and `web/developers.html` to match the project environment.

### Fixed
- docs(readme): remove non-working NVIDIA NemoClaw curl command; point to official NVIDIA instructions.

## 2026-06-25
- chore: braindump + initial project structure.
