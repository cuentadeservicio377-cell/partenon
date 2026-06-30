# TODOS — Partenon Final Transformation

> Master roadmap: `docs/superpowers/plans/2026-06-28-partenon-final-master-plan.md`

---

## Current Phase

**Phase 7 — Website Reality** (pending)  
Goal: align `web/` marketing copy and screenshots with the real capabilities documented in `docs/CAPABILITIES.md`.

### Phase 0 — Contaminants Cleanup ✅ CLOSED
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

## Repair Sprint — MCP Runtime Migration

- [x] Update `partenon_core/tools/workflow_engine.py` to write follow-up missions and nudges via `partenon-memory` MCP (`sync_call`)
- [x] Replace direct `mcp_servers.notifications.slack` import in workflow engine with MCP call
- [x] Add `AsyncDomainClient` to `partenon_api/mcp_client.py` for generic domain MCP servers
- [x] Rewrite `partenon_api/routers/integrations.py` to route all domains through MCP with dry-run short-circuit
- [x] Add `tests/test_api_integrations.py` covering list, unknown domain, dry-run, memory, and live-error paths
- [x] Verify full suite: `pytest tests/`, `ruff check`, `npm run build`

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
- [x] Implement dry-run wrappers in every MCP server
- [x] Define collaboration handoff events
- [x] Add example interaction tests for every hero

### Phase 3 — Real Integrations (6 weeks)
- [x] Select and pin one Google Workspace MCP server
- [x] Wire Google Workspace to Scribe, Herald, Strategist, Diplomat
- [x] Wire Stripe MCP to Collector
- [x] Wire Gmail/Calendar MCP
- [x] Add Slack MCP for Strategist notifications
- [x] Implement Guardian key audit and model recommendations
- [x] Add Stripe webhook handler

### Phase 4 — Real-Time Dashboard + API (4 weeks)
- [x] Build FastAPI backend with missions, heroes, cron, integrations, memory search, SSE
- [x] Refactor Next.js dashboard to consume API
- [x] Implement Server-Sent Events for mission updates
- [x] Add JWT auth with generated secret
- [x] Add workspace/company isolation foundation

### Phase 5 — Gateway Messaging (3 weeks) ✅ CLOSED
- [x] 5.1 Gateway skill scaffolding in all 7 profiles
- [x] 5.2 Command namespace parser tool (`parse_command`)
- [x] 5.3 Attachment routing tool (`route_attachment`)
- [x] 5.4 Guard tool (allowlists + group-chat rules + rate limits)
- [x] 5.5 Progressive onboarding conversation tool (`onboarding_reply`)
- [x] 5.6 Refactor `partenon_core/tools/router.py` into reusable `intent_router.py`
- [x] 5.7 Hermes gateway configuration template (`config/hermes_gateway.yaml`) and docs
- [x] 5.8 Optional API smoke-test endpoint (`POST /api/v1/gateway/dry_run`)
- [x] 5.9 Profile behavior docs (`docs/GATEWAY_SETUP.md`)
- [x] 5.10 Tests and verification (158 passed, target ≥130)
- [x] 5.11 Documentation and closure commit

Verification:
- `pytest tests/` PASS (158 passed)
- `ruff check partenon_api tests partenon_core/tools/intent_router.py partenon_core/tools/router.py` PASS
- `cd dashboard && npm run build` PASS
- `bash -n install.sh` PASS
- `python3 .github/scripts/secret_scan.py` PASS

### Phase 6 — Deployment World (4 weeks) ✅ CLOSED
- [x] Rewrite `docker-compose.yml` with all services
- [x] Dockerfiles with non-root users and health checks
- [x] GitHub Actions CI/CD
- [x] Expand test suite (unit, integration, E2E)
- [x] Structured logging, Prometheus metrics, health endpoints
- [x] Release process: SemVer, changelog, signed tags

Verification:
- `pytest tests/` PASS (184 passed)
- `ruff check partenon_api tests partenon_core/tools/intent_router.py partenon_core/tools/router.py` PASS
- `cd dashboard && npm run build` PASS
- `bash -n install.sh` PASS
- `python3 -m py_compile scripts/bump_version.py` PASS
- `python3 .github/scripts/secret_scan.py` PASS
- `docker build -t partenon-api .` Dockerfile validated (daemon not running locally)

### Phase 7 — Website Reality (2 weeks)
- [x] Audit every claim on marketing pages
- [x] Rewrite copy to distinguish live/credentials/roadmap
- [x] Create `web/workshop.html` landing for the installation workshop
- [x] Update README with website, workshop, and honest capability framing
- [ ] Create `web/capabilities.html` from `docs/CAPABILITIES.md`
- [ ] Update screenshots in README and repository

Verification:
- `pytest tests/` PASS (184 passed)
- `bash -n install.sh` PASS
- `cd dashboard && npm run build` PASS
- HTML parse check PASS for `web/index.html`, `web/heroes.html`, `web/developers.html`, `web/workshop.html`
- Chrome opened for visual review at `http://localhost:8080`

---

## Completed

- [x] Synthesize final master plan from 8-way architecture swarm
- [x] Create hackathon explainer video (2:28, English, Manim + Hermes `manim-video` skill)
  - Files: `video/partenon-hackathon/plan.md`, `script.py`, `voiceover.txt`
  - Output: `partenon-hackathon-video.mp4` (1280x720, 30 fps, AAC narration)
  - Skills used: `manim-video` (plan + code), `kanban-video-orchestrator` (discovery), `hyperframes` (evaluated for motion-graphics pipeline)
- [x] Write `docs/superpowers/plans/2026-06-28-partenon-final-master-plan.md`
- [x] Write `docs/CAPABILITIES.md` as single source of truth

---

## Parking Lot

_Discoveries made during planning that are NOT in the current phase_
- Consider pinning Python version constraints and documenting them.
- Keep NVIDIA NemoClaw/OpenShell as an optional roadmap item, not a core dependency.
- Social media publishing requires platform approvals; keep as roadmap.
