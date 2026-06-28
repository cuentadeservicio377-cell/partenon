# Simulated Partenon Onboarding: SaaS / Bootstrapped Startup

> Company: **Example SaaS** (bootstrapped Example CMS management SaaS, remote, 7 employees, ~$1.3M ARR)
> Based on public profile card: `workshop/companies/saas-startup--example-saas.md`

---

## 1. Company Interview

| Question | Answer |
|----------|--------|
| Company name | Example SaaS |
| Industry | SaaS / software |
| Location | Remote (team across US and Europe) |
| Employees | 7 |
| Currency | USD (also EUR revenue) |
| Primary revenue streams | Monthly/annual subscriptions for Example CMS site management |
| MRR / ARR | ~$110K MRR / ~$1.3M ARR |
| Biggest operational pain | Multi-currency revenue reconciliation, payment processor fee visibility, subscription failures, security hygiene |
| Tools already in use | Payment Processor, Cloud Provider A / Cloud Provider B, Example Wiki, Example Chat, Example Git Host, Google Workspace |
| Payment processor | Payment Processor |
| Top vendors | Cloud hosting, payment processor, email service, security monitoring |

Hermes writes `config/company.yaml`:

```yaml
company:
  name: "Example SaaS"
  industry: "saas"
  currency: "USD"
  timezone: "UTC"
  fiscal_year: 2026
  employees: 7

integrations:
  google_workspace: true
  stripe: true
  gbrain: true

profiles_active:
  - guardian
  - scribe
  - collector
  - strategist
  - brain
  - herald
```

---

## 2. Hero Selection

| Priority | Hero | Why first |
|----------|------|-----------|
| 1 | **Guardian** | API keys, server credentials, and access hygiene are non-negotiable when managing thousands of client sites. |
| 2 | **Scribe** | Cloud costs, contractor spend, payment processor fees, and runway must be visible. |
| 3 | **Collector** | Subscriptions, failed payments, refunds, and churn signals are the revenue engine. |
| 4 | **Strategist** | Sprints, incidents, hiring, and investor updates keep the team aligned. |
| 5 | **Brain** | Pricing, positioning, and architecture decisions must be indexed as the team grows. |
| 6 | **Herald** | Founder updates, changelog, and community content for Example Conferences/meetups. |

---

## 3. Config Files Created

### `.finance` (Scribe)

```toml
[company]
name = "Example SaaS"
tax_id = "XX-XXXXXXX"
currency = "USD"
fiscal_year = 2026
responsible = "Scribe"
master_spreadsheet = ""

[fixed_costs]
[[fixed_costs.item]]
name = "Engineering salaries"
amount = 38000.00
frequency = "biweekly"
category = "payroll"
due_day = 15

[[fixed_costs.item]]
name = "Cloud infrastructure (Cloud Provider A / Cloud Provider B)"
amount = 4500.00
frequency = "monthly"
category = "technology"
due_day = 5

[[fixed_costs.item]]
name = "Software stack (Example Git Host, Example Wiki, Example Chat, email)"
amount = 2200.00
frequency = "monthly"
category = "technology"
due_day = 10

[variable_costs]
[[variable_costs.item]]
name = "Payment processor fees"
category = "services"
monthly_budget = 3500.00

[[variable_costs.item]]
name = "Contractors and freelancers"
category = "services"
monthly_budget = 6000.00

[[variable_costs.item]]
name = "Marketing and community sponsorships"
category = "marketing"
monthly_budget = 2500.00

[vendors]
[[vendors.item]]
id = "P001"
name = "Payment Processor"
contact = "Support"
email = "support@payment.example.com"
payment_terms = "collected per transaction"
lead_time = "immediate"
rating = 5

[[vendors.item]]
id = "P002"
name = "Cloud Provider A"
contact = "Billing"
email = "billing@cloud.example.com"
payment_terms = "monthly card"
lead_time = "immediate"
rating = 4

[rules]
tax_rate = 0.00
minimum_expected_margin = 60.0
alert_days_before_due = 3
rounding_decimals = 2
allow_expense_without_budget = false
connect_with_messenger = true
```

### `.security` (Guardian)

```yaml
metadata:
  profile: partenon-guardian
  version: "1.0.0"

providers:
  stripe:
    env_var: STRIPE_SECRET_KEY
    pattern: "^sk_(test|live)_[A-Za-z0-9]+$"
    required: true
    key_reference: "env://STRIPE_SECRET_KEY"
    rotation_days: 90

  openai:
    env_var: OPENAI_API_KEY
    pattern: "^sk-[A-Za-z0-9]+$"
    required: true
    key_reference: "env://OPENAI_API_KEY"
    rotation_days: 90

  aws:
    env_var: AWS_SECRET_ACCESS_KEY
    pattern: "^[A-Za-z0-9/+=]{40}$"
    required: true
    key_reference: "env://AWS_SECRET_ACCESS_KEY"
    rotation_days: 90

permissions_by_profile:
  partenon-guardian:
    tools: [terminal, file, gbrain]
    skills: [security]
    actions: [list_keys, rotate_key, audit_access, audit_log]
  partenon-tesorero:
    tools: [terminal, file]
    skills: [finance]
    actions: [read_financial_data]
  partenon-cobrador:
    tools: [terminal, file]
    skills: [payments]
    actions: [manage_payments]

policies:
  least_privilege: true
  default_deny: true
  log_all_access: true
  mask_secrets_in_logs: true
  rotation_reminder_days: 90
  audit_retention_days: 365
```

### `.payments` (Collector)

```yaml
metadata:
  version: "0.1.0"
  profile: partenon-cobrador
  currency: USD
  timezone: UTC

products:
  - id: prod_startup_plan
    name: "Startup plan"
    description: "Up to 25 sites"
    active: true

  - id: prod_agency_plan
    name: "Agency plan"
    description: "Unlimited sites"
    active: true

prices:
  - id: price_startup_monthly
    product_id: prod_startup_plan
    amount: 2900
    currency: usd
    type: recurring
    interval: month

  - id: price_agency_annual
    product_id: prod_agency_plan
    amount: 99000
    currency: usd
    type: recurring
    interval: year

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

### `.ops` (Strategist) — excerpt

```yaml
profile: partenon-estratega
owner: "Founder / CEO"
assistant_name: "Strategist"

calendar:
  morning_briefing: "09:00"
  weekly_planning: "monday 09:00"
  weekly_retro: "friday 16:00"
  timezone: "UTC"

projects:
  default_duration_days: 14
  auto_checklist: true

tasks:
  default_priority: high
  default_duration_days: 5
  escalate_blocked_after_hours: 24

goals:
  review_day: friday
  default_type: weekly
  departments:
    - engineering
    - marketing
    - finance
```

### `.brain` (Brain)

```text
# Brain — Example SaaS

## Decisions
- 2026-01-10: Annual plan priced at $990/year (2 months free vs monthly).
- 2026-03-15: Backup retention increased from 30 to 90 days after customer reliability feedback.
- 2026-05-20: No new EU data-center region until revenue justifies cost.

## Learnings
- Agencies with 100+ sites value reliability reports more than feature velocity.
- Failed payment retry window of 3 days reduces involuntary churn vs 7 days.

## Rules
- Do not index customer site credentials.
- Tag every decision with author, date, and affected profile.
```

---

## 4. First 3 Missions per Hero

### Guardian

1. **List all keys and flag age.**
   - Command: `hermes profile use partenon-guardian`
   - Tool: `python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py list_keys`
   - Expected output: Keys for Payment Processor, Model Provider, Cloud Provider A with status; flags older than 90 days as `pending_rotation`.

2. **Audit profile permissions.**
   - Tool: `python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py audit_access --profile partenon-cobrador`
   - Expected output: Permissions match canonical role; any violation flagged.

3. **Rotate payment processor secret key.**
   - Tool: `python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py rotate_key --provider stripe`
   - Expected output: Rotation event logged; manual console step required to generate new key.
   - Gap: No real secrets-manager integration; rotation is semi-manual.

### Scribe

1. **Create runway dashboard.**
   - Command: `hermes profile use partenon-tesorero`
   - Tool: `python3 hermes/profiles/partenon-tesorero/skills/finance/tools/google_sheets.py --create "Example SaaS Runway"`
   - Expected output: Workbook with MRR, expenses, payment processor fees, runway tabs.

2. **Track payment processor fees vs. budget.**
   - Tool: `python3 hermes/profiles/partenon-tesorero/skills/finance/tools/audit.py --category services --budget 3500`
   - Expected output: Alert if fees exceed budget by >10%.

3. **Parse Cloud Provider A cost export.**
   - Tool: `python3 hermes/profiles/partenon-tesorero/skills/finance/tools/parsers.py data/example-saas_cloud_costs_2026-05.csv`
   - Expected output: Classified infrastructure spend.

### Collector

1. **List recent payment charges.**
   - Command: `hermes profile use partenon-cobrador`
   - Tool: `python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py list_charges --start 2026-06-01 --end 2026-06-30`
   - Expected output: Local-mode list or real payment charges if key is live.

2. **Get failed subscriptions.**
   - Tool: `python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py get_failed_subscriptions`
   - Expected output: Failed charge list for retry.

3. **Generate monthly income report.**
   - Tool: `python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py generate_income_report --start 2026-06-01 --end 2026-06-30`
   - Expected output: Total collected, pending, overdue, by-product and by-customer.

### Strategist

1. **Create "Backup reliability sprint" project.**
   - Command: `hermes profile use partenon-estratega`
   - Tool: `python3 hermes/profiles/partenon-estratega/skills/ops/tools/projects.py create "Backup reliability sprint" --type saas`
   - Expected output: Project with engineering checklist.

2. **Assign incident post-mortem task.**
   - Tool: `python3 hermes/profiles/partenon-estratega/skills/ops/tools/tasks.py create "Write backup incident post-mortem" --project "Backup reliability sprint" --owner engineer@example-saas.example.test --due 2026-07-02 --priority high`
   - Expected output: Task stored.

3. **Weekly retro.**
   - Tool: `python3 hermes/profiles/partenon-estratega/skills/ops/tools/briefings.py weekly_retro`
   - Expected output: Completed tasks, blockers, goals status.

### Brain

1. **Index pricing decision.**
   - Command: `hermes profile use partenon-brain`
   - Tool: `python3 hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py put_page --slug "example-saas/decisions/2026-01-10-agency-plan-pricing" --content "Annual agency plan set at $990/year (2 months free vs monthly)." --tags ["pricing","subscriptions"]`
   - Expected output: Page slug or local stub if `gbrain` binary missing.

2. **Search learnings on churn.**
   - Tool: `python3 hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py search --query "failed payment retry churn"`
   - Expected output: Related slugs.

3. **Detect conflicts.**
   - Tool: `python3 hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py conflicts`
   - Expected output: Flags if any recent decision contradicts a past one.
   - Gap: Depends on external `gbrain` binary and persistent G-Brain.

### Herald

1. **Draft founder update.**
   - Command: `hermes profile use partenon-mensajero`
   - Tool: `python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py --type email --channel newsletter --offer "June founder update"`
   - Expected output: Draft email.

2. **Create changelog post.**
   - Tool: `python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py --type post --channel blog --offer "Backup retention increase"`
   - Expected output: Draft changelog post.

3. **Build content calendar for Example Conference season.**
   - Tool: `python3 hermes/profiles/partenon-mensajero/skills/comms/tools/content_calendar.py --topic "Example CMS agency reliability" --channels blog,newsletter`
   - Expected output: 30-day calendar.

---

## 5. Expected End-to-End Outputs

- `.security` audit report and `data/audit/security.log`.
- Runway workbook and expense audit report.
- `.payments` income report and failed subscription list.
- `data/projects.json` with backup reliability sprint.
- Brain pages (or local stubs) for decisions and learnings.
- Founder update and changelog drafts.

---

## 6. Gaps Documented

| Gap | Severity | Evidence |
|-----|----------|----------|
| G-Brain local store has limited semantic search. | MEDIUM | `gbrain_client.py` now uses the bundled `GBrainStore`; full-text ranking and link graph are not implemented. |
| Multi-currency reconciliation is not automated. | MEDIUM | `.finance` supports single currency; EUR revenue requires manual conversion. |
| Guardian rotation is semi-manual. | MEDIUM | `rotate_key` logs event but requires console action. |
| No CI/CD or infrastructure audit integration. | LOW | Guardian covers API keys, not Cloud Provider A IAM or Cloud Provider B deployments. |
| Herald cannot auto-publish blog or newsletter. | MEDIUM | Drafts only. |
