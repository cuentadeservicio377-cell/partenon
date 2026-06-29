# Website Phase 7 Design — Align Marketing Copy with Hermes-Native Reality

**Status:** Approved by user on 2026-06-29.
**Scope:** Rewrite `web/index.html`, `web/heroes.html`, and `web/developers.html` to match the actual codebase, clarify the relationship with Hermes, and remove misleading claims.
**Approach:** Surgical rewrite — keep existing visual design system, change copy, structure, and claims.

---

## 1. Design principles

- English copy only. No emojis. No generic AI filler.
- Parthenon is the home for Hermes profiles; heroes are not separate AIs.
- Every capability is tagged as **live**, **connect** (needs credentials), or **roadmap**.
- Keep the existing visual system: Cinzel display, Inter body, marble/parchment palette, asymmetric bento, mobile-first, no massive gradients.
- Do not break existing tests, build, or install scripts.

---

## 2. `web/index.html`

### 2.1 Meta description
- Remove NVIDIA NemoClaw as core technology.
- New focus: *“The Parthenon: a Hermes Agent system for entrepreneurs. Seven profiles handle finance, brand, payments, security, operations, relationships, and memory — all sharing one brain.”*

### 2.2 Foundation / hero copy
- Replace “Archetypes, not algorithms” with a paragraph that frames the Parthenon as the place where Hermes profiles live.
- Key line: *“Every business needs its heroes. The Parthenon is where your Hermes profiles live — seven archetypes that make a single agent system understandable.”*
- Add 1-2 sentences clarifying that heroes are Hermes profiles sharing memory through the Brain.

### 2.3 Seven heroes grid
- Keep the grid and cards.
- Add intro line: *“Seven Hermes profiles. One shared memory. Pick the ensemble your business needs.”*

### 2.4 Process section
Replace the four steps with:
1. **Download the Parthenon** — clone, run `./install.sh`.
2. **Configure your Heroes Ensemble** — connect the skills you need (Google Workspace, Stripe, Slack).
3. **Missions in motion** — each hero picks up its mission from intent, commands, or the dashboard.
4. **The Parthenon drives** — the Brain keeps context, follow-ups, and handoffs across profiles.

Remove claims that payments flow automatically or that the Brain continuously optimizes everything.

### 2.5 Counter
- Change `10 → 1M` to `1 → 1M`.

### 2.6 Partners / trust
- Remove “Powered by NVIDIA”.
- Keep honest hackathon footer: *“Built for the Nous Research × NVIDIA × Stripe Hackathon.”*
- Badges:
  - “MCP Ready” — live.
  - “Google Workspace Connectable” — needs credentials.
  - “Stripe Connectable” — needs credentials.

### 2.7 CTA
- Button copy: *“Install the Parthenon”*.
- Command: `git clone https://github.com/.../partenon && cd partenon && ./install.sh`.
- Note: *“Requires the Hermes Agent CLI by Nous Research.”*

---

## 3. `web/heroes.html`

### 3.1 Lead
- *“Each hero is a Hermes profile. Install the ones you need; they share memory through the Brain.”*

### 3.2 Per-hero status tags
Every hero card shows three small tags:
- `live` — works without credentials (dry-run / local).
- `connect` — requires API key / service account.
- `roadmap` — not implemented yet.

### 3.3 Hero-by-hero capabilities

#### Scribe
- **Live:** parse finance data, classify expenses, build local dashboards.
- **Connect:** Google Sheets / Workspace writes.
- **Roadmap:** Google Drive operations.

#### Herald
- **Live:** copy drafts, content calendar, presentation outlines.
- **Connect:** Google Docs / Slides creation.
- **Roadmap:** Instagram, Twitter, LinkedIn, Mailchimp publishing.

#### Collector
- **Live:** dry-run invoices, subscriptions, revenue reports.
- **Connect:** Stripe secret key.
- **Roadmap:** Stripe Connect.

#### Guardian
- **Live:** key-strength audit, provider detection, policy logging.
- **Connect:** secrets manager (optional).
- **Roadmap:** NVIDIA GPU allocation / NemoClaw integration.

#### Strategist
- **Live:** project / task / checklist planning, local ops.
- **Connect:** Google Calendar, Gmail, Slack bot token.
- **Roadmap:** Notion, Google Tasks PM suite.

#### Diplomat
- **Live:** client / vendor tracking, follow-up drafts.
- **Connect:** Google Workspace, Gmail.
- **Roadmap:** HubSpot / Salesforce CRM sync.

#### Brain
- **Live:** memory pages, profile storage, conflict detection, SQLite / Postgres.
- **Connect:** Postgres for team-scale memory.
- **Roadmap:** advanced cross-agent optimization.

### 3.4 Tool badges
- Remove badges for tools that do not exist (Google Drive, Notion, Security Dashboard, Encryption, MCP Security, etc.) or mark them `roadmap`.

### 3.5 Workflow timeline
- Keep the product-launch example but replace misleading steps:
  - “Live payment processing” → “Stripe-connected payment flow (requires Stripe key).”
  - “CRM updates” → “Relationship tracking (external CRM sync is roadmap).”

---

## 4. `web/developers.html`

### 4.1 Lead
- *“A technical overview for the Nous Research, NVIDIA, and Stripe teams.”*
- Four building blocks: Google Workspace, Hermes Agent, NVIDIA Cloud (roadmap), Stripe Platform.

### 4.2 Architecture diagram
- Label live MCP servers: `memory`, `finance`, `payments`, `google_workspace`, `comms`, `security`, `ops`, `relations`.
- Label roadmap servers: social APIs, CRM, NVIDIA.
- Remove boxes labeled “Social APIs MCP”, “CRM MCP”, or “NVIDIA MCP” as live components.

### 4.3 Per-hero tabs
Replace current tabs with three uniform tabs per hero:
1. **Capabilities** — what this hero does conceptually.
2. **Live now** — implemented tools (dry-run or with credentials).
3. **To connect** — credentials / skills needed for live mode and roadmap items.

### 4.4 API reference
Correct endpoints:
- `GET /api/v1/integrations`
- `POST /api/v1/integrations/{domain}/{action}`
- `GET /api/v1/health/ready`
- `GET /api/v1/metrics`
- `POST /api/v1/gateway/dry_run`

Remove non-existent `/api/v1/mcp/tools` and `/api/v1/mcp/call`.

### 4.5 Install section
- **Quick Start:** clone Parthenon, `./install.sh`, edit `.env`.
- **Hermes:** *“Install Hermes Agent separately if you want the CLI profile experience.”*
- **Docker:** `docker compose up --build -d`.

### 4.6 Protocol / data flow
- Keep flow examples but add inline notes where a step needs credentials or is roadmap.

---

## 5. Visual system constraints

- Fonts: Cinzel (display), Inter (body), JetBrains Mono (code).
- Palette: marble white `#F7F5F0`, parchment `#EDE8DF`, deep stone `#2A2A2E`, midnight `#1A1A1E`, stripe indigo `#635BFF`, nvidia green `#76B900`, glow amber `#FFB800`, myth gold `#D4A853`.
- No massive gradients or generic glows.
- Mobile-first: asymmetric layouts collapse to `w-full` + `px-4` below 768px.
- Only animate `transform` and `opacity`.

---

## 6. Verification gates

- `bash -n install.sh` PASS.
- `ruff check partenon_api tests ...` PASS.
- `pytest tests/` PASS.
- `cd dashboard && npm run build` PASS.
- `python3 .github/scripts/secret_scan.py` PASS.
- HTML renders correctly at 1440px and 390px.
- No new broken internal links.

---

## 7. Out of scope

- Creating `web/capabilities.html` (deferred; can be added later if needed).
- Redesigning visual system.
- Adding new interactive features beyond copy/structure changes.
- Generating new screenshots (Phase 7 subtask; can be done after copy is final).
