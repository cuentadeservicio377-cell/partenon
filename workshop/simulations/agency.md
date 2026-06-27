# Simulated Partenon Onboarding: Clickers 2 Clients

This simulation walks Clickers 2 Clients (The Dalles / Central Oregon) through a first-week Partenon setup. The agency's core pain points are project deadlines, client follow-ups, scope control, and proof of ROI.

## Company snapshot
- **Business**: Small digital marketing agency
- **Location**: The Dalles / Central Oregon, USA
- **Team**: ~3–5 people plus an automated virtual assistant
- **Services**: SEO, websites, social media, email, video editing, Google Business Profile
- **Top pain points**: juggling delivery and operations, client follow-ups, manual reporting, scope creep

---

## Step 1: Company interview

```yaml
company:
  name: "Clickers 2 Clients"
  industry: "professional services"
  sub_industry: "digital marketing agency"
  location: "The Dalles, Oregon, USA"
  employees: 5
  currency: "USD"
  fiscal_year: 2026
  timezone: "America/Los_Angeles"
  primary_services:
    - seo
    - website_management
    - social_media
    - email_marketing
    - video_editing
    - google_business_profile
  current_tools:
    - "Google Workspace"
    - "WordPress"
    - "Meta Business Suite"
    - "Canva"
    - "Stripe"
  top_pain_points:
    - "No dedicated project manager; owner does sales + delivery"
    - "Client follow-ups fall through the cracks"
    - "Reporting is manual and inconsistent"
    - "Scope creep on flat-fee retainers"
  compliance_needs:
    - "Client data privacy"
    - "Ad spend access controls"
```

## Step 2: Hero selection

Recommended first heroes for an agency: **Strategist → Diplomat → Scribe → Herald → Collector**.

| Priority | Hero | First responsibility |
|----------|------|----------------------|
| 1 | Strategist | Track projects, deadlines, and task owners |
| 2 | Diplomat | Log client milestones, contracts, and follow-ups |
| 3 | Scribe | Match project budgets to actual hours and contractor costs |
| 4 | Herald | Generate case-study content and proposal copy |
| 5 | Collector | Invoice retainers and flag overdue accounts |

## Step 3: Profile config files

```bash
cp hermes/profiles/partenon-estratega/templates/.ops.example .ops
cp hermes/profiles/partenon-diplomatico/templates/.relations.example .relations
cp hermes/profiles/partenon-tesorero/templates/.finance.example .finance
cp hermes/profiles/partenon-mensajero/templates/.design.example .design
cp hermes/profiles/partenon-cobrador/templates/.payments.example .payments
```

### `.ops` — Strategist

```yaml
profile: partenon-estratega
owner: "Rebecca Van Diest"
assistant_name: "Strategist"

calendar:
  morning_briefing: "08:00"
  midday_pulse: "13:00"
  evening_wrap: "17:00"
  weekly_planning: "monday 08:00"
  weekly_retro: "friday 16:00"
  timezone: "America/Los_Angeles"

projects:
  default_duration_days: 30
  auto_checklist: true
  notify_diplomat_on_milestones: true

tasks:
  default_priority: medium
  default_duration_days: 5
  escalate_blocked_after_hours: 48

goals:
  review_day: friday
  default_type: weekly
  departments:
    - general
    - sales
    - operations
    - finance
```

### `.relations` — Diplomat

```json
{
  "company": "Clickers 2 Clients",
  "updated": "2026-06-27T00:00:00",
  "clients": [
    {
      "id": "CLI-001",
      "name": "Local Roofer LLC",
      "main_contact": {
        "name": "Pat Readyhough",
        "email": "pat@localroofer.example.com",
        "phone": "+1 555 0101"
      },
      "category": "home services",
      "origin": "referral",
      "status": "active",
      "rating": "A",
      "rating_reason": "Pays on time, clear briefs.",
      "registered_at": "2026-06-27T00:00:00",
      "last_activity": "2026-06-27T00:00:00",
      "notes": "Monthly SEO + GBP retainer.",
      "projects": ["PROJ-001"],
      "milestones": [
        {
          "id": "MIL-CLI-001-01",
          "description": "Deliver June SEO report",
          "date": "2026-06-30",
          "status": "proposed",
          "confirmed_in_writing": false,
          "responsible": "Strategist",
          "next_step": "Confirm report scope and send draft"
        }
      ]
    }
  ],
  "vendors": [
    {
      "id": "VEN-001",
      "name": "Freelance Video Editor",
      "main_contact": {
        "name": "Jordan",
        "email": "jordan@freelance.example.com"
      },
      "category": "creative",
      "service": "Video editing",
      "status": "active",
      "rating": "B",
      "rating_reason": "Good work, occasional missed deadlines.",
      "registered_at": "2026-06-27T00:00:00",
      "last_activity": "2026-06-27T00:00:00",
      "notes": "Used for client social packages.",
      "contracts": [],
      "milestones": []
    }
  ],
  "contracts": [],
  "communications": [],
  "reminders": []
}
```

### `.finance` — Scribe (project-cost view)

```toml
[company]
name = "Clickers 2 Clients"
currency = "USD"
fiscal_year = 2026
responsible = "Scribe"

[fixed_costs]
[[fixed_costs.item]]
name = "Owner salary draw"
amount = 5000.00
frequency = "monthly"
category = "payroll"
due_day = 1

[[fixed_costs.item]]
name = "Software stack"
amount = 800.00
frequency = "monthly"
category = "technology"
due_day = 15

[variable_costs]
[[variable_costs.item]]
name = "Freelancer spend"
category = "contractors"
monthly_budget = 4000.00

[[variable_costs.item]]
name = "Meta ads pass-through"
category = "marketing"
monthly_budget = 6000.00

[budgets]
[[budgets.area]]
name = "SEO retainers"
amount = 12000.00
period = "2026-Q3"
responsible = "Strategist"

[[budgets.area]]
name = "Website projects"
amount = 8000.00
period = "2026-Q3"
responsible = "Strategist"

[rules]
tax_rate = 0.00
minimum_expected_margin = 40.0
alert_days_before_due = 3
```

### `.design` — Herald

```yaml
meta:
  version: "0.1.0"
  profile: partenon-herald

brand:
  brand_name: "Clickers 2 Clients"
  website: "https://clickers2clients.com"
  industry: "professional services"
  market: "The Dalles / Columbia River Gorge + remote small businesses"
  stage: "growth"

positioning:
  what_you_sell: "Digital marketing that brings small-business ideal clients straight to them"
  who_you_help: "Small business owners who need to show up online but do not have time to manage it"
  how_you_do_it: "We handle SEO, websites, social, email, and video so owners can focus on running their business"
  differentiator: "Local, relationship-first service with an automated assistant for fast responses"

voice:
  tone: "direct"
  addressing: "you informal"
  style: "clear, no filler, no jargon"
  emojis: false

channels:
  - linkedin
  - facebook
  - instagram
  - newsletter

messaging:
  key_messages:
    - "Show up online when your ideal client is looking"
    - "Marketing done right and on time"
  claims_to_avoid:
    - "Guaranteed #1 ranking"
    - "Instant results"

operations:
  final_approver: "Rebecca Van Diest"
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
  timezone: America/Los_Angeles

products:
  - id: prod_seo_retainer
    name: "Monthly SEO + GBP retainer"
    description: "Ongoing SEO and Google Business Profile management"
    active: true
  - id: prod_website_project
    name: "Website refresh project"
    description: "5-page website update"
    active: true

prices:
  - id: price_seo
    product_id: prod_seo_retainer
    amount: 150000
    currency: usd
    type: recurring
    interval: month
  - id: price_web
    product_id: prod_website_project
    amount: 250000
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

### Mission 1 — Strategist: project + deadline tracking

Command:

```bash
hermes profile use partenon-estratega
python3 hermes/profiles/partenon-estratega/skills/ops/tools/projects.py \
  --create "Local Roofer LLC — June SEO + GBP" \
  --client CLI-001 \
  --delivery 2026-06-30 \
  --amount 1500
```

Expected output:

```json
{
  "success": true,
  "project": {
    "id": "PROJ-001",
    "name": "Local Roofer LLC — June SEO + GBP",
    "client_id": "CLI-001",
    "delivery_date": "2026-06-30T...",
    "amount": 1500
  },
  "message": "Project created: Local Roofer LLC — June SEO + GBP (PROJ-001)"
}
```

Add tasks:

```python
from hermes.profiles.partenon-estratega.skills.ops.tools.tasks import get_tasks

tasks = get_tasks()
tasks.create_task("PROJ-001", "Run SEO audit", "SEO lead", "2026-06-28", "high", tags=["seo"])
tasks.create_task("PROJ-001", "Update Google Business Profile posts", "Social lead", "2026-06-29", "medium", tags=["gbp"])
tasks.create_task("PROJ-001", "Deliver monthly report", "Rebecca", "2026-06-30", "high", tags=["reporting"])
```

### Mission 2 — Diplomat: client milestone and follow-up

Commands:

```bash
hermes profile use partenon-diplomatico
python3 -c "
from hermes.profiles.partenon-diplomatico.skills.relations.tools.crm import get_relations_crm
crm = get_relations_crm()
print(crm.add_client('Mountain View Dental', email='hello@mountainviewdental.example.com', category='healthcare', rating='B'))
print(crm.add_milestone('CLI-002', 'Send proposal for website refresh', '2026-07-03', responsible='Diplomat', next_step='Draft proposal'))
"
```

Expected output:

```json
{
  "success": true,
  "entity": { "id": "CLI-002", "name": "Mountain View Dental", ... },
  "message": "Client registered: Mountain View Dental (CLI-002)"
}
{
  "success": true,
  "milestone": { "id": "MIL-CLI-002-01", ... },
  "message": "Milestone added to CLI-002: Send proposal for website refresh"
}
```

Run daily follow-ups:

```bash
python3 hermes/profiles/partenon-diplomatico/skills/relations/tools/followups.py
```

Expected output: a list of milestones due in the next 3 days with draft reminder copy.

**Gap found**: `followups.py` can generate reports but does not send real emails. Gmail integration is not wired.

### Mission 3 — Herald + Scribe + Collector: proposal copy, budget check, invoice

Herald generates proposal copy:

```bash
hermes profile use partenon-mensajero
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py \
  "website refresh for a dental practice"
```

Expected output: draft copy saved to `output/copy/` with hooks, body, and CTA.

Scribe checks the project budget:

```text
Scribe, compare the budget for "SEO retainers" against actual freelancer spend and Meta pass-through for June.
```

Collector invoices the retainer:

```bash
hermes profile use partenon-cobrador
python3 -c "
from hermes.profiles.partenon-cobrador.skills.payments.tools.stripe_tools import create_invoice
print(create_invoice(
    {'email': 'pat@localroofer.example.com', 'name': 'Pat Readyhough'},
    [{'description': 'June SEO + GBP retainer', 'amount': 150000, 'currency': 'usd'}]
))
"
```

Expected output (local mode):

```json
{
  "success": true,
  "invoice_id": "inv_001",
  "amount": 150000,
  "currency": "USD",
  "status": "open",
  "hosted_invoice_url": "https://invoice.stripe.com/test_inv_001"
}
```

---

## Step 5: Smoke test summary

| Hero | Test command | Expected result | Status |
|------|--------------|-----------------|--------|
| Strategist | `python3 .../projects.py --create ...` | Project JSON created | PASS |
| Diplomat | `python3 -c "...crm.add_client..."` | Client + milestone added | PASS |
| Scribe | `python3 scripts/demo_tesorero.py` | Local workbook + report | PASS |
| Herald | `python3 .../copy_generator.py ...` | Draft copy generated | PASS |
| Collector | `python3 -c "...create_invoice..."` | Local invoice record | PASS (local mode) |

---

## Consolidated gaps for Clickers 2 Clients

1. **No live CRM sync**. Diplomat writes local JSON; HubSpot/Salesforce sync is a documented stub.
2. **No email dispatch**. Follow-up reminders are drafted but not sent.
3. **No time-tracking integration**. Scribe cannot pull hours from a tool like Toggl or Harvest.
4. **No ad-platform publishing**. Herald cannot publish directly to Meta or LinkedIn.
5. **No real Stripe invoicing**. Invoices are local records until `STRIPE_SECRET_KEY` is live.
