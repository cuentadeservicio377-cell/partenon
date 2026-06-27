# Simulated Partenon Onboarding: Chatbase

This simulation walks through onboarding a bootstrapped AI SaaS startup using the real Partenon repository. It is based on the public company card in [`workshop/companies/saas-startup--chatbase.md`](../companies/saas-startup--chatbase.md).

---

## 1. Business context

- **Company:** Chatbase
- **Industry:** SaaS / AI chatbots
- **Location:** Toronto, ON, Canada (remote team)
- **Headcount:** ~18 employees
- **Top pains:** support responsiveness, billing/refund friction, accuracy/hallucination, integration limitations, data capacity and pricing predictability

---

## 2. Hermes interview questions

Hermes asks the founder or operations lead:

1. What is your primary currency and fiscal year? (USD, calendar year)
2. What is your current MRR, trial volume, and churn signal source? (Stripe, analytics DB)
3. Which API keys and provider accounts must be audited first? (OpenAI, Stripe, model providers, cloud host)
4. How do you track cloud infrastructure and contractor spend? (AWS/GCP console, accounting tool)
5. What is your refund/cancellation policy and how are disputes handled today?
6. How do you prioritize support tickets and feature requests? (support tool, GitHub issues, community forum)
7. What decisions need to be indexed for new hires? (pricing, model selection, backup architecture)
8. Do you publish changelogs, founder updates, or community content?

---

## 3. Hero selection

| Priority | Hero | Why first |
|----------|------|-----------|
| 1 | **Guardian** | API key hygiene and access audit are non-negotiable for a SaaS handling customer data. |
| 2 | **Scribe** | Cloud costs, contractor spend, and runway visibility come before growth. |
| 3 | **Collector** | Stripe subscriptions, failed payments, refunds, and churn signals need automation. |
| 4 | **Strategist** | Sprints, incident post-mortems, and hiring pipelines keep the team aligned. |
| 5 | **Brain** | Pricing, model, and architecture decisions must be indexed for a growing team. |
| 6 | **Herald** | Changelog and founder updates reduce support load and build community trust. |

Diplomat is deferred until enterprise/wholesale accounts become a focus.

---

## 4. Config files created

### `client.yaml`

```yaml
company:
  name: "Chatbase"
  industry: "saas"
  sub_industry: "ai chatbot platform"
  currency: "USD"
  timezone: "America/Toronto"
  fiscal_year_start: "2026-01-01"
  locations: 0
  employees: 18

contacts:
  owner: "Yasser Elsaid"
  operations: "ops@chatbase.example.com"
  finance: "finance@chatbase.example.com"

integrations:
  google_workspace: true
  stripe: true
  gbrain: false

active_profiles:
  - partenon-guardian
  - partenon-tesorero
  - partenon-cobrador
  - partenon-estratega
  - partenon-brain
  - partenon-mensajero
```

### `.security` (Guardian)

```yaml
metadata:
  profile: partenon-guardian
  version: "1.0.0"

providers:
  openai:
    env_var: OPENAI_API_KEY
    pattern: "^sk-[A-Za-z0-9]+$"
    required: true
    rotation_days: 90
  stripe:
    env_var: STRIPE_SECRET_KEY
    pattern: "^sk_(test|live)_[A-Za-z0-9]+$"
    required: true
    rotation_days: 90
  kimi:
    env_var: KIMI_API_KEY
    pattern: "^[A-Za-z0-9_-]{16,}$"
    required: false
    rotation_days: 90
  nvidia:
    env_var: NVIDIA_API_KEY
    pattern: "^nvapi-[A-Za-z0-9_-]+$"
    required: false
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
  partenon-cobrador:
    tools: [terminal, file]
    skills: [payments]
    actions: [read_payments]
  partenon-estratega:
    tools: [terminal, file]
    skills: [ops]
    actions: [read_projects]
  partenon-brain:
    tools: [terminal, file, gbrain]
    mcp_servers: [gbrain]
    skills: [memory]
    actions: [read_memory]
  partenon-mensajero:
    tools: [terminal, file]
    skills: [comms]
    actions: [read_brand]

policies:
  least_privilege: true
  default_deny: true
  log_all_access: true
  mask_secrets_in_logs: true
  rotation_reminder_days: 90
  audit_retention_days: 365
```

### `.finance` (Scribe)

```toml
[company]
name = "Chatbase"
currency = "USD"
fiscal_year = 2026
responsible = "Scribe"

[fixed_costs]
[[fixed_costs.item]]
name = "Cloud infrastructure"
amount = 4500.00
frequency = "monthly"
category = "technology"

[[fixed_costs.item]]
name = "Software stack"
amount = 3200.00
frequency = "monthly"
category = "technology"

[[fixed_costs.item]]
name = "Payroll"
amount = 95000.00
frequency = "biweekly"
category = "payroll"

[variable_costs]
[[variable_costs.item]]
name = "Contractors"
category = "services"
monthly_budget = 12000.00

[[variable_costs.item]]
name = "Model API usage"
category = "technology"
monthly_budget = 18000.00

[rules]
tax_rate = 0.0
minimum_expected_margin = 25.0
alert_days_before_due = 3
```

### `.payments` (Collector)

```yaml
metadata:
  version: "0.1.0"
  profile: partenon-cobrador
  currency: USD
  timezone: America/Toronto

products:
  - id: prod_essential
    name: "Essential Plan"
    description: "AI chatbot builder for small teams"
    active: true
  - id: prod_premium
    name: "Premium Plan"
    description: "Higher message limits and integrations"
    active: true
  - id: prod_enterprise
    name: "Enterprise Plan"
    description: "Custom limits and white-label"
    active: true

policies:
  max_reminders: 3
  days_before_reminder: 3
  days_after_due_for_escalation: 7
  allow_partial_payments: false
```

### `.ops` (Strategist)

```yaml
profile: partenon-estratega
owner: "Founder"
assistant_name: "Strategist"

calendar:
  morning_briefing: "09:00"
  midday_pulse: "13:30"
  weekly_planning: "monday 09:00"
  weekly_retro: "friday 17:00"
  timezone: "America/Toronto"

projects:
  default_duration_days: 14
  auto_checklist: true
  notify_diplomat_on_milestones: false

tasks:
  default_priority: high
  default_duration_days: 3
  escalate_blocked_after_hours: 48

goals:
  review_day: friday
  default_type: weekly
  departments:
    - engineering
    - growth
    - support
```

### `.brain` (Brain)

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

## Initial decisions to index

- 2026-06-27: Pricing is usage-based with message credits; no unlimited tiers.
- 2026-06-27: Primary model provider is OpenAI; fallback to Kimi for security audits.
- 2026-06-27: Refund policy is 14 days for annual plans, pro-rata for monthly.
```

---

## 5. Commands and expected outputs

### Install and verify

```bash
./install.sh
python3 scripts/demo_tesorero.py
```

Expected output matches the verified Scribe demo report.

### Guardian: list keys and audit all profiles

```bash
python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py
```

Expected output: a list of configured provider keys with status. In local mode most keys are `missing` because `.env` contains placeholders.

### Scribe: build a unit-economics workbook

```bash
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/templates.py
```

This generates local budget/vendors/cash-flow templates. With real Google credentials, the Scribe would run `google_sheets.py` to publish the dashboard.

### Collector: run the Stripe demo

```bash
python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py
```

Local-mode output shows payment-link creation, subscription creation, invoice creation, payment recording, and sync-with-Treasurer flag.

> **Gap:** The Collector runs in local mode without a real Stripe key. Live mode requires `STRIPE_SECRET_KEY` in `.env`.

### Strategist: create a sprint project

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-estratega/skills/ops/tools")
from projects import get_projects
from tasks import get_tasks

p = get_projects().create_project(
    name="Reduce hallucination rate",
    client_id="internal",
    client_name="Chatbase",
    delivery_date="2026-07-14",
    amount=0
)
print(p)

t = get_tasks().create_task(
    project_id=p["project"]["id"],
    title="Add retrieval confidence threshold",
    assignee="Engineering Lead",
    due_date="2026-07-07",
    priority="high"
)
print(t)
PY
```

Expected output: project `PROJ-001` and task `TASK-001` written to `partenon-core/data/projects.json` and `data/tasks.json`.

### Herald: draft a changelog update

```bash
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py post "new retrieval confidence feature" linkedin
```

Actual output is structurally valid but generic. A real onboarding would feed a complete `.design` file into `brand_intake.py` first.

---

## 6. First three missions per hero

### Guardian

1. **List all API keys** and flag any older than 90 days or missing.
2. **Audit permissions** for every active profile and note any role that exceeds least privilege.
3. **Set a 90-day rotation reminder** and append the audit to `data/audit/security.log`.

### Scribe

1. **Create a unit-economics dashboard** with MRR, cloud spend, model-API spend, and contractor costs.
2. **Classify all fixed and variable costs** and compare them to the runway target.
3. **Run a weekly budget review** and flag any cost area exceeding budget by more than 10%.

### Collector

1. **Generate the monthly income report** from Stripe and flag failed payments and refunds.
2. **Create payment links** for the Essential, Premium, and Enterprise plans.
3. **Set up dunning reminders** for subscriptions with failed payment methods.

### Strategist

1. **Create a project** for the top support theme (e.g., hallucination or handoff) with delivery date and owner.
2. **Build a sprint checklist** and assign tasks to engineers and support leads.
3. **Generate the Friday retro** with open tasks, blocked items, and support trends.

### Brain

1. **Index the three core decisions** from the `.brain` file into G-Brain.
2. **Search for contradictions** between pricing, model, and refund decisions.
3. **Prepare onboarding context** for the next engineering hire.

### Herald

1. **Complete the brand interview** and write the full `.design` file.
2. **Generate a 14-day content calendar** for LinkedIn, Twitter/X, and the changelog.
3. **Draft a founder update** about the latest reliability improvement and run banned-claim QA.

---

## 7. Gaps found during simulation

| Gap | Severity | Evidence |
|-----|----------|----------|
| No end-to-end Stripe MCP wiring | HIGH | `stripe_tools.py` runs in local mode; live subscriptions require real credentials. |
| No model-provider key rotation API | MEDIUM | Guardian rotates placeholders only; OpenAI/Stripe keys must be replaced manually. |
| No automated support-ticket routing | MEDIUM | Support themes are tracked manually in the Strategist; no integration with Intercom/Zendesk. |
| No live G-Brain persistence | HIGH | `gbrain_client.py` shells out to a `gbrain` binary that is not bundled. |
| No cost-per-customer roll-up | MEDIUM | Scribe tracks aggregate spend; per-customer unit economics require extra tooling. |
