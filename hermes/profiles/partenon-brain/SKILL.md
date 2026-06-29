# Partenon Brain — Memory Skill Pack

> Memory and collective intelligence keeper for Partenon.
> Indexes learnings, resolves context conflicts, and feeds onboarding for the other heroes.

## Included skills

### `memory`
- Store and retrieve pages in G-Brain.
- Search missions, entities, and historical decisions.
- Detect contradictions across hero outputs.
- Orchestrate shared context and daily memory sync.

## Quick start

1. Copy `.env.example` to `.env` and fill in credentials.
2. Copy `templates/.brain.example` to your workspace as `.brain`.
3. Use `mcp_servers.memory.server` as the `partenon-memory` MCP server.
4. Run `skills/memory/tools/sync.py` to execute the daily memory sync.

## Safety rules

- Never index sensitive data such as API keys or passwords.
- Always tag learnings with author profile and date.
- Surface contradictions to the Strategist, never silently override them.

## MCP Tools

The Brain exposes the `partenon-memory` MCP server. Available tools:

- `gbrain_read_profile`
- `gbrain_write_profile`
- `gbrain_write_mission`
- `gbrain_search_missions`
- `gbrain_search_entities`
- `gbrain_store_learning`
- `memory_put_page`
- `memory_get_page`
- `memory_search`
- `memory_link`
- `memory_conflicts`

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|---|---|---|
| `gbrain_read_profile` | Reads from local cache if available | `GBRAIN_DATABASE_URL` |
| `gbrain_write_profile` | Simulates write; returns preview | `GBRAIN_DATABASE_URL` |
| `gbrain_write_mission` | Simulates write; returns preview | `GBRAIN_DATABASE_URL` |
| `gbrain_search_missions` | Searches local cache | `GBRAIN_DATABASE_URL` |
| `gbrain_search_entities` | Searches local cache | `GBRAIN_DATABASE_URL` |
| `gbrain_store_learning` | Simulates write; returns preview | `GBRAIN_DATABASE_URL` |
| `memory_put_page` | Simulates write; returns preview | `GBRAIN_DATABASE_URL` |
| `memory_get_page` | Reads from local cache | `GBRAIN_DATABASE_URL` |
| `memory_search` | Searches local cache | `GBRAIN_DATABASE_URL` |
| `memory_link` | Simulates link creation | `GBRAIN_DATABASE_URL` |
| `memory_conflicts` | Runs conflict detection on local cache | `GBRAIN_DATABASE_URL` |
