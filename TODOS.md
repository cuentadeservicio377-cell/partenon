# TODOS

## In Progress
- [ ] Integrate Google Workspace, Stripe, and G-Brain with real credentials
- [ ] Validate end-to-end flows with a pilot business

## Pending
- [ ] Implement functional eval loop in the Scribe (tests/evals + judge skill + threshold)
- [ ] Add eval loop to the remaining hero profiles
- [ ] Install skill ui-ux-pro-max for systematic design reviews
- [ ] Test real Stripe Link CLI and Stripe Projects commands in sandbox
- [ ] Configure NVIDIA NemoClaw/OpenShell onboarding with Hermes profile

## Completed
- [x] Final review: verified `python3 scripts/demo_tesorero.py` PASS, `cd dashboard && npm run build` PASS, internal doc links OK, English consistency OK
- [x] Rewrite `README.md` with ASCII banner, badges, use cases, feature matrix, architecture, roadmap, and links to all new docs
- [x] Create `docs/ENTREPRENEUR_PLAYBOOK.md` with hero selection guide, copy-paste prompts, 30-60-90 checklist, and example profile configs
- [x] Create `docs/HERO_GUIDE.md` with real tools, MCP/env vars, cron jobs, example commands, and integration points for all 7 heroes
- [x] Create `docs/QUICKSTART.md` with 15-minute step-by-step commands, expected outputs, and screenshot placeholders
- [x] Create `docs/SECURITY.md` covering credential storage, `.env` handling, Google service accounts, Guardian responsibilities, and audit logging
- [x] Create `docs/API.md` with API/CLI reference for core tools, profile tools, scripts, and examples
- [x] Create `docs/FAQ.md` with 20 honest questions and answers
- [x] Create `docs/assets/architecture-diagram.mmd`, `docs/assets/hero-matrix.md`, and `docs/assets/partenon-logo.svg`
- [x] Verify all new docs reference each other with valid links
- [x] Verify `python3 scripts/demo_tesorero.py` PASS and `cd dashboard && npm run build` PASS
- [x] Migrate `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Developers.tsx` to `web/developers.html` with classic React app aesthetic (marble white, Cinzel, Inter) and mandatory information corrections
- [x] Migrate `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Heroes.tsx` to `web/heroes.html` with classic React app aesthetic (marble white, Cinzel, Inter) and mandatory information corrections
- [x] Migrate `Kimi_Agent_10 Storytelling Web Sites/app/src/pages/Home.tsx` to `web/index.html` with classic React app aesthetic (marble white, Cinzel, Inter) and mandatory information corrections
- [x] UX/UI/structure/storytelling diagnosis of `index.html` and `developers.html`
- [x] Rewrite `web/index.html` with narrative arc, before/after, timeline, hero tabs/accordion, and abbreviated letter
- [x] Rewrite `web/developers.html` with short hero, hero profiles in tabs/accordion, Quality Layer section, and demo code
- [x] Diversify visual components: timeline, tabs, accordion, blockquote, before/after
- [x] Mobile review: hero accordion, readable timeline, simplified diagrams
- [x] Generate and review desktop/mobile screenshots for both pages
- [x] Loop Phase 1: Rewrite marketing page (`web/index.html`) with archetype narrative, Pegasus, letter of intent, and go-to-market
- [x] Loop Phase 2: Rewrite technical page (`web/developers.html`) with architecture, Mermaid diagrams, technical cards, and workshop
- [x] Previous Task 14: Verification, documentation, and commit
- [x] Previous Task 13: Update technical page
- [x] Previous Task 12: Update marketing page
- [x] Previous Task 11: Google Sheet base + functional Scribe demo
- [x] Partenon dashboard created in `dashboard/`
- [x] Six Hermes profiles created
- [x] Initial braindump completed
- [x] Memory structure and initial plan created
- [x] Repositories analyzed
- [x] Visual and technical stack confirmed
- [x] `DESIGN.md`, `SPEC.md`, `AGENTS.md` updated
- [x] Improvement loop: research with AgentSwarm on NVIDIA NemoClaw, Nemotron 3 Ultra, OpenShell, CUDA-X skills, Stripe Skills, and Hermes core features
- [x] Enrich `web/index.html` with hackathon stack (Hermes + NVIDIA + Stripe), self-improvement, and gateway
- [x] Enrich `web/developers.html` with NVIDIA/Stripe architecture, updated technical profiles, Hermes Core, and command examples
- [x] Regenerate desktop/mobile screenshots after changes
- [x] Visually verify pages and validate HTML
- [x] Audit `Kimi_Agent_10 Storytelling Web Sites/` with AgentSwarm and recover valuable storytelling
- [x] Enrich `web/index.html` with 4-step process, animated counters, milestone bar, impact metrics, 4-channel growth plan, and typed CTA
- [x] Enrich `web/developers.html` with technical badges, per-hero specification tables, API reference, visual workshop timeline, install tabs with copy feedback
- [x] Update `scripts/capture.py` to force `.stat-value` and regenerate screenshots
- [x] Correct "G-Brain of Garitán" → "G-Brain of Garry Tan"
- [x] Update `README.md` with the new 3-page structure and information corrections
- [x] Regenerate desktop/mobile screenshots for `index.html`, `heroes.html`, and `developers.html`
- [x] Deploy site on `hermespartenon.online` domain via Hostinger File Manager
- [x] Verify deployed site on real domain (HTTP 200, no banned terms, assets loading)
- [x] Close web development phase: memory, TODOS, gbrain, and final commit
- [x] Create public GitHub repository for Partenon
- [x] Complete repo structure with 7 profiles, global `.env.example`, `install.sh`, and `scripts/setup_hermes.py`
- [x] Create full documentation: `docs/for-founders.md`, `docs/for-developers.md`, `docs/architecture.md`
- [x] Verify builds/demo/dashboard and regenerate `web-deploy.zip`

## Web-Repo Consistency Audit (this session)
- [x] Audit `web/index.html`, `web/heroes.html`, `web/developers.html` against repository contents
- [x] Create `MISSING_IMPLEMENTATION.md` with prioritized gaps
- [x] Create CLI/API/MCP example stubs in `examples/`
- [x] Update `web/developers.html` install section to reflect current local setup
- [x] Fix GitHub repository links across all three web pages
- [x] Replace fictional `npx create-hermes@latest` CTA with real clone command

## English Translation & Core Tooling Audit (this session)
- [x] Translate all profile configuration templates to English (.finance, .design, .payments, .relations, .brain)
- [x] Translate all profile cron JSON files to English
- [x] Translate Strategist ops Python tools to English and align JSON keys
- [x] Translate Diplomat relations Python tools to English and align .relations keys
- [x] Translate Brain gbrain_client.py to English
- [x] Audit and gap-fix `partenon-brain` profile: translate all files to English, add MCP tools (`share_context`, `find_patterns`, `orchestrate_agents`, `register_agent`, `generate_insight`), fix `gbrain_client.put_page` stdin handling, add daily sync tools, and verify Python compilation
- [x] Translate data/cron.json and data/tasks.json to English with runnable commands
- [x] Translate AGENTS.md, DESIGN.md, SPEC.md, and docs/superpowers plan snippets to English
- [x] Translate Next.js dashboard UI strings, status/priority enums, and profile display names to English
- [x] Update MISSING_IMPLEMENTATION.md with current state and gaps
- [x] Fix Diplomat .relations parser to handle nested objects
- [x] Fix Strategist briefings import (goals.py) so the tool runs standalone
- [x] Remove Spanish fallbacks from partenon-core config_loader
- [x] Verify onboarding_engine.py loads config_loader correctly
- [x] Syntax-check all profile Python tools
- [x] Run demo_tesorero.py successfully
- [x] Build dashboard (Next.js) successfully
- [x] Audit and gap-fix `partenon-diplomatico` profile (template translation, config.yaml, SKILL.md, .env.example)
- [x] Add Diplomat MCP-aligned tools: `sync_contacts`, `schedule_meeting`, `log_interaction`, `auto_followup`, `generate_proposal`
- [x] Verify all Diplomat Python tools compile with `python3 -m py_compile`
- [x] Audit and gap-fix `partenon-cobrador` profile (template schema alignment, config.yaml, SKILL.md, .env.example)
- [x] Add Collector MCP-aligned tools: `create_invoice`, `list_charges`, `monitor_fraud`, `read_pending_payments`, `read_overdue_payments`, `classify_risk`, `schedule_followup`, `notify`
- [x] Verify all Collector Python tools compile with `python3 -m py_compile`
- [x] Audit and gap-fix `partenon-mensajero` profile (SOUL.md, config.yaml, SKILL.md, .env.example, templates, cron JSON) — translate to English, align with Herald capabilities, add MCP-aligned tools (`publish_post`, `schedule_content`, `seo_geo_optimizer`, `analyze_engagement`, `presentation_builder`, `read_brand_config`, `read_content_calendar`, `generate_post_ideas`, `read_social_metrics`, `detect_opportunities`, `notify`), and verify Python compilation

## Documentation Rewrite (this session)
- [x] Rewrite `README.md` from scratch with banner, badges, use cases, feature matrix, architecture, roadmap, and links to new docs
- [x] Create `docs/ENTREPRENEUR_PLAYBOOK.md` with business-type hero selection, copy-paste prompts, 30-60-90 checklist, and example configs
- [x] Create `docs/HERO_GUIDE.md` with per-hero tools, MCP servers, env vars, cron jobs, prompts, and integration points
- [x] Create `docs/QUICKSTART.md` with 15-minute step-by-step demo commands and expected outputs
- [x] Create `docs/SECURITY.md` covering credential storage, service accounts, key rotation, Guardian, and audit logging
- [x] Create `docs/API.md` referencing actual code in `partenon-core/tools/`, `scripts/`, and `examples/`
- [x] Create `docs/FAQ.md` with 20 honest questions and answers
- [x] Create `docs/assets/architecture-diagram.mmd`, `docs/assets/hero-matrix.md`, and `docs/assets/partenon-logo.svg`
- [x] Verify `python3 scripts/demo_tesorero.py` still runs
- [x] Verify `cd dashboard && npm run build` still succeeds
- [x] Cross-check internal documentation links and English consistency

## Pending
- [ ] Standardize `GBRAIN_DATABASE_URL` naming across .env and gbrain server
- [ ] Add automated tests for translated tools
- [ ] Implement real intent router and workflow engine runtime
- [ ] Add publishing/dispatch integrations for Messenger, Collector, and Diplomat

## Parking Lot
_Discoveries made during development that are NOT in the current plan_
