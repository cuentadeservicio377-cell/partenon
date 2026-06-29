---
name: gateway
description: Hermes gateway skill for Partenon. Parses commands, routes attachments, enforces group and rate-limit guards, and drives the progressive onboarding conversation.
version: 0.1.0
metadata:
  hermes:
    auto_load: true
    tags: [gateway, telegram, email, routing, onboarding, guard]
    related_skills: [partenon-core, finance, comms, payments, security, ops, relations, memory]
    status: draft
---

# Skill: Gateway — Partenon v0.1

## Role

I am the Partenon gateway. I sit between users (Telegram, Email) and the seven hero profiles. I decide who handles every message, file, or onboarding reply.

## Activation

I activate when:
- A user sends a direct command like `/scribe classify expense 120 USD lunch`.
- A user sends an alias like `/s classify expense 120 USD lunch`.
- A user sends a free-form message with no prefix.
- A user uploads a file (CSV, image, PDF, text, etc.).
- A user starts or continues the onboarding conversation.
- A request arrives in a group chat and must be validated.

## Python tools

### `tools/parse_command.py`
- `parse_command(message)` — Detects `/profile action args...` and aliases; falls back to `route_intent` for free-form messages.

### `tools/route_attachment.py`
- `route_attachment(file_name, mime_type, context)` — Routes uploaded files to the right profile based on type and filename hints.

### `tools/check_guard.py`
- `check_guard(user_id, message, is_group, bot_username)` — Enforces allowlists, group-mention rules, and per-user rate limits.

### `tools/onboarding_reply.py`
- `onboarding_reply(user_id, text)` — Runs the progressive onboarding state machine and persists state in `partenon-memory`.

## Command namespace

| Prefix | Alias | Profile | Example |
|--------|-------|---------|---------|
| `/scribe` | `/s` | `partenon-scribe` | `/s classify expense 100 USD office supplies` |
| `/herald` | `/h` | `partenon-herald` | `/h create campaign Q3 launch` |
| `/collector` | `/c` | `partenon-collector` | `/c generate payment link 500 USD` |
| `/guardian` | `/g` | `partenon-guardian` | `/g rotate openai key` |
| `/strategist` | `/st` | `partenon-strategist` | `/st create project Website redesign` |
| `/diplomat` | `/d` | `partenon-diplomat` | `/d follow up with client Acme Inc` |
| `/brain` | `/b` | `partenon-brain` | `/b remember we invoice on net-15` |

## Attachment routing rules

| Type | Profile | Action |
|------|---------|--------|
| `csv`, `xlsx`, `ods` | `partenon-scribe` | `process_attachment` |
| `png`, `jpg`, `webp`, `gif` | `partenon-herald` | `process_attachment` |
| `pdf` with `contract/proposal/invoice` in name | `partenon-diplomat` | `process_attachment` |
| Other `pdf` | `partenon-brain` | `process_attachment` |
| `txt`, `md`, `json` | `partenon-brain` | `process_attachment` |
| Unknown | `partenon-brain` | `process_attachment` |

## Guard rules

- `GATEWAY_ALLOWED_USERS` or `TELEGRAM_ALLOWED_USERS` must contain the user ID; otherwise the request is denied by default.
- In group chats the message must mention the bot (`@botname` or `@<bot_username>`).
- Each user is rate-limited to 30 calls per minute.

## Onboarding flow

1. `welcome` — Greeting and consent.
2. `company_name` — Ask for the company name.
3. `industry` — Ask for the industry.
4. `team_size` — Ask for the team size.
5. `main_pain` — Ask for the main operational pain.
6. `confirm` — Summarize and ask for confirmation.
7. `done` — Write `config/company.yaml`, run `OnboardingEngine`, create first missions, and return a summary.

State is persisted in `partenon-memory` under slug `onboarding/{user_id}`.

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|------|------------------|------------------|
| `parse_command` | Always local | None |
| `route_attachment` | Returns target profile; no file read | None |
| `check_guard` | Local allowlist/rate-limit check | Env vars for allowlists |
| `onboarding_reply` | Persists state in memory; on `done` writes local files | `GBRAIN_DATABASE_URL` or SQLite default |
