# Project Memory: Partenon

> Last session: 2026-06-27T00:36Z

## Current Context

- **Project**: Partenon
- **Started**: 2026-06-23
- **Status**: Public GitHub repository translated to English. README rewritten from scratch and a full documentation package created: entrepreneur playbook, hero guide, quickstart, security, API, FAQ, and visual assets. A complete workshop package was added with five real company cards, five simulated onboardings, a Hermes onboarding guide, agendas, slides, handout, and a production-readiness checklist. All docs and simulations are grounded in actual code, in English, and cross-linked. Remaining gaps are tracked in `MISSING_IMPLEMENTATION.md`.
- **Live site**: `https://hermespartenon.online/`
- **Repo**: `https://github.com/cuentadeservicio377-cell/partenon`
- **Profiles**: Scribe/Treasurer, Herald/Messenger, Collector, Guardian, Strategist, Diplomat, Brain.
- **Verified**: `python3 scripts/demo_tesorero.py` PASS, `cd dashboard && npm run build` PASS, `python3 -m unittest discover tests` PASS (4 tests), `bash -n install.sh` PASS, `python3 -m py_compile` on all profile tools PASS, `python3 workshop/simulations/sim_runner.py` actions PASS, Brain `GBrainClient().put_page` PASS after stdin fix.
- **Next**: implement real intent router and workflow engine runtime, add publishing/dispatch integrations for Messenger/Collector/Diplomat, build end-to-end bank/CSV-to-Sheets flow for Scribe, add Shopify/order import and inventory tracking for retail, add AWS cost import and churn-signal worksheet for SaaS, bundle or replace external `gbrain` binary with a local fallback, and add a public support channel/issue template.

## Braindump

### 1. What is this project?

Partenon is an AI agent system organized as a pantheon of heroes that work for a "god" named Hermes. Hermes represents the company/entrepreneur. The heroes are specialized agents that execute missions (tasks) to improve, organize and grow the company.

The brand narrative uses archetypes (not mythology cosplay) to give personality to each profile. Tone should be marketing storytelling, not forced or geeky.

### 2. Who uses it?

- **Entrepreneurs and small businesses** that need to organize operations, finance, sales, communication, collections, security and administration.
- **Hackathon judges** from Nous Research, Nvidia and Stripe.
- **Developers** who want to understand the architecture and install the system.
- **Universities, accelerators, chambers of commerce, coworking spaces and business organizations** (BNI, Way Pío, Rotary, etc.) for workshops and events.

### 3. What technology stack do you prefer?

**Confirmed for web pages:**
- **Web pages**: static HTML + Tailwind CSS + vanilla JavaScript. Hosted on GitHub Pages.
- **Aesthetic**: Based on the React app `Kimi_Agent_10 Storytelling Web Sites/app`: white marble `#F7F5F0`, parchment `#EDE8DF`, deep-stone `#2A2A2E`, midnight `#1A1A1E`, Cinzel + Inter + JetBrains Mono fonts.

**System stack (based on analyzed repositories):**
- **Agent Core**: Hermes Agent (Nous Research) — Python
- **Sandbox / Orchestration**: NVIDIA NemoClaw + OpenShell
- **Models**: NVIDIA Nemotron 3 Ultra / Super, OpenAI, Kimi / Moonshot
- **Native skills**: Hermes Business OS (HBOS) — 6 base skills
- **Payments**: Stripe API + Stripe Skills (`stripe-link-cli`, `mpp-agent`, `stripe-projects`)
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Document Engine**: Python + WeasyPrint (Kami v3)
- **Data**: Google Sheets (master data) + local JSON
- **Communication**: Hermes messaging gateway (Telegram, WhatsApp, Slack, Discord, Email, LINE, etc.)
- **Integrations**: Google Workspace, Stripe, G-Brain via MCP
- **Infrastructure**: Docker / Docker Compose, optional AWS EC2

### 4. Is there a deadline or priority?

- **Priority 1**: Build the three web pages for the hackathon (marketing, heroes, technical).
- **Priority 2**: Define technical architecture and create the system repository.
- **Deadline**: hackathon (exact date to be confirmed).

### 5. What is already built?

- Initial Partenon project structure created by braindump-init.
- **Hermes Business OS (HBOS)** already exists with 6 base skills:
  - `hermes-business-core` — config, routing, Google Workspace, onboarding
  - `hermes-ventas` — CRM, quotes, pipeline
  - `hermes-operaciones` — projects, tasks, logistics
  - `hermes-finanzas` — budgets, payments, reports
  - `hermes-rrhh` — teams, attendance, payroll
  - `hermes-documentos` — PDF/Docs/Slides generation
- **OpenWork Paola Meneses** is an operational adaptation with OpenWork + OpenCode + React + FastAPI + Google Workspace + AWS.
- **Agente Marketing Kimi** has Campaign Manager, parallel subagents, GBrain, Control Center in Sheets and deliverables in Drive.
- **Open Design** is a design tool with agents (31 skills, 129 design systems). Possible visual reference.
- **Hermes Bible** (hermesbible.com) is unofficial Hermes Agent documentation.
- **HBOS Research Paper** already written and published in the repo.

### 6. Important constraints?

- Must work with free Google Workspace if possible.
- Must feel like a Nous Research / Nous Research subproduct (aesthetic to copy).
- Must not feel cheesy or forced with the Greek theme; use marketing archetypes.
- Must have three clearly differentiated web pages: marketing (`index.html`), heroes (`heroes.html`) and technical (`developers.html`).
- Business owners must be able to work in tools they know (Google Workspace), not just MD files in an agent workspace.
- Pages first, system second.

### 7. What would make it a success?

- Have three impactful web pages for the hackathon.
- Impact counter: 10 → 100 → 1,000 → 10,000 → 100,000 → 1,000,000 people/companies helped.
- Generate biweekly installation webinars.
- Events at universities, accelerators, chambers of commerce, coworking spaces.
- Make Hermes the customized agent for accelerators, backed by Stripe, Nvidia and Nous Research.
- Make 10 pilot companies improve revenue, quality, financial order and save hours.

## Brand Concept

- **Hermes** = the company (not just the CEO). The god that needs help.
- **The Partenon** = the whole: Hermes + its heroes.
- **Heroes** = specialized agents that take missions from the Partenon.
- **Hero tools** = skills, MCPs, APIs and open-source platforms.

## Hero Profiles (agents)

Profiles map directly to existing or proposed HBOS skills:

1. **Finance / Sheets Hero** (`hermes-finanzas`)
   - Expert in Google Sheets, dashboards, fixed/variable costs, financial analysis.
   - Creates `.finance` file per company.
   - Works with the entrepreneur to organize numbers.

2. **Communication / Sales / Marketing Hero** (`hermes-ventas` + marketing)
   - Expert in social media, brand, storytelling, growth.
   - Access to company `.design` file.
   - Creates campaigns, content calendars, SEO, presentations, emails.
   - Connects to Sheets for budgets and data.

3. **Collections / Stripe Hero**
   - Expert in Stripe and payments.
   - Connects to online stores, services and physical products.
   - Handles subscriptions, payments, reminders.

4. **Security / Models Hero**
   - Manages API keys, AI models, accounts (Nvidia, OpenAI, Kimi Code, etc.).
   - Manages permissions, security and service access.

5. **Administration / Operations Hero** (`hermes-operaciones`)
   - Operational manager, project manager.
   - Access to Google Calendar, email, reminders, customer/operation details.
   - Allocates resources and helps coordinate the other heroes.

6. **Relations Hero (Customers and Vendors)**
   - Manages external relationships.
   - Coordinates between customer and operations to reach middle ground.
   - Reminders, milestones, pending information.

7. **Documents Hero** (`hermes-documentos`)
   - Generates contracts, quotes, proposals, presentations.
   - Kami v3 engine (WeasyPrint) + Google Docs/Slides.

## Key Integrations

- Google Workspace (Sheets, Drive, Docs, Slides, Calendar, Gmail)
- Stripe + Stripe Skills (`stripe-link-cli`, `mpp-agent`, `stripe-projects`)
- NVIDIA NemoClaw + OpenShell + Nemotron 3 Ultra / Super
- G-Brain of Garry Tan (central brain via MCP)
- Hermes Agent (Nous Research)
- MCPs for each hero
- Hermes messaging gateway (Telegram, WhatsApp, Slack, Discord, Email, LINE, etc.)
- Nous Research / NVIDIA / Stripe (backing and judging)

## Company File Structure

- `.finance` → financial data and dashboards
- `.design` → identity, brand and communication strategy
- `.payments` → Stripe and payment configuration
- `.security` → API keys, models and permissions
- `.ops` → operations, calendar, tasks
- `.relations` → customers, vendors, milestones
- `client.yaml` → company configuration
- Additional files as needed by each hero

## Go-to-Market Strategy

- Website with impact counter (10, 100, 1K, 10K, 100K, 1M).
- Biweekly installation webinars.
- Events at universities and accelerators.
- Workshops at chambers of commerce, BNI, Rotary, coworking spaces.
- Alliance with accelerators so Hermes becomes their customized agent.

## Analyzed Repositories

| Repo | What it is | Reusable for Partenon |
|------|------------|------------------------|
| hermes-business-os | Business skills distribution for Hermes Agent | Base system, skills, architecture, paper |
| paola-meneses-openwork | OpenWork adapted for events (Paola Meneses) | Google Workspace patterns, templates, MCPs |
| openwork-paola | Simpler version of the above | Same case |
| agente-marketing-kimi | Marketing system with Campaign Manager | Subagent patterns, GBrain, Control Center |
| open-design / open-design-migration | Design tool with agents | Design systems, visual reference, landing skills |
| hermesbible.com | Unofficial Hermes Agent docs | Hermes Agent context |

## Architectural Decisions

- The three web pages are built first, before the system.
- `web/index.html` (marketing) explains the concept, benefits, profiles and go-to-market.
- `web/heroes.html` (heroes) details the 7 profiles, capabilities, tools, connections and collaboration workflow.
- `web/developers.html` (technical) explains architecture, MCPs, diagrams and workshop process.
- The system will be built based on the pages.
- Google Workspace as shared working surface with the entrepreneur.
- HBOS as existing technical base; Partenon is the presentation and profile-extension layer.
- Public GitHub repository: `https://github.com/cuentadeservicio377-cell/partenon`.
- `partenon-brain` profile added as seventh hero for collective memory via G-Brain.
- `partenon-brain` exposes MCP tools (`share_context`, `find_patterns`, `orchestrate_agents`, `register_agent`, `generate_insight`) and daily sync tools (`collect_learnings`, `collect_decisions`, `index_in_gbrain`, `notify`) to match `web/heroes.html` and `web/developers.html`.
- `partenon-diplomatico` profile translated to English, restructured `config.yaml`, expanded `.env.example`, and aligned with `web/heroes.html` / `web/developers.html` promises.
- `partenon-diplomatico` exposes MCP-aligned tools: `sync_contacts`, `schedule_meeting`, `log_interaction`, `auto_followup`, `generate_proposal`.
- `partenon-cobrador` exposes MCP-aligned tools: `create_payment_link`, `create_subscription`, `create_invoice`, `list_charges`, `monitor_fraud`, `send_payment_reminder`, `record_payment`, `generate_income_report`, `read_pending_payments`, `read_overdue_payments`, `classify_risk`, `schedule_followup`, `notify`, `get_upcoming_payments`, `get_failed_subscriptions`.
- Global `.env.example` with safe placeholders to avoid GitHub secret scanning.
- `install.sh` and `scripts/setup_hermes.py` for local environment setup; they do not download unverified binaries and provide clear instructions when Hermes CLI is missing.
- `partenon-core/tools/eval_loop.py` added as a lightweight QA stub for hero mission outputs.
- `partenon-core/tools/config_loader.py` added so the onboarding engine can run without external HBOS dependencies.
- All scripts/core/install files translated to English.
- Repo documentation decoupled from web pages: `docs/for-founders.md`, `docs/for-developers.md`, `docs/architecture.md`.
- Hackathon stack explicit on the three pages: Hermes Agent + NVIDIA NemoClaw/OpenShell/Nemotron 3 Ultra + Stripe Skills.
- Nous Research / open-source manual aesthetic: background `#050505`, cyan accent `#00D4FF`, monospace hero font, no emojis or em-dashes.
- Anti-AI-slop copy: concrete verbs, claim + proof, no intensifiers or dramatic transition phrases.

## APIs / Integrations

- Google Workspace APIs
- Stripe API + Stripe Skills
- NVIDIA NemoClaw / OpenShell / Nemotron
- G-Brain (MCP)
- Hermes Agent APIs
- MCPs for each tool/skill

## Known Gotchas

- The mythological tone must be subtle; avoid cheesiness.
- Pages must impress technical judges (Nvidia, Stripe, Nous Research).
- It must be clear that Hermes = company, not just CEO.
- The system must deliver value in tools the entrepreneur already knows (Google Workspace).
- open-design is very large (331MB); used as reference, not dependency.
- Some private repos require gh CLI to access.

## Useful Links

- Hermes Bible: https://www.hermesbible.com/
- Hermes Business OS: https://github.com/cuentadeservicio377-cell/hermes-business-os
- Research Paper (EN): https://github.com/cuentadeservicio377-cell/hermes-business-os/blob/main/docs/RESEARCH-PAPER.en.md
- Open Design: https://github.com/cuentadeservicio377-cell/open-design
- OpenWork Paola: https://github.com/cuentadeservicio377-cell/paola-meneses-openwork
- Agente Marketing Kimi: https://github.com/cuentadeservicio377-cell/agente-marketing-kimi
