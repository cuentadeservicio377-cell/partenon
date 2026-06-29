# Website Phase 7 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `web/index.html`, `web/heroes.html`, and `web/developers.html` to align marketing copy with the Hermes-native codebase, clarify the Hermes-profile relationship, and remove misleading claims.

**Architecture:** Surgical rewrite of three static HTML files. No new components or build steps. Keep existing CSS/Tailwind custom config, fonts, and layout patterns. Changes are limited to copy, section structure, status tags, and honest credential/roadmap labels.

**Tech Stack:** Static HTML + Tailwind CSS CDN + vanilla JS. Design system already defined in each file.

## Global Constraints

- English copy only.
- No emojis.
- No generic AI filler phrases.
- Keep existing visual system: Cinzel display, Inter body, marble/parchment palette, asymmetric bento, mobile-first, no massive gradients.
- Only animate `transform` and `opacity`.
- Do not break `pytest`, `ruff`, dashboard build, or `secret_scan.py`.
- All capability claims must map to `docs/CAPABILITIES.md` or code reality.

---

## Task 1: Reframe `web/index.html` foundation, process, and CTA

**Files:**
- Modify: `web/index.html`

**Interfaces:**
- Consumes: existing CSS classes and component structure.
- Produces: updated marketing copy that frames Parthenon as the home for Hermes profiles.

- [ ] **Step 1: Update meta description**
  Replace the NVIDIA NemoClaw reference with a Hermes-only framing.
  New text: `The Parthenon: a Hermes Agent system for entrepreneurs. Seven profiles handle finance, brand, payments, security, operations, relationships, and memory — all sharing one brain.`

- [ ] **Step 2: Reframe foundation / hero copy**
  Locate the section with the line *“Archetypes, not algorithms.”*
  Replace with:
  ```
  Every business needs its heroes.
  For millennia, the Parthenon has stood as a monument to collective excellence, where individual mastery served a greater purpose. Today, the Parthenon brings that archetype to your business.
  The Parthenon is where your Hermes profiles live. Seven archetypes — Scribe, Herald, Collector, Guardian, Strategist, Diplomat, and Brain — make a single agent system understandable. They are not separate AIs. They are facets of your Hermes agent, sharing one memory.
  ```

- [ ] **Step 3: Add context above the seven-hero grid**
  Add a short line before the hero cards:
  `Seven Hermes profiles. One shared memory. Pick the ensemble your business needs.`

- [ ] **Step 4: Rewrite the four process steps**
  Locate the existing 4-step process section.
  Replace the steps with:
  1. **Download the Parthenon** — clone the repo and run `./install.sh`.
  2. **Configure your Heroes Ensemble** — connect the skills you need: Google Workspace, Stripe, Slack.
  3. **Missions in motion** — each hero picks up its mission from intent, commands, or the dashboard.
  4. **The Parthenon drives** — the Brain keeps context, follow-ups, and handoffs across profiles.
  Remove any sentence that says payments flow automatically or that the Brain continuously optimizes everything.

- [ ] **Step 5: Change the counter from `10 → 1M` to `1 → 1M`**
  Locate the animated counter section and change the start value label from `10` to `1`.
  Keep the label text *“From first customer to one million.”*

- [ ] **Step 6: Update partner / trust badges**
  Remove or rephrase *“Powered by NVIDIA”*.
  Keep the footer line: *“Built for the Nous Research × NVIDIA × Stripe Hackathon.”*
  Change trust badges to:
  - `MCP Ready`
  - `Google Workspace Connectable`
  - `Stripe Connectable`
  Add a small caption below: *“Connect your own accounts; the Parthenon ships in dry-run mode.”*

- [ ] **Step 7: Change install CTA from Hermes to Parthenon**
  Button copy: `Install the Parthenon`.
  Typewriter / code snippet: `git clone https://github.com/.../partenon && cd partenon && ./install.sh`
  Add note: *“Requires the Hermes Agent CLI by Nous Research.”*

- [ ] **Step 8: Verify with browser open at 1440px and 390px**
  Run: `open web/index.html`
  Check that the new copy renders without broken layout.

- [ ] **Step 9: Commit**
  ```bash
  git add web/index.html
  git commit -m "feat(web): reframe index.html around Hermes profiles and honest credentials"
  ```

---

## Task 2: Update `web/heroes.html` per-hero status tags and capabilities

**Files:**
- Modify: `web/heroes.html`

**Interfaces:**
- Consumes: existing hero card CSS classes.
- Produces: hero cards with `live`, `connect`, and `roadmap` status tags.

- [ ] **Step 1: Update lead copy**
  Locate the hero page title / subtitle.
  Add: *“Each hero is a Hermes profile. Install the ones you need; they share memory through the Brain.”*

- [ ] **Step 2: Define status tag CSS**
  Add three tiny utility classes in the `<style>` block if they do not exist:
  ```css
  .tag-live { background: #76B900; color: #fff; }
  .tag-connect { background: #635BFF; color: #fff; }
  .tag-roadmap { background: #D4A853; color: #1A1A1E; }
  .tag { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; padding: 0.25rem 0.5rem; border-radius: 999px; font-weight: 600; }
  ```

- [ ] **Step 3: Update each hero card**
  For every hero card (Scribe, Herald, Collector, Guardian, Strategist, Diplomat, Brain):
  - Add the three status tags near the hero name.
  - Rewrite the capability bullets to match the spec.
  - Remove badges for tools that do not exist or mark them `roadmap`.

  **Scribe**
  - Live: parse finance data, classify expenses, build local dashboards.
  - Connect: Google Sheets / Workspace writes.
  - Roadmap: Google Drive operations.

  **Herald**
  - Live: copy drafts, content calendar, presentation outlines.
  - Connect: Google Docs / Slides creation.
  - Roadmap: Instagram, Twitter, LinkedIn, Mailchimp publishing.

  **Collector**
  - Live: dry-run invoices, subscriptions, revenue reports.
  - Connect: Stripe secret key.
  - Roadmap: Stripe Connect.

  **Guardian**
  - Live: key-strength audit, provider detection, policy logging.
  - Connect: secrets manager (optional).
  - Roadmap: NVIDIA GPU allocation / NemoClaw integration.

  **Strategist**
  - Live: project / task / checklist planning, local ops.
  - Connect: Google Calendar, Gmail, Slack bot token.
  - Roadmap: Notion, Google Tasks PM suite.

  **Diplomat**
  - Live: client / vendor tracking, follow-up drafts.
  - Connect: Google Workspace, Gmail.
  - Roadmap: HubSpot / Salesforce CRM sync.

  **Brain**
  - Live: memory pages, profile storage, conflict detection, SQLite / Postgres.
  - Connect: Postgres for team-scale memory.
  - Roadmap: advanced cross-agent optimization.

- [ ] **Step 4: Verify with browser open at 1440px and 390px**
  Run: `open web/heroes.html`
  Check that tags and bullets render cleanly on mobile.

- [ ] **Step 5: Commit**
  ```bash
  git add web/heroes.html
  git commit -m "feat(web): add live/connect/roadmap tags and real capabilities to heroes"
  ```

---

## Task 3: Update `web/heroes.html` workflow timeline

**Files:**
- Modify: `web/heroes.html`

**Interfaces:**
- Consumes: existing timeline CSS and markup.
- Produces: timeline steps that reflect credential requirements and roadmap status.

- [ ] **Step 1: Locate the product-launch workflow timeline**
  Find the section with steps like *“The Herald schedules social content”* and *“The Collector Stripe Products & Checkout Live”*.

- [ ] **Step 2: Replace misleading step copy**
  - “Live payment processing” → “Stripe-connected payment flow (requires Stripe key).”
  - “CRM updates” → “Relationship tracking (external CRM sync is roadmap).”
  - Any “schedules social content” → “Prepares content for your review (social publishing is roadmap).”

- [ ] **Step 3: Add a small legend**
  Add a one-line legend under the timeline:
  *“Green = live without credentials. Indigo = needs your account. Gold = roadmap.”*

- [ ] **Step 4: Commit**
  ```bash
  git add web/heroes.html
  git commit -m "feat(web): honest labels in heroes workflow timeline"
  ```

---

## Task 4: Reposition `web/developers.html` lead and architecture

**Files:**
- Modify: `web/developers.html`

**Interfaces:**
- Consumes: existing hero, diagram, and tab CSS.
- Produces: judge-facing technical brief with accurate architecture labels.

- [ ] **Step 1: Update lead copy**
  Replace the existing developer hero title / subtitle with:
  ```
  Technical Brief
  Built for the Nous Research, NVIDIA, and Stripe teams.
  The Parthenon is a Hermes-native agent system. Its four building blocks are Google Workspace, the Hermes Agent runtime, NVIDIA Cloud (roadmap), and the Stripe Platform.
  ```

- [ ] **Step 2: Update architecture diagram labels**
  Locate the SVG or text diagram showing MCP servers.
  Label live servers: `partenon-memory`, `partenon-finance`, `partenon-payments`, `partenon-google-workspace`, `partenon-comms`, `partenon-security`, `partenon-ops`, `partenon-relations`.
  Label roadmap: social APIs, CRM, NVIDIA.
  Remove any box that says “Social APIs MCP”, “CRM MCP”, or “NVIDIA MCP” as a live component.

- [ ] **Step 3: Add a building-blocks callout**
  Add a 4-column (2x2 on mobile) block below the diagram:
  - Google Workspace — Docs, Sheets, Slides, Calendar, Gmail.
  - Hermes Agent — profile runtime, intent routing, skills.
  - NVIDIA Cloud — model catalog and GPU allocation (roadmap).
  - Stripe Platform — payment links, invoices, subscriptions.

- [ ] **Step 4: Commit**
  ```bash
  git add web/developers.html
  git commit -m "feat(web): reposition developers.html as judge-facing technical brief"
  ```

---

## Task 5: Replace per-hero tabs in `web/developers.html`

**Files:**
- Modify: `web/developers.html`

**Interfaces:**
- Consumes: existing tab JavaScript and CSS.
- Produces: uniform `Capabilities / Live now / To connect` tabs per hero.

- [ ] **Step 1: Replace tab labels globally**
  For each hero spec section, replace the existing tab labels (Quick Start, Config, CLI Examples) with:
  - `Capabilities`
  - `Live now`
  - `To connect`

- [ ] **Step 2: Fill Capabilities tab**
  Write a short paragraph of what the hero does conceptually.

- [ ] **Step 3: Fill Live now tab**
  List implemented tools with the `live` / `connect` distinction.
  Example for Scribe:
  - `parse_finance_data` — live
  - `classify_expenses` — live
  - `write_to_sheets` — connect (Google Workspace)

- [ ] **Step 4: Fill To connect tab**
  List credentials or skills needed and roadmap items.
  Example for Herald:
  - Connect: Google service account for Docs/Slides.
  - Roadmap: Instagram, Twitter, LinkedIn, Mailchimp APIs.

- [ ] **Step 5: Remove fictional CLI examples**
  Delete any `hermes activate scribe` or `hermes mission ...` examples.
  If a tab still needs CLI content, use real commands like:
  ```bash
  git clone https://github.com/.../partenon
  cd partenon && ./install.sh
  uvicorn partenon_api.main:app --reload
  ```

- [ ] **Step 6: Commit**
  ```bash
  git add web/developers.html
  git commit -m "feat(web): uniform capabilities/live/roadmap tabs on developers page"
  ```

---

## Task 6: Correct API reference and install section in `web/developers.html`

**Files:**
- Modify: `web/developers.html`

**Interfaces:**
- Consumes: actual API routes from `partenon_api/main.py` and routers.
- Produces: accurate API reference table and install instructions.

- [ ] **Step 1: Update API reference table**
  Replace the existing endpoints with:
  | Method | Endpoint | Description |
  |--------|----------|-------------|
  | GET | `/api/v1/health` | Liveness probe. |
  | GET | `/api/v1/health/ready` | Readiness probe. |
  | GET | `/api/v1/metrics` | Prometheus metrics. |
  | GET | `/api/v1/integrations` | List available integration domains. |
  | POST | `/api/v1/integrations/{domain}/{action}` | Call an integration action. |
  | POST | `/api/v1/gateway/dry_run` | Test gateway command parsing. |
  Remove `/api/v1/mcp/tools` and `/api/v1/mcp/call`.

- [ ] **Step 2: Update system status example**
  Replace the mock status JSON with the actual shape returned by `/health/ready`:
  ```json
  {
    "status": "ok",
    "service": "partenon-api",
    "ready": true,
    "store": "mcp"
  }
  ```
  Add caption: *“Actual response shape. Integration health is per-tool at call time.”*

- [ ] **Step 3: Rewrite install section**
  Three tabs:
  - **Quick Start**: clone Parthenon, `./install.sh`, edit `.env`.
  - **Hermes**: *“Install Hermes Agent separately if you want the CLI profile experience.”*
  - **Docker**: `docker compose up --build -d`.

- [ ] **Step 4: Update env vars table**
  Mark only `PARTENON_API_SECRET`, `DASHBOARD_AUTH_SECRET`, `DASHBOARD_APP_USERNAME`, `DASHBOARD_APP_PASSWORD` as required.
  Mark Google, Stripe, Slack, NVIDIA as optional / needed for live mode.
  Remove `MCP_PORT` and `HERMES_ENV` if present.

- [ ] **Step 5: Commit**
  ```bash
  git add web/developers.html
  git commit -m "feat(web): correct API reference and install instructions on developers page"
  ```

---

## Task 7: Sync `docs/CAPABILITIES.md` with website claims

**Files:**
- Modify: `docs/CAPABILITIES.md`

**Interfaces:**
- Consumes: updated website copy.
- Produces: consistent source of truth.

- [ ] **Step 1: Update any status that changed during the rewrite**
  Ensure the statuses in `docs/CAPABILITIES.md` still match what the website now claims.

- [ ] **Step 2: Update the date**
  Set `Last updated:` to `2026-06-29`.

- [ ] **Step 3: Add a note about website status tags**
  Add a line in the legend explaining that website cards use `live`, `connect`, and `roadmap` tags derived from this file.

- [ ] **Step 4: Commit**
  ```bash
  git add docs/CAPABILITIES.md
  git commit -m "docs: sync CAPABILITIES.md with website rewrite"
  ```

---

## Task 8: Verification

**Files:**
- Read-only: all modified files, plus test/build scripts.

- [ ] **Step 1: Run Python tests**
  Command: `pytest tests/ -q`
  Expected: 184 passed.

- [ ] **Step 2: Run linter**
  Command: `ruff check partenon_api tests partenon_core/tools/intent_router.py partenon_core/tools/router.py scripts/bump_version.py`
  Expected: All checks passed.

- [ ] **Step 3: Check install script syntax**
  Command: `bash -n install.sh`
  Expected: no output (success).

- [ ] **Step 4: Compile bump_version.py**
  Command: `python3 -m py_compile scripts/bump_version.py`
  Expected: no output.

- [ ] **Step 5: Run secret scan**
  Command: `python3 .github/scripts/secret_scan.py`
  Expected: no hardcoded secrets.

- [ ] **Step 6: Build dashboard**
  Command: `cd dashboard && npm run build`
  Expected: build succeeds.

- [ ] **Step 7: Validate HTML**
  Command: `python3 -c "from html.parser import HTMLParser; [HTMLParser().feed(open(f).read()) for f in ['web/index.html','web/heroes.html','web/developers.html']]"`
  Expected: no parse errors.

- [ ] **Step 8: Commit verification results only if fixes are needed**
  If any verification fails, fix and commit. If all pass, no extra commit.

---

## Task 9: Open final pages in Chrome

**Files:**
- `web/index.html`
- `web/heroes.html`
- `web/developers.html`

- [ ] **Step 1: Open pages in Chrome**
  ```bash
  open -a "Google Chrome" web/index.html web/heroes.html web/developers.html
  ```

- [ ] **Step 2: Ask user for final review**
  Prompt user to check desktop (1440px) and mobile (390px) views.

---

## Self-review checklist

- [ ] Spec coverage: every section of `docs/superpowers/specs/2026-06-29-website-phase7-design.md` maps to a task.
- [ ] Placeholder scan: no TBD, TODO, or vague steps.
- [ ] Type consistency: not applicable for static HTML copy.
- [ ] No new broken internal links introduced.
