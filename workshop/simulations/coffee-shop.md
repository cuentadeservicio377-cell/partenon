# Simulated Partenon Onboarding: Coffee By Design

This simulation walks Coffee By Design (Portland, Maine) through a first-week Partenon setup. All commands use the actual Hermes profiles and Python tools in this repository.

## Company snapshot
- **Business**: Independent coffee roaster and cafe chain
- **Locations**: Four coffeehouses + one roastery in Greater Portland, Maine
- **Team**: ~55 employees
- **Channels**: Cafes, wholesale (~600 accounts), online store, events
- **Top pain points**: labor scheduling, multi-channel margins, inventory coordination, founder dependency

---

## Step 1: Company interview

Hermes asks the founder or operations manager the following questions. Answers are written to `client.yaml`.

```yaml
company:
  name: "Coffee By Design"
  industry: "food and beverage"
  sub_industry: "coffee roaster and cafe chain"
  location: "Portland, Maine, USA"
  employees: 55
  currency: "USD"
  fiscal_year: 2026
  timezone: "America/New_York"
  primary_sales_channels:
    - cafe_sales
    - wholesale
    - online_store
    - events
  current_tools:
    - "Square POS"
    - "QuickBooks"
    - "Google Workspace"
    - "Instagram / Facebook"
  top_pain_points:
    - "Do not know true margin by channel"
    - "Scheduling is manual and reactive"
    - "Wholesale orders and green-coffee lead times live in spreadsheets"
    - "Marketing depends on the founder"
  compliance_needs:
    - "Sales tax by Maine jurisdiction"
    - "Food safety logs"
    - "B Corp reporting"
```

## Step 2: Hero selection

Recommended first heroes for a coffee shop: **Scribe → Strategist → Herald → Collector**.

| Priority | Hero | First responsibility |
|----------|------|----------------------|
| 1 | Scribe | Build a channel-level finance dashboard |
| 2 | Strategist | Schedule staff, roasting, and supplier deadlines |
| 3 | Herald | Generate a weekly local-social content calendar |
| 4 | Collector | Set up Stripe payment links for catering and merch |

Guardian and Diplomat are added in week two after the first four are running.

## Step 3: Profile config files

Copy the templates from each profile:

```bash
cp hermes/profiles/partenon-tesorero/templates/.finance.example .finance
cp hermes/profiles/partenon-estratega/templates/.ops.example .ops
cp hermes/profiles/partenon-mensajero/templates/.design.example .design
cp hermes/profiles/partenon-cobrador/templates/.payments.example .payments
```

### `.finance` — Scribe

Trimmed to Coffee By Design's fixed and variable costs:

```toml
[company]
name = "Coffee By Design"
tax_id = "XX-XXXXXXX"
currency = "USD"
fiscal_year = 2026
responsible = "Scribe"
master_spreadsheet = ""

[fixed_costs]
[[fixed_costs.item]]
name = "Diamond Street roastery rent"
amount = 8500.00
frequency = "monthly"
category = "office"
due_day = 1

[[fixed_costs.item]]
name = "Congress Street cafe rent"
amount = 5200.00
frequency = "monthly"
category = "office"
due_day = 1

[[fixed_costs.item]]
name = "Base payroll"
amount = 38000.00
frequency = "biweekly"
category = "payroll"
due_day = 15

[[fixed_costs.item]]
name = "Roasting equipment lease"
amount = 1200.00
frequency = "monthly"
category = "technology"
due_day = 20

[variable_costs]
[[variable_costs.item]]
name = "Green coffee beans"
category = "materials"
monthly_budget = 18000.00
default_vendor = "Importer A"

[[variable_costs.item]]
name = "Meta and Instagram ads"
category = "marketing"
monthly_budget = 2500.00
default_vendor = "Meta"

[[variable_costs.item]]
name = "Local delivery"
category = "logistics"
monthly_budget = 900.00

[budgets]
[[budgets.area]]
name = "Cafe operations"
amount = 45000.00
period = "2026-Q3"
responsible = "Strategist"

[[budgets.area]]
name = "Wholesale"
amount = 35000.00
period = "2026-Q3"
responsible = "Strategist"

[[budgets.area]]
name = "Marketing"
amount = 8000.00
period = "2026-Q3"
responsible = "Messenger"

[rules]
tax_rate = 0.055
minimum_expected_margin = 25.0
alert_days_before_due = 3
rounding_decimals = 2
allow_expense_without_budget = false
connect_with_messenger = true
```

### `.ops` — Strategist

```yaml
profile: partenon-estratega
owner: "Mary Allen Lindemann"
assistant_name: "Strategist"

calendar:
  morning_briefing: "07:30"
  midday_pulse: "13:00"
  evening_wrap: "17:00"
  weekly_planning: "monday 08:00"
  weekly_retro: "sunday 19:00"
  timezone: "America/New_York"

projects:
  default_duration_days: 14
  auto_checklist: true
  notify_diplomat_on_milestones: true

tasks:
  default_priority: medium
  default_duration_days: 3
  escalate_blocked_after_hours: 24

goals:
  review_day: sunday
  default_type: weekly
  departments:
    - general
    - sales
    - operations
    - finance
```

### `.design` — Herald

Generated through the brand intake tool. Example answers:

```yaml
meta:
  version: "0.1.0"
  profile: partenon-herald

brand:
  brand_name: "Coffee By Design"
  website: "https://coffeebydesign.com"
  industry: "food and beverage"
  market: "Greater Portland, Maine + online"
  stage: "growth"

positioning:
  what_you_sell: "Handcrafted coffee, in-house roasting, and community cafes"
  who_you_help: "Local coffee drinkers, wholesale accounts, and online buyers who care about ethical sourcing"
  how_you_do_it: "We roast in small batches in Portland and reinvest in local arts and coffee-farming communities"
  positioning: "For Portland-area coffee lovers who want quality without pretension, Coffee By Design offers fresh, ethical coffee that supports the local community"
  differentiator: "30-year local track record, B Corp certification, direct relationships with coffee farmers"

voice:
  tone: "direct"
  addressing: "you informal"
  style: "clear, warm, no filler"
  emojis: false
  slang: false

channels:
  - instagram
  - facebook
  - newsletter
  - blog

messaging:
  key_messages:
    - "Great coffee changes lives when the whole chain is treated fairly"
    - "Roasted in Portland, enjoyed everywhere"
  claims_to_avoid:
    - "Best coffee in the world"
    - "100% sustainable"

operations:
  final_approver: "Mary Allen Lindemann"
  autonomy:
    draft_copy: true
    create_calendar: true
    publish_social: false
    send_email: false
    launch_ads: false
```

### `.payments` — Collector

```yaml
metadata:
  version: "0.1.0"
  profile: partenon-cobrador
  currency: USD
  timezone: America/New_York

products:
  - id: prod_catering
    name: "Catering package — 50 cups"
    description: "Coffee catering for offices and events"
    active: true
  - id: prod_merch
    name: "Branded mug"
    description: "Ceramic mug with Coffee By Design logo"
    active: true

prices:
  - id: price_catering
    product_id: prod_catering
    amount: 17500
    currency: usd
    type: one_time
  - id: price_mug
    product_id: prod_merch
    amount: 1800
    currency: usd
    type: one_time

links: []
subscriptions: []
customers: []
invoices: []
payments: []
reminders: []

policies:
  max_reminders: 3
  days_before_reminder: 3
  days_after_due_for_escalation: 7
  allow_partial_payments: false
```

---

## Step 4: First 3 missions

### Mission 1 — Scribe: channel-level finance dashboard

Command:

```bash
hermes profile use partenon-tesorero
python3 scripts/demo_tesorero.py
```

Expected output:

```json
{
  "timestamp": "2026-06-27T...Z",
  "income": 4000.00,
  "fixed_expenses": 609.00,
  "variable_expenses": 1030.00,
  "margin": 2361.00,
  "margin_pct": 59.03,
  "alerts": []
}
```

Next, Scribe reads `.finance` and proposes a real Google Sheet:

```text
Scribe, create a master spreadsheet "Coffee By Design — Finances" with sheets:
Income by Channel, Fixed Costs, Variable Costs, Vendors, Budget vs Actual.
Populate Fixed Costs and Variable Costs from .finance.
```

**Gap found**: `google_sheets.py` can create a spreadsheet and seed headers, but it does not yet parse an uploaded Square/QuickBooks export and write it to Sheets end-to-end. The user must export data manually or connect the Google Workspace MCP.

### Mission 2 — Strategist: weekly schedule and supplier deadlines

Commands:

```bash
hermes profile use partenon-estratega
python3 hermes/profiles/partenon-estratega/skills/ops/tools/projects.py \
  --create "Wholesale order cycle — week of 2026-07-06" \
  --delivery 2026-07-10
```

Expected output:

```json
{
  "success": true,
  "project": {
    "id": "PROJ-001",
    "name": "Wholesale order cycle — week of 2026-07-06",
    "status": "planned",
    "delivery_date": "2026-07-10T..."
  },
  "message": "Project created: Wholesale order cycle — week of 2026-07-06 (PROJ-001)"
}
```

Add tasks:

```python
from hermes.profiles.partenon-estratega.skills.ops.tools.tasks import get_tasks

tasks = get_tasks()
tasks.create_task(
    project_id="PROJ-001",
    title="Confirm green-coffee delivery with importer",
    assignee="Roastery manager",
    due_date="2026-07-07",
    priority="high",
    tags=["supplier", "inventory"]
)
tasks.create_task(
    project_id="PROJ-001",
    title="Publish weekly staff schedule",
    assignee="Cafe lead",
    due_date="2026-07-05",
    priority="high",
    tags=["scheduling", "staff"]
)
```

**Gap found**: The Strategist's tools read and write local JSON only. There is no live Google Calendar or Gmail MCP integration, so calendar invites and shift reminders are not dispatched automatically.

### Mission 3 — Herald + Collector: content calendar and payment link

Herald generates the calendar:

```bash
hermes profile use partenon-mensajero
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/content_calendar.py \
  "summer cold brew and community events" \
  instagram,newsletter \
  7
```

Expected output:

```json
{
  "success": true,
  "campaign_id": "CAL-20260627-abc123",
  "calendar_path": ".../output/campaigns/CAL-20260627-abc123/content-calendar.json",
  "days": 7,
  "channels": ["instagram", "newsletter"]
}
```

Collector creates a catering payment link:

```bash
hermes profile use partenon-cobrador
python3 -c "
from hermes.profiles.partenon-cobrador.skills.payments.tools.stripe_tools import create_payment_link
print(create_payment_link(
    {'name': 'Catering package — 50 cups'},
    {'amount': 17500, 'currency': 'usd'}
))
"
```

Expected output (local mode, because Stripe MCP is not configured):

```json
{
  "success": true,
  "url": "https://buy.stripe.com/test_link_001",
  "payment_link_id": "link_001",
  "message": "Payment link created in local mode (Stripe MCP not available)."
}
```

**Gap found**: `publish_post.py` and `schedule_content.py` exist, but there is no actual LinkedIn, Instagram, or Facebook publishing integration. Posts are drafted and saved locally. The Collector also cannot create a real Stripe link without `STRIPE_SECRET_KEY`.

---

## Step 5: Smoke test summary

| Hero | Test command | Expected result | Status |
|------|--------------|-----------------|--------|
| Scribe | `python3 scripts/demo_tesorero.py` | Workbook + JSON report created | PASS (with local data) |
| Strategist | `python3 .../projects.py --create ...` | Project JSON created | PASS |
| Herald | `python3 .../content_calendar.py ...` | Calendar JSON created | PASS |
| Collector | `python3 -c "...create_payment_link..."` | Local payment link record created | PASS (local mode) |
| Brain | `python3 .../gbrain_client.py` | Requires `gbrain` binary | FAIL / not configured |

---

## Consolidated gaps for Coffee By Design

1. **No live Google Sheets write**. Scribe builds local templates only until `GOOGLE_SERVICE_ACCOUNT_JSON` is configured.
2. **No POS integration**. Square/QuickBooks exports are not parsed automatically.
3. **No social publishing**. Herald drafts content but cannot post to Instagram/Facebook.
4. **No real Stripe link**. Collector runs in local mode without `STRIPE_SECRET_KEY`.
5. **No calendar/email dispatch**. Strategist stores tasks locally but does not send calendar invites or reminders.
