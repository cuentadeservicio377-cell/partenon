# Simulation: Onboarding Flora Coffee & Culture

This walkthrough shows how Partenon's heroes set up Flora Coffee for daily operations. It uses only the code in the repository: no live Stripe charges and no Google credentials.

- **Company card:** [`workshop/companies/coffee-shop--flora-coffee.md`](../companies/coffee-shop--flora-coffee.md)
- **Hero activation order:** Scribe → Strategist → Herald → Collector → Diplomat

---

## Prerequisites

```bash
./install.sh                 # creates .venv, installs deps, runs Scribe demo
source .venv/bin/activate
```

If the Hermes CLI is not installed, run the Python tools directly as shown below.

---

## Step 1 — Scribe: understand the numbers

**Hermes prompt:**

```text
Scribe, create a finance dashboard called "Flora Coffee Finances" and parse
workshop/data/flora-june-expenses.xlsx. Classify every row as fixed or variable.
```

**Direct Python:**

```bash
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/templates.py
```

This generates local Excel templates (`budget.xlsx`, `vendors.xlsx`, `cash_flow.xlsx`) that Flora can fill with rent, payroll, bean, milk, and pastry costs.

Expected output:

```text
Budget template written to budget.xlsx
Vendor directory written to vendors.xlsx
Cash flow template written to cash_flow.xlsx
```

---

## Step 2 — Strategist: schedule staff and events

**Hermes prompt:**

```text
Strategist, create a project "Flora Summer Cold Brew Push" for Flora Coffee with
delivery 2026-07-15 and amount $2,500. Add a retail checklist and assign
"Schedule staff for weekend tasting events" to Manager with high priority due
2026-07-01.
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
    name="Flora Summer Cold Brew Push",
    client_id="CLI-FLORA",
    client_name="Flora Coffee",
    delivery_date="2026-07-15",
    amount=2500,
    type="retail"
)
print(p["message"])

t = get_tasks().create_task(
    project_id=p["project"]["id"],
    title="Schedule staff for weekend tasting events",
    assignee="Manager",
    due_date="2026-07-01",
    priority="high"
)
print(t["message"])

c = get_checklists().create_project_checklist(p["project"]["id"], industry="retail")
print(c["message"])
PY
```

Expected output:

```text
Project created: Flora Summer Cold Brew Push (PROJ-001)
Task created: Schedule staff for weekend tasting events (TASK-001)
Checklist created for PROJ-001 with 12 items
```

---

## Step 3 — Herald: build the brand file and content calendar

Create `.design` so the Herald knows the brand voice:

```bash
cat > .design <<'EOF'
meta:
  version: "0.1.0"
  profile: partenon-herald
brand:
  brand_name: "Flora Coffee"
  website: "https://floracoffee.co"
  industry: "food"
  market: "Austin, TX"
  stage: "growth"
positioning:
  what_you_sell: "Ethically sourced, locally roasted coffee and community events"
  who_you_help: "Coffee lovers in Austin who care about craft and culture"
  how_you_do_it: "Small-batch roasting, expert baristas, and a welcoming cafe space"
voice:
  tone: "direct"
  addressing: "you informal"
  style: "clear, no filler, no emojis"
  emojis: false
channels:
  - instagram
  - linkedin
messaging:
  key_messages:
    - "Run your coffee shop with numbers, not guesswork"
  claims_to_avoid:
    - "100% guaranteed"
audience:
  primary:
    pain: "inconsistent service and long waits"
    outcome: "a reliable local cafe experience"
operations:
  final_approver: "Owner"
  autonomy:
    draft_copy: true
    create_calendar: true
    publish_social: false
    send_email: false
EOF
```

Generate a content calendar:

```bash
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/content_calendar.py \
  "run club and brewing classes" instagram,linkedin 7
```

Expected output:

```json
{
  "success": true,
  "campaign_id": "CAL-20260626-...",
  "calendar_path": ".../output/campaigns/CAL-20260626-.../content-calendar.json",
  "days": 7,
  "channels": ["instagram", "linkedin"]
}
```

Generate a post:

```bash
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py \
  post "summer cold brew flight" instagram
```

Expected output includes a `qa` block showing whether any banned claims were found.

---

## Step 4 — Collector: sell tickets and subscriptions locally

**Hermes prompt:**

```text
Collector, create a Stripe payment link for "Brewing Class Ticket" at $45 USD.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-cobrador/skills/payments/tools")
from stripe_tools import create_payment_link, create_invoice, send_payment_reminder

print(create_payment_link(
    {"name": "Brewing Class Ticket", "description": "2-hour home brewing workshop"},
    {"amount": 4500, "currency": "usd"}
))

print(create_invoice(
    {"email": "student@example.com", "name": "Student"},
    [{"description": "Brewing class ticket", "amount": 4500, "currency": "usd"}]
))

print(send_payment_reminder({
    "email": "student@example.com",
    "name": "Student",
    "amount_due": 45.00,
    "currency": "USD",
    "due_date": "2026-07-05"
}))
PY
```

Expected output (local mode):

```json
{
  "success": true,
  "url": "https://buy.stripe.com/test_link_...",
  "payment_link_id": "link_...",
  "message": "Payment link created in local mode (Stripe MCP not available)."
}
```

---

## Step 5 — Diplomat: track roasters and suppliers

**Hermes prompt:**

```text
Diplomat, register Flora Coffee as a client with email hello@floracoffee.co and
rating A. Register Local Roaster Collective as a vendor for coffee beans with
rating B. Add a milestone "Confirm Q3 bean contract" for Flora Coffee on
2026-07-15.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-diplomatico/skills/relations/tools")
from crm import get_relations_crm

crm = get_relations_crm()
print(crm.add_client("Flora Coffee", email="hello@floracoffee.co", category="coffee_shop", rating="A"))
print(crm.add_vendor("Local Roaster Collective", email="orders@localroaster.example", category="supplier", service="coffee beans", rating="B"))
print(crm.add_milestone("CLI-001", "Confirm Q3 bean contract", "2026-07-15"))
PY
```

Expected output:

```text
Client registered: Flora Coffee (CLI-001)
Vendor registered: Local Roaster Collective (VEN-001)
Milestone added to CLI-001: Confirm Q3 bean contract
```

---

## Local-mode notes

- The Collector returns test Stripe URLs. Real charges require `STRIPE_SECRET_KEY` in `.env`.
- Google Sheets creation is skipped without `GOOGLE_SERVICE_ACCOUNT_JSON`.
- The Diplomat writes to `data/relations_cache.json` (or `.relations` if present).

---

## Outcome

Flora Coffee leaves the onboarding with:

- A local finance template for fixed/variable costs.
- A retail project checklist and assigned task.
- A 7-day content calendar and brand voice file.
- Local payment links and invoice records.
- A client/vendor registry with a Q3 contract milestone.
