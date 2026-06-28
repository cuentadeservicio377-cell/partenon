# Retail Simulation — Example Bookstore

This document walks through a simulated Partenon onboarding for Example Bookstore, an independent bookstore in Example City, Example State. See the company card in [`workshop/companies/retail--example-bookstore.md`](../companies/retail--example-bookstore.md).

## 1. Company interview

| Question | Answer |
|----------|--------|
| Company name | Example Bookstore |
| Industry | Independent bookstore / retail |
| Location | 123 Example Street, Example City, EX |
| Team size | ~20–30 employees plus event staff |
| Currency and fiscal year | USD, calendar year |
| Annual revenue | Estimated $3M–$8M (private company) |
| Biggest operational pain | Razor-thin margins, rising rent, inventory management across books/gifts/events |
| Tools already in use | Example POS, Google Workspace, Example Store Platform (online orders), Example Email Platform, Instagram, Example Events Platform |
| Who approves events and promotions | Co-owner / events director |
| Who manages inventory | Buyer / head book buyer |

## 2. Hero selection

Following the Entrepreneur Playbook priority for retail / e-commerce, Hermes recommends:

1. **Scribe** — track COGS, shipping, event costs, rent, and margins by product line.
2. **Collector** — handle online orders, event ticket links, and loyalty subscriptions.
3. **Herald** — plan promotional calendars, event announcements, and newsletter content.
4. **Strategist** — coordinate restocking, event setup, and supplier deadlines.
5. **Diplomat** — manage publisher/author relationships and community partnerships.

## 3. Config files created

### `.finance` (Scribe)

```toml
[company]
name = "Example Bookstore"
currency = "USD"
fiscal_year = 2026
responsible = "Scribe"

[fixed_costs]
[[fixed_costs.item]]
name = "Example Street rent"
amount = 22000.00
frequency = "monthly"
category = "office"
due_day = 1

[[fixed_costs.item]]
name = "Payroll"
amount = 32000.00
frequency = "biweekly"
category = "payroll"
due_day = 15

[[fixed_costs.item]]
name = "POS and software subscriptions"
amount = 1200.00
frequency = "monthly"
category = "technology"
due_day = 5

[variable_costs]
[[variable_costs.item]]
name = "Book inventory"
category = "materials"
monthly_budget = 80000.00

[[variable_costs.item]]
name = "Gift and sidelines inventory"
category = "materials"
monthly_budget = 25000.00

[[variable_costs.item]]
name = "Event costs"
category = "marketing"
monthly_budget = 5000.00

[[variable_costs.item]]
name = "Shipping and freight"
category = "logistics"
monthly_budget = 4000.00

[vendors]
[[vendors.item]]
id = "P001"
name = "Example Publisher"
contact = "Sales rep"
payment_terms = "net 30"
lead_time = "1-2 weeks"
rating = 5

[[vendors.item]]
id = "P002"
name = "Publisher B"
contact = "Sales rep"
payment_terms = "net 30"
lead_time = "1-2 weeks"
rating = 5

[rules]
minimum_expected_margin = 5.0
alert_days_before_due = 3
```

### `.payments` (Collector)

```yaml
metadata:
  version: "0.1.0"
  profile: partenon-cobrador
  currency: USD
  timezone: America/New_York

products:
  - id: prod_event_ticket
    name: "Author event ticket"
    description: "Reserved seat at in-store author event"
    active: true

  - id: prod_book_club
    name: "Book club subscription"
    description: "Monthly book club pick with discussion guide"
    active: true

prices:
  - id: price_event
    product_id: prod_event_ticket
    amount: 500
    currency: usd
    type: one_time

  - id: price_book_club
    product_id: prod_book_club
    amount: 2500
    currency: usd
    type: recurring
    interval: month
    interval_count: 1

links: []
subscriptions: []
customers: []
invoices: []
payments: []
reminders: []

policies:
  max_reminders: 2
  days_before_reminder: 1
  days_after_due_for_escalation: 1
  allow_partial_payments: false
```

### `.design` (Herald)

```yaml
meta:
  version: "0.1.0"
  profile: partenon-herald

brand:
  brand_name: "Example Bookstore"
  website: "https://www.harborbooks.example.com"
  industry: "retail"
  market: "Example City, Example Region, and online customers"
  stage: "established"

positioning:
  what_you_sell: "Curated books, gifts, and community events in a neighborhood bookstore"
  who_you_help: "Readers and gift buyers who value curation, community, and independent retail"
  how_you_do_it: "Our staff picks the best new and used books and hosts authors in conversation"

voice:
  tone: "warm"
  addressing: "you informal"
  style: "clear, no filler, no emojis"
  emojis: false

channels:
  - instagram
  - newsletter
  - blog

messaging:
  key_messages:
    - "A bookstore is a public living room"
    - "Staff picks you can trust"
    - "Meet authors where ideas live"
  claims_to_avoid:
    - "Largest selection in Example City"
    - "Cheapest prices guaranteed"

operations:
  final_approver: "Events director"
  autonomy:
    draft_copy: true
    create_calendar: true
    publish_social: false
    send_email: false
```

### `.ops` (Strategist)

```yaml
profile: partenon-estratega
owner: "Co-owner"
assistant_name: "Strategist"

calendar:
  morning_briefing: "08:00"
  midday_pulse: "13:00"
  evening_wrap: "17:00"
  weekly_planning: "monday 08:00"
  weekly_retro: "sunday 18:00"
  timezone: "America/New_York"

projects:
  default_duration_days: 14
  auto_checklist: true
  notify_diplomat_on_milestones: true

tasks:
  default_priority: medium
  default_duration_days: 3
  escalate_blocked_after_hours: 48

goals:
  review_day: sunday
  default_type: weekly
  departments:
    - operations
    - sales
```

## 4. First missions

### Mission 1 — Scribe: margin by product line

```bash
hermes profile use partenon-tesorero
```

Prompt:

```text
Scribe, load last quarter's POS export and categorize sales into books, gifts,
and events. Show revenue, COGS, and margin for each line. Flag any category
below the 5% minimum margin.
```

Actual Python equivalent:

```bash
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/parsers.py \
  --input data/example-q2-pos.xlsx \
  --by-category "books,gifts,events" \
  --output data/example-margin-by-line.json
```

**Expected output:**

```json
{
  "period": "2026-Q2",
  "lines": [
    { "category": "books", "revenue": 420000, "cogs": 378000, "margin_pct": 10.0 },
    { "category": "gifts", "revenue": 95000, "cogs": 57000, "margin_pct": 40.0 },
    { "category": "events", "revenue": 18000, "cogs": 15000, "margin_pct": 16.7 }
  ],
  "alerts": []
}
```

**Actual gap:** `parsers.py` classifies expenses but does not automatically map POS sales categories to product-line margins. The user must provide a category mapping.

### Mission 2 — Herald: monthly event and promotion calendar

```bash
hermes profile use partenon-mensajero
```

Prompt:

```text
Herald, read .design and create a July calendar with two author events, one book
club meeting, and a sidelines summer promotion. Output to
output/campaigns/july-2026/content-calendar.json.
```

Actual Python equivalent:

```bash
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/content_calendar.py \
  --topic "July author events, book club, and summer sidelines promotion" \
  --channels instagram,newsletter \
  --days 31 \
  --output output/campaigns/july-2026/content-calendar.json
```

**Expected output:**

```json
{
  "campaign_id": "july-2026",
  "days": 31,
  "events": [
    { "date": "2026-07-09", "type": "author_event", "channel": "newsletter" },
    { "date": "2026-07-16", "type": "book_club", "channel": "instagram" },
    { "date": "2026-07-23", "type": "author_event", "channel": "newsletter" },
    { "date": "2026-07-25", "type": "promotion", "channel": "instagram" }
  ],
  "status": "draft_pending_approval"
}
```

**Actual gap:** Calendar output is JSON only; no direct Example Email Platform or Instagram scheduling integration.

### Mission 3 — Strategist: restocking and event coordination

```bash
hermes profile use partenon-estratega
```

Prompt:

```text
Strategist, create a project "July 2026 events and restock" with tasks for
ordering gift inventory, confirming author travel, setting up event seating,
and scheduling staff. Generate a retail checklist.
```

Actual Python equivalent:

```bash
python3 hermes/profiles/partenon-estratega/skills/ops/tools/projects.py \
  --create "July 2026 events and restock" \
  --due 2026-07-31

python3 hermes/profiles/partenon-estratega/skills/ops/tools/checklists.py \
  --project "July 2026 events and restock" \
  --type retail
```

**Expected output:**

```json
{
  "project_id": "PROJ-001",
  "title": "July 2026 events and restock",
  "checklist": {
    "inventory": [
      "Review low-stock report",
      "Place gift orders",
      "Receive and tag deliveries"
    ],
    "events": [
      "Confirm author travel",
      "Order event chairs",
      "Publish event listings",
      "Assign event staff"
    ]
  }
}
```

**Actual gap:** No retail-specific checklist template is included; the example above is manually configured.

## 5. Smoke test summary

| Hero | Command | Expected result | Status |
|------|---------|-----------------|--------|
| Scribe | `python3 .../parsers.py --by-category` | Margin by line | PARTIAL (manual mapping) |
| Collector | `python3 .../stripe_tools.py --create-link` | Ticket link | PARTIAL (needs Stripe test key) |
| Herald | `python3 .../content_calendar.py` | Calendar JSON | PASS (draft only) |
| Strategist | `python3 .../projects.py --create` + `checklists.py` | Project + checklist | PASS (manual template) |

## 6. Gaps documented

- **No POS sales-to-margin mapping.** The Scribe parses expenses but does not automatically pull revenue categories from Square.
- **No inventory-level tracking.** Partenon tracks budgets but not SKU-level stock or reorder points.
- **No event platform integration.** Example Events Platform or Example Store Platform event ticket links must be created manually.
- **No retail checklist template.** The Strategist checklist tool needs a retail/events template.
- **No publisher API integration.** The Diplomat cannot sync with publisher portals or author contacts.
