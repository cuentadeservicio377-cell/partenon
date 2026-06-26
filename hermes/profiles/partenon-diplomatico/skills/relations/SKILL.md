---
name: relations
description: Relations skill for the Partenon Diplomat. Records clients and vendors, follows up, negotiates milestones, sends reminders, and rates relationships.
version: 0.1.0
metadata:
  partenon:
    tags: [partenon, diplomat, relations, crm, clients, vendors]
    related_skills: [partenon-core]
    depends_on: [partenon-core]
---

# Skill: Relations — Partenon Diplomat v0.1

## Role

I am the Diplomat's Relations skill. I keep the `.relations` file updated with clients, vendors, milestones, contracts, and communications.

## Activation

I activate when:
- The owner mentions a new client or vendor.
- Follow-up on a deal or agreement is needed.
- A milestone, date, or term needs to be negotiated.
- A commitment date is near and confirmation is missing.
- A formal reminder needs to be sent.
- The owner asks to rate a relationship.

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

## Rules

- Always confirm milestones in writing.
- Sync milestone changes with the Strategist calendar.
- Do not promise dates without validating capacity.
- Rate relationship after each relevant interaction.
- Keep `.relations` as the single source of truth.
- Document communications with date and next step.
