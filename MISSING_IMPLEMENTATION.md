# Missing Implementation Audit — The Partenon

> Scope: `web-repo-consistency`  
> Audited: `web/index.html`, `web/heroes.html`, `web/developers.html` against repository contents.  
> Date: 2026-06-26

This document lists every feature, tool, MCP server, API endpoint, or architecture component described in the public web pages that is **not yet implemented** in the repository. Items are ordered by priority: **P0 (blocks installation)**, **P1 (major feature gaps)**, **P2 (consistency / polish gaps)**.

---

## P0 — Installation / Runtime Blockers

These gaps prevent a visitor from installing or running the system as advertised.

| # | Gap | Where it is promised | Current reality | Recommended fix |
|---|-----|----------------------|-----------------|-----------------|
| 1 | **`npx create-hermes@latest` does not exist** | CTA on `index.html`, copy box on `heroes.html`, install tabs on `developers.html` | No npm package named `create-hermes` is published. The command fails. | Replace the public CTA with the real local setup flow (`git clone` + Python venv + `pip install`) and publish a stub package only after it works. |
| 2 | **`fastmcp>=1.0.0` is not a valid dependency** | `requirements.txt` | PyPI has no package `fastmcp`. The dependency blocks `pip install -r requirements.txt`. | Change to the correct package (`mcp>=1.0.0`) or remove if unused. |
| 3 | **`config_loader` module is missing** | `partenon-core/tools/onboarding_engine.py` line 15 | `from config_loader import get_config, ConfigLoader` fails because the file does not exist. | Add `partenon-core/tools/config_loader.py` with a minimal `ConfigLoader` class that reads `config/empresa.yaml` or environment variables. |
| 4 | **`hermes` CLI is not implemented** | `developers.html` CLI reference, `install.sh`, `scripts/setup_hermes.py` | No `hermes` binary or Python package provides `hermes activate`, `hermes mission`, etc. | Create a Python CLI entry point (`partenon-core/cli.py`) that implements the documented commands as stubs. |
| 5 | **REST API endpoints are not implemented** | `developers.html` `/api/v1/heroes`, `/api/v1/missions`, `/api/v1/mcp/tools`, `/api/v1/mcp/call` | No HTTP server file exists for these routes. | Add a minimal FastAPI/Flask server (`partenon-core/api_server.py`) that returns the documented JSON shapes. |

---

## P1 — Major Feature Gaps

These are capabilities heavily featured on the website but missing or only stubbed in code.

| # | Gap | Promised in | Current reality | Recommended fix |
|---|-----|-------------|-----------------|-----------------|
| 6 | **Eval loop / judge skill** | `docs/architecture.md`, `developers.html` "Quality Layer" (implied) | No eval loop, judge skill, or threshold code exists. | Add `partenon-core/tools/eval_loop.py` with a pluggable judge and pass/fail threshold. |
| 7 | **Real Google Workspace MCP integration** | `developers.html`, profiles (Scribe, Strategist) | `servers.yaml` references `@taylorwilsdon/google-workspace-mcp`; profile `config.yaml` references `@modelcontextprotocol/server-google-workspace`. Neither is confirmed installed or wired to real credentials. | Pick one working MCP server, document setup, and add a small wrapper that authenticates with `GOOGLE_SERVICE_ACCOUNT_JSON`. |
| 8 | **Stripe operations beyond placeholders** | `developers.html`, Collector profile | `stripe_tools.py` exists but only as a stub. No real payment link, subscription, invoice, or webhook handling. | Implement `create_payment_link`, `create_invoice`, `create_subscription`, and `list_charges` using the Stripe Python SDK. |
| 9 | **Social media APIs (Instagram, Twitter/X, LinkedIn)** | `developers.html`, Herald profile | No API clients or posting logic. | Add stub OAuth + posting modules under `hermes/profiles/partenon-mensajero/skills/comms/tools/`. |
| 10 | **CRM integration (HubSpot / Salesforce)** | `developers.html`, Diplomat profile | `crm.py` is a placeholder. No contact sync, meeting scheduler, or follow-up engine. | Implement HubSpot CRM stub with contact/metting/follow-up actions. |
| 11 | **NVIDIA NemoClaw / OpenShell integration** | `index.html`, `developers.html`, Guardian profile | No code connects to NVIDIA APIs, allocates GPUs, or manages model access. | Add a Guardian tool that reads `NVIDIA_API_KEY` and reports model availability (stub is acceptable for alpha). |
| 12 | **Calendar / Gmail API actions** | `developers.html`, Strategist profile | No Google Calendar event creation or Gmail sending logic. | Add thin wrappers around Google API client libraries. |
| 13 | **Workshop deliverables** | `developers.html` workshop section | Slides, participant handbook, and facilitator script buttons show "Coming soon!" but no files exist. | Create `workshops/slides/`, `workshops/handbooks/`, `workshops/facilitator/` with markdown templates. |
| 14 | **Docker image `ghcr.io/theparthenon/hermes:latest`** | `developers.html` Docker install tab | No Dockerfile or GitHub Actions workflow builds this image. | Add a root `Dockerfile` and a `.github/workflows/docker.yml` workflow, or remove the tab until ready. |
| 15 | **Real-time dashboards / Google Sheets dashboards** | `index.html`, `heroes.html`, Scribe profile | `demo_tesorero.py` creates a static `.xlsx` file, not a live Google Sheets dashboard. | Add a script that creates/updates a Google Sheet with charts using the Sheets API. |

---

## P2 — Consistency / Polish Gaps

These reduce trust or create confusion between the website and the repository.

| # | Gap | Promised in | Current reality | Recommended fix |
|---|-----|-------------|-----------------|-----------------|
| 16 | **GitHub links point to wrong URLs** | `index.html` footer "View on GitHub", `heroes.html` CTA GitHub link, `developers.html` manual setup | Links go to `https://github.com` or `github.com/the-parthenon/hermes.git` instead of `github.com/cuentadeservicio377-cell/partenon`. | Update all GitHub links to the actual repository URL. |
| 17 | **Repository structure diagram is fictional** | `developers.html` "Repository Structure" tree | Tree shows `apps/hermes/`, `packages/mcp-sdk/`, `packages/heroes/`, etc. Actual repo is flat. | Replace with the real tree or label it as the target architecture. |
| 18 | **`.env.example` still in Spanish** | Global project | The file mixes Spanish comments and placeholder instructions. | Translate to English and align variables with `developers.html` env table. |
| 19 | **Profile file extensions are inconsistent** | `developers.html` mentions `.finance`, `.design`, etc. | Some profiles use Spanish-derived names (`.ops`, `.relations`) without explanation. | Document the mapping in `docs/file-formats.md` or rename to English equivalents. |
| 20 | **No `LICENSE` or `CONTRIBUTING.md`** | `developers.html` repo structure lists both | Neither file exists. | Add MIT `LICENSE` and a minimal `CONTRIBUTING.md`. |
| 21 | **No test suite** | Implied by production-ready claims | No `tests/` directory. | Add `tests/test_router.py`, `tests/test_demo.py`, and a CI runner. |
| 22 | **MCP protocol methods (`mcp.register`, `mcp.context.share`, etc.) are not wired to real code** | `developers.html` MCP section | `gbrain/server.py` only exposes `gbrain_*` tools, not the generic MCP methods shown. | Clarify in the page that these are conceptual methods or implement them in `gbrain/server.py`. |
| 23 | **`scripts/setup_hermes.py` and `install.sh` reference a fake Hermes install URL** | Setup scripts | `https://install.hermes-agent.nousresearch.com` and `https://www.nvidia.com/nemoclaw.sh` are not guaranteed to work and may fail. | Replace with clear placeholder instructions and error messages. |
| 24 | **Docs are in Spanish** | `README.md`, `docs/` | The user-facing docs are Spanish while the website is English. | Translate docs to English (handled by `docs-and-readme` scope). |
| 25 | **No web deployment assets / build verification** | `index.html` references many image assets | Some assets may be missing; build verification is manual. | Add an asset manifest and a simple HTML validator script. |

---

## Quick-Win Placeholders Already Created

To move the repo closer to the website promises, this audit scope created:

- `examples/hermes-cli-stub.py` — demonstrates the documented CLI commands as local stubs.
- `examples/api-server-stub.py` — minimal FastAPI server returning the documented `/api/v1/*` JSON shapes.
- `examples/mcp-client-example.py` — example of calling G-Brain MCP tools.
- `examples/README.md` — how to run the stubs.

These stubs are **not production code**; they exist so visitors can see the intended interfaces while real implementations are built by the corresponding scopes.

---

## Priority Action Summary

1. **Fix P0 blockers first** so `pip install` and the onboarding script run without errors.
2. **Implement P1 stubs** for the highest-impact features: Hermes CLI, REST API, eval loop, Stripe tools, Google Workspace wrapper.
3. **Resolve P2 consistency issues** so the website, README, and repository stay aligned.
