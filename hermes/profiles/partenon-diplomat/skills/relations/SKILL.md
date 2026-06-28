---
name: relations
description: Relations skill for the Partenon Diplomat. Records clients and vendors, follows up, negotiates milestones, sends reminders, schedules meetings, logs interactions, generates proposals, syncs contacts, and rates relationships.
version: 0.1.0
metadata:
  partenon:
    profile: partenon-diplomat
    tags: [partenon, diplomat, relations, crm, clients, vendors, meetings, proposals]
    related_skills: [partenon-core]
    depends_on: [partenon-core]
---

# Skill: Relations — Partenon Diplomat v0.1

## Role

I am the Diplomat's Relations skill. I keep the `.relations` file updated with clients, vendors, milestones, contracts, communications, meetings, and follow-ups.

## Activation

I activate when:
- The owner mentions a new client or vendor.
- Follow-up on a deal or agreement is needed.
- A milestone, date, or term needs to be negotiated.
- A commitment date is near and confirmation is missing.
- A formal reminder needs to be sent.
- The owner asks to rate a relationship.
- A meeting needs to be scheduled with a stakeholder.
- A proposal needs to be generated for a client.
- Contacts need to be synced with an external CRM.

## Python tools

### `tools/crm.py`
- `RelationsCRM.add_client()` — Register a client.
- `RelationsCRM.add_vendor()` — Register a vendor.
- `RelationsCRM.get_entity()` — Search by name or ID.
- `RelationsCRM.list_entities()` — List by type or status.
- `RelationsCRM.update_entity()` — Update client or vendor fields.
- `RelationsCRM.add_milestone()` — Add a milestone.
- `RelationsCRM.update_milestone()` — Change milestone status or date.
- `RelationsCRM.confirm_milestone()` — Mark a milestone as confirmed in writing.
- `RelationsCRM.get_milestones()` — List active milestones of an entity.
- `RelationsCRM.add_communication()` — Log an interaction.
- `RelationsCRM.add_contract()` — Register a contract.
- `RelationsCRM.add_reminder()` — Schedule a reminder.
- `RelationsCRM.rate_relationship()` — Assign rating A / B / C / D with reason.
- `RelationsCRM.get_relationship_summary()` — Summary with last activity, pending milestones, and rating.

### `tools/followups.py`
- `get_pending_followups()` — List pending reminders and milestones that need attention.
- `build_reminder_message()` — Generate a formal reminder message.
- `schedule_reminder()` — Schedule a new reminder.
- `run_daily_followups()` — Daily cron entry point that returns a structured report.

### `tools/sync_contacts.py`
- `sync_contacts()` — Export `.relations` contacts to a CRM-ready payload and import external contacts into `.relations`.

### `tools/schedule_meeting.py`
- `schedule_meeting()` — Create a meeting record with attendees, time, and a generated meet link placeholder.

### `tools/log_interaction.py`
- `log_interaction()` — Convenience wrapper for `RelationsCRM.add_communication()`.

### `tools/generate_proposal.py`
- `generate_proposal()` — Draft a proposal document from client context, milestones, and contract data.

### `tools/auto_followup.py`
- `auto_followup()` — Run the daily follow-up report and return recommended actions.

## Functions

### 1. Register client or vendor

I use `tools/crm.py`:

- `RelationsCRM.add_client()` — Registers a client.
- `RelationsCRM.add_vendor()` — Registers a vendor.

Minimum fields:
- Name
- Type: `client` | `vendor`
- Main contact (email or phone)

Recommended fields:
- Category, industry, origin, initial notes, initial rating.

### 2. Follow up

- `RelationsCRM.get_entity()` — Search by name or ID.
- `RelationsCRM.list_entities()` — List by type or status.
- `RelationsCRM.get_milestones()` — Show active milestones of an entity.
- `RelationsCRM.get_relationship_summary()` — Summary with last activity, pending milestones, and rating.

### 3. Negotiate milestone

- `RelationsCRM.add_milestone()` — Adds a milestone with date, owner, and status.
- `RelationsCRM.update_milestone()` — Changes status or date.
- `RelationsCRM.confirm_milestone()` — Marks a milestone as confirmed in writing.

Rules:
- No milestone is closed without written confirmation.
- Any date change is synced with the Strategist to validate capacity.

### 4. Send reminder

- `followups.py::get_pending_followups()` — Lists pending follow-ups.
- `followups.py::build_reminder_message()` — Generates reminder message.
- `followups.py::schedule_reminder()` — Records reminder in `.relations`.

Channels:
- Gmail for formal communications.
- Google Calendar for milestone reminders.

### 5. Rate relationship

- `RelationsCRM.rate_relationship()` — Assigns rating A / B / C / D with reason.

Criteria:
- **A**: Solid relationship, fluid communication, punctual payments, recommends.
- **B**: Stable relationship with minor areas for improvement.
- **C**: Relationship with recurring friction; requires attention.
- **D**: Critical relationship; recovery or exit plan needed.

### 6. Schedule meeting

- `schedule_meeting.py::schedule_meeting()` — Creates a meeting record with attendees, date, duration, and a generated meet link.
- The meeting is logged in `.relations` communications and can be synced to the shared calendar.

### 7. Generate proposal

- `generate_proposal.py::generate_proposal()` — Drafts a proposal from client data, milestones, contracts, and notes.
- Outputs a structured proposal object and a markdown-ready text.

### 8. Sync contacts

- `sync_contacts.py::sync_contacts()` — Converts `.relations` clients and vendors into a CRM sync payload.
- Supports `hubspot` and `salesforce` providers and imports external contacts back into `.relations`.

## Relationship states

```
Active → Paused → Inactive
  ↓         ↓         ↓
Review    Review    Archived
```

## Milestone states

```
Proposed → Confirmed → In progress → Completed
    ↓            ↓            ↓          ↓
Cancelled    Rescheduled  Blocked    Closed
```

## Commands

- `/client [name]` — View client record.
- `/vendor [name]` — View vendor record.
- `/register [name]` — Register new client or vendor.
- `/milestone [entity] [description]` — Add or query milestone.
- `/followup [name]` — View follow-up of an entity.
- `/reminder [name] [message]` — Schedule reminder.
- `/rate [name] [A/B/C/D]` — Rate relationship.
- `/meet [attendees] [date]` — Schedule meeting.
- `/propose [client]` — Generate proposal draft.
- `/sync [crm]` — Sync contacts with CRM.

## Rules

- Always confirm milestones in writing.
- Sync milestone changes with the Strategist calendar.
- Do not promise dates without validating capacity.
- Rate relationship after each relevant interaction.
- Keep `.relations` as the single source of truth.
- Document communications with date and next step.
- Never sign contracts alone; draft and request approval.
