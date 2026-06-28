# partenon-core

Core of Partenon. Adapts `hermes-business-core` from HBOS to route conversations to the 7 hero profiles, coordinate handoffs, and run the general onboarding.

## Responsibilities

- `router.py`: Routes user intents to `partenon-scribe`, `partenon-herald`, `partenon-collector`, `partenon-guardian`, `partenon-strategist`, `partenon-diplomat`, or `partenon-brain`.
- `onboarding_engine.py`: Installation wizard that creates profile files and generates initial missions.
- `onboarding_flow.py`: Lightweight onboarding flow that creates `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations` files and initial tasks.
- `workflow_engine.py`: Handoffs between profiles and mission logging in G-Brain.
- `eval_loop.py`: Stub for a judge-based evaluation loop that scores hero outputs against rubrics.
- `config/mcp/servers.yaml`: MCP server configuration (Google Workspace, Stripe, Gmail, G-Brain, etc.).

## Usage

```bash
python -m py_compile partenon-core/tools/*.py
```
