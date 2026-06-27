# Simulation: Onboarding Outseta

This walkthrough shows how Partenon's heroes help a bootstrapped SaaS company protect access, control spend, manage subscriptions, and document decisions. Everything runs in local mode.

- **Company card:** [`workshop/companies/saas-startup--outseta.md`](../companies/saas-startup--outseta.md)
- **Hero activation order:** Guardian → Scribe → Collector → Strategist → Brain

---

## Prerequisites

```bash
./install.sh
source .venv/bin/activate
```

---

## Step 1 — Guardian: audit keys and profile access

**Hermes prompt:**

```text
Guardian, list all API keys, flag any older than 90 days, and run audit_access
for every Partenon profile.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-guardian/skills/security/tools")
from key_manager import list_keys, audit_access

for key in list_keys():
    print(f"{key['provider']}: {key['status']} ({key['key_id']})")

for profile in [
    "partenon-tesorero", "partenon-mensajero", "partenon-cobrador",
    "partenon-guardian", "partenon-estratega", "partenon-diplomatico", "partenon-brain"
]:
    audit = audit_access(profile)
    print(f"{profile}: tools={audit['tools']} violations={audit['violations']}")
PY
```

Expected output (depends on your `.env`):

```text
nvidia: active (NVIDIA_API_KEY)
openai: missing (OPENAI_API_KEY)
kimi: missing (KIMI_API_KEY)
stripe: missing (STRIPE_SECRET_KEY)
partenon-tesorero: tools=['file', 'terminal'] violations=[]
...
```

---

## Step 2 — Scribe: cloud spend and runway

**Hermes prompt:**

```text
Scribe, create a cash-flow projection for the next 6 months and a budget with
line items for hosting, contractors, payment processing fees, and support tools.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-tesorero/skills/finance/tools")
from templates import get_templates

t = get_templates()
t.create_cash_flow("outseta-cash-flow.xlsx", months=6)
t.create_budget(
    "outseta-budget.xlsx",
    period="2026-H2",
    line_items=[
        {"line_item": "Cloud hosting", "budget": 2500, "actual": 0},
        {"line_item": "Contractor payments", "budget": 15000, "actual": 0},
        {"line_item": "Stripe + Outseta fees", "budget": 3500, "actual": 0},
        {"line_item": "Support and help desk tools", "budget": 800, "actual": 0},
    ]
)
print("Finance templates created.")
PY
```

Expected output:

```text
Finance templates created.
```

---

## Step 3 — Collector: subscriptions, failed payments, and churn signals

**Hermes prompt:**

```text
Collector, create a monthly subscription for founder@example.com at $87 USD/month
and generate the income report for 2026-06-01 to 2026-06-30.
```

**Direct Python:**

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-cobrador/skills/payments/tools")
from stripe_tools import create_subscription, generate_income_report

print(create_subscription(
    {"email": "founder@example.com", "name": "Founder"},
    {"amount": 8700, "currency": "usd", "interval": "month"}
))

print(generate_income_report("2026-06-01", "2026-06-30"))
PY
```

Expected output (local mode):

```json
{
  "success": true,
  "subscription_id": "sub_001",
  "status": "active",
  "next_payment": "...",
  "message": "Subscription sub_001 created in local mode for founder@example.com."
}
{
  "success": true,
  "period": {"start": "2026-06-01", "end": "2026-06-30"},
  "total_collected": 0,
  "pending": 0,
  "overdue": 0,
  ...
}
```

---

## Step 4 — Strategist: sprint and feature-launch checklist

**Hermes prompt:**

```text
Strategist, create a project "Add native mobile dashboard" for client
CLI-OUTSETA with delivery 2026-09-30. Add a consulting checklist and assign
"Scope iOS view" to Lead Engineer with high priority due 2026-07-10.
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
    name="Add native mobile dashboard",
    client_id="CLI-OUTSETA",
    client_name="Outseta",
    delivery_date="2026-09-30",
    amount=0,
    type="consulting"
)
print(p["message"])

t = get_tasks().create_task(
    project_id=p["project"]["id"],
    title="Scope iOS view",
    assignee="Lead Engineer",
    due_date="2026-07-10",
    priority="high"
)
print(t["message"])

print(get_checklists().create_project_checklist(p["project"]["id"], industry="consulting")["message"])
PY
```

Expected output:

```text
Project created: Add native mobile dashboard (PROJ-001)
Task created: Scope iOS view (TASK-001)
Checklist created for PROJ-001 with 15 items
```

---

## Step 5 — Brain: index a decision

**Hermes prompt:**

```text
Brain, index this validated decision: "We will not build our own subscription
management logic; we will use Stripe Billing for new products."
```

**Direct Python:**

The Brain's G-Brain client shells out to the `gbrain` binary, which is not bundled. In local mode, record the decision as a local markdown note:

```bash
cat > docs/decisions/2026-06-26-stripe-billing.md <<'EOF'
# Decision: Use Stripe Billing for new products

- **Author:** Outseta engineering
- **Date:** 2026-06-26
- **Status:** validated
- **Context:** Maintaining our own subscription management logic creates ongoing
  engineering overhead and reduces interoperability with the Stripe ecosystem.
- **Decision:** New products will use Stripe Billing instead of custom logic.
- **Consequences:** Faster time to market, less maintenance, but migration effort
  for legacy products.
EOF
```

Expected result: a decision file that new hires can read.

---

## Local-mode notes

- Real G-Brain indexing requires `GBRAIN_DATABASE_URL` and the `gbrain` binary.
- Real Stripe subscription management requires `STRIPE_SECRET_KEY`.

---

## Outcome

Outseta leaves the onboarding with:

- A Guardian audit of API keys and profile permissions.
- A 6-month cash-flow projection and operating budget.
- Local subscription and income-report records.
- A product-launch project with an iOS scoping task.
- A documented architecture decision for new hires.
