# Partenon Marketing Claims Audit — `web/index.html`

**Scope:** Public marketing claims on the Partenon landing page (`web/index.html`) compared against the repository code, `docs/CAPABILITIES.md`, `README.md`, `docs/ENTREPRENEUR_PLAYBOOK.md`, and `MISSING_IMPLEMENTATION.md`.

**Auditor:** Kimi Code CLI subagent  
**Date:** 2026-06-29  
**Method:** Read-only review; no files modified.

---

## Summary of Findings

| Status | Count | Meaning |
|--------|-------|---------|
| `live` | 5 | Implemented and works without credentials. |
| `needs_credentials` | 5 | Implemented, but live execution requires API keys / service accounts. |
| `beta` / `partial` | 3 | Implemented but stabilized only in dry-run or local mode. |
| `roadmap` | 3 | Mentioned on the site but not yet implemented. |
| `incorrect` | 5 | Contradicts the codebase or docs. |
| `unclear` | 5 | Framed in a way a reasonable visitor could misinterpret. |

**Highest severity risks:** NVIDIA/NemoClaw is referenced as a core build partner on the page even though it is not integrated; social-media publishing and CRM sync are advertised as hero capabilities but are roadmap-only; and the process section implies payments run automatically, while the code requires explicit approval and is dry-run by default.

---

## Detailed Claim-by-Claim Audit

### Hero Capability Cards

| Claim (short quote) | Location | Actual status | Severity | Note / recommendation |
|---------------------|----------|---------------|----------|-----------------------|
| "Seven heroes handle finance, brand, payments, security, operations, relationships, and cross-agent intelligence." | Meta description, `web/index.html:7` | `incorrect` | **high** | Adds "NVIDIA NemoClaw" to the same sentence. The seven hero profiles exist (`hermes/profiles/partenon-*`), but NVIDIA NemoClaw/OpenShell is **roadmap**, not a core dependency (`docs/CAPABILITIES.md:98`, `MISSING_IMPLEMENTATION.md:82`). |
| "The Scribe transforms chaotic business data into crystal-clear dashboards, financial models, and strategic insights using Google Sheets." | Scribe card, `web/index.html:499-501` | `needs_credentials` | medium | Scribe tools (`hermes/profiles/partenon-scribe/SKILL.md`) implement parsing, classification, dashboard generation, and Sheets writing, but default to dry-run. Live Sheets writes require `GOOGLE_SERVICE_ACCOUNT_JSON` (`docs/CAPABILITIES.md:35`). |
| "Google Sheets, Financial Modeling, Dashboards, Data Analysis, .finance files" | Scribe tags, `web/index.html:503-507` | `needs_credentials` / `live` (local) | low | Tags match real tools. Local dry-run works without credentials; live Sheets needs credentials. |
| "The Herald crafts campaigns, manages social presence, builds SEO strategies..." + "Social Media" tag | Herald card, `web/index.html:526-534` | `incorrect` / `roadmap` | **high** | SEO/GEO, copy, calendars, and presentations exist, but **no social-media publishing integration exists**. `mcp_servers/comms/server.py:54-74` returns `error: live execution requires social API credentials` for `comms_publish_post`, `comms_schedule_content`, and `comms_analyze_engagement`. `MISSING_IMPLEMENTATION.md:63` confirms "No actual publishing integration (LinkedIn, Instagram, WordPress, etc.)." |
| "Brand Strategy, Content Calendar, .design files" | Herald tags, `web/index.html:531-535` | `live` (local) / `needs_credentials` | low | These are implemented locally; Google Docs/Slides creation requires credentials. |
| "The Collector manages Stripe operations — subscriptions, invoices, payment processing, and revenue tracking." | Collector card, `web/index.html:553-555` | `needs_credentials` | low | `mcp_servers/payments/server.py` implements payment links, subscriptions, invoices, charge lists, and income reports. All live calls require `STRIPE_SECRET_KEY` (`docs/CAPABILITIES.md:37`). |
| "Stripe API, Payment Links, Invoicing, Revenue Tracking, Subscriptions" | Collector tags, `web/index.html:557-561` | `needs_credentials` | low | Match implemented Stripe tools. |
| "The Guardian manages API keys, NVIDIA integrations, model access, and security protocols." + "NVIDIA Security" tag | Guardian card, `web/index.html:580-588` | `incorrect` / `unclear` | **high** | Guardian does key-strength audit, provider detection, and model recommendation (`mcp_servers/security/key_manager.py`), including a static NVIDIA model catalog. However, **no real NVIDIA NemoClaw / OpenShell integration exists** (`MISSING_IMPLEMENTATION.md:82`, `docs/CAPABILITIES.md:98`). "NVIDIA Security" as a tag implies an integrated security product that is not present. |
| "API Management, Model Administration, Access Control, MCP Protocols" | Guardian tags, `web/index.html:584-588` | `partial` / `beta` | medium | `security_list_keys`, `security_audit_access`, and `security_validate_access` are stubs in `mcp_servers/security/server.py:15-44`. Model recommendations are local heuristics, not live administration. |
| "The Strategist manages projects, calendars, deadlines, and internal coordination." + "Google Calendar, Project Management, Task Orchestration, Email Management, Operations" | Strategist card, `web/index.html:607-615` | `needs_credentials` / `partial` | medium | Project/task/checklist/goal tools work locally. Calendar and email require `GOOGLE_SERVICE_ACCOUNT_JSON`. Slack notifications require `SLACK_BOT_TOKEN`. `MISSING_IMPLEMENTATION.md:90` notes "No Google Calendar or Gmail MCP integration is wired; tools read local JSON only." |
| "The Diplomat manages client communications, vendor coordination, and external partnerships." + "CRM Management, Client Communication, Vendor Relations, Negotiation, Follow-ups" | Diplomat card, `web/index.html:634-642` | `needs_credentials` / `roadmap` | medium | Client/vendor tracking and follow-up reports exist locally. **CRM sync with HubSpot/Salesforce is roadmap** (`hermes/profiles/partenon-diplomat/SKILL.md:15`). Calendar/email require Google credentials. "Negotiation" is overstated — the Diplomat drafts options and proposals but does not negotiate autonomously. |
| "The Brain analyzes cross-hero data, identifies patterns, suggests optimizations, and ensures The Partenon operates as a unified organism through MCP." + "Cross-Agent Analysis, Pattern Recognition, Strategic Insights, Data Synthesis" | Brain card, `web/index.html:661-669` | `partial` / `beta` | medium | Memory MCP and conflict detection exist (`mcp_servers/memory/server.py`, `hermes/profiles/partenon-brain/SKILL.md`). However, cross-agent "optimization" is not automatic; the workflow engine (`partenon_core/tools/workflow_engine.py`) has handoff workflows but many action handlers are stubs. `MISSING_IMPLEMENTATION.md:107` notes persistent G-Brain requires an external `gbrain` binary. |

### Process / "How It Works" Section

| Claim (short quote) | Location | Actual status | Severity | Note / recommendation |
|---------------------|----------|---------------|----------|-----------------------|
| "Hermes doesn't just automate — it understands your business, assembles the right heroes, and guides you through a collaborative journey of transformation." | `web/index.html:698` | `unclear` | medium | The intent router (`partenon_core/tools/intent_router.py`) maps text to hero profiles, and the onboarding engine exists, but **automatic hero assembly and guided journey are not wired end-to-end** (`MISSING_IMPLEMENTATION.md:38-43`). |
| "Hermes activates the right heroes. The Scribe sets up your financial tracking. The Herald begins brand discovery. The Strategist creates your operational calendar. Each hero starts their mission." | Step 2, `web/index.html:726` | `partial` | medium | Profiles can be installed and the router can classify intent, but there is no automated activation or mission-start loop. Users must run tools / CLI commands manually. |
| "All progress tracked in shared Google Workspace." | Step 3, `web/index.html:738` | `needs_credentials` | medium | Google Workspace MCP exists, but default storage is local JSON/SQLite. Shared Workspace tracking requires credential setup. |
| "Payments flow automatically." | Step 4, `web/index.html:750` | `incorrect` | **high** | Collector is **dry-run by default** and **never creates real charges or sends reminders without explicit owner approval** (`hermes/profiles/partenon-collector/SOUL.md:120-122`). |
| "The Brain continuously optimizes everything through cross-agent intelligence." | Step 4, `web/index.html:750` | `incorrect` / `unclear` | **high** | Brain indexes memory and detects conflicts, but it does not "continuously optimize" operations. Workflow handoffs are mostly stub actions in `partenon_core/tools/workflow_engine.py:427-443`. |

### Install / CTA Section

| Claim (short quote) | Location | Actual status | Severity | Note / recommendation |
|---------------------|----------|---------------|----------|-----------------------|
| "Open Source" trust badge | `web/index.html:1017` | `live` | low | Repository is public and `LICENSE` exists. Note: `pyproject.toml:10` says MIT while `LICENSE` is Apache-2.0 — a metadata inconsistency, but the project is open source. |
| "Free Forever" trust badge | `web/index.html:1020` | `unclear` | medium | True for the current codebase, but "forever" is a business commitment, not a code guarantee. The repo has no monetization code, yet this claim could create unverifiable expectations. |
| "MCP Ready" trust badge | `web/index.html:1023` | `live` | low | Multiple MCP servers exist under `mcp_servers/`. |
| "Google Workspace Integrated" trust badge | `web/index.html:1026` | `needs_credentials` | medium | Integration exists (`mcp_servers/google_workspace/server.py`) but is not enabled without credentials. The badge reads as "works out of the box." |
| "Hermes is open source and free to install. One command sets up your entire operational system." | `web/index.html:984` | `unclear` | medium | The typewriter animation displays only `git clone ...` (`web/index.html:1144`). Full setup requires `./install.sh`, credential configuration, and optional Hermes CLI installation (`install.sh:80-91`). |
| "INSTALL HERMES" button | `web/index.html:1003` | `unclear` | low | Links to `developers.html`. Hermes Agent CLI is distributed separately by Nous Research (`install.sh:7-8`). |

### Vision / Metrics / Growth Section

| Claim (short quote) | Location | Actual status | Severity | Note / recommendation |
|---------------------|----------|---------------|----------|-----------------------|
| Counter labels: "Adoption projection", "Design objective", "Hypothesis", "Projection", "Growth hypothesis" | `web/index.html:776-811` | `live` (appropriate framing) | low | The page explicitly frames counters as projections, not historical metrics. Good practice. |
| Milestones 10K/100K/1M marked "Coming soon" | `web/index.html:837-856` | `roadmap` (clearly labeled) | low | Explicitly marked as future milestones. |
| "BIWEEKLY WEBINARS ... Target: 500 participants per session" | `web/index.html:880-884` | `roadmap` / `unclear` | medium | No evidence of scheduled webinar infrastructure or registration flow in the repo. Reads as a planned program. |
| "UNIVERSITY PARTNERSHIPS ... Target: 50 universities in Year 1" | `web/index.html:897-901` | `roadmap` / `unclear` | medium | Aspirational growth target; no partner-management code. |
| "BUSINESS ORGANIZATIONS ... Target: 200 organizations per year" | `web/index.html:911-915` | `roadmap` / `unclear` | low | Aspirational target. |
| "COWORKING & ACCELERATORS ... Target: 100 spaces, 20 accelerators in Year 1" | `web/index.html:928-932` | `roadmap` / `unclear` | low | Aspirational target. |

### Partners / Footer

| Claim (short quote) | Location | Actual status | Severity | Note / recommendation |
|---------------------|----------|---------------|----------|-----------------------|
| "POWERED BY Nous Research, NVIDIA, Stripe" | `web/index.html:954-966` | `incorrect` / `unclear` | **high** | Stripe integration exists. Nous Research Hermes is referenced but the CLI is not bundled. **NVIDIA is not integrated** despite being listed as a power source. The footer later says "Built for the Nous Research × NVIDIA × Stripe Hackathon" which is more accurate. |
| "A complete AI agent system for entrepreneurs. Built with Hermes Agent, NVIDIA NemoClaw / OpenShell, and Stripe tools for the Nous Research hackathon." | Footer, `web/index.html:1042` | `incorrect` | **high** | Repeats the false NVIDIA integration claim. `docs/CAPABILITIES.md:98` lists NVIDIA NemoClaw / OpenShell as 🗓️ Roadmap. |
| "Hermes, NemoClaw, and OpenShell references are alpha / early preview." | Footer, `web/index.html:1067` | `live` | low | Accurate disclaimer, but it contradicts the adjacent "Built with" claim rather than resolving it. |
| "Built for the Nous Research × NVIDIA × Stripe Hackathon. Not an official product of Nous Research, NVIDIA, or Stripe." | Footer, `web/index.html:1064` | `live` | low | Accurate and appropriate disclaimer. |

---

## Executive Summary — Biggest Trust Risks

1. **NVIDIA is marketed as a core technology partner, but no NemoClaw/OpenShell integration exists.** The meta description, partner section, and footer all state the system is "built with" NVIDIA NemoClaw/OpenShell, while `docs/CAPABILITIES.md` and `MISSING_IMPLEMENTATION.md` list it as roadmap-only. This is the most damaging discrepancy.

2. **Social-media publishing is advertised as a Herald capability, yet no live social APIs are implemented.** The "Social Media" tag and "manages social presence" copy imply working integrations; `mcp_servers/comms/server.py` and `MISSING_IMPLEMENTATION.md:63` confirm these are not wired.

3. **The process section claims payments flow automatically and the Brain continuously optimizes everything.** In reality, Collector actions are dry-run by default and require explicit approval; workflow handoffs and Brain optimization are largely stubs.

4. **Trust badges and hero cards understate credential requirements.** "Google Workspace Integrated" and several hero tags read as out-of-the-box features, while most live functionality requires service accounts, Stripe keys, or Slack tokens.

5. **CRM sync and several integrations are labeled as hero capabilities but are roadmap-only.** The Diplomat's "CRM Management" tag conflicts with `hermes/profiles/partenon-diplomat/SKILL.md`, which states HubSpot/Salesforce sync is "roadmap; no MCP tool available yet."

**Recommended priority for fixes:** Remove or qualify NVIDIA claims; replace "Social Media" with "Content Planning" for Herald; add "with credentials" qualifiers to integration badges; soften automated-payment and continuous-optimization language; and move CRM sync to a roadmap card.
