# Partenon Capabilities

> Single source of truth for what Partenon can do today, what requires credentials, and what is on the roadmap.

Last updated: 2026-06-29

---

## Legend

- ✅ **Live** — works immediately after install.
- ⚡ **Requires credentials** — works after you provide your own API keys or service accounts.
- 🗓️ **Roadmap** — not yet implemented.
- 🧪 **Beta** — implemented but still being stabilized.

---

## Core Platform

| Capability | Status | Notes |
|------------|--------|-------|
| Install via Hermes CLI | ✅ Live | `hermes profile install github.com/owner/partenon` |
| Seven hero profiles | ✅ Live | Scribe, Herald, Collector, Guardian, Strategist, Diplomat, Brain |
| Dry-run mode | ✅ Live | No credentials required; works with local templates |
| Hermes-native skills | ✅ Live | Routing, onboarding, eval hooks |
| G-Brain memory | ✅ Live | SQLite default; Postgres optional |
| Profile validation | ✅ Live | `scripts/validate_profiles.py` |

---

## Heroes

| Hero | Dry-run | Live | Notes |
|------|---------|------|-------|
| Scribe | ✅ | ⚡ Google Workspace | Finance reports and expense classification |
| Herald | ✅ | ⚡ Google Workspace + social tokens | Copy, content calendar, presentations |
| Collector | ✅ | ⚡ Stripe | Payment links, invoices, subscriptions |
| Guardian | ✅ | ⚡ Secret manager (optional) | Key audit, model recommendations |
| Strategist | ✅ | ⚡ Google Workspace + Slack | Projects, tasks, calendar |
| Diplomat | ✅ | ⚡ Google Workspace + CRM | Contacts, follow-ups, proposals |
| Brain | ✅ | ✅ SQLite / ⚡ Postgres | Memory, learnings, context |

---

## Integrations

| Integration | Status | Notes |
|-------------|--------|-------|
| Google Workspace (Sheets, Docs, Slides, Drive, Calendar, Gmail, Contacts) | ⚡ | Service account or OAuth setup required |
| Stripe | ⚡ | Test mode supported; live keys opt-in |
| Gmail | ⚡ | Via Google Workspace MCP |
| Google Calendar | ⚡ | Via Google Workspace MCP |
| Slack | ⚡ | Bot token required |
| Telegram | ⚡ | Hermes gateway + bot token |
| Email (SMTP/IMAP) | ⚡ | Hermes gateway |
| Discord | 🗓️ | Planned |
| WhatsApp | 🗓️ | Meta Business API approval required |
| Calendly | 🗓️ | Optional scheduling integration |
| HubSpot / Salesforce | 🗓️ | CRM sync |
| WordPress | 🗓️ | Publishing integration |
| Shopify | 🗓️ | Order/inventory import |
| AWS Cost Explorer | 🗓️ | Cost and runway tracking |

---

## Messaging / Gateway

| Capability | Status | Notes |
|------------|--------|-------|
| Telegram commands | ⚡ | Requires bot token and allowlist |
| Email commands | ⚡ | Requires SMTP/IMAP |
| Discord commands | 🗓️ | Planned |
| WhatsApp commands | 🗓️ | Roadmap |
| File attachments (CSV, PDF, images) | 🧪 | CSV → Scribe, image → Herald, PDF → Diplomat/Brain |
| Chat-based onboarding | 🧪 | Progressive credential setup |

---

## Dashboard

| Capability | Status | Notes |
|------------|--------|-------|
| Mission board | ✅ | Local JSON mode today |
| Hero status page | ✅ | Local JSON mode today |
| Cron manager | ✅ | Local JSON mode today |
| Real-time mission updates | 🗓️ | FastAPI + SSE planned |
| Integration health | 🗓️ | Planned |
| Multi-tenancy | 🗓️ | Roadmap |

---

## Advanced / NVIDIA

| Capability | Status | Notes |
|------------|--------|-------|
| Multi-model routing via OpenRouter | ✅ | Configurable per hero |
| NVIDIA model recommendations | ⚡ | Guardian can query NVIDIA/OpenRouter catalogs |
| NVIDIA NemoClaw / OpenShell sandbox | 🗓️ | Experimental; not a core dependency |

---

## How to Update This File

1. Change status in this markdown file.
2. Update `web/capabilities.html` manually once it exists (planned in Phase 7).
3. Commit both files together.

This file is the source of truth until the website status page is generated from it.
