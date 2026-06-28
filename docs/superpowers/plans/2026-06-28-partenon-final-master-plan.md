# Partenon — Final Master Plan
## From prototype to world-ready Hermes distribution

**Date:** 2026-06-28  
**Status:** Draft — pending Gate 1 approval  
**Constraint:** This is a product delivery, not a patch. The repository must be clean, honest, and globally installable.

---

## 1. Executive Summary

Partenon is a strong concept with a static site, seven hero archetypes, local Python tools, a local-JSON dashboard, and partial G-Brain memory. It is **not yet** the world-ready product promised on the website.

The final transformation makes Partenon a native Hermes Agent distribution:
- Installable with `hermes profile install`.
- All heroes work in dry-run without credentials.
- Live integrations (Google Workspace, Stripe, Gmail, Calendar, messaging) activate only when credentials are provided.
- Real-time dashboard backed by a FastAPI service and G-Brain.
- Messaging commands through Hermes gateway.
- Production deployment with Docker, CI/CD, tests, and observability.
- Honest website with a public capabilities/status page.

**Timeline:** ~4–5 months of focused engineering with parallel workstreams.  
**Phases:** 8 phases, each ending in a Gate.

---

## 2. Principles

1. **Hermes is the runtime.** Do not rebuild routing, cron, gateway, or MCP orchestration.
2. **Dry-run by default.** A new user must get value in 15 minutes without credentials.
3. **No false claims.** The website must match reality; aspirational features go to the roadmap.
4. **Clean repo.** No real PII, no dead code, no inconsistent schemas, no unvendored binaries.
5. **MCP is the integration boundary.** All external services are reached through MCP servers.
6. **World-ready.** English-first, canonical English profile names, open-source license, install docs.

---

## 3. Final Architecture

```
User
 ├── Web Dashboard (Next.js) → FastAPI API → G-Brain
 ├── Telegram / Email / Discord / WhatsApp → Hermes Gateway
 └── Hermes CLI
         │
         ▼
 Hermes Agent Runtime
         │
    ┌────┴────┐
    ▼         ▼
 Partenon   Partenon MCP Servers
 Skills     (finance, payments, ops, relations, security, comms, memory)
    │         │
    └────┬────┘
         ▼
   Google Workspace, Stripe, Gmail, Slack, G-Brain
```

- **Profiles:** `partenon-scribe`, `partenon-herald`, `partenon-collector`, `partenon-guardian`, `partenon-strategist`, `partenon-diplomat`, `partenon-brain`.
- **Core skills:** `partenon-core` (routing, onboarding, workflow hooks), `partenon-judge` (eval loop).
- **Memory:** Bundled `gbrain/server.py` MCP server. SQLite default, Postgres optional.
- **Dashboard:** FastAPI backend + Next.js frontend. Server-Sent Events for real-time updates.

---

## 4. Master Implementation Roadmap

| Phase | Scope | Duration | Gate |
|-------|-------|----------|------|
| **0** | Contaminants cleanup | 2 weeks | Gate 0 |
| **1** | Hermes-native foundation | 3 weeks | Gate 1 |
| **2** | Hero final design + MCP wrappers | 4 weeks | Gate 2 |
| **3** | Real integrations | 6 weeks | Gate 3 |
| **4** | Real-time dashboard + API | 4 weeks | Gate 4 |
| **5** | Gateway messaging | 3 weeks | Gate 5 |
| **6** | Deployment world | 4 weeks | Gate 6 |
| **7** | Website reality | 2 weeks | Gate 7 |

**Total:** ~28 weeks of engineering. With parallel tracks, **4–5 months** wall-clock.

---

### Phase 0 — Contaminants Cleanup (2 weeks)

**Goal:** The repository is safe to distribute worldwide.

**Tasks:**
- Run secret/PII scan; fix all findings.
- Delete dead code: `examples/*-stub.py`, legacy React source, research caches, generated artifacts.
- Anonymize workshop company cards and sample data.
- Rename profile directories to English canonical names (`partenon-scribe`, etc.).
- Standardize all `config.yaml` files to one Hermes-compatible schema.
- Remove default dashboard credentials (`admin`/`partenon`).
- Replace external `gbrain` binary calls with bundled MCP server.
- Add `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `NOTICE.md`.
- Make `install.sh` idempotent and safe.

**Deliverables:**
- Clean repo passing secret scan and profile validation.
- `scripts/validate_profiles.py` green for all 7 profiles.
- Updated `.gitignore` and no generated artifacts committed.

**Gate 0 criteria:**
- [ ] No real PII, emails, phones, IPs, or credentials in source.
- [ ] All profile directories use English names.
- [ ] All `config.yaml` validate against one schema.
- [ ] CI passes: lint, tests, build, secret scan.

---

### Phase 1 — Hermes-Native Foundation (3 weeks)

**Goal:** Partenon installs and runs as a Hermes distribution.

**Tasks:**
- Create root `distribution.yaml` and `pyproject.toml`.
- Convert `partenon-core/tools/` into Hermes skills:
  - `partenon-core` — router, onboarding, context loader.
  - `partenon-judge` — eval loop.
  - `partenon-workflows` — mission dispatcher.
- Build `mcp_servers/` wrappers for each domain.
- Bundle G-Brain as `partenon-memory` MCP server.
- Wire profiles to MCP servers via canonical `config.yaml`.
- Verify `hermes profile install` end-to-end.

**Deliverables:**
- `hermes profile install github.com/owner/partenon` succeeds.
- Every hero responds to a dry-run command.
- G-Brain memory persists across calls.

**Gate 1 criteria:**
- [ ] Distribution manifest loads in Hermes.
- [ ] All 7 profiles install without errors.
- [ ] Dry-run command works for at least Scribe, Herald, Collector.
- [ ] Brain stores and retrieves a learning.

---

### Phase 2 — Hero Final Design + MCP Wrappers (4 weeks)

**Goal:** Each hero has a precise, tested contract.

**Tasks:**
- Finalize tool lists and dry-run/live behavior for all 7 heroes.
- Rewrite `SOUL.md` and `SKILL.md` for each hero with Hermes frontmatter.
- Implement dry-run wrappers in every MCP server.
- Define collaboration handoff events (Scribe ↔ Collector, Diplomat ↔ Strategist, etc.).
- Add example interaction tests for every hero.
- Build helper templates for `.finance`, `.design`, `.payments`, etc.

**Deliverables:**
- Per-hero `SKILL.md` and `config.yaml` consistent with architecture.
- Collaboration event schema documented.
- Unit tests for every MCP tool in dry-run mode.

**Gate 2 criteria:**
- [ ] Every hero has a defined tool list, dry-run path, and live path.
- [ ] Cross-hero handoff events are emitted and stored.
- [ ] `pytest` covers all MCP tool modules.

---

### Phase 3 — Real Integrations (6 weeks)

**Goal:** Core integrations work with real credentials.

**Tasks:**
- Select and pin one Google Workspace MCP server.
- Wire Google Workspace to Scribe, Herald, Strategist, Diplomat.
- Wire Stripe MCP to Collector (payment links, invoices, subscriptions, webhooks).
- Wire Gmail/Calendar MCP to Strategist and Diplomat.
- Add Slack MCP for Strategist notifications.
- Implement Guardian key audit and model recommendation helpers.
- Add webhook handler for Stripe events.
- Document credential setup for each integration.

**Deliverables:**
- Scribe creates a real Google Sheet from a CSV with service-account credentials.
- Collector creates a Stripe test payment link.
- Strategist creates a Google Calendar event.
- Guardian audits API keys and recommends models.

**Gate 3 criteria:**
- [ ] Google Workspace + Stripe end-to-end in test mode.
- [ ] Gmail and Calendar actions work with credentials.
- [ ] Every integration has clear dry-run/live behavior and docs.

---

### Phase 4 — Real-Time Dashboard + API (4 weeks)

**Goal:** Dashboard shows live mission state.

**Tasks:**
- Build FastAPI backend (`partenon/dashboard_api/`):
  - `/missions`, `/heroes`, `/cron`, `/integrations`, `/memory/search`, `/events` (SSE).
- Refactor Next.js dashboard to consume the API.
- Implement Server-Sent Events for mission updates.
- Add JWT auth with generated secret (no default password).
- Add workspace/company isolation foundation.
- Build integration health page.

**Deliverables:**
- Dashboard loads missions, heroes, and cron from API.
- Mission status updates appear in real time via SSE.
- Auth requires a real secret; no default credentials.

**Gate 4 criteria:**
- [ ] Dashboard reads from API, not local JSON.
- [ ] SSE stream delivers mission updates.
- [ ] Auth hardened; service refuses weak/default secrets.

---

### Phase 5 — Gateway Messaging (3 weeks)

**Goal:** Users chat with Partenon through familiar platforms.

**Tasks:**
- Configure Hermes gateway for Telegram and Email.
- Define command namespace (`/scribe`, `/collector`, `/status`, `/onboard`, etc.).
- Implement intent routing fallback when no prefix is used.
- Add file attachment routing (CSV → Scribe, image → Herald, PDF → Diplomat/Brain).
- Add group-chat rules and allowlists.
- Build progressive onboarding conversation.
- Document Discord/WhatsApp setup (WhatsApp as later phase).

**Deliverables:**
- Telegram bot responds to `/scribe review June expenses`.
- Email adapter handles formal approvals and reminders.
- Onboarding chat creates company files and first missions.

**Gate 5 criteria:**
- [ ] Telegram and Email commands route to correct hero.
- [ ] File attachments are handled and routed.
- [ ] Onboarding conversation works end-to-end.

---

### Phase 6 — Deployment World (4 weeks)

**Goal:** Partenon deploys cleanly anywhere.

**Tasks:**
- Rewrite `docker-compose.yml` with all services: Hermes runtime, API, dashboard, G-Brain Postgres, optional reverse proxy.
- Dockerfiles for each service with non-root users and health checks.
- GitHub Actions CI/CD: lint, test, build, secret scan, dependency audit, Docker push.
- Expand test suite: unit, integration, E2E (Playwright).
- Structured JSON logging, Prometheus metrics, health endpoints.
- Secrets via Docker secrets or external manager.
- Write `docs/INSTALL.md`, `docs/RUNBOOK.md`, `docs/TROUBLESHOOTING.md`, `docs/CONTRIBUTING.md`.
- Release process: SemVer, changelog, signed tags.

**Deliverables:**
- `docker compose up` runs the full stack.
- CI passes on every PR.
- Release workflow builds and tags images.

**Gate 6 criteria:**
- [ ] Full Docker Compose stack runs on a fresh machine.
- [ ] CI passes: tests, lint, build, secret scan, dependency audit.
- [ ] Docs cover install, runbook, troubleshooting, and contribution.

---

### Phase 7 — Website Reality (2 weeks)

**Goal:** The website tells the truth.

**Tasks:**
- Audit every claim on `index.html`, `heroes.html`, `developers.html`.
- Rewrite copy to distinguish:
  - **Live now** — dry-run heroes, Hermes install, local dashboard.
  - **Requires credentials** — Google Workspace, Stripe, Gmail, Calendar, Slack.
  - **Roadmap** — WhatsApp, Shopify, AWS cost, NVIDIA NemoClaw sandbox, multi-tenant SaaS.
- Create `web/capabilities.html` driven by `docs/CAPABILITIES.md`.
- Update screenshots and README.
- Link status page from nav and footer.

**Deliverables:**
- No misleading claims remain.
- Public capabilities page is live.
- Website and docs stay synchronized.

**Gate 7 criteria:**
- [ ] Every marketing claim maps to an implemented feature or a roadmap label.
- [ ] `web/capabilities.html` is published and linked.
- [ ] README reflects current capabilities honestly.

---

## 5. Parallel Workstreams

| Track | Lead Concerns | Phases |
|-------|---------------|--------|
| **Core / Backend** | Hermes skills, MCP servers, integrations, G-Brain | 0–3 |
| **Frontend / Dashboard** | FastAPI, Next.js, SSE, auth | 0, 4 |
| **Messaging / UX** | Gateway config, commands, onboarding chat | 1, 5 |
| **Platform / DevOps** | Docker, CI/CD, tests, observability, docs | 0, 6 |
| **Product / Copy** | Website reality, capabilities page, README | 0, 7 |

---

## 6. Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hermes CLI schema changes | High | Pin `hermes_requires`; validate in CI. |
| Credential setup friction | High | Dry-run first; progressive onboarding; video docs. |
| Scope creep | High | Strict phase gates; new ideas go to `ROADMAP.md`. |
| Third-party MCP server breakage | Medium | Pin versions; keep dry-run fallbacks. |
| Live credential leak | Critical | Secret scanning, least privilege, no defaults, Guardian rotation. |
| Website vs. reality drift | Medium | Capabilities page auto-synced with docs. |

---

## 7. Success Criteria for v1.0

- [ ] `hermes profile install github.com/owner/partenon` succeeds on a fresh machine.
- [ ] All seven heroes respond to dry-run commands without credentials.
- [ ] Google Workspace and Stripe integrations work in test mode with credentials.
- [ ] Dashboard shows live mission state from the API with real-time updates.
- [ ] Telegram/Email gateway routes commands to the correct hero.
- [ ] Docker Compose runs the full stack with one command.
- [ ] CI/CD passes tests, secret scans, and dependency audits.
- [ ] Website has no misleading claims and includes a public capabilities page.
- [ ] `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, and runbooks exist.

---

## 8. Recommended First Action

**Start Phase 0 immediately:** cleanup is a blocker for everything else and has no external dependencies. After Gate 0, proceed to Phase 1 (Hermes-native foundation).

---

*This plan was synthesized from an 8-way architecture swarm covering contaminants cleanup, Hermes-native architecture, hero design, data integrations, real-time dashboard, gateway messaging, deployment world, and website reality.*
