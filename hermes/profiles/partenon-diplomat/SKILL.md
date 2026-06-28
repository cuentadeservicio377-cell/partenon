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
- Sync contacts with HubSpot or Salesforce.

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
