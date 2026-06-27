# Simulation: Onboarding Boreal Contractors

This walkthrough shows how Partenon's heroes help a small Phoenix-area contractor manage projects, subcontractors, permits, and job costing. Everything runs in local mode.

- **Company card:** [`workshop/companies/construction-company--boreal-contractors.md`](../companies/construction-company--boreal-contractors.md)
- **Hero activation order:** Strategist → Diplomat → Scribe → Guardian → Collector

---

## Prerequisites

```bash
./install.sh
source .venv/bin/activate
```

---

## Step 1 — Strategist: project phases and site tasks

**Hermes prompt:**

```text
Strategist, create a project "Multi-family finishes - Phase 2" for client
CLI-ALTA-VISTA with delivery 2026-10-15 and amount $120,000. Add a consulting
checklist and assign "Submit permit application" to Project Manager with high
priority due 2026-07-05.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-estratega/skills/ops/tools")
from projects import get_projects
from tasks import get_tasks
from checklists import get_checklists

p = get_projects().create_project(
    name="Multi-family finishes - Phase 2",
    client_id="CLI-ALTA-VISTA",
    client_name="Alta Vista Apartments",
    delivery_date="2026-10-15",
    amount=120000,
    type="consulting"
)
print(p["message"])

t = get_tasks().create_task(
    project_id=p["project"]["id"],
    title="Submit permit application",
    assignee="Project Manager",
    due_date="2026-07-05",
    priority="high"
)
print(t["message"])

print(get_checklists().create_project_checklist(p["project"]["id"], industry="consulting")["message"])
PY
```

Expected output:

```text
Project created: Multi-family finishes - Phase 2 (PROJ-001)
Task created: Submit permit application (TASK-001)
Checklist created for PROJ-001 with 15 items
```

---

## Step 2 — Diplomat: register owner, subs, and suppliers

**Hermes prompt:**

```text
Diplomat, register Alta Vista Apartments as a client with rating A. Register
Drywall Specialists LLC and Flooring Pros as vendors. Add milestones "Pre-con
meeting" on 2026-07-10 and "Final inspection" on 2026-10-10 for Alta Vista.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-diplomatico/skills/relations/tools")
from crm import get_relations_crm

crm = get_relations_crm()
print(crm.add_client("Alta Vista Apartments", email="pm@altavista.example", category="real_estate", rating="A"))
print(crm.add_vendor("Drywall Specialists LLC", email":"jobs@drywallspecialists.example", category":"subcontractor", service":"drywall", rating":"B"))
print(crm.add_vendor("Flooring Pros", email":"orders@flooringpros.example", category":"subcontractor", service":"flooring", rating":"B"))
print(crm.add_milestone("CLI-001", "Pre-con meeting", "2026-07-10"))
print(crm.add_milestone("CLI-001", "Final inspection", "2026-10-10"))
PY
```

Expected output:

```text
Client registered: Alta Vista Apartments (CLI-001)
Vendor registered: Drywall Specialists LLC (VEN-001)
Vendor registered: Flooring Pros (VEN-002)
Milestone added to CLI-001: Pre-con meeting
Milestone added to CLI-001: Final inspection
```

---

## Step 3 — Scribe: job costing by project

Create a project-specific budget to compare estimate vs. actual:

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-tesorero/skills/finance/tools")
from templates import get_templates

get_templates().create_budget(
    "boreal-job-cost.xlsx",
    period="2026-Q3/Q4",
    line_items=[
        {"line_item": "Drywall labor and materials", "budget": 35000, "actual": 0},
        {"line_item": "Flooring labor and materials", "budget": 28000, "actual": 0},
        {"line_item": "Paint and coatings", "budget": 15000, "actual": 0},
        {"line_item": "Permits and inspections", "budget": 4000, "actual": 0},
        {"line_item": "Project management", "budget": 12000, "actual": 0},
    ]
)
print("Job-cost budget written to boreal-job-cost.xlsx")
PY
```

Expected output:

```text
Job-cost budget written to boreal-job-cost.xlsx
```

---

## Step 4 — Guardian: audit access and credentials

**Hermes prompt:**

```text
Guardian, list all API keys and audit access for partenon-tesorero and
partenon-estratega.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-guardian/skills/security/tools")
from key_manager import list_keys, audit_access

print(list_keys())
print(audit_access("partenon-tesorero"))
print(audit_access("partenon-estratega"))
PY
```

Expected output (will vary based on your `.env`):

```json
[
  {"provider": "nvidia", "key_id": "NVIDIA_API_KEY", "status": "pending_rotation", ...},
  {"provider": "openai", "key_id": "OPENAI_API_KEY", "status": "missing", ...},
  ...
]
{"profile": "partenon-tesorero", "tools": ["file", "terminal"], "skills": ["finance"], "violations": []}
{"profile": "partenon-estratega", "tools": ["file", "terminal"], "skills": ["ops"], "violations": []}
```

---

## Step 5 — Collector: progress invoice

**Hermes prompt:**

```text
Collector, invoice Alta Vista Apartments for "Drywall rough-in milestone" at
$35,000 USD.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-cobrador/skills/payments/tools")
from stripe_tools import create_invoice

print(create_invoice(
    {"email": "pm@altavista.example", "name": "Alta Vista Apartments"},
    [{"description": "Drywall rough-in milestone", "amount": 3500000, "currency": "usd"}]
))
PY
```

Expected output (local mode):

```json
{
  "success": true,
  "invoice_id": "inv_001",
  "amount": 3500000,
  "currency": "USD",
  "status": "open",
  "hosted_invoice_url": "https://invoice.stripe.com/test_inv_001",
  "message": "Invoice inv_001 created in local mode for pm@altavista.example."
}
```

---

## Local-mode notes

- Real permit tracking requires Google Calendar/Drive MCP integration.
- Subcontractor COI tracking is currently a manual checklist item; automated alerts are on the roadmap.

---

## Outcome

Boreal Contractors leaves the onboarding with:

- A phased project with a consulting checklist and permit task.
- A client/subcontractor registry with pre-con and inspection milestones.
- A job-cost budget template to compare estimate vs. actual weekly.
- A Guardian audit of profile access and key rotation status.
- A local progress invoice record.
