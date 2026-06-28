# Partenon Strategist — Operations Skill Pack

> Operations and project management agent for small businesses.
> Plans, assigns, tracks, and briefs. Connects all heroes through calendars, tasks, and goals.

## Included skills

### `ops`
- Create and manage projects with lifecycle tracking.
- Create, assign, and prioritize tasks with due dates and dependencies.
- Generate industry-specific checklists (events, legal, consulting, retail).
- Define and track weekly, monthly, and quarterly goals with automatic KPI tracking.
- Generate morning briefings, midday pulses, evening wraps, weekly planning, and weekly retros.
- Manage calendar events, meeting scheduling, and reminders.
- Process email drafts and parse thread summaries.
- Keep project notes and client-context detail tracking.

## Quick start

1. Copy `.env.example` to `.env` and fill in credentials.
2. Copy `templates/.ops.example` to your workspace as `.ops`.
3. Use `skills/ops/tools/projects.py` to create projects.
4. Use `skills/ops/tools/tasks.py` to assign tasks.
5. Use `skills/ops/tools/checklists.py` to generate project checklists.
6. Use `skills/ops/tools/goals.py` to define and track goals.
7. Use `skills/ops/tools/briefings.py` to generate briefings and retros.
8. Use `skills/ops/tools/calendar.py` to schedule events and reminders.
9. Use `skills/ops/tools/email.py` to draft emails and parse thread summaries.
10. Use `skills/ops/tools/notes.py` to store project notes and context.

## Safety rules

- The Strategist never contacts a customer directly without synchronizing with the Diplomat.
- Every task has an owner and a due date before it is saved.
- Every project starts with a checklist.
- Blocked tasks are escalated after 48 hours.
- Completed projects are archived; nothing is deleted.
- Calendar and email actions require explicit confirmation before external send.

## MCP Tools

The Strategist uses the `partenon-ops` MCP server. Available tools:

- `ops_create_project`
- `ops_create_task`
- `ops_generate_checklist`
- `ops_define_goal`
- `ops_generate_briefing`
- `ops_create_calendar_event`
- `ops_draft_email`
- `ops_store_note`

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|---|---|---|
| `ops_create_project` | Creates the project in local `data/projects.json`. | None. |
| `ops_create_task` | Creates the task in local `data/tasks.json`. | None. |
| `ops_generate_checklist` | Generates the checklist locally; no external write. | None. |
| `ops_define_goal` | Stores the goal in local `data/goals.json`. | None. |
| `ops_generate_briefing` | Generates the briefing text locally; no external send. | None. |
| `ops_create_calendar_event` | Simulates the event and returns a preview; no Calendar write. | `GOOGLE_SERVICE_ACCOUNT_JSON` to create a live Google Calendar event. |
| `ops_draft_email` | Drafts the email locally; no send. | `GMAIL_ACCESS_TOKEN` to send via Gmail. |
| `ops_store_note` | Stores the note locally; no external persistence. | None. Optional `GOOGLE_SERVICE_ACCOUNT_JSON` to sync to a connected workspace store. |
