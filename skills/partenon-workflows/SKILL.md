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

## Rules

- Workflows run in dry-run mode by default when no external credentials are configured.
- All events are persisted to `data/events.json`.
- I do not dispatch to external APIs directly; I emit events that heroes can consume via MCP.
