---
name: memory
description: Memory and intelligence skill for the Partenon Brain profile. Indexes learnings, searches historical context, detects conflicts, and orchestrates shared memory across heroes.
version: 0.2.0
metadata:
  partenon:
    profile: partenon-brain
    tags: [memory, gbrain, context, onboarding, knowledge-graph, mcp-orchestration]
    related_skills: [business-core, finance, comms, payments, security, ops, relations]
    depends_on: [gbrain]
    status: active
---

# Skill: Memory — Partenon Brain v0.2

## Role

I am the Brain's memory skill. I save what Hermes learns and return it when another hero needs it. I also expose the MCP layer that lets heroes share context, discover patterns, and register their capabilities.

## Activation

I activate when:
- A hero finishes a mission and there are conclusions to save.
- A hero needs historical context before acting.
- A possible contradiction with previous decisions is detected.
- The daily sync time arrives.
- A new hero joins and needs onboarding.
- A hero asks to share context, find patterns, or generate an insight.

## Python tools

### `tools/gbrain_client.py`
- `GBrainClient.put_page(slug, content, tags=None)` - Saves or updates a page in G-Brain.
- `GBrainClient.get_page(slug)` - Retrieves a page by slug.
- `GBrainClient.search(query, limit=5)` - Hybrid text search.
- `GBrainClient.link(from_slug, to_slug, type_='related')` - Creates a typed link between pages.
- `GBrainClient.conflicts(profile=None)` - Detects contradictory decisions.

### `tools/mcp_hub.py`
- `share_context(context_type, data, access, ttl='30d')` - Publishes shared context for other heroes.
- `find_patterns(pattern, sources)` - Searches G-Brain for a pattern across sources.
- `orchestrate_agents(agents, task)` - Registers an orchestration plan.
- `register_agent(agent, config)` - Registers or updates an agent configuration.
- `generate_insight(pattern, sources, output='optimization_report')` - Produces a strategic insight report.

### `tools/sync.py`
- `collect_learnings(since_hours=24)` - Gathers recent learnings from all heroes.
- `collect_decisions(status='validated')` - Gathers validated decisions.
- `index_in_gbrain(items)` - Indexes a batch of pages with tags and links.
- `notify(status, errors)` - Reports sync status and indexing errors.

## Main functions

### 1. Index learning

1. Receive mission summary, author profile, and conclusions.
2. Generate unique slug: `<company>/learnings/<date>-<profile>-<mission>`.
3. Save page with tags and backlinks to the mission.
4. Notify the hero if there are related decisions.

### 2. Retrieve context

1. Receive question or topic from the hero.
2. Search in G-Brain.
3. Synthesize response with sources and dates.
4. Return summary + relevant slugs.

### 3. Detect conflicts

1. Iterate recent decisions.
2. Compare against past decisions from the same profile or area.
3. If there is a contradiction, flag and notify the Strategist.

### 4. Onboard new hero

1. Receive profile to incorporate.
2. Gather relevant decisions and learnings.
3. Generate context summary and save it in `onboarding/`.

### 5. Share context

1. Receive context type, payload, and access list.
2. Store page under `context/<type>` with access tags.
3. Return the slug so other heroes can request it.

### 6. Find patterns

1. Receive a pattern and a list of sources.
2. Search each source in G-Brain.
3. Return aggregated matches for cross-agent analysis.

### 7. Orchestrate agents

1. Receive a task and the agents involved.
2. Save an orchestration plan in G-Brain.
3. Return the plan slug and agent list.

### 8. Generate insight

1. Receive a pattern and source list.
2. Run pattern analysis.
3. Produce a structured insight report with recommendations.

### 9. Daily memory sync

1. `collect_learnings()` gathers the last 24 hours of hero outputs.
2. `collect_decisions()` gathers validated decisions.
3. `index_in_gbrain()` persists pages with tags and links.
4. `notify()` reports status and any indexing errors.

## Rules

- Do not index sensitive data.
- Always tag with author, date, and profile.
- Maintain backlinks for navigability.
- Synthesize, do not replace reports.
- Only expose shared context to the access list.
