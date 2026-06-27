# Simulation: Onboarding Mack Media Group

This walkthrough shows how Partenon's heroes help Mack Media Group manage retainers, clients, and cash flow. Everything runs in local mode.

- **Company card:** [`workshop/companies/marketing-agency--mack-media-group.md`](../companies/marketing-agency--mack-media-group.md)
- **Hero activation order:** Strategist → Diplomat → Scribe → Herald → Collector

---

## Prerequisites

```bash
./install.sh
source .venv/bin/activate
```

---

## Step 1 — Strategist: create a retainer project template

**Hermes prompt:**

```text
Strategist, create a project "SEO Retainer - Downtown Dental" for client
CLI-DOWNTOWN-DENTAL with delivery 2026-09-30 and amount $5,000/month. Add a
consulting checklist and assign "Kickoff discovery call" to Account Manager with
high priority due 2026-07-03.
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
    name="SEO Retainer - Downtown Dental",
    client_id="CLI-DOWNTOWN-DENTAL",
    client_name="Downtown Dental",
    delivery_date="2026-09-30",
    amount=5000,
    type="consulting"
)
print(p["message"])

t = get_tasks().create_task(
    project_id=p["project"]["id"],
    title="Kickoff discovery call",
    assignee="Account Manager",
    due_date="2026-07-03",
    priority="high"
)
print(t["message"])

print(get_checklists().create_project_checklist(p["project"]["id"], industry="consulting")["message"])
PY
```

Expected output:

```text
Project created: SEO Retainer - Downtown Dental (PROJ-001)
Task created: Kickoff discovery call (TASK-001)
Checklist created for PROJ-001 with 15 items
```

---

## Step 2 — Diplomat: register prospects and clients

**Hermes prompt:**

```text
Diplomat, register Downtown Dental as a client with rating A. Register
WordPress Wizards as a vendor for web development with rating B. Add a milestone
"Deliver monthly report" for Downtown Dental on 2026-07-31.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-diplomatico/skills/relations/tools")
from crm import get_relations_crm

crm = get_relations_crm()
print(crm.add_client("Downtown Dental", email="hello@downtowndental.example", category="dental", rating="A"))
print(crm.add_vendor("WordPress Wizards", email="dev@wpwizards.example", category="technology", service="web development", rating="B"))
print(crm.add_milestone("CLI-001", "Deliver monthly report", "2026-07-31"))
PY
```

Expected output:

```text
Client registered: Downtown Dental (CLI-001)
Vendor registered: WordPress Wizards (VEN-001)
Milestone added to CLI-001: Deliver monthly report
```

---

## Step 3 — Scribe: track retainer budget vs. hours

Generate a budget template and fill it with the retainer line items:

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-tesorero/skills/finance/tools")
from templates import get_templates

get_templates().create_budget(
    "mack-media-budget.xlsx",
    period="2026-Q3",
    line_items=[
        {"line_item": "Retainer revenue", "budget": 5000, "actual": 5000},
        {"line_item": "Account manager labor", "budget": 1800, "actual": 0},
        {"line_item": "PPC spend", "budget": 1200, "actual": 0},
        {"line_item": "Content writing", "budget": 800, "actual": 0},
        {"line_item": "Reporting tools", "budget": 200, "actual": 0},
    ]
)
print("Budget written to mack-media-budget.xlsx")
PY
```

Expected output:

```text
Budget written to mack-media-budget.xlsx
```

The agency can update actuals weekly and watch the variance column.

---

## Step 4 — Herald: generate case-study copy

Create a minimal `.design` file:

```bash
cat > .design <<'EOF'
meta:
  version: "0.1.0"
  profile: partenon-herald
brand:
  brand_name: "Mack Media Group"
  website: "https://mackmediagroup.com"
  industry: "marketing"
  market: "Connecticut and Florida"
  stage: "growth"
positioning:
  what_you_sell: "Results-driven digital marketing for local businesses"
  who_you_help: "SMBs that have been burned by bad agencies"
  how_you_do_it: "Transparent reporting, local SEO, and disciplined account management"
voice:
  tone: "direct"
  addressing: "you informal"
  style: "clear, no filler, no emojis"
  emojis: false
channels:
  - linkedin
messaging:
  key_messages:
    - "No more black-box marketing reports"
  claims_to_avoid:
    - "100% guaranteed"
audience:
  primary:
    pain: "wasted marketing spend and unclear ROI"
    outcome: "predictable lead flow"
operations:
  final_approver: "Owner"
  autonomy:
    draft_copy: true
    create_calendar: true
    publish_social: false
    send_email: false
EOF
```

Generate LinkedIn copy:

```bash
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py \
  post "how Downtown Dental grew organic leads" linkedin
```

Expected output includes a post body and a `qa` block. If any banned claim is found, the `passed` field becomes `false`.

---

## Step 5 — Collector: invoice the retainer

**Hermes prompt:**

```text
Collector, invoice Downtown Dental for "July SEO retainer" at $5,000 USD.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-cobrador/skills/payments/tools")
from stripe_tools import create_invoice, send_payment_reminder

print(create_invoice(
    {"email": "hello@downtowndental.example", "name": "Downtown Dental"},
    [{"description": "July SEO retainer", "amount": 500000, "currency": "usd"}]
))

print(send_payment_reminder({
    "email": "hello@downtowndental.example",
    "name": "Downtown Dental",
    "amount_due": 5000.00,
    "currency": "USD",
    "due_date": "2026-07-15"
}))
PY
```

Expected output (local mode):

```json
{
  "success": true,
  "invoice_id": "inv_001",
  "amount": 500000,
  "currency": "USD",
  "status": "open",
  "hosted_invoice_url": "https://invoice.stripe.com/test_inv_001",
  "message": "Invoice inv_001 created in local mode for hello@downtowndental.example."
}
```

---

## Local-mode notes

- Invoices are stored in `.payments` until a Stripe key is added.
- Real email reminders require the Gmail MCP and `GMAIL_ACCESS_TOKEN`.

---

## Outcome

Mack Media Group leaves the onboarding with:

- A retainer project template with a consulting checklist.
- A client/vendor registry with monthly-report milestone.
- A budget-vs-actual file for each retainer.
- LinkedIn case-study copy checked for banned claims.
- A local invoice and reminder record.
