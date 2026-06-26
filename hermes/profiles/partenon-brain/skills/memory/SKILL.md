---
name: memory
description: Memory and intelligence skill for the Partenon Brain profile. Indexes learnings, searches historical context, and detects conflicts between decisions.
version: 0.1.0
metadata:
  partenon:
    profile: partenon-brain
    tags: [memory, gbrain, context, onboarding, knowledge-graph]
    related_skills: [business-core, finance, comms, payments, security, ops, relations]
    depends_on: [gbrain]
    status: draft
---

# Skill: Memory — Partenon Brain v0.1

## Role

I am the Brain's memory skill. I save what Hermes learns and return it when another hero needs it.

## Activation

I activate when:
- A hero finishes a mission and there are conclusions to save.
- A hero needs historical context before acting.
- A possible contradiction with previous decisions is detected.
- The daily sync time arrives.
- A new hero joins and needs onboarding.

## Python tools

### `tools/gbrain_client.py`
- `GBrainClient.put_page(slug, content, tags=None)` - Saves or updates a page in G-Brain.
- `GBrainClient.get_page(slug)` - Retrieves a page by slug.
- `GBrainClient.search(query, limit=5)` - Hybrid text search.
- `GBrainClient.link(from_slug, to_slug, type='related')` - Creates a link between pages.
- `GBrainClient.conflicts(profile=None)` - Detects contradictory decisions.

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

## Rules

- Do not index sensitive data.
- Always tag with author, date, and profile.
- Maintain backlinks for navigability.
- Synthesize, do not replace reports.
