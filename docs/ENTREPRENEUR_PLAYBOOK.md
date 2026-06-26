# Partenon Entrepreneur Playbook

This is a practical guide for business owners who want to run Partenon for their company. It is not a marketing brochure. Every recommendation is tied to real files and tools in this repository.

Before using this playbook, run the 15-minute demo in [`docs/QUICKSTART.md`](QUICKSTART.md). For the full technical spec of each hero, see [`docs/HERO_GUIDE.md`](HERO_GUIDE.md).

---

## 1. Which heroes to activate first

You do not need all seven heroes on day one. Start with the ones that remove the most friction for your business type, then add the rest.

### Coffee shop (1-3 locations)

**Activate first**: Scribe → Strategist → Herald → Collector

A coffee shop has predictable daily operations, tight margins, and recurring customers. The biggest wins are knowing your numbers, staying on top of orders, and posting consistently without hiring a marketer.

| Priority | Hero | Why first |
|----------|------|-----------|
| 1 | Scribe | Classify rent, payroll, supplies, and daily sales into fixed/variable costs. Build a margin dashboard. |
| 2 | Strategist | Schedule staff, suppliers, and social posts; remind you of low-margin days. |
| 3 | Herald | Generate weekly Instagram/Reels calendars and local SEO copy without starting from a blank page. |
| 4 | Collector | Set up Stripe payment links for catering orders and loyalty subscriptions. |

### Agency (consulting, design, legal)

**Activate first**: Strategist → Diplomat → Scribe → Herald → Collector

Agencies sell time and deliverables. The critical path is project deadlines, client commitments, and cash flow visibility.

| Priority | Hero | Why first |
|----------|------|-----------|
| 1 | Strategist | Track projects, tasks, deadlines, and resource allocation. |
| 2 | Diplomat | Log client milestones, contracts, and follow-ups so nothing falls through the cracks. |
| 3 | Scribe | Match project budgets to actual hours and vendor costs. |
| 4 | Herald | Generate case-study content and proposal copy. |
| 5 | Collector | Invoice retainers and follow up on overdue accounts. |

### Construction / events / logistics

**Activate first**: Strategist → Diplomat → Scribe → Guardian

These businesses run on phases, suppliers, and physical deadlines. One missed delivery or permit can derail a project.

| Priority | Hero | Why first |
|----------|------|-----------|
| 1 | Strategist | Build phase checklists (pre-event, during-event, post-event or pre-construction, construction, closeout). |
| 2 | Diplomat | Track suppliers, contracts, and confirmation milestones. |
| 3 | Scribe | Cost each project separately: materials, labor, equipment, subcontractors. |
| 4 | Guardian | Protect shared accounts, model API keys, and supplier login credentials. |

### SaaS / tech startup

**Activate first**: Guardian → Scribe → Collector → Strategist → Brain

A startup has code, API keys, subscriptions, and investors. Security and unit economics come before everything else.

| Priority | Hero | Why first |
|----------|------|-----------|
| 1 | Guardian | Audit API keys, model access, and provider accounts from day one. |
| 2 | Scribe | Track cloud costs, contractor spend, and runway. |
| 3 | Collector | Manage Stripe subscriptions, trials, and churn signals. |
| 4 | Strategist | Run sprints, investor updates, and hiring pipelines. |
| 5 | Brain | Index decisions about pricing, positioning, and architecture so new team members catch up fast. |

### Retail / e-commerce

**Activate first**: Scribe → Collector → Herald → Strategist

Retail moves fast: inventory, payments, promotions, and seasonality.

| Priority | Hero | Why first |
|----------|------|-----------|
| 1 | Scribe | Track COGS, shipping, ads, and margins by product line. |
| 2 | Collector | Handle Stripe checkout, subscriptions, and refunds. |
| 3 | Herald | Plan promotional calendars and product launches. |
| 4 | Strategist | Coordinate restocking, campaigns, and supplier deadlines. |

---

## 2. Copy-paste prompts and mission statements

Each prompt maps to a real tool in the repository. Use them as mission statements with Hermes or run the tools directly.

### Scribe

```text
Scribe, create a finance dashboard called "[Company] Finances" with Income, Fixed Costs,
Variable Costs, and Vendors sheets. Then parse data/2026-06_expenses.xlsx and classify every
row as fixed or variable using tools/parsers.py.
```

```text
Scribe, run Audit.run_weekly_review and tell me which budget areas are over by more than 10%.
```

### Strategist

```text
Strategist, create a project "[Project name]" for client [client] with delivery [date] and
amount [amount]. Generate a consulting checklist with Checklists.create_project_checklist.
```

```text
Strategist, create a weekly goal: "Close 2 contracts" tracked from pipeline.contracted.
```

### Herald

```text
Herald, run the brand interview with our founder answers and save .design. Then generate a
7-day content calendar for LinkedIn and Instagram about "[topic]".
```

```text
Herald, generate three LinkedIn ad variants for "[offer]" and check them against the banned
claims list in copy_generator.py.
```

### Collector

```text
Collector, create a Stripe payment link for "[Product]" priced at [amount] [currency].
```

```text
Collector, generate the income report for [start] to [end] and flag any overdue account older
than 7 days.
```

### Diplomat

```text
Diplomat, register client [name] with email [email] and rating [A/B/C/D]. Add milestone
"[description]" on [date] and confirm it in writing.
```

```text
Diplomat, run run_daily_followups and draft reminder emails for anyone with a milestone in
the next 3 days.
```

### Guardian

```text
Guardian, list all API keys, flag any older than 90 days, and run audit_access for every
Partenon profile.
```

```text
Guardian, rotate the Stripe secret key and append the rotation event to data/audit/security.log.
```

### Brain

```text
Brain, index this validated decision: "[decision]" under decisions/2026-06-26-strategist-pricing.
```

```text
Brain, search for all learnings about customer churn and generate an insight report.
```

---

## 3. 30-60-90 day rollout checklist

### Days 1-30: Foundation

- [ ] Clone repo and run `./install.sh` (see [`docs/QUICKSTART.md`](QUICKSTART.md)).
- [ ] Fill `.env` with `OPENROUTER_API_KEY` and `GOOGLE_SERVICE_ACCOUNT_JSON`.
- [ ] Create `config/company.yaml` with your company name, industry, currency, and timezone.
- [ ] Copy the profile templates you need:
  ```bash
  cp hermes/profiles/partenon-tesorero/templates/.finance.example .finance
  cp hermes/profiles/partenon-mensajero/templates/.design.example .design
  cp hermes/profiles/partenon-estratega/templates/.ops.example .ops
  cp hermes/profiles/partenon-diplomatico/templates/.relations.example .relations
  cp hermes/profiles/partenon-guardian/templates/.security.example .security
  cp hermes/profiles/partenon-cobrador/templates/.payments.example .payments
  cp hermes/profiles/partenon-brain/templates/.brain.example .brain
  ```
- [ ] Customize `.finance` with your fixed costs, variable budgets, and vendors.
- [ ] Run `python3 scripts/demo_tesorero.py` and verify the workbook.
- [ ] Start the dashboard (`cd dashboard && npm install && npm run dev`).

### Days 31-60: Operations

- [ ] Run the Herald brand interview to complete `.design`.
- [ ] Create your first project in the Strategist and assign tasks with owners and due dates.
- [ ] Register your top 10 clients/vendors in `.relations`.
- [ ] Set up your first payment link or subscription in `.payments` (local mode first, then Stripe).
- [ ] Schedule the Strategist's morning briefing and the Diplomat's daily follow-ups.
- [ ] Guardian: list keys, audit all profiles, and write the first `.security` policy.

### Days 61-90: Scale

- [ ] Connect live Google Workspace, Stripe, and G-Brain credentials.
- [ ] Automate weekly reports from the Scribe and Collector.
- [ ] Build reusable checklists for your industry (events, consulting, retail, legal).
- [ ] Use the Brain to index decisions and onboard new heroes.
- [ ] Review the Guardian's weekly audit and rotate any key older than 90 days.
- [ ] Document your company's standard operating procedures in `docs/WELCOME.md`.

---

## 4. Example configuration files

These are trimmed, realistic versions of the profile files. Copy the full templates from `hermes/profiles/<profile>/templates/` and adapt them.

### `.finance` — Scribe

```toml
[company]
name = "Acme Coffee"
tax_id = "XAXX010101000"
currency = "USD"
fiscal_year = 2026
responsible = "Scribe"
master_spreadsheet = ""

[fixed_costs]
[[fixed_costs.item]]
name = "Rent"
amount = 2500.00
frequency = "monthly"
category = "office"
due_day = 1

[[fixed_costs.item]]
name = "Payroll"
amount = 8000.00
frequency = "biweekly"
category = "payroll"
due_day = 15

[variable_costs]
[[variable_costs.item]]
name = "Coffee beans"
category = "materials"
monthly_budget = 3000.00

[[variable_costs.item]]
name = "Meta ads"
category = "marketing"
monthly_budget = 1200.00
default_vendor = "Meta"

[budgets]
[[budgets.area]]
name = "Marketing"
amount = 5000.00
period = "2026-Q3"
responsible = "Messenger"

[vendors]
[[vendors.item]]
id = "P001"
name = "Roasters United"
contact = "Sam Bean"
phone = "555-0101"
email = "sam@roastersunited.example.com"
payment_terms = "net 15"
lead_time = "3 days"
rating = 5

[rules]
tax_rate = 0.16
minimum_expected_margin = 30.0
alert_days_before_due = 3
rounding_decimals = 2
allow_expense_without_budget = false
connect_with_messenger = true
```

### `.design` — Herald

```yaml
meta:
  version: "0.1.0"
  profile: partenon-herald

brand:
  brand_name: "Acme Coffee"
  website: "https://acmecoffee.example.com"
  industry: "food"
  market: "Portland, OR"
  stage: "growth"

positioning:
  what_you_sell: "Operations consulting for independent coffee shops"
  who_you_help: "Coffee shop owners with 1-3 locations"
  how_you_do_it: "We diagnose waste, fix scheduling, and train the team in 30 days"

voice:
  tone: "direct"
  addressing: "you informal"
  style: "clear, no filler, no emojis"
  emojis: false

channels:
  - instagram
  - linkedin
  - newsletter

messaging:
  key_messages:
    - "Run your coffee shop with numbers, not guesswork"
    - "Reduce waste and labor cost in 30 days"
  claims_to_avoid:
    - "100% guaranteed"
    - "Best coffee consultants in the world"

operations:
  final_approver: "Owner"
  autonomy:
    draft_copy: true
    create_calendar: true
    publish_social: false
    send_email: false
```

### `.payments` — Collector

```yaml
metadata:
  version: "0.1.0"
  profile: partenon-cobrador
  currency: USD
  timezone: America/Los_Angeles

products:
  - id: prod_001
    name: "Coffee shop diagnostic"
    description: "60-minute operations diagnostic session"
    active: true

prices:
  - id: price_001
    product_id: prod_001
    amount: 15000
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
  days_after_due_for_escalation: 3
  allow_partial_payments: false
```

### `.security` — Guardian

```yaml
metadata:
  profile: partenon-guardian
  version: "1.0.0"

providers:
  openai:
    env_var: OPENAI_API_KEY
    pattern: "^sk-[A-Za-z0-9]+$"
    required: true
    key_reference: "env://OPENAI_API_KEY"
    rotation_days: 90
  stripe:
    env_var: STRIPE_SECRET_KEY
    pattern: "^sk_(test|live)_[A-Za-z0-9]+$"
    required: true
    key_reference: "env://STRIPE_SECRET_KEY"
    rotation_days: 90

permissions_by_profile:
  partenon-guardian:
    tools: [terminal, file, gbrain]
    mcp_servers: [gbrain]
    skills: [security]
    actions: [list_keys, rotate_key, audit_access, audit_log]
  partenon-tesorero:
    tools: [terminal, file]
    skills: [finance]
    actions: [read_financial_data]

policies:
  least_privilege: true
  default_deny: true
  log_all_access: true
  mask_secrets_in_logs: true
  rotation_reminder_days: 90
  audit_retention_days: 365
```

### `.ops` — Strategist

```yaml
profile: partenon-estratega
owner: "Owner"
assistant_name: "Strategist"

calendar:
  morning_briefing: "08:00"
  midday_pulse: "14:00"
  evening_wrap: "18:00"
  weekly_planning: "monday 09:00"
  weekly_retro: "sunday 20:00"
  timezone: "America/Los_Angeles"

projects:
  default_duration_days: 30
  auto_checklist: true
  notify_diplomat_on_milestones: true

tasks:
  default_priority: medium
  default_duration_days: 7
  escalate_blocked_after_hours: 48

goals:
  review_day: sunday
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
  "company": "Acme Coffee",
  "updated": "2026-06-26T00:00:00",
  "clients": [
    {
      "id": "CLI-001",
      "name": "Roasters United",
      "main_contact": {
        "name": "Sam Bean",
        "email": "sam@roastersunited.example.com"
      },
      "category": "supplier",
      "status": "active",
      "rating": "A",
      "milestones": [
        {
          "id": "MIL-001",
          "description": "Negotiate Q3 bean contract",
          "date": "2026-07-15",
          "status": "proposed",
          "confirmed_in_writing": false,
          "next_step": "Send draft terms"
        }
      ]
    }
  ],
  "vendors": [],
  "contracts": [],
  "communications": [],
  "reminders": []
}
```

### `.brain` — Brain

The `.brain` file is mostly a declaration. The actual memory lives in G-Brain. Keep this minimal:

```text
# Brain — Partenon profile file

## Memory structure

- decisions/ — validated company decisions
- learnings/ — insights from completed missions
- profiles/ — preferences for each hero
- onboarding/ — historical context for new heroes

## Rules

1. Every page has author, date, and tags.
2. Credentials and personal data are not indexed.
3. Contradictory decisions are marked with conflict: true.
```

---

## 5. Common mistakes to avoid

1. **Turning on all heroes at once** — Start with 2-4. The others add noise before you have data.
2. **Skipping `.design`** — The Herald refuses to publish without a brand file for good reason.
3. **Forgetting to assign task owners** — The Strategist will reject tasks without an owner and due date.
4. **Storing real keys in profile files** — Keys belong in `.env` or a secrets manager, never in `.security`.
5. **Ignoring the Guardian** — Add it before you connect real payment or model providers.

---

## 6. When to call a human

Partenon is an operations system, not a replacement for professional judgment.

- **Taxes and legal contracts**: the Scribe and Diplomat draft, but your accountant and lawyer sign off.
- **Security incidents**: the Guardian flags and rotates, but a security engineer investigates breaches.
- **Client disputes**: the Diplomat mediates, but you make the final call.
- **Medical, financial, or regulated advice**: never delegate to an agent.

---

## See also

- [`docs/QUICKSTART.md`](QUICKSTART.md) — get a demo running in 15 minutes.
- [`docs/HERO_GUIDE.md`](HERO_GUIDE.md) — every tool, env var, and cron job per hero.
- [`docs/SECURITY.md`](SECURITY.md) — how credentials, rotation, and audit logs work.
- [`docs/API.md`](API.md) — commands and return values for scripts and core tools.
- [`docs/FAQ.md`](FAQ.md) — honest answers to common questions.
