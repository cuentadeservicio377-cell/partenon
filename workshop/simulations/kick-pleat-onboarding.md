# Simulation: Onboarding Kick Pleat

This walkthrough shows how Partenon's heroes help an independent boutique manage inventory, payments, marketing, and vendor relationships. Everything runs in local mode.

- **Company card:** [`workshop/companies/retail-store--kick-pleat.md`](../companies/retail-store--kick-pleat.md)
- **Hero activation order:** Scribe → Collector → Herald → Strategist → Diplomat

---

## Prerequisites

```bash
./install.sh
source .venv/bin/activate
```

---

## Step 1 — Scribe: margin dashboard by channel

**Hermes prompt:**

```text
Scribe, create a budget called "Kick Pleat Q3" with line items for wholesale
COGS, shipping, returns, and Meta ads. Then create a vendor directory for our
top designers and consignment partners.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-tesorero/skills/finance/tools")
from templates import get_templates

t = get_templates()
t.create_budget(
    "kick-pleat-q3.xlsx",
    period="2026-Q3",
    line_items=[
        {"line_item": "Wholesale COGS", "budget": 45000, "actual": 0},
        {"line_item": "Shipping", "budget": 3500, "actual": 0},
        {"line_item": "Returns and exchanges", "budget": 2500, "actual": 0},
        {"line_item": "Meta ads", "budget": 6000, "actual": 0},
        {"line_item": "Store labor", "budget": 12000, "actual": 0},
    ]
)
t.create_vendors("kick-pleat-vendors.xlsx")
print("Finance templates created.")
PY
```

Expected output:

```text
Finance templates created.
```

---

## Step 2 — Collector: checkout, subscriptions, and refunds

**Hermes prompt:**

```text
Collector, create a payment link for "Summer Linen Dress" at $245 USD.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-cobrador/skills/payments/tools")
from stripe_tools import create_payment_link

print(create_payment_link(
    {"name": "Summer Linen Dress", "description": "Lightweight linen dress"},
    {"amount": 24500, "currency": "usd"}
))
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

## Step 3 — Herald: new-arrival calendar and copy

Create `.design`:

```bash
cat > .design <<'EOF'
meta:
  version: "0.1.0"
  profile: partenon-herald
brand:
  brand_name: "Kick Pleat"
  website: "https://kickpleat.com"
  industry: "retail"
  market: "Austin, TX and online"
  stage: "growth"
positioning:
  what_you_sell: "Curated minimalist clothing and accessories"
  who_you_help: "Design-focused shoppers who want timeless pieces"
  how_you_do_it: "Hand-picked designers, in-store styling, and a tight online experience"
voice:
  tone: "direct"
  addressing: "you informal"
  style: "clear, no filler, no emojis"
  emojis: false
channels:
  - instagram
  - email
messaging:
  key_messages:
    - "Fewer, better pieces"
  claims_to_avoid:
    - "100% guaranteed"
audience:
  primary:
    pain: "slow shipping and inventory that does not sync"
    outcome: "a wardrobe that works"
operations:
  final_approver: "Buyer"
  autonomy:
    draft_copy: true
    create_calendar: true
    publish_social: false
    send_email: false
EOF
```

Generate a calendar and email copy:

```bash
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/content_calendar.py \
  "new arrivals and styling tips" instagram,email 7

python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py \
  email "new linen drop" newsletter
```

Expected output: a calendar JSON file and an email draft with a `qa` block.

---

## Step 4 — Strategist: coordinate restocking and campaign deadlines

**Hermes prompt:**

```text
Strategist, create a project "July New Arrivals Launch" for client CLI-KP with
delivery 2026-07-15 and amount $8,000. Add a retail checklist and assign
"Confirm reorder cutoff with designer" to Buyer with high priority due
2026-06-30.
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
    name="July New Arrivals Launch",
    client_id="CLI-KP",
    client_name="Kick Pleat",
    delivery_date="2026-07-15",
    amount=8000,
    type="retail"
)
print(p["message"])

t = get_tasks().create_task(
    project_id=p["project"]["id"],
    title="Confirm reorder cutoff with designer",
    assignee="Buyer",
    due_date="2026-06-30",
    priority="high"
)
print(t["message"])

print(get_checklists().create_project_checklist(p["project"]["id"], industry="retail")["message"])
PY
```

Expected output:

```text
Project created: July New Arrivals Launch (PROJ-001)
Task created: Confirm reorder cutoff with designer (TASK-001)
Checklist created for PROJ-001 with 12 items
```

---

## Step 5 — Diplomat: track designers and consignment partners

**Hermes prompt:**

```text
Diplomat, register Kick Pleat as a client and WP Martin as a vendor for the
house line. Add a milestone "Review consignment terms" for WP Martin on
2026-07-31.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-diplomatico/skills/relations/tools")
from crm import get_relations_crm

crm = get_relations_crm()
print(crm.add_client("Kick Pleat", email="hello@kickpleat.com", category="retail", rating="A"))
print(crm.add_vendor("WP Martin", email="studio@wpmartin.example", category="designer", service="house line", rating="A"))
print(crm.add_milestone("VEN-001", "Review consignment terms", "2026-07-31"))
PY
```

Expected output:

```text
Client registered: Kick Pleat (CLI-001)
Vendor registered: WP Martin (VEN-001)
Milestone added to VEN-001: Review consignment terms
```

---

## Local-mode notes

- Real inventory sync requires connecting the POS/e-commerce platform (not yet implemented).
- Payment links are local placeholders until `STRIPE_SECRET_KEY` is configured.

---

## Outcome

Kick Pleat leaves the onboarding with:

- A Q3 margin budget and vendor directory.
- A local payment link for a flagship product.
- A new-arrival content calendar and email draft.
- A retail launch project with reorder deadline.
- A designer/vendor registry with consignment milestone.
