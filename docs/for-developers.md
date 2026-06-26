# Partenon for Developers

> Technical documentation to install, extend and contribute to Partenon.

## Repository

- **Website**: [https://hermespartenon.online/](https://hermespartenon.online/)
- **Code**: [https://github.com/cuentadeservicio377-cell/partenon](https://github.com/cuentadeservicio377-cell/partenon)

## Stack

- **Frontend pages**: static HTML + Tailwind CSS CDN + vanilla JS (`web/`)
- **Dashboard**: Next.js 15 + React 19 + TypeScript + Tailwind CSS (`dashboard/`)
- **Agent core**: Hermes Agent (Nous Research) + Python skills + `partenon-core` (`partenon-core/`)
- **Profiles**: seven Hermes Agent distributions (`hermes/profiles/`)
- **Sandbox / orchestration**: NVIDIA NemoClaw + OpenShell (alpha / early preview)
- **Models**: NVIDIA Nemotron 3 Ultra / Super, OpenAI, Kimi / Moonshot
- **Documents**: Python + WeasyPrint (Kami v3)
- **Data**: Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail)
- **Payments**: Stripe API + Hermes Stripe Skills (`stripe-link-cli`, `mpp-agent`, `stripe-projects`)
- **Memory**: G-Brain of Garry Tan via MCP
- **Infrastructure**: Docker / Docker Compose

## Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                         Hermes (company)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │ publishes missions
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      partenon-core                            │
│  onboarding → router → workflow → eval loop (stub) → G-Brain │
└──────────────────────┬──────────────────────────────────────┘
                       │ assigns missions
                       ▼
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│ Scribe  │ Herald  │Collector│ Guardian│Strategist│Diplomat│ Brain   │
│ (finance)│(comms) │(payments│(security│  (ops)   │(relations)│(memory)│
└────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┴────┬────┘
     │         │         │         │         │         │         │
     ▼         ▼         ▼         ▼         ▼         ▼         ▼
Google    Google    Stripe    NVIDIA    Google    Google    G-Brain
Sheets    Docs/     API       NemoClaw  Calendar  Contacts  (MCP)
          Slides                      /Gmail
```

The eval-loop component is currently a stub. It is planned to measure output quality with a judge skill and a configurable threshold.

## Repository structure

```text
partenon/
├── web/                    # Static web pages
│   ├── index.html          # Marketing
│   ├── heroes.html         # Hero profiles
│   └── developers.html     # Technical documentation
├── dashboard/              # Operations dashboard (Next.js)
├── hermes/profiles/        # Hermes Agent profiles
│   ├── partenon-tesorero/
│   ├── partenon-mensajero/
│   ├── partenon-cobrador/
│   ├── partenon-guardian/
│   ├── partenon-estratega/
│   ├── partenon-diplomatico/
│   └── partenon-brain/
├── partenon-core/          # Core skill: onboarding, router, workflow
├── gbrain/                 # Local MCP memory server
├── scripts/                # Utilities and demos
│   ├── demo_tesorero.py
│   └── setup_hermes.py
├── templates/              # Google Sheets templates
├── docs/                   # Documentation
├── install.sh              # Bash installer
├── .env.example            # Environment variables
├── requirements.txt
└── docker-compose.yml
```

## Quick install

### Option A: Bash

```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon
./install.sh
```

### Option B: Python

```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon
python scripts/setup_hermes.py
```

### Environment variables

Copy `.env.example` to `.env` and fill it in:

```bash
cp .env.example .env
```

Required fields to start:

- `OPENROUTER_API_KEY`
- `GOOGLE_SERVICE_ACCOUNT_JSON`
- `STRIPE_SECRET_KEY` (only if you use the Collector)
- `GBRAIN_DATABASE_URL` (only if you use the Brain)

## Technical profiles

Each profile is a Hermes Agent distribution with:

- `SOUL.md` — personality, role, rules and limits.
- `config.yaml` — default model, enabled tools, MCP servers.
- `.env.example` — profile-specific environment variables.
- `skills/<skill>/SKILL.md` — skill documentation.
- `skills/<skill>/tools/*.py` — Python tools.
- `cron/*.json` — scheduled tasks.
- `templates/` — configuration templates.

### Models

| Profile | Default | Fallback |
|---------|---------|----------|
| Scribe | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Herald | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Collector | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Guardian | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Strategist | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Diplomat | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |
| Brain | `openrouter/anthropic/claude-opus-4` | `openrouter/anthropic/claude-sonnet-4` |

### MCP servers

- `google_workspace`: access to Sheets, Docs, Slides, Calendar, Gmail.
- `gbrain`: persistent memory MCP server.
- `stripe`: payment operations (via Hermes Stripe Skills).

## Demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/demo_tesorero.py
```

This generates:

- `data/sample_gastos.xlsx`
- `data/sample_gastos_report.json`

## Dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:3000. Default credentials: `admin` / `partenon`.

## Production build

```bash
cd dashboard
npm run build
```

## Docker

```bash
docker-compose up --build
```

## API reference

### Hermes CLI

```bash
hermes profile use partenon-tesorero
hermes profile use partenon-mensajero
hermes run "Record a $500 advertising expense"
```

### G-Brain MCP

Methods exposed by the `gbrain` MCP server:

| Method | Description |
|--------|-------------|
| `gbrain_read_profile` | Read a profile memory scope. |
| `gbrain_write_profile` | Write a profile memory scope. |
| `gbrain_write_mission` | Register or update a mission. |
| `gbrain_search_missions` | Search missions by profile and/or status. |
| `gbrain_search_entities` | Search entities by name and optional kind. |
| `gbrain_store_learning` | Store a learning insight for a profile. |

## 90-minute workshop

1. **Pre-installation** (15 min): Python, Node.js, Google Workspace and Stripe accounts.
2. **Setup** (20 min): `git clone`, `./install.sh`, configure `.env`.
3. **Practice** (40 min): Scribe, Herald and Collector demos.
4. **Q&A and roadmap** (15 min).

## Contributing

1. Fork the repository.
2. Create a branch: `git checkout -b feat/feature-name`.
3. Commit with a descriptive message.
4. Open a PR with evidence of tests/build.

## Roadmap

- [ ] Functional eval loop in all profiles.
- [ ] Live integrations for Google Workspace, Stripe and G-Brain.
- [ ] End-to-end validation with 10 pilot companies.
- [ ] Marketplace of specialized profiles.

## Known gaps

- The eval-loop stub in `partenon-core` is not yet implemented.
- The `GBRAIN_DATABASE_URL` variable name in `.env.example` does not match the `GBrain_DATABASE_URL` default used by `gbrain/server.py` and `partenon-core/config/mcp/servers.yaml`. Use the exact name required by the component you run.
- NVIDIA NemoClaw / OpenShell onboarding is alpha; follow NVIDIA's current instructions.
- Live Google Workspace, Stripe and G-Brain flows require real credentials and are not enabled by default.
