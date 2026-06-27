# TODOS

## In Progress
- [ ] Integrate Google Workspace, Stripe, and G-Brain with real credentials
- [ ] Validate end-to-end flows with a pilot business

## Pending
- [ ] Fix `install.sh` to recreate venv when existing `.venv` Python is below 3.10
- [ ] Implement or remove `workshop/simulations/sim_runner.py` and align simulation commands with real tool CLIs
- [ ] Add construction checklist template to Strategist `checklists.py`
- [ ] Align simulation markdowns with existing company cards or create missing cards
- [ ] Implement functional eval loop in the Scribe (tests/evals + judge skill + threshold)
- [ ] Add eval loop to the remaining hero profiles
- [ ] Install skill ui-ux-pro-max for systematic design reviews
- [ ] Test real Stripe Link CLI and Stripe Projects commands in sandbox
- [ ] Configure NVIDIA NemoClaw/OpenShell onboarding with Hermes profile
- [ ] Build end-to-end bank/CSV → classification → Google Sheets script for Scribe
- [ ] Add Shopify/order import and inventory tracking for retail
- [ ] Add AWS cost import and churn-signal worksheet for SaaS
- [ ] Bundle or replace external `gbrain` binary with local fallback
- [ ] Implement real intent router and workflow engine runtime
- [ ] Add publishing/dispatch integrations for Messenger, Collector, and Diplomat
- [ ] Add invoice/receipt PDF generation to the Collector
- [ ] Add `.github/ISSUE_TEMPLATE.md` and a public support channel

## Completed
- [x] Run production-readiness test for construction/retail/SaaS simulations and create `workshop/PRODUCTION_READINESS_RESEARCH.md`
- [x] Research five real small businesses with public data
- [x] Create `workshop/companies/` cards for coffee shop, agency, construction, retail, SaaS
- [x] Create five `workshop/simulations/` scenarios with runnable commands
- [x] Create `workshop/guides/HERMES_ONBOARDING.md`
- [x] Create `workshop/README.md`, `workshop/AGENDA.md`, `workshop/SLIDES.md`, `workshop/HANDOUT.md`
- [x] Create `workshop/checklists/PRODUCTION_READINESS.md`
- [x] Update `MISSING_IMPLEMENTATION.md` with workshop findings and PyYAML gap
- [x] Add `pyyaml>=6.0` to `requirements.txt`
- [x] Update `README.md` and `docs/ENTREPRENEUR_PLAYBOOK.md` with workshop links
- [x] Verify `python3 scripts/demo_tesorero.py` PASS
- [x] Verify `cd dashboard && npm run build` PASS
- [x] Verify simulation tools compile with `python3 -m py_compile`
- [x] Final verification and commit of the workshop package
- [x] Final review: verified `python3 scripts/demo_tesorero.py` PASS, `cd dashboard && npm run build` PASS, internal doc links OK, English consistency OK
- [x] Standardize `GBRAIN_DATABASE_URL` naming across `.env.example`, `gbrain/server.py`, and `partenon-core/config/mcp/servers.yaml`
- [x] Add initial automated tests in `tests/` (`test_scribe_demo.py`, `test_onboarding_engine.py`)
- [x] Enable Guardian key-manager cron entry with a runnable CLI (`key_manager.py`)
- [x] Rewrite `README.md` with ASCII banner, badges, use cases, feature matrix, architecture, roadmap, and links to all new docs
- [x] Create `docs/ENTREPRENEUR_PLAYBOOK.md` with hero selection guide, copy-paste prompts, 30-60-90 checklist, and example profile configs
- [x] Create `docs/HERO_GUIDE.md` with real tools, MCP/env vars, cron jobs, example commands, and integration points for all 7 heroes
- [x] Create `docs/QUICKSTART.md` with 15-minute step-by-step commands, expected outputs, and screenshot placeholders
- [x] Create `docs/SECURITY.md` covering credential storage, `.env` handling, Google service accounts, Guardian responsibilities, and audit logging
- [x] Create `docs/API.md` with API/CLI reference for core tools, profile tools, scripts, and examples
- [x] Create `docs/FAQ.md` with 20 honest questions and answers
- [x] Create `docs/assets/architecture-diagram.mmd`, `docs/assets/hero-matrix.md`, and `docs/assets/partenon-logo.svg`
- [x] Verify all new docs reference each other with valid links
- [x] Migrate `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Developers.tsx` to `web/developers.html`
- [x] Migrate `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Heroes.tsx` to `web/heroes.html`
- [x] Migrate `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Home.tsx` to `web/index.html`
- [x] UX/UI/structure/storytelling diagnosis of `index.html` and `developers.html`
- [x] Rewrite `web/index.html` with narrative arc, before/after, timeline, hero tabs/accordion, and abbreviated letter
- [x] Rewrite `web/developers.html` with short hero, hero profiles in tabs/accordion, Quality Layer section, and demo code
- [x] Diversify visual components: timeline, tabs, accordion, blockquote, before/after
- [x] Mobile review: hero accordion, readable timeline, simplified diagrams
- [x] Generate and review desktop/mobile screenshots for both pages
- [x] Deploy site on `hermespartenon.online` domain via Hostinger File Manager
- [x] Create public GitHub repository for Partenon
- [x] Complete repo structure with 7 profiles, global `.env.example`, `install.sh`, and `scripts/setup_hermes.py`
- [x] Translate all profile configuration templates to English (.finance, .design, .payments, .relations, .brain)
- [x] Translate all profile cron JSON files to English
- [x] Translate Strategist ops Python tools to English and align JSON keys
- [x] Translate Diplomat relations Python tools to English and align .relations keys
- [x] Translate Brain `gbrain_client.py` to English and fix stdin encoding
- [x] Translate `data/cron.json` and `data/tasks.json` to English with runnable commands
- [x] Translate Next.js dashboard UI strings, status/priority enums, and profile display names to English
- [x] Update `MISSING_IMPLEMENTATION.md` with current state and gaps
- [x] Fix Diplomat `.relations` parser to handle nested objects
- [x] Fix Strategist briefings import (`goals.py`) so the tool runs standalone
- [x] Remove Spanish fallbacks from `partenon-core` config_loader
- [x] Audit and gap-fix `partenon-cobrador` profile
- [x] Audit and gap-fix `partenon-mensajero` profile

## Parking Lot
_Discoveries made during development that are NOT in the current plan_
- Several profile tools import `yaml` but `pyyaml` was not declared until this pass. Consider pinning and documenting all Python version constraints.
