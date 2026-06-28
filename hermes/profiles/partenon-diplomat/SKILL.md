# Partenon Diplomat — Relations Skill Pack

> Client and vendor relationship agent for small businesses.
> Bridges internal operations and external stakeholders. Does not move money or sign contracts alone.

## Included skills

### `relations`
- Register clients and vendors in `.relations`.
- Log interactions, meetings, calls, and emails.
- Track milestones, contracts, and deliverables.
- Rate relationships (A / B / C / D).
- Run daily follow-up reports and reminders.
- Generate proposals from client context.
- Sync contacts with HubSpot or Salesforce. *(roadmap; no MCP tool available yet)*

## Quick start

1. Copy `.env.example` to `.env` and fill in credentials.
2. Copy `templates/.relations.example` to your workspace as `.relations`.
3. Use `skills/relations/tools/crm.py` to register clients and vendors.
4. Use `skills/relations/tools/followups.py` to run daily follow-up reports.
5. Use `skills/relations/tools/schedule_meeting.py` to plan meetings.
6. Use `skills/relations/tools/generate_proposal.py` to draft proposals.

## Safety rules

- The Diplomat never signs contracts alone; it drafts and requests approval.
- It never promises dates without validating capacity with the Strategist.
- Every milestone and agreement is confirmed in writing in `.relations`.
- Every relevant interaction is logged with date, channel, subject, summary, and next step.

## MCP Tools

The Diplomat uses the `partenon-relations` MCP server. Available tools:

- `relations_register_client` — Create a client record.
- `relations_register_vendor` — Create a vendor record.
- `relations_log_interaction` — Record a call, email, meeting, or message.
- `relations_track_milestone` — Add or update a milestone.
- `relations_track_deliverable` — Add or update a deliverable.
- `relations_rate_relationship` — Assign a relationship rating with reason.
- `relations_run_followups` — Generate the daily follow-up report.
- `relations_generate_proposal` — Draft a proposal from context.
- `relations_sync_contacts` — Prepare a CRM sync payload.
- `relations_schedule_meeting` — Schedule a meeting and optional calendar event.

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|------|------------------|------------------|
| `relations_register_client` | Writes the client to `.relations` only. | `GOOGLE_SERVICE_ACCOUNT_JSON` to sync to Sheets. |
| `relations_register_vendor` | Writes the vendor to `.relations` only. | `GOOGLE_SERVICE_ACCOUNT_JSON` to sync to Sheets. |
| `relations_log_interaction` | Appends the interaction to `.relations` only. | `GOOGLE_SERVICE_ACCOUNT_JSON` to append to Sheets. |
| `relations_track_milestone` | Updates `.relations`; no calendar event created. | `GOOGLE_SERVICE_ACCOUNT_JSON` to create/update Calendar events. |
| `relations_track_deliverable` | Updates `.relations`; no calendar event created. | `GOOGLE_SERVICE_ACCOUNT_JSON` to create/update Calendar events. |
| `relations_rate_relationship` | Stores the rating in `.relations` only. | `GOOGLE_SERVICE_ACCOUNT_JSON` to sync to Sheets. |
| `relations_run_followups` | Returns a structured report; no messages sent. | `GMAIL_ACCESS_TOKEN` to send reminder emails. |
| `relations_generate_proposal` | Drafts a local markdown proposal. | `GOOGLE_SERVICE_ACCOUNT_JSON` to create a Doc or Slide. |
| `relations_sync_contacts` | Returns a CRM-ready payload; no external push. | External CRM connector (roadmap). |
| `relations_schedule_meeting` | Creates a local meeting record only. | `GOOGLE_SERVICE_ACCOUNT_JSON` to create a Calendar event. |

Live mode is opt-in via `.env`. The default dry-run mode never sends emails, creates calendar events, or pushes data to external systems.
