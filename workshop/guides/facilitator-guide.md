# Partenon Onboarding Workshop — Facilitator Guide

This guide helps a facilitator run a 90-minute Partenon onboarding workshop with a small group of founders or operators.

---

## Goals

By the end of the workshop, each participant should:

1. Understand the seven Partenon heroes and what each owns.
2. Identify the 2–4 heroes that remove the most friction for their business type.
3. Have a draft `client.yaml` and at least one profile config file for their company.
4. Know how to run the Scribe demo and create their first project/task/payment link.
5. Be able to name the live-integration gaps that block production use.

---

## Materials

- A laptop with the Partenon repo cloned and `./install.sh` already run.
- This `workshop/` directory open in a text editor or browser.
- A whiteboard or shared doc for the hero-selection exercise.
- A timer.

---

## Agenda

| Time | Activity | Purpose |
|------|----------|---------|
| 0:00–0:10 | Intro and hero overview | Set context; show the hero matrix. |
| 0:10–0:25 | Hero-selection exercise | Match business type to hero priority. |
| 0:25–0:40 | Demo: Scribe and Strategist | Show real tools running locally. |
| 0:40–0:70 | Breakout: simulation by business type | Each group works through one simulation. |
| 0:70–0:85 | Share gaps and next steps | Surface blockers and 30-day plan. |
| 0:85–0:90 | Close and resources | Point to docs, checklists, and production readiness. |

---

## Hero-selection exercise (15 minutes)

1. Ask each participant to name their business type from the list:
   - Coffee shop / food & beverage
   - Marketing / professional services agency
   - Construction / events / logistics
   - Retail / e-commerce
   - SaaS / tech startup
2. Show the hero priority table from [`hero-selection-guide.md`](hero-selection-guide.md).
3. For each business type, ask: *"Which hero removes the most friction in the first 30 days?"*
4. Write the top 2–4 heroes on the board.
5. Debate edge cases. For example:
   - A SaaS with no paid customers yet should still activate Guardian and Scribe before Collector.
   - A retailer with high transaction volume should activate Collector before Herald.

---

## Demo script (15 minutes)

Run these commands from the repo root and narrate what is happening.

### 1. Verify the install

```bash
python3 scripts/demo_scribe.py
```

Explain: this is the finance demo. It creates a sample workbook and a JSON report.

### 2. Show the Strategist creating a project

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-strategist/skills/ops/tools")
from projects import get_projects
from tasks import get_tasks

p = get_projects().create_project(
    name="Workshop demo project",
    client_id="CLI-001",
    client_name="Demo Client",
    delivery_date="2026-12-31",
    amount=5000
)
print(p)

t = get_tasks().create_task(
    project_id=p["project"]["id"],
    title="Draft first deliverable",
    assignee="You",
    due_date="2026-07-07",
    priority="high"
)
print(t)
PY
```

Explain: projects and tasks live in `partenon_core/data/` as JSON. The dashboard reads them.

### 3. Show the Collector in local mode

```bash
python3 hermes/profiles/partenon-collector/skills/payments/tools/stripe_tools.py
```

Explain: this runs without real Stripe credentials. In production, set `STRIPE_SECRET_KEY` in `.env`.

### 4. Show the Guardian listing keys

```bash
python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py
```

Explain: keys are masked; the tool reports missing, active, or pending-rotation status.

---

## Breakout instructions (30 minutes)

1. Split participants into groups by business type.
2. Assign each group one simulation:
   - Coffee shop → [`simulations/coffee-shop.md`](../simulations/coffee-shop.md)
   - Agency → [`simulations/agency.md`](../simulations/agency.md)
   - Construction → [`simulations/construction-company.md`](../simulations/construction-company.md)
   - Retail → [`simulations/retail-store.md`](../simulations/retail-store.md)
   - SaaS → [`simulations/saas-startup.md`](../simulations/saas-startup.md)
3. Ask each group to:
   - Read the business context and pain points.
   - Copy the example config files into a scratch document.
   - Run at least two commands from the simulation.
   - Fill out the first three missions for their top hero.
4. Circulate and answer questions.

---

## Share gaps and next steps (15 minutes)

Ask each group to report:

1. Which hero would they activate first and why?
2. Which command worked out of the box?
3. Which gap would block a live onboarding first?

Record the gaps on the board. Common answers:

- No live Stripe / Google Workspace credentials.
- No POS-to-Scribe integration for retail/coffee.
- No construction checklist template.
- No G-Brain binary bundled.

Close by pointing to:

- [`../PRODUCTION_READINESS.md`](../PRODUCTION_READINESS.md)
- [`../MISSING_IMPLEMENTATION.md`](../MISSING_IMPLEMENTATION.md)
- [`../docs/HERMES_ONBOARDING.md`](../docs/HERMES_ONBOARDING.md)

---

## Tips

- Keep the demo fast. Participants will explore deeper in the breakout.
- Emphasize that Partenon is an operations system, not a replacement for accountants, lawyers, or security engineers.
- If the Hermes CLI is not installed, show the graceful fallback in `install.sh` and explain that live onboarding uses Nous Research's Hermes Agent CLI.
