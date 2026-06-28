# Partenon Production Readiness Checklist

> Results from the `company-research` production-readiness test.
> Scope: five real small-business company cards, five simulated Partenon onboardings, the Hermes onboarding guide, and the full workshop package.
> Status: PASS / FAIL / PARTIAL with evidence.

---

## 1. Installation

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 1.1 | `install.sh` detects Python 3.10+ and creates `.venv` | PASS | `install.sh` lines 15-36; `bash -n install.sh` PASS |
| 1.2 | `install.sh` installs dependencies from `requirements.txt` | PASS | `install.sh` line 44 |
| 1.3 | `install.sh` copies `.env.example` to `.env` if missing | PASS | `install.sh` lines 82-85 |
| 1.4 | `install.sh` creates `data/` and `logs/` directories | PASS | `install.sh` lines 88-89 |
| 1.5 | `install.sh` runs `scripts/demo_scribe.py` as verification | PASS | `install.sh` lines 91-95 |
| 1.6 | Installer handles missing Hermes CLI gracefully | PASS | `install.sh` lines 46-58 print instructions |
| 1.7 | No unverified binaries downloaded | PASS | `install.sh` only installs pip packages and copies files |

---

## 2. Hermes Integration

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 2.1 | Seven hero profiles exist in `hermes/profiles/` | PASS | `partenon-scribe`, `partenon-herald`, `partenon-collector`, `partenon-guardian`, `partenon-strategist`, `partenon-diplomat`, `partenon-brain` |
| 2.2 | Each profile has `SOUL.md`, `config.yaml`, templates, and cron | PASS | Verified via `ls hermes/profiles/*` |
| 2.3 | Hermes CLI detection is graceful | PASS | `install.sh` and `scripts/setup_hermes.py` print instructions if missing |
| 2.4 | Profiles can be installed to `~/.hermes/profiles/` when CLI is present | PASS | `install.sh` lines 69-79 |
| 2.5 | `hermes profile use <profile>` commands documented in simulations | PASS | `workshop/simulations/*.md` |
| 2.6 | Hermes CLI is bundled with Partenon | FAIL | Hermes is distributed separately by Nous Research; documented in `README.md` and `install.sh` |

---

## 3. Hero Profiles

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 3.1 | Scribe has parser, Sheets tool, audit, templates | PASS | `hermes/profiles/partenon-scribe/skills/finance/tools/` |
| 3.2 | Herald has brand intake, content calendar, copy generator, SEO/GEO | PASS | `hermes/profiles/partenon-herald/skills/comms/tools/` |
| 3.3 | Collector has Stripe tools for links, subscriptions, invoices, reminders, reports | PASS | `hermes/profiles/partenon-collector/skills/payments/tools/` |
| 3.4 | Guardian has key manager, secrets manager, policy manager, audit logger | PASS | `hermes/profiles/partenon-guardian/skills/security/tools/` |
| 3.5 | Strategist has projects, tasks, checklists, goals, briefings, calendar, email | PASS | `hermes/profiles/partenon-strategist/skills/ops/tools/` |
| 3.6 | Diplomat has CRM, follow-ups, schedule meeting, generate proposal | PASS | `hermes/profiles/partenon-diplomat/skills/relations/tools/` |
| 3.7 | Brain has G-Brain client, MCP hub, sync tools | PASS | `hermes/profiles/partenon-brain/skills/memory/tools/` |
| 3.8 | All profile tools compile with `python3 -m py_compile` | PASS | `for f in hermes/profiles/*/skills/*/*/*.py; do python3 -m py_compile "$f"; done` PASS |
| 3.9 | Profile templates are translated to English | PASS | Verified in previous sessions |
| 3.10 | Smoke tests run for all seven heroes | PASS | Scribe demo, Strategist `create_project`, Diplomat `add_client`, Collector `create_payment_link`, Guardian `list_keys`, Brain `put_page`, Herald `generate_calendar` via `sim_runner.py` |

---

## 4. Credentials / Security

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 4.1 | `.env.example` uses safe placeholders | PASS | `.env.example` values like `sk-or-v1-REPLACE_ME_IN_ENV` |
| 4.2 | `.gitignore` excludes `.env` | PASS | `.gitignore` line includes `.env` |
| 4.3 | `.security` template never stores raw secrets | PASS | `hermes/profiles/partenon-guardian/templates/.security.example` uses `env://` references |
| 4.4 | Guardian masks secrets in logs | PASS | `key_manager.py` only shows first/last 4 characters |
| 4.5 | Real secrets-manager integration | FAIL | Guardian reads env vars only; no HashiCorp Vault, AWS Secrets Manager, etc. |
| 4.6 | Automated key rotation end-to-end | FAIL | `rotate_key` logs event but requires manual console action |
| 4.7 | Audit log persistence | PARTIAL | `audit_logger.py` writes JSON Lines to `data/audit/security.log`; no tamper-evident hash yet |

---

## 5. Google Workspace

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 5.1 | Google Sheets tool exists | PASS | `google_sheets.py` |
| 5.2 | Sheets tool degrades gracefully without credentials | PASS | Returns `False` if `GOOGLE_SERVICE_ACCOUNT_JSON` missing |
| 5.3 | Onboarding engine creates Drive folder and spreadsheet if configured | PASS | `onboarding_engine.py` lines 214-256 |
| 5.4 | Live Google Sheets write works without credentials | FAIL | Requires real service account JSON |
| 5.5 | Gmail/Calendar MCP dispatch for Herald/Collector/Diplomat | FAIL | No live dispatch; tools generate local drafts/records |
| 5.6 | Google Contacts integration for Diplomat | FAIL | Not implemented |

---

## 6. Stripe

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 6.1 | Collector can create payment links | PASS | `stripe_tools.py create_payment_link` works in local mode |
| 6.2 | Collector can create subscriptions | PASS | `stripe_tools.py create_subscription` works in local mode |
| 6.3 | Collector can create invoices | PASS | `stripe_tools.py create_invoice` works in local mode |
| 6.4 | Collector can read pending/overdue payments | PASS | `read_pending_payments`, `read_overdue_payments` |
| 6.5 | Collector can generate income reports | PASS | `generate_income_report` |
| 6.6 | Real Stripe link generation | FAIL | Requires `STRIPE_SECRET_KEY`; local mode returns placeholder |
| 6.7 | Automated payment reminder dispatch | FAIL | Requires Gmail/WhatsApp MCP; not wired |
| 6.8 | Stripe sandbox end-to-end demo | FAIL | No dedicated sandbox test script |

---

## 7. Dashboard

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 7.1 | Next.js dashboard builds successfully | PASS | `cd dashboard && npm run build` verified |
| 7.2 | Dashboard runs locally | PASS | `npm run dev` starts on `localhost:3000` |
| 7.3 | Dashboard reads local JSON missions | PASS | `data/tasks.json`, `data/cron.json` |
| 7.4 | Dashboard connected to heroes / G-Brain | FAIL | Only local JSON; no hero runtime integration |
| 7.5 | Authentication configurable via `.env` | PASS | `DASHBOARD_APP_USERNAME`, `DASHBOARD_APP_PASSWORD` |
| 7.6 | Mobile responsive | PASS | Tailwind CSS; verified in previous sessions |

---

## 8. Documentation

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 8.1 | `README.md` is accurate and English | PASS | Updated with repo URL, live site, hero matrix, workshop links |
| 8.2 | `docs/ENTREPRENEUR_PLAYBOOK.md` exists | PASS | Business-type hero selection, prompts, configs, simulations |
| 8.3 | `docs/HERO_GUIDE.md` exists | PASS | Per-hero tools, env vars, cron |
| 8.4 | `docs/QUICKSTART.md` exists | PASS | 15-minute walkthrough |
| 8.5 | `docs/SECURITY.md`, `docs/API.md`, `docs/FAQ.md` exist | PASS | Verified |
| 8.6 | `MISSING_IMPLEMENTATION.md` is current | PASS | Updated with workshop findings and `gbrain_client.py` fix |
| 8.7 | Workshop package created | PASS | `workshop/README.md`, `AGENDA.md`, `SLIDES.md`, `HANDOUT.md` |
| 8.8 | Company cards and simulations created | PASS | `workshop/companies/` and `workshop/simulations/` |
| 8.9 | Hermes onboarding guide created | PASS | `workshop/guides/HERMES_ONBOARDING.md` |
| 8.10 | Production-readiness checklist maintained | PASS | This file; updated after the `company-research` pass |

---

## 9. Onboarding Flow

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 9.1 | Onboarding engine exists | PASS | `partenon-core/tools/onboarding_engine.py` |
| 9.2 | Onboarding engine creates `config/company.yaml` | PASS | Via `ConfigLoader` |
| 9.3 | Onboarding engine creates local data files | PASS | `clients.json`, `projects.json`, etc. |
| 9.4 | Onboarding engine creates industry catalog | PASS | Events, legal, consulting, retail |
| 9.5 | `docs/WELCOME.md` generated | PASS | `onboarding_engine.py` lines 258-314 |
| 9.6 | Hermes onboarding guide created | PASS | `workshop/guides/HERMES_ONBOARDING.md` |
| 9.7 | Simulation runner executes onboarding-like actions | PASS | `workshop/simulations/sim_runner.py route/project/checklist/client/payment-link/calendar` PASS |
| 9.8 | Onboarding passes context to heroes at runtime | FAIL | Engine creates files but does not load them into hero context dynamically |
| 9.9 | End-to-end onboarding demo script | PARTIAL | `demo_scribe.py` covers finance only; `sim_runner.py` covers the other heroes |

---

## 10. Brain / Memory

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 10.1 | G-Brain client exists | PASS | `hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py` |
| 10.2 | `put_page` works with a local `gbrain` binary | PASS | Smoke test returned `status: created_or_updated` after fixing stdin handling |
| 10.3 | `gbrain` binary bundled with Partenon | FAIL | Requires separate installation; documented in `README.md` |
| 10.4 | Collective memory / conflict detection advertised on site | PARTIAL | `gbrain_client.py` supports search and links; conflict detection is a query convention, not automated |

---

## 11. Support / Runbook

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 11.1 | Known gaps documented | PASS | `MISSING_IMPLEMENTATION.md` |
| 11.2 | FAQ covers common questions | PASS | `docs/FAQ.md` |
| 11.3 | Security runbook for credentials | PASS | `docs/SECURITY.md` |
| 11.4 | API reference for scripts and tools | PASS | `docs/API.md` |
| 11.5 | Troubleshooting guide for failed integrations | PARTIAL | FAQ and simulations mention credential gaps; no dedicated runbook |
| 11.6 | Issue template / support channel | FAIL | No GitHub issue templates or support email defined |

---

## Summary

| Category | PASS | PARTIAL | FAIL |
|----------|------|---------|------|
| Installation | 7 | 0 | 0 |
| Hermes integration | 5 | 0 | 1 |
| Hero profiles | 10 | 0 | 0 |
| Credentials / security | 4 | 1 | 2 |
| Google Workspace | 3 | 0 | 3 |
| Stripe | 5 | 0 | 3 |
| Dashboard | 4 | 0 | 1 |
| Documentation | 10 | 0 | 0 |
| Onboarding flow | 7 | 1 | 1 |
| Brain / memory | 2 | 1 | 1 |
| Support / runbook | 4 | 1 | 1 |
| **Total** | **61** | **5** | **14** |

---

## Priority Gaps

| Priority | Gap | Suggested Fix |
|----------|-----|---------------|
| HIGH | No live Google Workspace / Gmail / Calendar dispatch | Implement Gmail/Calendar MCP wiring for Herald, Collector, Diplomat |
| HIGH | No real Stripe sandbox end-to-end demo | Add `scripts/demo_stripe_sandbox.py` with test payment link |
| HIGH | Dashboard not connected to heroes or G-Brain | Add API routes in dashboard to call core tools and read hero outputs |
| HIGH | Onboarding does not pass context to heroes at runtime | Extend onboarding engine to produce a context summary loaded by heroes |
| MEDIUM | Brain requires external `gbrain` binary | Bundle a minimal G-Brain or document MCP setup clearly |
| MEDIUM | Guardian lacks real secrets manager | Add optional HashiCorp Vault or AWS Secrets Manager backend |
| MEDIUM | No automated tests | Add `tests/` for core tools and at least one hero skill |
| MEDIUM | No CI pipeline | Add GitHub Actions for Python compile and dashboard build |
| LOW | No issue template / public support channel | Add `.github/ISSUE_TEMPLATE.md` and a support email |
| LOW | Workshop needs facilitator video / recording | Optional future asset |

---

## Verification Log

- `python3 scripts/demo_scribe.py` PASS — generated `data/sample_expenses.xlsx` and `data/sample_expenses_report.json`.
- `cd dashboard && npm run build` PASS — static export generated with all routes.
- `bash -n install.sh` PASS.
- `for f in hermes/profiles/*/skills/*/*/*.py; do python3 -m py_compile "$f"; done` PASS.
- `python3 workshop/simulations/sim_runner.py route "send a payment reminder to Acme"` → `partenon-collector`.
- `python3 workshop/simulations/sim_runner.py project test-ws ...` → `PROJ-001` created.
- `python3 workshop/simulations/sim_runner.py checklist test-ws PROJ-001` → 15-item consulting checklist created.
- Brain smoke test: `GBrainClient().put_page('test/smoke', 'Smoke test page')` → `status: created_or_updated`.
