# Partenon Architecture

## Overview

Partenon is an AI agent operating system organized as a pantheon of heroes. Each hero is a Hermes Agent (Nous Research) distribution with a personality, a role and a set of skills. All heroes share a memory brain (G-Brain of Garry Tan) and deliver results in Google Workspace.

## Design principles

1. **Hermes = company**: the user does not talk to a generic chatbot; they talk to their company represented by specialized agents.
2. **One hero, one territory**: each profile has clear responsibilities and does not invade another's territory.
3. **Shared memory**: every learning is indexed in G-Brain so future heroes have context.
4. **Delivery in familiar tools**: Sheets, Docs, Slides, Calendar, Gmail.
5. **Security by design**: the Guardian protects keys, models and access.

## Components

### 1. Partenon Core (`partenon_core/`)

- **Onboarding engine**: asks company type, needs and initial context.
- **Router**: assigns missions to the correct profile by intent and availability.
- **Workflow engine**: orchestrates missions that require collaboration between heroes.
- **Eval loop** (planned): measures output quality with a judge skill and a configurable threshold. Currently a stub.

### 2. Hermes profiles (`hermes/profiles/`)

Each profile includes:

- `SOUL.md`: identity and behavior rules.
- `config.yaml`: model, tools, MCP servers.
- `skills/<skill>/`: documentation and Python tools.
- `cron/`: scheduled tasks.
- `templates/`: configuration templates.

### 3. Dashboard (`dashboard/`)

A Next.js application that shows:

- KPIs per profile.
- Mission kanban.
- Cron job manager.
- Simple cookie auth.

### 4. Web pages (`web/`)

- `index.html`: marketing for founders.
- `heroes.html`: hero profiles.
- `developers.html`: technical documentation.

### 5. Memory (`gbrain/`)

- Local MCP server for G-Brain.
- Read/write profile pages.
- Hybrid search and relationship graph.

## Mission flow

```text
User
  │
  ▼
Hermes (active company profile)
  │
  ▼
partenon-core: router
  │
  ├──► Scribe      ──► Google Sheets
  ├──► Herald      ──► Google Docs / Slides / Social
  ├──► Collector   ──► Stripe API
  ├──► Guardian    ──► NVIDIA / OpenAI / Kimi keys
  ├──► Strategist  ──► Google Calendar / Tasks
  ├──► Diplomat    ──► Google Contacts / CRM
  └──► Brain       ──► G-Brain (memory)
```

## Communication between heroes

Heroes do not call each other directly. They communicate through:

1. **G-Brain**: each hero writes learnings and reads context.
2. **Google Workspace**: shared sheets, documents and calendar act as a visible board.
3. **partenon-core**: the workflow engine orchestrates multi-hero missions.

## Security

- The Guardian manages API keys and rotations.
- No profile exposes credentials in conversations.
- `.env` is never committed.
- Google Workspace uses a service account with minimum scopes.

## Scalability

- Each profile is independent and can run in its own container.
- G-Brain can migrate from local PGLite to Postgres/Supabase.
- The dashboard scales horizontally if a shared database is used.

## Key technologies

| Layer | Technology |
|-------|------------|
| Agent core | Hermes Agent (Nous Research) |
| Sandbox | NVIDIA NemoClaw + OpenShell |
| Models | NVIDIA Nemotron 3 Ultra, OpenAI, Kimi / Moonshot |
| Payments | Stripe API + Hermes Stripe Skills |
| Memory | G-Brain of Garry Tan (MCP) |
| Data | Google Workspace |
| Dashboard | Next.js 15 + React 19 + TypeScript |
| Docs/PDF | Python + WeasyPrint |
| Infra | Docker + Docker Compose |
