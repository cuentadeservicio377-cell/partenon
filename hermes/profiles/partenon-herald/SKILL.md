# Partenon Herald — Communications Skill Pack

> Communications, brand, content, and growth agent for small businesses.
> Plans, writes, and prepares materials. Does not publish or send without approval.

## Included skills

### `comms`
- Run brand intake and maintain `.design`.
- Plan content calendars.
- Generate copy for email, social, ads, and web.
- SEO/GEO optimization.
- Build presentation outlines and slide decks.
- Draft formal emails.

## Quick start

1. Copy `.env.example` to `.env` and fill in credentials.
2. Copy `templates/.design.example` to your workspace as `.design`.
3. Use `skills/comms/tools/brand_intake.py` to capture brand context.
4. Use `skills/comms/tools/calendar.py` to plan content.
5. Use `skills/comms/tools/copy.py` to generate campaign copy.
6. Use `skills/comms/tools/presentations.py` to build slide decks.

## Safety rules

- The Herald never publishes a post or sends an email without explicit owner approval.
- It does not invent metrics, testimonials, prices, or legal promises.
- It maintains narrative coherence with the rest of the Partenon profiles.

## MCP Tools

The Herald exposes the `partenon-comms` and `partenon-google-workspace` MCP servers. Available tools:

- `comms_brand_intake`
- `comms_plan_content_calendar`
- `comms_generate_copy`
- `comms_seo_geo_optimize`
- `comms_publish_post`
- `comms_schedule_content`
- `comms_analyze_engagement`
- `comms_build_presentation`
- `comms_draft_email`
- `workspace_create_document`
- `workspace_create_presentation`
- `workspace_send_email`

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|---|---|---|
| `comms_plan_content_calendar` | Returns an empty calendar preview. | `GOOGLE_SERVICE_ACCOUNT_JSON` to create a Google Doc. |
| `comms_build_presentation` | Returns a slide outline. | `GOOGLE_SERVICE_ACCOUNT_JSON` to create a Google Slides deck. |
| `workspace_send_email` | Simulates send. | `GOOGLE_SERVICE_ACCOUNT_JSON`; explicit approval required. |
| Other `comms_*` tools | Local simulation or placeholder response. | Varies by channel; social publishing remains roadmap. |
