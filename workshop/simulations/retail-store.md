# Simulated Partenon Onboarding: Brazos Bookstore

This simulation walks through onboarding an independent bookstore using the real Partenon repository. It is based on the public company card in [`workshop/companies/retail-store--brazos-bookstore.md`](../companies/retail-store--brazos-bookstore.md).

---

## 1. Business context

- **Company:** Brazos Bookstore
- **Industry:** Retail / independent bookstore
- **Location:** Houston, TX
- **Headcount:** ~6 employees
- **Top pains:** razor-thin margins, inventory management in a small footprint, price competition, event coordination, staff attentiveness

---

## 2. Hermes interview questions

Hermes asks the owner or general manager:

1. What is your primary currency and fiscal year? (USD, calendar year)
2. How do you track inventory today? (POS system, spreadsheets, publisher invoices)
3. What are your main revenue streams? (book sales, gifts, events, online orders, subscriptions)
4. Which product categories have the best and worst margins? (new books, used books, gifts, events)
5. How do you plan author events and book clubs? (calendar, email, social media)
6. Who are your top three distributors or publishers?
7. Do you sell online or through any subscription/loyalty program?
8. What shared logins exist? (POS, e-commerce, social media, accounting)

---

## 3. Hero selection

| Priority | Hero | Why first |
|----------|------|-----------|
| 1 | **Scribe** | Margin visibility by product line is the biggest lever. |
| 2 | **Collector** | Event tickets, online orders, and loyalty subscriptions need simple checkout. |
| 3 | **Herald** | Events and staff picks drive foot traffic; content calendars reduce blank-page friction. |
| 4 | **Strategist** | Event calendars, restocking, and supplier deadlines must stay coordinated. |
| 5 | **Diplomat** | Publisher and author relationships need milestone tracking. |

Guardian and Brain are deferred to month two.

---

## 4. Config files created

### `client.yaml`

```yaml
company:
  name: "Brazos Bookstore"
  industry: "retail"
  sub_industry: "independent bookstore"
  currency: "USD"
  timezone: "America/Chicago"
  fiscal_year_start: "2026-01-01"
  locations: 1
  employees: 6

contacts:
  owner: "General Manager"
  operations: "ops@brazosbookstore.example.com"
  finance: "finance@brazosbookstore.example.com"

integrations:
  google_workspace: true
  stripe: true
  gbrain: false

active_profiles:
  - partenon-tesorero
  - partenon-cobrador
  - partenon-mensajero
  - partenon-estratega
  - partenon-diplomatico
```

### `.finance` (Scribe)

```toml
[company]
name = "Brazos Bookstore"
currency = "USD"
fiscal_year = 2026
responsible = "Scribe"

[fixed_costs]
[[fixed_costs.item]]
name = "Store rent"
amount = 6200.00
frequency = "monthly"
category = "office"

[[fixed_costs.item]]
name = "Payroll"
amount = 14000.00
frequency = "biweekly"
category = "payroll"

[variable_costs]
[[variable_costs.item]]
name = "Book inventory"
category = "materials"
monthly_budget = 25000.00
default_vendor = "Ingram Content Group"

[[variable_costs.item]]
name = "Gift and sidelines inventory"
category = "materials"
monthly_budget = 4000.00

[[variable_costs.item]]
name = "Event costs"
category = "marketing"
monthly_budget = 1500.00

[rules]
tax_rate = 0.0
minimum_expected_margin = 8.0
alert_days_before_due = 3
```

### `.payments` (Collector)

```yaml
metadata:
  version: "0.1.0"
  profile: partenon-cobrador
  currency: USD
  timezone: America/Chicago

products:
  - id: prod_event_ticket
    name: "Author Event Ticket"
    description: "Reserved seating and signed copy"
    active: true
  - id: prod_book_club
    name: "Book Club Season Pass"
    description: "Quarterly book club membership"
    active: true
  - id: prod_online_order
    name: "Online Book Order"
    description: "Shipped book order"
    active: true

policies:
  max_reminders: 2
  days_before_reminder: 3
  days_after_due_for_escalation: 5
  allow_partial_payments: false
```

### `.design` (Herald)

```yaml
meta:
  version: "0.1.0"
  profile: partenon-mensajero

brand:
  brand_name: "Brazos Bookstore"
  website: "https://www.brazosbookstore.com"
  industry: "retail"
  market: "Houston, TX"
  stage: "established"

positioning:
  what_you_sell: "Curated books, gifts, and community events"
  who_you_help: "Readers, families, and local authors in Houston"
  how_you_do_it: "We hand-pick titles and host the conversations that matter"

voice:
  tone: "warm"
  addressing: "you informal"
  style: "clear, no filler, no emojis"
  emojis: false

channels:
  - instagram
  - newsletter
  - events

operations:
  final_approver: "Owner"
  autonomy:
    draft_copy: true
    create_calendar: true
    publish_social: false
    send_email: false
```

### `.ops` (Strategist)

```yaml
profile: partenon-estratega
owner: "General Manager"
assistant_name: "Strategist"

calendar:
  morning_briefing: "08:30"
  midday_pulse: "13:00"
  weekly_planning: "monday 09:00"
  timezone: "America/Chicago"

projects:
  default_duration_days: 14
  auto_checklist: true
  notify_diplomat_on_milestones: true

tasks:
  default_priority: medium
  default_duration_days: 3
  escalate_blocked_after_hours: 48
```

### `.relations` (Diplomat)

```json
{
  "company": "Brazos Bookstore",
  "updated": "2026-06-27T00:00:00",
  "clients": [
    {
      "id": "CLI-001",
      "name": "Local Author Series",
      "main_contact": { "name": "Events Coordinator", "email": "events@brazosbookstore.example.com" },
      "category": "partner",
      "status": "active",
      "rating": "A",
      "milestones": [
        { "id": "MIL-001", "description": "Confirm July author lineup", "date": "2026-07-01", "status": "proposed", "confirmed_in_writing": false, "next_step": "Send contract drafts" }
      ]
    }
  ],
  "vendors": [
    { "id": "VEN-001", "name": "Ingram Content Group", "category": "distributor", "status": "active", "rating": "A" }
  ],
  "contracts": [],
  "communications": [],
  "reminders": []
}
```

---

## 5. Commands and expected outputs

### Install and verify

```bash
./install.sh
python3 scripts/demo_tesorero.py
```

Expected output matches the verified Scribe demo report.

### Scribe: build a margin workbook

```bash
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/templates.py
```

This generates local budget/vendors/cash-flow templates. With real Google credentials, the Scribe would run `google_sheets.py` to publish the dashboard.

### Collector: create an event ticket payment link

```bash
python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py
```

Local-mode output shows payment-link creation, invoice creation, payment recording, and sync-with-Treasurer flag.

> **Gap:** The Collector runs in local mode without a real Stripe key. Live mode requires `STRIPE_SECRET_KEY` in `.env`.

### Herald: generate a staff-pick post

```bash
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py post "staff pick: new literary fiction" instagram
```

Actual output from this repo is structurally valid but generic. A real onboarding would first run `brand_intake.py` with the full `.design` file.

### Strategist: create an event project

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-estratega/skills/ops/tools")
from projects import get_projects

p = get_projects().create_project(
    name="July Author Reading Series",
    client_id="CLI-001",
    client_name="Local Author Series",
    delivery_date="2026-07-15",
    amount=3000
)
print(p)
PY
```

Expected output: project `PROJ-001` written to `partenon-core/data/projects.json`.

### Diplomat: run daily follow-ups

```bash
python3 hermes/profiles/partenon-diplomatico/skills/relations/tools/followups.py
```

Actual output (with the sample `.relations`):

```text
Daily Follow-ups — Diplomat
Date: 2026-06-27
Total pending: 1

[MILESTONE] Milestone MIL-001: Confirm July author lineup (2026-07-01) — Send contract drafts
```

> **Gap:** Follow-ups only work after clients and milestones are preloaded. There is no bulk import from a CRM export yet.

---

## 6. First three missions per hero

### Scribe

1. **Parse last month's POS export** and classify every line as fixed, variable, or COGS by product category.
2. **Build a category-level margin summary** showing revenue, COGS, and margin for books, gifts, and events.
3. **Run a weekly budget review** comparing actual inventory and event spend to the budgets set in `.finance`.

### Collector

1. **Create a Stripe payment link** for "Author Event Ticket" priced at $25.
2. **Create a quarterly "Book Club Season Pass" subscription** priced at $45.
3. **Run the daily collection review** and flag any online order overdue by more than 5 days.

### Herald

1. **Run the brand interview** (`brand_intake.py`) and save the refined `.design` file.
2. **Generate a 30-day event calendar** for Instagram and the newsletter.
3. **Draft three staff-pick posts** and run banned-claim QA.

### Strategist

1. **Create a project** for each upcoming author event with delivery date and owner.
2. **Generate an event-prep checklist** (promotion, seating, signing, inventory) and assign tasks.
3. **Schedule restocking reminders** tied to distributor delivery windows.

### Diplomat

1. **Register the top five distributors and regular authors** using `crm.py`.
2. **Add milestones** for event confirmations, seasonal catalog deadlines, and contract renewals.
3. **Run daily follow-ups** and draft reminder emails for anyone with a milestone in the next 3 days.

---

## 7. Gaps found during simulation

| Gap | Severity | Evidence |
|-----|----------|----------|
| No POS-to-Scribe integration | HIGH | `parsers.py` reads Excel/CSV, but no script imports a live POS export and classifies it. |
| No inventory sync | HIGH | Stock levels are not connected to the Strategist or Scribe. |
| No event-ticketing integration | MEDIUM | Collector can create payment links, but event RSVP/seating is manual. |
| Herald copy generator lacks brand context | MEDIUM | Output is generic unless `.design` is fully populated. |
| No automated restock triggers | MEDIUM | Strategist can schedule tasks, but reorder points are not calculated. |
