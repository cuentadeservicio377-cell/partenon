# TODOS — Partenon Final Transformation

> Master roadmap: `docs/superpowers/plans/2026-06-28-partenon-final-master-plan.md`

---

## Current Phase

**Phase 0 — Contaminants Cleanup**  
Goal: make the repository safe, clean, and globally distributable before any Hermes-native work begins.

- [x] Run secret/PII scan and fix findings
- [x] Delete dead code and stubs (`examples/*-stub.py`, legacy React source, research caches)
- [x] Anonymize workshop company cards and sample data
- [x] Rename profile directories to English canonical names
- [x] Standardize all `config.yaml` files to one Hermes-compatible schema
- [x] Remove default dashboard credentials (`admin`/`partenon`)
- [x] Replace external `gbrain` binary calls with bundled MCP server
- [x] Add `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `NOTICE.md`
- [x] Make `install.sh` idempotent and safe
- [x] Verify CI passes: lint, tests, build, secret scan

---

## Pending Phases

### Phase 1 — Hermes-Native Foundation (3 weeks)
- [x] Create root `distribution.yaml` and `pyproject.toml`
- [x] Convert `partenon_core/tools/` into Hermes skills
- [x] Build `mcp_servers/` wrappers for each domain
- [x] Bundle G-Brain as `partenon-memory` MCP server
- [x] Wire profiles to MCP servers via canonical `config.yaml`
- [x] Verify `hermes profile install` end-to-end

### Phase 2 — Hero Final Design + MCP Wrappers (4 weeks)
- [x] Finalize tool lists and dry-run/live behavior for all 7 heroes
- [x] Update `SOUL.md` and `SKILL.md` for each hero with operating modes, MCP tools, and dry-run/live tables
- [ ] Implement dry-run wrappers in every MCP server
- [ ] Define collaboration handoff events
- [ ] Add example interaction tests for every hero

### Phase 3 — Real Integrations (6 weeks)
- [ ] Select and pin one Google Workspace MCP server
- [ ] Wire Google Workspace to Scribe, Herald, Strategist, Diplomat
- [ ] Wire Stripe MCP to Collector
- [ ] Wire Gmail/Calendar MCP
- [ ] Add Slack MCP for Strategist notifications
- [ ] Implement Guardian key audit and model recommendations
- [ ] Add Stripe webhook handler

### Phase 4 — Real-Time Dashboard + API (4 weeks)
- [ ] Build FastAPI backend with missions, heroes, cron, integrations, memory search, SSE
- [ ] Refactor Next.js dashboard to consume API
- [ ] Implement Server-Sent Events for mission updates
- [ ] Add JWT auth with generated secret
- [ ] Add workspace/company isolation foundation

### Phase 5 — Gateway Messaging (3 weeks)
- [ ] Configure Hermes gateway for Telegram and Email
- [ ] Define command namespace and intent routing fallback
- [ ] Add file attachment routing
- [ ] Add group-chat rules and allowlists
- [ ] Build progressive onboarding conversation

### Phase 6 — Deployment World (4 weeks)
- [ ] Rewrite `docker-compose.yml` with all services
- [ ] Dockerfiles with non-root users and health checks
- [ ] GitHub Actions CI/CD
- [ ] Expand test suite (unit, integration, E2E)
- [ ] Structured logging, Prometheus metrics, health endpoints
- [ ] Release process: SemVer, changelog, signed tags

### Phase 7 — Website Reality (2 weeks)
- [ ] Audit every claim on marketing pages
- [ ] Rewrite copy to distinguish live/credentials/roadmap
- [ ] Create `web/capabilities.html` from `docs/CAPABILITIES.md`
- [ ] Update screenshots and README

---

## Completed

- [x] Synthesize final master plan from 8-way architecture swarm
- [x] Write `docs/superpowers/plans/2026-06-28-partenon-final-master-plan.md`
- [x] Write `docs/CAPABILITIES.md` as single source of truth

---

## Parking Lot

_Discoveries made during planning that are NOT in the current phase_
- Consider pinning Python version constraints and documenting them.
- Keep NVIDIA NemoClaw/OpenShell as an optional roadmap item, not a core dependency.
- Social media publishing requires platform approvals; keep as roadmap.
