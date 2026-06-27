# Progress

## Session History

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
