# Partenon

[![Site](https://img.shields.io/badge/live-hermespartenon.online-00D4FF)](https://hermespartenon.online/)
[![GitHub](https://img.shields.io/badge/repo-github.com%2Fpartenon-181717?logo=github)](https://github.com/cuentadeservicio377-cell/partenon)

> An AI agent operating system for small businesses, presented as a pantheon of heroes serving Hermes. Built for the Nous Research / NVIDIA / Stripe hackathon.
>
> 🌐 **Live site**: [https://hermespartenon.online/](https://hermespartenon.online/)
> 📦 **Repository**: [https://github.com/cuentadeservicio377-cell/partenon](https://github.com/cuentadeservicio377-cell/partenon)

## What is Partenon

Partenon organizes AI agents as an operating system for your business:

- **Hermes** = the company (not a CEO, not a chatbot). The "god" that publishes missions because it needs help.
- **The heroes** = seven specialized agents that take missions from The Partenon.
- **The Partenon** = Hermes + his heroes working together.
- **Pegasus** = each hero's toolkit: skills, MCPs, APIs, and open-source platforms.
- **G-Brain of Garry Tan** = the brain that connects everything through MCP.
- **Google Workspace** = the shared surface where the company and agents work.

## Documentation

- [`docs/for-founders.md`](docs/for-founders.md) — Guide for entrepreneurs: what Partenon is, the 7 heroes, examples, and growth plan.
- [`docs/for-developers.md`](docs/for-developers.md) — Complete technical guide: stack, architecture, installation, API, and workshop.
- [`docs/architecture.md`](docs/architecture.md) — Overview of the system architecture and mission flow.

## The three master pages

The system documentation lives in three static web pages migrated from the React app `Kimi_Agent_10 Storytelling Web Sites/app`.

1. **`web/index.html`** — Marketing page. Two-panel hero gateway, the myth of archetypes, the 7 heroes, a 4-step process, impact counters with milestone bar, growth plan, and CTA.
2. **`web/heroes.html`** — Hero detail page. Full profiles, capabilities, tools, comparison matrix, and interconnected workflow.
3. **`web/developers.html`** — Technical documentation. Architecture, hero specifications, MCP protocol, data-flow patterns, installation workshop, install instructions, and CLI/API reference.
4. **`dashboard/`** — Operations dashboard (Next.js 15 + React 19 + TypeScript + Tailwind CSS). Shows KPIs, a mission kanban filtered by profile, a cron job manager, and simple cookie auth. Reads and writes `data/tasks.json` and `data/cron.json`.

The web pages use static HTML, Tailwind CSS via CDN, Google Fonts (Cinzel, Inter, JetBrains Mono), and vanilla JavaScript. The palette comes from the original app: marble `#F7F5F0`, parchment `#EDE8DF`, deep-stone `#2A2A2E`, midnight `#1A1A1E`, and hero-specific accents.

## The 7 heroes

| Hero | Role | Description |
|------|------|-------------|
| The Scribe | Finance | Spreadsheets, financial models, dashboards, and analysis. |
| The Herald | Communication / Marketing | Brand voice, content, social media, SEO/GEO, calendar. |
| The Collector | Payments / Stripe | Collections, subscriptions, invoices, expense tracking. |
| The Guardian | Security / NVIDIA | API keys, policies, sandbox, model routing, audit. |
| The Strategist | Operations / PM | Calendar, tasks, reminders, briefings, cron. |
| The Diplomat | Relations | Clients, vendors, contracts, follow-ups. |
| The Brain | Intelligence | G-Brain, collective memory, knowledge orchestration. |

## How it works

1. **Hermes asks**: what business is this? What needs to be organized?
2. **Hermes breaks it into missions**: converts intent into tasks posted in The Partenon.
3. **The hero takes the mission**: reads their profile, consults G-Brain, and starts working with the entrepreneur.
4. **Delivery in Google Workspace**: the result lives in Sheets, Docs, Slides, or Calendar where everyone can see it.

## Stack

- **Frontend pages**: static HTML + Tailwind CSS CDN + vanilla JS
- **Agent core**: Hermes Agent (Nous Research) + Python skills + `partenon-core` (router, onboarding, workflow, eval loop stubs)
- **Sandbox / orchestration**: NVIDIA NemoClaw + OpenShell (alpha / early preview)
- **Models**: NVIDIA Nemotron 3 Ultra / Super, OpenAI, Kimi / Moonshot
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind (in `dashboard/`)
- **Documents**: Python + WeasyPrint (Kami v3)
- **Data**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail); Excel templates with openpyxl
- **Payments**: Stripe API + Hermes Stripe Skills (`stripe-link-cli`, `mpp-agent`, `stripe-projects`)
- **Memory / orchestration**: G-Brain of Garry Tan via MCP, Hermes `MEMORY.md`/`USER.md`
- **Messaging**: Hermes messaging gateway: Telegram, WhatsApp, Slack, Discord, Email, and many more platforms
- **Infrastructure**: Docker / Docker Compose

## Functional demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/demo_tesorero.py
```

This creates:

- `data/sample_expenses.xlsx` — workbook with Dashboard, Income, Fixed Expenses, Variable Expenses, and Vendors sheets.
- `data/sample_expenses_report.json` — income, fixed expenses, variable expenses, margin, and alerts.

## Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:3000 and log in with username `admin` and password `partenon` (configurable via `DASHBOARD_APP_USERNAME` and `DASHBOARD_APP_PASSWORD`). Reads and writes `data/tasks.json` and `data/cron.json` relative to the project root.

## Status

- Started: 2026-06-23
- **Public repository**: [github.com/cuentadeservicio377-cell/partenon](https://github.com/cuentadeservicio377-cell/partenon)
- **Deployed site**: [https://hermespartenon.online/](https://hermespartenon.online/)
- Current phase: Public repository created with 7 Hermes profiles, complete documentation, and install scripts.
- Implemented profiles: Scribe (`.finance`), Herald (`.design`), Collector (`.payments`), Guardian (`.security`), Strategist (`.ops`), Diplomat (`.relations`), Brain (`.brain`).
- Web verified: `web/index.html`, `web/heroes.html`, and `web/developers.html` on desktop (1440px) and mobile (390px). Screenshots updated in `screenshots/`. HTML validated.
- Dashboard verified: `npm install` and `npm run build` pass without TypeScript errors.
- Demo verified: `python scripts/demo_tesorero.py` generates Excel + JSON with metrics.
- Known gaps: the eval-loop stub in `partenon-core` is not yet functional; live Google Workspace, Stripe and G-Brain integrations require real credentials; the `GBRAIN_DATABASE_URL` variable name in `.env.example` does not match the `GBrain_DATABASE_URL` default used by `gbrain/server.py` and `partenon-core/config/mcp/servers.yaml`.
- Next: implement a functional eval loop in the Scribe, test Stripe Skills in sandbox, and configure NVIDIA NemoClaw onboarding.

## Quick install

```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon

# Option A: bash installer
./install.sh

# Option B: Python setup helper
python scripts/setup_hermes.py
```

> **Note:** The installer prepares the local Python environment, copies profile templates and creates `.env`. Hermes Agent CLI must be installed separately; see the official Nous Research instructions. NVIDIA NemoClaw / OpenShell onboarding is alpha; follow NVIDIA's current instructions instead of any hard-coded command.

Then:
1. Copy `.env.example` to `.env` and fill in your credentials.
2. Review the base Google Sheet generator in `templates/google-sheet-base/`.
3. Run `python scripts/demo_tesorero.py` to verify the install.
4. Open the dashboard: `cd dashboard && npm install && npm run dev`.

## Environment variables

Copy `.env.example` to `.env` and set at least:

- `OPENROUTER_API_KEY` — default LLM router
- `GOOGLE_SERVICE_ACCOUNT_JSON` — path to Google Cloud service account JSON
- `STRIPE_SECRET_KEY` — only if you use the Collector
- `GBRAIN_DATABASE_URL` — only if you use the Brain

> Note: `gbrain/server.py` and `partenon-core/config/mcp/servers.yaml` read `GBrain_DATABASE_URL` by default. Set the exact variable name required by the component you run.

## Related repositories

- [Hermes Agent](https://hermes-agent.nousresearch.com/)
- [NVIDIA NemoClaw](https://www.nvidia.com/en-us/ai/nemoclaw/)
- [NVIDIA OpenShell](https://github.com/NVIDIA/openshell)
- [Stripe Agent Toolkit](https://github.com/stripe/ai)
- [Open Design](https://github.com/nexu-io/open-design)
- [G-Brain](https://github.com/garrytan/gbrain)

## Project memory

See [`.kimi-code/memory/`](.kimi-code/memory/)
