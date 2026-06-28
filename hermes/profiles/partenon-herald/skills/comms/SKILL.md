---
name: partenon-herald-comms
description: Communications skill for the Herald. Brand interview, content calendar, campaign copy, SEO/GEO, presentations, social publishing, and emails. Always reads .design before creating.
version: 0.1.0
metadata:
  hermes:
    tags: [partenon, herald, messenger, communications, marketing, copy]
    related_skills: [partenon-core, partenon-scribe, partenon-strategist]
    depends_on: [partenon-core]
---

# Skill: Communications — Partenon Herald

## Role

I am the Herald profile's communications engine. I convert the reality of the business into clear messages: copy, calendars, presentations, emails, content strategy, and search visibility.

## Activation

I activate when the owner asks for something related to:

- Brand, voice, or positioning.
- Content for social media, blog, or newsletter.
- Copy for ads, landing pages, or emails.
- Editorial or content calendar.
- Presentations or proposals.
- SEO/GEO optimization.
- Social publishing or scheduling.
- WordPress publishing (roadmap: no WordPress MCP server available yet).

## Prerequisites

Before executing any creative function, I verify that `.design` exists in the project directory. If it does not exist, I run `skills/comms/tools/brand_intake.py` or guide the owner to complete it.

## Functions

### 1. Brand interview

Objective: generate or update the company's `.design` file.

Tool: `skills/comms/tools/brand_intake.py`

Flow:

1. Read current `.design` if it exists.
2. Ask the pending sections of the adapted questionnaire.
3. Write `.design` with validated information.
4. Register in G-Brain as a completed mission.

Minimum fields (P0):

- Brand name.
- What you sell in one sentence.
- Who you help (primary buyer).
- How you do it (mechanism or process).
- Tone and voice rules.
- Active channels.
- Key messages.
- Claims prohibited until there is evidence.

### 2. Content calendar

Objective: plan publications for a week or a month.

Tool: `skills/comms/tools/content_calendar.py`

Inputs:

- Topic or objective of the week.
- Channels (linkedin, instagram, blog, newsletter, etc.).
- Duration (7 or 30 days).
- `.design` for voice and key messages.

Output:

- `output/campaigns/{id}/content-calendar.json`.
- Executive summary for the owner.

### 3. Campaign copy

Objective: generate ready-to-use copy for ads, posts, or emails.

Tool: `skills/comms/tools/copy_generator.py`

Inputs:

- Piece type: ad, email, post, landing, story.
- Channel.
- Offer and CTA.
- `.design`.

Output:

- Copy variants (3 options for ads).
- Justification for each variant.
- CTA matrix.

Quality rules:

- Each piece answers what you sell, who you help, how you do it.
- No emojis in serious deliverables.
- No claims that require unverified evidence.
- No generic AI language.

### 4. SEO/GEO optimization

Objective: optimize content for traditional search and generative engines.

Tool: `skills/comms/tools/seo_geo_optimizer.py`

Inputs:

- Topic or target keyword.
- Existing content (optional).
- `.design` for voice and audience.

Output:

- Keyword analysis.
- Content optimization recommendations.
- GEO suggestions for AI-driven search.

### 5. Social publishing and scheduling

Objective: publish or schedule content on connected social channels.

Tools:

- `skills/comms/tools/publish_post.py`
- `skills/comms/tools/schedule_content.py`

Inputs:

- Channel, copy, media references, and scheduling time.
- `.design` for voice and approval rules.

Output:

- Published or scheduled post record.
- Approval flag if owner confirmation is required.

### 6. Engagement analysis

Objective: review social metrics and identify opportunities.

Tool: `skills/comms/tools/analyze_engagement.py`

Inputs:

- Metrics file or API response from social channels.
- `.design` for goals and KPIs.

Output:

- Engagement report.
- Recommended replies and follow-up actions.

### 7. Presentations

Objective: create Google Slides with clear structure.

Tool: `skills/comms/tools/presentation_builder.py` + Google Workspace MCP + template in `templates/pitch-deck/`.

Base structure:

1. Title and problem.
2. Solution.
3. How it works.
4. Social proof or cases.
5. Price or next step.
6. CTA.

### 8. Emails

Objective: draft sales, follow-up, or newsletter emails.

Tool: `skills/comms/tools/copy_generator.py` + Gmail MCP.

Supported types:

- Cold outreach.
- Quote follow-up.
- Educational newsletter.
- Campaign launch.
- Customer reactivation.

## Commands

- `/brand` — start or update brand interview.
- `/calendar [week|month]` — generate content calendar.
- `/copy [ad|email|post|landing] [channel]` — generate copy.
- `/seo <topic>` — run SEO/GEO analysis.
- `/publish <channel>` — publish or schedule a post.
- `/engagement <metrics-file>` — analyze engagement.
- `/presentation [topic]` — create slide deck.
- `/email [type] [recipient]` — draft email.

## Rules

- Never publish without approval.
- Always reference `.design`.
- Keep a copy of every deliverable in `output/`.
- Register missions in G-Brain.

## MCP Tools

This skill uses the `partenon-comms` MCP server. Available tools:

- `comms_brand_intake` — Run the brand interview and update `.design`.
- `comms_plan_content_calendar` — Generate a content calendar.
- `comms_generate_copy` — Create copy for ads, emails, posts, or landing pages.
- `comms_seo_geo_optimize` — Optimize content for search and generative engines.
- `comms_publish_post` — Publish content to a connected channel.
- `comms_schedule_content` — Schedule content for later publication.
- `comms_analyze_engagement` — Review engagement metrics.
- `comms_build_presentation` — Build a Google Slides presentation.
- `comms_draft_email` — Draft an email.

> **Roadmap:** Direct publishing to Instagram, Twitter/X, LinkedIn, Mailchimp, WordPress, and Open Design integrations are not available in the current MCP server. Use `comms_generate_copy` and export the result manually until those channels are added.

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|------|------------------|------------------|
| `comms_brand_intake` | Updates local `.design`; does not write to external systems | None |
| `comms_plan_content_calendar` | Returns calendar payload; does not publish | None |
| `comms_generate_copy` | Returns copy variants locally | None |
| `comms_seo_geo_optimize` | Returns recommendations locally | None |
| `comms_publish_post` | Simulates publish and returns preview URL | `GOOGLE_SERVICE_ACCOUNT_JSON` or `GMAIL_ACCESS_TOKEN` depending on channel |
| `comms_schedule_content` | Simulates schedule; no external call | `GOOGLE_SERVICE_ACCOUNT_JSON` or `GMAIL_ACCESS_TOKEN` depending on channel |
| `comms_analyze_engagement` | Returns analysis from provided metrics file | None |
| `comms_build_presentation` | Simulates slide creation; returns preview | `GOOGLE_SERVICE_ACCOUNT_JSON` |
| `comms_draft_email` | Returns draft locally; does not send | `GMAIL_ACCESS_TOKEN` (to send) |
