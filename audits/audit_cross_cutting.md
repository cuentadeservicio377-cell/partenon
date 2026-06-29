# Cross-cutting Claims Audit — NVIDIA, Stripe, Hermes, Live Status

**Scope:** Compare public website claims across `web/index.html`, `web/heroes.html`, and `web/developers.html` against the actual codebase and documentation, focusing on NVIDIA, Stripe, Hermes, and live-integration status.

**Auditor:** Kimi Code CLI (read-only audit)

**Date:** 2026-06-29

---

## Findings

| Claim (short quote) | Location | Actual status | Severity | Note / recommendation |
|---|---|---|---|---|
| "complete AI agent system built with Hermes Agent, NVIDIA NemoClaw, and Stripe tools" | `web/index.html:7` (meta description) | incorrect | high | NVIDIA NemoClaw / OpenShell is not integrated (`docs/CAPABILITIES.md:98` lists it as 🗓️ roadmap; `MISSING_IMPLEMENTATION.md:2.4`). Hermes Agent CLI is also not bundled with the repo. |
| "Powered by ... NVIDIA" partner branding | `web/index.html:951-969`, `web/heroes.html:1337-1338` | unclear / incorrect | medium | The project is a hackathon entry using the NVIDIA brand, but there is no shipping NVIDIA integration. Only a dry-run `security_allocate_gpu` placeholder exists in `mcp_servers/security/server.py:56-60`. Recommend labeling NVIDIA as "hackathon partner" rather than a shipped integration. |
| Guardian "manages API keys, NVIDIA integrations, model access, and security protocols" | `web/index.html:580-589`, `web/heroes.html:690-691`, `web/developers.html:645` | incorrect | high | No NVIDIA API calls exist. `mcp_servers/security/server.py` has no NVIDIA integration; `security_allocate_gpu` returns a canned recommendation in dry-run and errors live. `partenon_core/config/mcp/servers.yaml` does not list an NVIDIA MCP server. |
| "NVIDIA account (API key for security features)" listed as required pre-workshop account | `web/developers.html:1532-1534` | incorrect | medium | `NVIDIA_API_KEY` is defined in `.env.example:17` but is never consumed by any live-mode check (`mcp_servers/_shared/live_mode.py` does not include NVIDIA) or MCP server. |
| Collector "manages Stripe operations — subscriptions, invoices, payment processing, and revenue tracking" | `web/index.html:553-555`, `web/heroes.html:583-606`, `web/developers.html:544` | needs_credentials | low | Tools are implemented in `mcp_servers/payments/server.py`, but every tool defaults to `dry_run=True` and only executes live when `STRIPE_SECRET_KEY` is set **and** `dry_run=false`. `docs/CAPABILITIES.md:50` correctly marks Stripe as ⚡. Marketing pages should add a "Stripe account required" caveat. |
| "Payments flow automatically" / "Live payment processing" | `web/index.html:749-750`, `web/heroes.html:1182-1186` | needs_credentials / unclear | medium | Payments do not flow automatically after install; live execution requires Stripe credentials and explicit opt-out of dry-run per tool. The heroes workflow explicitly labels the step "Live payment processing" without that caveat. |
| "Google Workspace Integrated" trust badge | `web/index.html:1024-1027` | needs_credentials | low | `mcp_servers/google_workspace/server.py` defaults to dry-run; live calls require `GOOGLE_SERVICE_ACCOUNT_JSON` or OAuth credentials (`.env.example:24-28`, `live_mode.py:16-23`). Badge should be qualified. |
| "Hermes is open source and free to install. One command sets up your entire operational system." | `web/index.html:983-984`, `web/heroes.html:1265-1274` | incorrect / unclear | high | The CTA command is `git clone` of the Partenon repo, not an `install hermes` command. The Hermes Agent CLI is **not** bundled; `install.sh:79-90` and `scripts/setup_hermes.py:45-59` explicitly tell users to install it separately. |
| Hermes CLI commands (`hermes activate`, `hermes mission`, `hermes deploy`, etc.) documented as available | `web/developers.html:1766-1809`, CLI examples throughout hero specs | incorrect / roadmap | high | No `hermes` binary is shipped in the repo. `examples/README.md:3-5` says previous CLI stubs were removed. The CLI table and hero CLI examples present fictional commands unless the user installs Hermes separately. |
| System status example shows all heroes active and Google Workspace / Stripe / NVIDIA "connected" | `web/developers.html:1856-1877` | incorrect / misleading | medium | The JSON is purely illustrative. Actual `/health/ready` in `partenon_api/main.py:93-106` only checks memory-store reachability; there is no integration-health endpoint. |
| Environment variables table marks GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, NVIDIA_API_KEY as "Required" | `web/developers.html:1691-1736` | incorrect | medium | Only dashboard/API secrets are required for a basic install (`.env.example`). Google, Stripe, and NVIDIA credentials are optional; the system runs in dry-run mode without them (`live_mode.py`). |
| "MCP Ready" badge | `web/index.html:1022-1024` | live (with caveat) | low | MCP servers exist and are configured in `partenon_core/config/mcp/servers.yaml`, but most are dry-run wrappers. The badge is acceptable if qualified. |
| "The Partenon is built for the Nous Research × NVIDIA × Stripe Hackathon" | `web/index.html:969`, `web/index.html:1064` | live | low | Factually accurate per `README.md` and repository context. |
| "Install Hermes from source" and "pre-built Hermes image is not yet published" | `web/developers.html:1577`, `web/developers.html:1634-1641` | live | low | Honest disclaimers that correctly set expectations. |

---

## Executive Summary

The website materially overstates shipping integrations in three areas that could erode trust if left unchanged:

1. **NVIDIA is presented as a live integration, but it is not.** The Guardian hero is described as managing NVIDIA API connections and GPU allocation, yet the codebase contains no NVIDIA MCP server and no live NVIDIA calls. The only related code is a dry-run GPU recommendation stub.

2. **Hermes is marketed as the install path, but the CLI is not bundled.** Phrases like "Install Hermes" and documented `hermes activate` / `hermes mission` commands imply a working CLI out of the box, while `install.sh` and `scripts/setup_hermes.py` explicitly handle the case where Hermes is missing.

3. **Live Stripe and Google Workspace functionality is implied to work immediately.** Trust badges and workflow examples omit that real credentials and per-tool `dry_run=false` opt-in are required; the developers page also incorrectly marks those credentials as "Required" and shows a fabricated status response with all integrations "connected."

**Recommended fix priority:** add prominent "requires credentials" qualifiers to Stripe/Google Workspace claims, remove or reframe NVIDIA integration claims until implemented, and replace "Install Hermes" language with "Install Partenon" while clearly noting that the Hermes Agent CLI is a separate dependency.
