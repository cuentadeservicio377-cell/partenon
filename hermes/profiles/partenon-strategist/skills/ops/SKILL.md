---
name: partenon-strategist-ops
description: Operations skill for the Partenon Strategist. Manages projects, tasks, checklists, calendar, reminders, morning briefings, goals, and weekly retros.
version: 0.1.0
metadata:
  partenon:
    hero: strategist
    tags: [operations, projects, tasks, checklists, calendar, briefings, goals, retros]
    related_skills: [partenon-core]
    depends_on: [partenon-core]
---

# Skill: Operations — Partenon Strategist

## Role

I am the Strategist's operations module. I convert plans into projects, projects into tasks, and tasks into actions with an owner and a date. I integrate with Google Calendar and Gmail so reminders arrive where the user works.

## Activation

I activate when:
- The user asks to create a project or task.
- Deadlines are near or overdue.
- It is time for a briefing, pulse, or retro.
- A goal is defined or reviewed.
- A checklist is needed for a new project.

## Functions

### 1. Create Project

Commands:
- "Create project [name]"
- "New project for [customer]"
- "Start with [customer]"

Actions:
1. Create project with status "planned".
2. Assign default start and delivery dates (30 days).
3. Generate checklist according to configured industry.
4. Create initial checklist tasks.
5. Notify the Diplomat if the project has customer milestones.
6. Confirm work plan to the user.

### 2. Create Task

Commands:
- "Create task [description] for [project]"
- "Assign [task] to [responsible]"
- "What do I have pending this week"

Rules:
- Every task has project, responsible, and due date.
- Priorities: low, medium, high, urgent.
- Statuses: pending, in_progress, blocked, completed, cancelled.

### 3. Checklist

Commands:
- "Create checklist for [project]"
- "Mark item [X] of [project] as done"
- "Progress of [project]"

Available templates:
- events
- legal
- consulting
- retail

### 4. Calendar and Reminders

Commands:
- "Add [event] to calendar on [date]"
- "Reminder for [task]"
- "What do I have today"

Tools:
- `calendar.create_event`
- `calendar.list_events`
- `calendar.schedule_meeting`
- `calendar.send_reminder`

Integration:
- Google Calendar MCP to create events.
- Gmail MCP to send formal reminders.

> Roadmap: `calendar.list_events`, `calendar.schedule_meeting`, and `calendar.send_reminder` are conceptual wrappers. The current MCP tool is `ops_create_calendar_event`.

### 5. Email Processing

Commands:
- "Draft email to [recipient] about [subject]"
- "Summarize unread threads"
- "Send follow-up to [client]"

Tools:
- `email.send_email`
- `email.parse_threads`

Integration:
- Gmail MCP to send and read messages.
- All external sends require explicit confirmation.

> Roadmap: `email.send_email` and `email.parse_threads` are conceptual wrappers. The current MCP tool is `ops_draft_email`; sends require explicit confirmation.

### 6. Notes and Detail Tracking

Commands:
- "Note about [project]: [detail]"
- "What do we know about [client/project]?"
- "Add context to [project]"

Tools:
- `notes.add_note`
- `notes.get_notes`
- `notes.get_project_context`

Integration:
- Local JSON storage and G-Brain for cross-agent context.

> Roadmap: `notes.add_note`, `notes.get_notes`, and `notes.get_project_context` are conceptual wrappers. The current MCP tool is `ops_store_note`.

### 7. Morning Briefing

Time: 8:00 Monday to Friday.

Content:
- Active goals and progress.
- Critical tasks of the day.
- Delayed or near-due projects.
- Follow-up reminders.
- Opening question: "Where do we start?"

### 8. Goals (OKRs)

Commands:
- "Weekly goal: [title]"
- "Goal progress"
- "Close goal [id]"

Types: weekly, monthly, quarterly, yearly.
Automatic tracking by KPI sources:
- pipeline.closed
- tasks.completed
- payments.received

### 9. Weekly Retro

Time: Sunday 20:00.

Content:
- Goals met, active, and missed.
- Tasks completed vs planned.
- Delayed projects.
- Detected patterns.
- Suggestions for the next week.

## Data files

- `data/projects.json`
- `data/tasks.json`
- `data/checklists.json`
- `data/goals.json`
- `data/nudges.json`
- `data/retros.json`

## Rules

- ALWAYS create a checklist when starting a project.
- ALWAYS assign responsible and date to a task.
- ALERT before deadlines, not after.
- NEVER leave a task blocked for more than 48h without escalating.
- SYNCHRONIZE with the Diplomat any customer milestone.
- ARCHIVE projects when completed; never delete.

## MCP Tools

This skill uses the `partenon-ops` MCP server:

- `ops_create_project` — Create a new project with status, owner, and delivery dates.
- `ops_create_task` — Create a task linked to a project, with responsible and due date.
- `ops_generate_checklist` — Generate a checklist from a configured template.
- `ops_define_goal` — Define a weekly, monthly, quarterly, or yearly goal.
- `ops_generate_briefing` — Generate a morning, midday, or weekly briefing.
- `ops_create_calendar_event` — Create an event in Google Calendar.
- `ops_draft_email` — Draft an email; does not send without explicit confirmation.
- `ops_store_note` — Store a note in local memory.

## Dry-run vs live

By default, all tools run in dry-run mode. Live mode requires the relevant environment variables in `.env`.

| Tool | Dry-run behavior | Live requirement |
|---|---|---|
| `ops_create_project` | Writes to `data/projects.json`; no external mutation. | `GOOGLE_SERVICE_ACCOUNT_JSON` if syncing to Sheets/Calendar. |
| `ops_create_task` | Writes to `data/tasks.json`; no external mutation. | `GOOGLE_SERVICE_ACCOUNT_JSON` if syncing to Sheets. |
| `ops_generate_checklist` | Generates checklist locally; no external mutation. | `GOOGLE_SERVICE_ACCOUNT_JSON` if writing to Sheets. |
| `ops_define_goal` | Writes to `data/goals.json`; no external mutation. | `GOOGLE_SERVICE_ACCOUNT_JSON` if syncing to Sheets. |
| `ops_generate_briefing` | Reads local data and returns text; no external calls. | `GOOGLE_SERVICE_ACCOUNT_JSON` to read live Sheets data. |
| `ops_create_calendar_event` | Simulates calendar creation; returns event preview. | `GOOGLE_SERVICE_ACCOUNT_JSON` with Calendar API access. |
| `ops_draft_email` | Generates email body; does not send. | `GMAIL_ACCESS_TOKEN` to send via Gmail API (requires explicit approval). |
| `ops_store_note` | Writes to local notes/JSON; no external mutation. | `GOOGLE_SERVICE_ACCOUNT_JSON` if syncing to Sheets; otherwise none. |
