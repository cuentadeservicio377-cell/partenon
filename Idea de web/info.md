# Hermes Parthenon — Research Brief

## Project Context
Hackathon submission website for "The Hermes Agent Accelerated Business Hackathon" by Nous Research x NVIDIA x Stripe. Deadline: June 30, 2026. Prizes: $10K + NVIDIA DGX Spark + $5K Stripe Credits for 1st place.

## TWO Pages Required
1. **Page A — The Story (Marketing)**: Narrative-driven, mythological branding, impact metrics, outreach strategy. For judges AND entrepreneurs who want to install Hermes.
2. **Page B — The Architecture (Technical)**: Technical deep-dive, diagrams, MCP architecture, hero specs, repository. For developers who want to understand/build.

---

## BRAND IDENTITY: Hermes Parthenon

### Core Concept
Hermes IS the Company. The Parthenon is where all Heroes gather. Heroes (AI Agents) take missions (tasks) posted by Hermes. Each hero has tools (Pegasus = their tech stack).

### Mythology → Branding (Subtle, NOT cheesy)
Use archetypal marketing — the mythology is scaffolding for personality, not decorative overlay. Emphasize VALUES (speed, mediation, intelligence) not references.

### Hermes as "The Enterprise"
- Only god who moved freely between all worlds (Olympus, earth, underworld) → connects all departments
- Attributes: Caduceus (mediation), Winged Sandals (speed/agility), Purse (commerce/finance)
- Archetype: The Magician + The Communicator — transformer and mediator
- Values: velocity, connection, intelligence, mediation, adaptability

### The 6 Heroes (Agents)

| Hero | Greek Name | Business Role | Archetype | Tools |
|------|-----------|---------------|-----------|-------|
| **The Keeper** | Plutus (god of wealth) | Finance & Accounting | The Ruler + The Sage | Google Sheets, Excel, Financial dashboards, .finance files |
| **The Herald** | Apollo (god of light & arts) | Communication & Marketing | The Creator + The Sage | Social media APIs, .design files, SEO tools, content calendar |
| **The Scale** | Themis (goddess of divine law) | Payments & Collections | The Ruler + The Caregiver | Stripe Skills (stripe-link-cli, mpp-agent, stripe-projects) |
| **The Forge** | Hephaestus (god of fire & craft) | Security & Technology | The Creator + The Magician | NemoClaw, Nemotron 3 Ultra, NVIDIA Agent Skills |
| **The Mind** | Athena (goddess of wisdom) | Operations & Admin | The Sage + The Ruler | Google Calendar, Gmail, Project Management, .ops files |
| **The Twins** | Janus-like duality | Client Relations (external) + Team Coordination (internal) | The Caregiver + The Explorer | CRM, communication channels, status tracking |

### G-Brain (Garitan's Brain)
- Central MCP connector that links ALL agents to Hermes
- Uses Model Context Protocol to connect agents with tools
- Shared memory, state management, inter-agent communication

---

## VISUAL DESIGN DIRECTION

### Nous Research Aesthetic (Primary Reference)
**"Academic Cyberpunk meets Classical Mythology"**
- Raw, authentic, nerd-culture — NOT corporate
- **Home page palette**: White + teal/cyan dark (`#006B8F`)
- **Product page palette**: Electric blue (`#0000EE`) + white text — BOLD, immersive
- **Typography**: Courier Pro Bold/Regular (monospace) for body, elegant serif for hero headlines
- **UI elements**: Dashed separators, metadata blocks ("OUTPUT 96 / SEED: 3573860127" style), classical engravings, terminal-style code blocks
- **Zero animation fluff** — deliberately anti-effects
- **Tono de voz**: "A bunch of nerds making progress toward open source AI" — casual, authentic, anti-corporate, community-first

### For Hermes Parthenon
- Electric blue hero section with serif headline ("THE ARCHITECTURE THAT REASONS WITH YOU")
- Classical columns/Parthenon silhouette as allegory (subtle, not literal)
- Terminal-style code blocks for installation commands
- Clean transition from story → technical details
- Impact counter with animated numbers

---

## IMPACT COUNTER DATA (10 → 1M users)

### Key Metrics per User
| Metric | Value | Source |
|--------|-------|--------|
| Hours saved/employee/day | 2.5 hrs | Salesforce 2025 |
| Hours saved/week admin tasks | 23 hrs | Intuit QuickBooks 2024 |
| Cost reduction | 25% | McKinsey/Accenture |
| Revenue increase (SMBs with AI) | 91% report more revenue | Salesforce 2025 |
| Productivity improvement | 66% | Deloitte 2024 |
| Annual savings per employee | $14,000 | IBM Institute |
| Automatable tasks | 40% | McKinsey |

### Scalable Projections (Annual)
| Businesses | Hours Saved | Economic Impact |
|-----------|-------------|-----------------|
| 10 | 31,250 hrs | $1.49M USD |
| 100 | 312,500 hrs | $14.9M USD |
| 1,000 | 3.1M hrs | $149M USD |
| 10,000 | 31.2M hrs | $1.49B USD |
| 100,000 | 312.5M hrs | $14.9B USD |
| 1,000,000 | 3.1B hrs | $149B USD |

### By Industry
- **Restaurants**: 79% use AI, 40% less time on orders, 21.5 hrs/month saved on calls
- **Construction**: 15-25% less cost overruns, 30% fewer delays, 5 hrs/week freed per PM
- **E-commerce**: 10-12% revenue increase, +23% conversions, 35% better forecasting

---

## TECHNICAL ARCHITECTURE

### NVIDIA Integrations
1. **NemoClaw**: Open-source blueprint — agent security sandbox with OpenShell runtime, 4-layer defense (filesystem, network, process, inference), Privacy Router for sensitive data
2. **Nemotron 3 Ultra**: 550B params (55B active), 1M context, LatentMoE architecture, 5x throughput, 30% cost reduction on agent tasks, 91% on PinchBench
3. **NVIDIA Agent Skills**: Portable verified instructions, 6 categories (optimization, RAG/agents, inference, training, data/science, vision/video), install via `npx skills add nvidia/skills`

### Stripe Integrations
1. **stripe-link-cli**: Web purchases with single-use virtual cards (US only)
2. **mpp-agent**: Programmatic payments to HTTP 402 APIs (machine-to-machine payments)
3. **stripe-projects**: SaaS provisioning (49+ providers — DBs, hosting, phone)
4. **Stripe Agent Toolkit**: Python/TypeScript SDK with function calling
5. **Machine Payments Protocol (MPP)**: Open protocol co-authored by Stripe + Tempo

### MCP Architecture
- **Protocol**: JSON-RPC over HTTP or STDIO (Anthropic → Linux Foundation)
- **Components**: Host (AI app), Client (1:1 with server), Server (tool provider), Transport layer
- **Pattern for Hermes**: Hub-and-Spoke — Hermes (central) ↔ G-Brain (MCP hub) ↔ Heroes (agents) ↔ MCP Servers (tools)
- **Google Workspace MCP**: Sheets, Calendar, Drive, Docs, Gmail (12 services, 100+ tools)
- **Stripe MCP**: Payments, subscriptions, invoicing, provisioning

### Repository Structure (for technical page)
```
hermes-parthenon/
├── .finance/           # Business financial templates
├── .design/            # Brand identity & communication guides
├── .ops/               # Operations & procedures
├── heroes/
│   ├── keeper/         # Finance agent (Plutus)
│   ├── herald/         # Marketing agent (Apollo)
│   ├── scale/          # Payments agent (Themis)
│   ├── forge/          # Security agent (Hephaestus)
│   ├── mind/           # Operations agent (Athena)
│   └── twins/          # Relations agent (Janus)
├── g-brain/            # Central MCP connector
├── skills/
│   ├── nvidia/         # NVIDIA Agent Skills
│   ├── stripe/         # Stripe Skills for Hermes
│   └── google/         # Google Workspace integrations
└── docs/
```

---

## OUTREACH STRATEGY (for Page A)
1. **Bi-weekly webinars** — pre-registered global groups, install Hermes for each
2. **University partnerships** — innovation departments, business accelerators, auditoriums
3. **Business organizations** — BNI, Wayp.io, Chambers of Commerce, Rotary Clubs
4. **Coworking spaces** — workshops, member access
5. **Business accelerators** — Hermes as personalized agent for their clients

---

## INSTALLATION
Single command: `npx create-hermes@latest` or similar — instant setup with all heroes, G-Brain, and default configurations.
