---
name: partenon-workflows
description: Event-driven workflow engine for Partenon. Emits events, evaluates trigger conditions, and executes automatic handoffs between hero profiles. Persists events and actions locally.
version: 1.0.0
metadata:
  hermes:
    tags: [partenon, workflow, events, handoffs]
    related_skills: [partenon-core, partenon-scribe, partenon-herald, partenon-collector, partenon-guardian, partenon-strategist, partenon-diplomat, partenon-brain]
    auto_load: true
    priority: 3
---

# Skill: Partenon Workflows

## Role

I am the nervous system of Partenon. I listen for business events and run predefined workflows that create projects, tasks, goals, checklists, nudges, and client records across hero profiles.

## Python package

Implemented in `partenon_core.tools.workflow_engine`:

```python
from partenon_core.tools.workflow_engine import WorkflowEngine

engine = WorkflowEngine()
event = engine.emit_event(
    type="client_contracted",
    source="partenon-diplomat",
    entity_id="CLI-001",
    entity_type="client",
    data={"client_name": "Acme Inc", "project_name": "Website Redesign"},
)
print(event["actions_executed"])
```

## Built-in workflows

| Trigger | Actions |
|---------|---------|
| `client_contracted` | Create operations project, initiative goal, checklist, notify user. |
| `task_overdue` | Urgent nudge + suggest reschedule. |
| `pipeline_stalled` | Nudge pipeline + suggest campaign. |
| `quote_approved` | Generate contract, register expected income, create project. |
| `project_progress_50` | Review deadlines + alert if behind. |
| `new_client` | Register client, create follow-up task, welcome nudge. |

## Collaboration handoffs

The following events route context from one hero to another:

| Event | Source | Target | Purpose |
|-------|--------|--------|---------|
| `payment_confirmed` | Collector | Scribe | Record income and update dashboards. |
| `campaign_budget_requested` | Herald | Scribe | Validate campaign budget against financial plan. |
| `agreement_reached` | Diplomat | Strategist | Create project, tasks, and kickoff checklist. |
| `milestone_due_soon` | Strategist | Diplomat | Confirm milestone with the client or vendor. |
| `key_rotation_required` | Guardian | All affected heroes | Rotate credentials before they expire. |
| `learning_recorded` | Brain | Relevant hero | Surface historical context for a new decision. |

Each handoff creates a `handoff` nudge in `data/nudges.json` with `target_profile` and a message describing the required next step.

## Rules

- Workflows run in dry-run mode by default when no external credentials are configured.
- All events are persisted to `data/events.json`.
- I do not dispatch to external APIs directly; I emit events that heroes can consume via MCP.
