# Partenon Production-Readiness Checklist

Use this checklist before taking Partenon live for a small business.

**Legend**

- **Green** — works out of the box after install
- **Yellow** — works locally; needs live credentials or third-party account
- **Red** — not implemented or requires engineering

---

## 1. Core platform

| # | Item | Status | Notes |
|---|---|---|---|
| 1.1 | `install.sh` completes without errors | Green | Run from project root |
| 1.2 | `python3 scripts/demo_tesorero.py` passes | Green | Verifies tools and local workspace |
| 1.3 | `cd dashboard && npm run build` passes | Yellow | Needs Node 20+ and `npm install` |
| 1.4 | Router maps intents to heroes | Green | Rule-based; see `partenon-core/tools/router.py` |
| 1.5 | Router loads profile metadata dynamically | Red | Profiles are hard-coded today |
| 1.6 | Eval loop validates hero outputs | Red | Only manual verification exists |
| 1.7 | Multi-turn conversation memory | Red | G-Brain MCP not wired into runtime flow |

## 2. Hero profiles

| # | Item | Status | Notes |
|---|---|---|---|
| 2.1 | Scribe — local budget/actual JSON files | Green | `partenon-core/tools/google_sheets.py` |
| 2.2 | Scribe — Google Sheets write | Yellow | Needs `GOOGLE_SERVICE_ACCOUNT_JSON` |
| 2.3 | Scribe — industry templates | Yellow | Food, consulting, legal, retail exist; construction/SaaS fall back |
| 2.4 | Herald — brand interview | Green | Writes `.design` JSON |
| 2.5 | Herald — content calendar | Green | Local generation only |
| 2.6 | Herald — publish to social | Red | No API dispatch implemented |
| 2.7 | Collector — local payment link/invoice | Green | Stripe object shape, no network call |
| 2.8 | Collector — live Stripe payment links | Yellow | Needs `STRIPE_SECRET_KEY` |
| 2.9 | Collector — live Stripe subscriptions | Yellow | Needs `STRIPE_SECRET_KEY` |
| 2.10 | Guardian — key inventory | Green | `security_tools.py` |
| 2.11 | Guardian — automated key rotation | Red | Not implemented |
| 2.12 | Strategist — project + task + checklist | Green | `ops/tools/projects.py`, `tasks.py`, `checklists.py` |
| 2.13 | Strategist — morning briefing | Green | Combines files from other heroes |
| 2.14 | Diplomat — client/vendor/milestone | Green | `relations/tools/crm.py` |
| 2.15 | Diplomat — automated follow-up reminders | Green | Stored in local JSON; no external calendar dispatch |
| 2.16 | Brain — G-Brain memory lookup | Red | MCP available but not invoked in flows |

## 3. Integrations

| # | Item | Status | Notes |
|---|---|---|---|
| 3.1 | Google Sheets | Yellow | Service-account JSON required |
| 3.2 | Google Docs | Red | Not implemented |
| 3.3 | Google Slides | Red | Not implemented |
| 3.4 | Google Drive | Red | Not implemented |
| 3.5 | Gmail send | Red | Not implemented |
| 3.6 | Google Calendar | Red | Not implemented |
| 3.7 | Stripe payments | Yellow | Secret key required |
| 3.8 | Stripe webhooks | Red | Not implemented |
| 3.9 | G-Brain memory | Red | MCP exists; runtime wiring missing |
| 3.10 | Social media APIs | Red | Not implemented |

## 4. Onboarding

| # | Item | Status | Notes |
|---|---|---|---|
| 4.1 | `config/company.yaml` example documented | Green | `.env.example` lists vars; no `company.yaml` exists yet |
| 4.2 | Brand interview script | Green | `brand_intake.py` |
| 4.3 | First-week sequence by business type | Green | `docs/ENTREPRENEUR_PLAYBOOK.md` |
| 4.4 | Workshop simulations | Green | `workshop/simulations/` |
| 4.5 | Facilitator agenda | Green | `workshop/AGENDA.md` |
| 4.6 | Facilitator slides | Green | `workshop/SLIDES.md` |
| 4.7 | Participant handout | Green | `workshop/HANDOUT.md` |

## 5. Testing and quality

| # | Item | Status | Notes |
|---|---|---|---|
| 5.1 | Unit tests for tools | Red | No automated test suite |
| 5.2 | Simulation runner | Green | `workshop/simulations/sim_runner.py` |
| 5.3 | Linter / formatter | Yellow | No project-wide config; hooks may format |
| 5.4 | Type checking | Red | Python code is untyped; Next.js uses TypeScript |
| 5.5 | Dashboard smoke test | Yellow | `npm run build` covers build; no runtime tests |

## 6. Documentation

| # | Item | Status | Notes |
|---|---|---|---|
| 6.1 | README accurate | Green | Describes install and current scope |
| 6.2 | HERO_GUIDE complete | Green | `docs/HERO_GUIDE.md` |
| 6.3 | ENTREPRENEUR_PLAYBOOK complete | Green | `docs/ENTREPRENEUR_PLAYBOOK.md` |
| 6.4 | MISSING_IMPLEMENTATION maintained | Green | Updated during this workshop |
| 6.5 | TODOS.md maintained | Green | Updated after each session |

## 7. Security

| # | Item | Status | Notes |
|---|---|---|---|
| 7.1 | `.env.example` has placeholders only | Green | No real secrets |
| 7.2 | Sensitive files in `.gitignore` | Green | `.env`, `.kimi/`, `node_modules/`, etc. |
| 7.3 | API keys stored outside repo | Yellow | Tools read env vars; no validation of secure storage |
| 7.4 | Encryption at rest | Red | Local JSON files are unencrypted |
| 7.5 | RBAC / user permissions | Red | No multi-user access control |

---

## How to score a business

1. Run the simulation for the closest case study.
2. Walk the checklist and mark every item.
3. Count greens, yellows, and reds.
4. A business can go live when all items in sections 1, 2, and 7 are green or yellow with an owner and deadline.
5. Red items are engineering tasks. Do not promise founders a delivery date for red items.

## Suggested first live use

For most small businesses, the green/yellow combination supports:

- Local bookkeeping and planning
- Project and task management
- Client/vendor tracking
- Invoice/payment-link drafting
- Brand and content planning

Live payments and Google Sheets require credentials. Full automation across Gmail, calendar, and social posting requires additional engineering.
