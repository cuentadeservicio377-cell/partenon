# Changelog — Partenon

> Format: type(scope): description

## [Unreleased]

### Added
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
