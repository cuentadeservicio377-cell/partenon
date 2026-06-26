# Partenon System Build — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development or dispatching-parallel-agents to implement tasks. Independent tasks should run in parallel.

**Goal:** Assemble a working Partenon repository on top of Hermes Agent (Nous Research) with 6 hero profiles, a general onboarding flow that generates tasks polled by cron and shown in a kanban, G-Brain MCP integration, and updated marketing/technical web pages. Deliver a functional Tesorero demo.

**Architecture:** Partenon is an adapter layer, not a rewrite. Hermes Agent CLI is the runtime. Each hero is a Hermes profile distribution (`SOUL.md` + `config.yaml` + `skills/` + `cron/`). `partenon-core` adapts `hermes-business-core` for routing and onboarding. `partenon-dashboard` adapts `dashboard-completo` for kanban/cron UI. `partenon-gbrain` exposes G-Brain as an MCP server. Integrations reuse existing MCP servers and connectors.

**Tech Stack:** Hermes Agent CLI, Python 3.12 skills, Next.js 15 + TypeScript dashboard, Google Workspace APIs, Stripe MCP, G-Brain MCP, Tailwind HTML pages, Docker Compose optional.

## Global Constraints

- Do not fork Hermes Agent core. Use profiles, skills, and MCP.
- Every profile must be installable with `hermes profile install <path>`.
- All business output must land in Google Workspace (Sheets/Docs/Slides/Drive/Calendar/Gmail).
- Use existing repositories as source: HBOS, Hermes Growth, OpenWork Paola, Agente Marketing Kimi, Excel Agent, dashboard-completo.
- No emojis, no banned fonts (Inter/Roboto/Arial/Open Sans/Helvetica), no massive gradients.
- Copy anti-AI-slop: no em-dashes, no intensifiers, no filler phrases.
- Pages must remain responsive at 1440px and 390px.
- Each task ends with a commit.

---

## Task 1: Repository Scaffold

**Files:**
- Create: `README.md` (replace existing)
- Create: `AGENTS.md` (update with build commands)
- Create: `.env.example`
- Create: `docker-compose.yml`
- Create: `install.sh`
- Create: `partenon-core/README.md`
- Create: `partenon-core/SKILL.md`
- Create: `partenon-core/tools/__init__.py`
- Create: `partenon-core/tools/router.py`
- Create: `partenon-core/tools/onboarding_engine.py`
- Create: `partenon-core/tools/workflow_engine.py`
- Create: `partenon-core/config/mcp/servers.yaml`

**Interfaces:**
- Consumes: HBOS `hermes-business-core` skills and config.
- Produces: `partenon_core` Python package with `route_intent()`, `run_onboarding()`, `handoff()`.

**Steps:**
1. Copy `Hermes Bussines OS/skills/hermes-business-core/SKILL.md` into `partenon-core/SKILL.md` and rewrite name/description to Partenon.
2. Copy `Hermes Bussines OS/skills/hermes-business-core/tools/router.py` to `partenon-core/tools/router.py`; map 6 hero names as routes.
3. Copy `Hermes Bussines OS/skills/hermes-business-core/tools/onboarding_engine.py` to `partenon-core/tools/onboarding_engine.py`; strip HBOS-specific catalogs, keep wizard flow.
4. Copy `Hermes Bussines OS/skills/hermes-business-core/tools/workflow_engine.py` to `partenon-core/tools/workflow_engine.py`.
5. Copy `Hermes Bussines OS/config/mcp/servers.yaml` to `partenon-core/config/mcp/servers.yaml`.
6. Write `install.sh` that installs Hermes CLI, installs 6 profiles, copies `.env.example`, and prints next steps.
7. Write `docker-compose.yml` with PostgreSQL for G-Brain and optional dashboard service.
8. Run `python -m py_compile partenon-core/tools/*.py`.
9. Commit.

---

## Task 2: Tesorero Profile

**Files:**
- Create: `hermes/profiles/partenon-tesorero/SOUL.md`
- Create: `hermes/profiles/partenon-tesorero/config.yaml`
- Create: `hermes/profiles/partenon-tesorero/.env.example`
- Create: `hermes/profiles/partenon-tesorero/skills/finance/SKILL.md`
- Create: `hermes/profiles/partenon-tesorero/skills/finance/tools/google_sheets.py`
- Create: `hermes/profiles/partenon-tesorero/skills/finance/tools/parsers.py`
- Create: `hermes/profiles/partenon-tesorero/templates/.finance.example`
- Create: `hermes/profiles/partenon-tesorero/cron/daily-report.json`

**Interfaces:**
- Consumes: HBOS `hermes-finanzas`, Excel Agent templates/parsers, Google Workspace MCP.
- Produces: `partenon-tesorero` profile installable via `hermes profile install hermes/profiles/partenon-tesorero`.

**Steps:**
1. Write `SOUL.md` with Tesorero personality, goals, and rules.
2. Write `config.yaml` enabling Google Workspace MCP and finance tools.
3. Copy `Hermes Bussines OS/skills/hermes-finanzas/` tools into `skills/finance/tools/`.
4. Copy `Open Code/Excel Agent/templates/presupuesto.py` and `proveedores.py` into `skills/finance/tools/templates.py`.
5. Copy `Open Code/Excel Agent/parser_ordenes_arza.py` into `skills/finance/tools/parsers.py`.
6. Write `.finance.example` with fixed/variable costs, dashboards, and budgets.
7. Write `cron/daily-report.json` for daily financial summary.
8. Verify profile structure with a simple bash `ls` check.
9. Commit.

---

## Task 3: Mensajero Profile

**Files:**
- Create: `hermes/profiles/partenon-mensajero/SOUL.md`
- Create: `hermes/profiles/partenon-mensajero/config.yaml`
- Create: `hermes/profiles/partenon-mensajero/.env.example`
- Create: `hermes/profiles/partenon-mensajero/skills/comms/SKILL.md`
- Create: `hermes/profiles/partenon-mensajero/skills/comms/tools/brand_intake.py`
- Create: `hermes/profiles/partenon-mensajero/skills/comms/tools/content_calendar.py`
- Create: `hermes/profiles/partenon-mensajero/templates/.design.example`

**Interfaces:**
- Consumes: HBOS `hermes-ventas`, Agente Marketing Kimi `brand.md`/`campaign-manifest.yaml`, OpenWork docs generator.
- Produces: `partenon-mensajero` profile.

**Steps:**
1. Write `SOUL.md` for Mensajero.
2. Copy `Agente Marketing Kimi/docs/brand/brand-intake-questionnaire.md` into `templates/brand-intake.md`.
3. Copy `Agente Marketing Kimi/scripts/social_calendar.py` into `tools/content_calendar.py`.
4. Copy relevant copywriting prompts from `Agente Marketing Kimi/agents/creative-copy.md` and `content-strategy.md` into `skills/comms/SKILL.md`.
5. Write `.design.example` with voz, canales, objetivos.
6. Commit.

---

## Task 4: Cobrador Profile

**Files:**
- Create: `hermes/profiles/partenon-cobrador/SOUL.md`
- Create: `hermes/profiles/partenon-cobrador/config.yaml`
- Create: `hermes/profiles/partenon-cobrador/.env.example`
- Create: `hermes/profiles/partenon-cobrador/skills/payments/SKILL.md`
- Create: `hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py`
- Create: `hermes/profiles/partenon-cobrador/templates/.payments.example`

**Interfaces:**
- Consumes: HBOS `hermes-finanzas/pagos`, Stripe MCP server, Stripe Agent Toolkit docs.
- Produces: `partenon-cobrador` profile.

**Steps:**
1. Write `SOUL.md` for Cobrador.
2. Copy `Hermes Bussines OS/skills/hermes-finanzas/tools/pagos.py` into `skills/payments/tools/stripe_tools.py`.
3. Add Stripe MCP server reference from `partenon-core/config/mcp/servers.yaml`.
4. Write `.payments.example` with products, prices, links, and subscriptions.
5. Commit.

---

## Task 5: Guardian Profile

**Files:**
- Create: `hermes/profiles/partenon-guardian/SOUL.md`
- Create: `hermes/profiles/partenon-guardian/config.yaml`
- Create: `hermes/profiles/partenon-guardian/.env.example`
- Create: `hermes/profiles/partenon-guardian/skills/security/SKILL.md`
- Create: `hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py`
- Create: `hermes/profiles/partenon-guardian/templates/.security.example`

**Interfaces:**
- Consumes: Hermes Growth `business-operator` config patterns, HBOS `config_loader.py`.
- Produces: `partenon-guardian` profile.

**Steps:**
1. Write `SOUL.md` for Guardian.
2. Write `key_manager.py` with functions `list_keys()`, `rotate_key(provider)`, `audit_access(profile)`.
3. Write `.security.example` with providers (Nous/Nvidia/OpenAI/Kimi/Stripe), keys, permissions.
4. Commit.

---

## Task 6: Estratega Profile

**Files:**
- Create: `hermes/profiles/partenon-estratega/SOUL.md`
- Create: `hermes/profiles/partenon-estratega/config.yaml`
- Create: `hermes/profiles/partenon-estratega/.env.example`
- Create: `hermes/profiles/partenon-estratega/skills/ops/SKILL.md`
- Create: `hermes/profiles/partenon-estratega/skills/ops/tools/projects.py`
- Create: `hermes/profiles/partenon-estratega/skills/ops/tools/tasks.py`
- Create: `hermes/profiles/partenon-estratega/cron/morning-briefing.json`
- Create: `hermes/profiles/partenon-estratega/templates/.ops.example`

**Interfaces:**
- Consumes: HBOS `hermes-operaciones`, `hermes-iniciativa`, dashboard-completo parsers.
- Produces: `partenon-estratega` profile.

**Steps:**
1. Write `SOUL.md` for Estratega.
2. Copy `Hermes Bussines OS/skills/hermes-operaciones/tools/proyectos.py` and `tareas.py` (projects and tasks).
3. Copy `Hermes Bussines OS/skills/hermes-iniciativa/tools/morning_briefing.py` and `metas_engine.py`.
4. Write `cron/morning-briefing.json`, `midday-pulse.json`, `weekly-planning.json`, `weekly-retro.json`.
5. Write `.ops.example` with projects, goals, and calendar.
6. Commit.

---

## Task 7: Diplomatico Profile

**Files:**
- Create: `hermes/profiles/partenon-diplomatico/SOUL.md`
- Create: `hermes/profiles/partenon-diplomatico/config.yaml`
- Create: `hermes/profiles/partenon-diplomatico/.env.example`
- Create: `hermes/profiles/partenon-diplomatico/skills/relations/SKILL.md`
- Create: `hermes/profiles/partenon-diplomatico/skills/relations/tools/crm.py`
- Create: `hermes/profiles/partenon-diplomatico/templates/.relations.example`

**Interfaces:**
- Consumes: HBOS `hermes-ventas` CRM/pipeline, `hermes-rrhh`, OpenWork `paola-aliados`.
- Produces: `partenon-diplomatico` profile.

**Steps:**
1. Write `SOUL.md` for Diplomatico.
2. Copy `Hermes Bussines OS/skills/hermes-ventas/tools/crm.py` and `pipeline.py`.
3. Copy relevant patterns from `OpenWork Paola Meneses/workspace/skills/paola-aliados/SKILL.md`.
4. Write `.relations.example` with clients, vendors, and milestones.
5. Commit.

---

## Task 8: G-Brain MCP Server

**Files:**
- Create: `gbrain/README.md`
- Create: `gbrain/server.py`
- Create: `gbrain/tools.py`
- Create: `gbrain/.env.example`

**Interfaces:**
- Consumes: G-Brain local PostgreSQL/PGLite, gbrain-local skill.
- Produces: MCP server exposing `gbrain_read_profile`, `gbrain_write_mission`, `gbrain_search_entities`, `gbrain_store_learning`.

**Steps:**
1. Write `server.py` using `mcp.server.fastmcp.FastMCP` with 4 tools.
2. Implement `tools.py` with SQLite/PostgreSQL queries.
3. Add `gbrain` entry to `partenon-core/config/mcp/servers.yaml`.
4. Test with `python -m py_compile gbrain/*.py`.
5. Commit.

---

## Task 9: Onboarding General + Task Generator

**Files:**
- Create: `partenon-core/tools/onboarding_flow.py`
- Create: `partenon-core/templates/onboarding_questions.md`
- Create: `partenon-core/data/initial_tasks.json`
- Modify: `partenon-core/tools/onboarding_engine.py`

**Interfaces:**
- Consumes: `partenon-core` router, 6 profile templates.
- Produces: `run_onboarding()` returns list of missions and creates kanban tasks.

**Steps:**
1. Define onboarding questions (company type, industry, size, contact, branding).
2. Write `onboarding_flow.py` that asks questions, creates `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations` from examples, and generates initial missions.
3. Populate `initial_tasks.json` with 6 default missions (one per hero).
4. Hook into `onboarding_engine.py`.
5. Commit.

---

## Task 10: Kanban + Cron Dashboard

**Files:**
- Create: `dashboard/README.md`
- Create: `dashboard/package.json`
- Create: `dashboard/src/app/page.tsx`
- Create: `dashboard/src/app/kanban/page.tsx`
- Create: `dashboard/src/app/cron/page.tsx`
- Create: `dashboard/src/lib/data.ts`
- Create: `dashboard/src/components/KanbanBoard.tsx`
- Create: `dashboard/src/components/CronManager.tsx`
- Create: `dashboard/src/components/ProfileSwitcher.tsx`

**Interfaces:**
- Consumes: dashboard-completo components, HBOS kanban data model.
- Produces: Next.js dashboard with kanban and cron views.

**Steps:**
1. Copy `dashboard-completo/src/lib/env.ts` → `dashboard/src/lib/env.ts` with 6 Partenon profiles.
2. Copy `dashboard-completo/src/components/TopNav.tsx` → `ProfileSwitcher.tsx`.
3. Copy `dashboard-completo/src/components/CronManager.tsx`.
4. Build `KanbanBoard.tsx` with columns: ideas → backlog → to_do → in_progress → review → done.
5. Read `Hermes Bussines OS/dashboard/lib/data.ts` for data model.
6. Write `data.ts` to read/write `data/tasks.json`.
7. Run `npm install` and `npm run build`.
8. Commit.

---

## Task 11: Google Sheet Base + Demo Tesorero

**Files:**
- Create: `templates/google-sheet-base/README.md`
- Create: `templates/google-sheet-base/finance_sheet.py`
- Create: `templates/google-sheet-base/dashboard_sheet.py`
- Create: `scripts/demo_tesorero.py`
- Create: `data/sample_gastos.xlsx`

**Interfaces:**
- Consumes: Excel Agent parsers, Tesorero profile, Google Workspace API.
- Produces: A runnable demo that ingests sample expenses and writes a categorized Google Sheet.

**Steps:**
1. Build `finance_sheet.py` with openpyxl tabs: Income, Fixed Expenses, Variable Expenses, Dashboard, Suppliers.
2. Build `dashboard_sheet.py` with KPIs simples.
3. Write `demo_tesorero.py` that reads `data/sample_gastos.xlsx`, parses rows, categorizes with rules, and writes the Sheet.
4. Create `data/sample_gastos.xlsx` with 20 rows of sample expenses for a cafeteria.
5. Run `python scripts/demo_tesorero.py` locally (dry-run mode if no credentials).
6. Commit.

---

## Task 12: Marketing Page Update

**Files:**
- Modify: `web/index.html`
- Create: `web/assets/demo-tesorero.png`

**Interfaces:**
- Consumes: new system architecture, demo output, transcripción de usuario.
- Produces: updated marketing page with onboarding story and real demo section.

**Steps:**
1. Rewrite hero to focus on "install an operations team in your Google Workspace".
2. Add section: "Onboarding in 20 minutes" with 4 steps.
3. Add section: "Demo: Tesorero organiza gastos de una cafetería" with screenshot.
4. Update 6 hero cards to reference real profiles/SOUL.md.
5. Update impact metrics with concrete sources from HBOS research paper.
6. Verify no banned fonts/emojis.
7. Run Playwright screenshot at 1440px and 390px.
8. Commit.

---

## Task 13: Technical Page Update

**Files:**
- Modify: `web/developers.html`

**Interfaces:**
- Consumes: real repository structure, MCP config, profile distributions.
- Produces: updated technical page with real architecture and installation commands.

**Steps:**
1. Update architecture Mermaid diagram with real components: Hermes CLI, 6 profiles, G-Brain MCP, Google Workspace, Stripe MCP.
2. Add section "Profile distributions" showing `SOUL.md` + `config.yaml` + `skills/`.
3. Add section "Onboarding general" with task generator and kanban/cron.
4. Add section "90-minute technical workshop" with pre-install command.
5. Update install code block to use `install.sh` and real env vars.
6. Add reference to NemoClaw/Nemotron 3 Ultra/Stripe Agent Toolkit/MPP.
7. Verify Mermaid renders and responsive.
8. Run Playwright screenshots.
9. Commit.

---

## Task 14: Final Verification + Cierre

**Files:**
- Modify: `TODOS.md`
- Modify: `PROGRESS.md`
- Modify: `MEMORY.md`
- Modify: `README.md` (final polish)

**Steps:**
1. Run `python -m py_compile` on all Python files.
2. Run `npm run build` in `dashboard/`.
3. Verify `web/index.html` and `web/developers.html` open without console errors.
4. Update `TODOS.md`, `PROGRESS.md`, `MEMORY.md`.
5. Commit.
6. Run `git add -A && git commit -m "feat: assemble Partenon system with 6 Hermes profiles, onboarding, G-Brain MCP, and updated web pages"`.
