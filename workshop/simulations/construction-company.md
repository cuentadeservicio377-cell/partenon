# Simulated Partenon Onboarding: Marsh Bell Construction

This simulation walks through onboarding a commercial general contractor using the real Partenon repository. It is based on the public company card in [`workshop/companies/construction-company--marsh-bell-construction.md`](../companies/construction-company--marsh-bell-construction.md).

---

## 1. Business context

- **Company:** Marsh Bell Construction
- **Industry:** Commercial construction / design-build
- **Location:** Greenville, SC
- **Headcount:** ~18 office and field professionals
- **Top pains:** subcontractor coordination, change-order tracking, cash-flow timing, document scattering, repeat-client follow-up

---

## 2. Hermes interview questions

Hermes asks the owner or project manager:

1. What is your primary currency and fiscal year? (USD, calendar year)
2. How do you currently estimate and track project costs? (Excel, accounting software, project-management tool)
3. Which projects are active right now and who are the owners/PMs?
4. Who are your top five subcontractors and suppliers? (electrical, plumbing, concrete, steel, roofing)
5. How do you handle change orders today? (email, formal CO log, verbal)
6. What shared logins exist? (supplier portals, CAD tools, insurance systems, project-management apps)
7. How do you invoice clients? (monthly progress, milestone-based, retainers)
8. What is your biggest scheduling risk? (permits, material lead times, subcontractor availability)

---

## 3. Hero selection

| Priority | Hero | Why first |
|----------|------|-----------|
| 1 | **Strategist** | Construction lives by phase checklists and deadlines. |
| 2 | **Diplomat** | Supplier contracts and client milestones prevent delays. |
| 3 | **Scribe** | Project-level costing is the only way to protect margin. |
| 4 | **Guardian** | Shared accounts for supplier portals and CAD tools need audit. |
| 5 | **Collector** | Progress invoices and retainers must follow the schedule. |

Brain and Herald are deferred to month two.

---

## 4. Config files created

### `client.yaml`

```yaml
company:
  name: "Marsh Bell Construction"
  industry: "construction"
  sub_industry: "commercial general contractor"
  currency: "USD"
  timezone: "America/New_York"
  fiscal_year_start: "2026-01-01"
  locations: 1
  employees: 18

contacts:
  owner: "Paul Westberry"
  operations: "ops@marshbell.example.com"
  finance: "finance@marshbell.example.com"

integrations:
  google_workspace: true
  stripe: true
  gbrain: false

active_profiles:
  - partenon-estratega
  - partenon-diplomatico
  - partenon-tesorero
  - partenon-guardian
  - partenon-cobrador
```

### `.ops` (Strategist)

```yaml
profile: partenon-estratega
owner: "Project Manager"
assistant_name: "Strategist"

calendar:
  morning_briefing: "07:00"
  midday_pulse: "12:00"
  weekly_planning: "monday 07:00"
  timezone: "America/New_York"

projects:
  default_duration_days: 90
  auto_checklist: true
  notify_diplomat_on_milestones: true

tasks:
  default_priority: high
  default_duration_days: 3
  escalate_blocked_after_hours: 24
```

### `.relations` (Diplomat)

```json
{
  "company": "Marsh Bell Construction",
  "updated": "2026-06-27T00:00:00",
  "clients": [
    {
      "id": "CLI-001",
      "name": "Greer Industrial Park",
      "main_contact": { "name": "Facility Director", "email": "director@greerip.example.com" },
      "category": "client",
      "status": "active",
      "rating": "A",
      "milestones": [
        { "id": "MIL-001", "description": "Foundation pour", "date": "2026-07-15", "status": "confirmed", "confirmed_in_writing": true, "next_step": "Confirm concrete delivery" }
      ]
    }
  ],
  "vendors": [
    { "id": "VEN-001", "name": "Carolina Electric", "category": "subcontractor", "status": "active", "rating": "A" },
    { "id": "VEN-002", "name": "Upstate Plumbing", "category": "subcontractor", "status": "active", "rating": "B" }
  ],
  "contracts": [],
  "communications": [],
  "reminders": []
}
```

### `.finance` (Scribe)

```toml
[company]
name = "Marsh Bell Construction"
currency = "USD"
fiscal_year = 2026
responsible = "Scribe"

[fixed_costs]
[[fixed_costs.item]]
name = "Office rent"
amount = 3500.00
frequency = "monthly"
category = "office"

[[fixed_costs.item]]
name = "Insurance"
amount = 4200.00
frequency = "monthly"
category = "operations"

[[fixed_costs.item]]
name = "Payroll"
amount = 95000.00
frequency = "biweekly"
category = "payroll"

[variable_costs]
[[variable_costs.item]]
name = "Materials"
category = "materials"
monthly_budget = 180000.00
default_vendor = "Lumberyard Supply"

[[variable_costs.item]]
name = "Subcontractor labor"
category = "services"
monthly_budget = 120000.00

[rules]
tax_rate = 0.0
minimum_expected_margin = 15.0
alert_days_before_due = 3
```

### `.security` (Guardian)

```yaml
metadata:
  profile: partenon-guardian
  version: "1.0.0"

providers:
  procore:
    env_var: PROCORE_API_KEY
    pattern: "^[A-Za-z0-9_-]+$"
    required: false
    rotation_days: 90
  quickbooks:
    env_var: QUICKBOOKS_API_KEY
    pattern: "^[A-Za-z0-9_-]+$"
    required: false
    rotation_days: 90
  stripe:
    env_var: STRIPE_SECRET_KEY
    pattern: "^sk_(test|live)_[A-Za-z0-9]+$"
    required: true
    rotation_days: 90

policies:
  least_privilege: true
  default_deny: true
  log_all_access: true
  rotation_reminder_days: 90
```

### `.payments` (Collector)

```yaml
metadata:
  version: "0.1.0"
  profile: partenon-cobrador
  currency: USD
  timezone: America/New_York

products:
  - id: prod_progress
    name: "Progress Payment"
    description: "Monthly progress invoice for active project"
    active: true
  - id: prod_retainer
    name: "Project Retainer"
    description: "Up-front project deposit"
    active: true

policies:
  max_reminders: 3
  days_before_reminder: 7
  days_after_due_for_escalation: 7
  allow_partial_payments: true
```

---

## 5. Commands and expected outputs

### Install and verify

```bash
./install.sh
python3 scripts/demo_tesorero.py
```

Expected output matches the verified Scribe demo report.

### Activate the Strategist profile

```bash
hermes profile use partenon-estratega
```

> **Gap:** If the Hermes CLI is not installed, this command fails. The repo handles this gracefully in `install.sh`, but the live onboarding requires Nous Research's Hermes Agent CLI.

### Strategist: create a project with a construction checklist

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-estratega/skills/ops/tools")
from projects import get_projects
from checklists import Checklists

p = get_projects().create_project(
    name="Greer Industrial Build-Out",
    client_id="CLI-001",
    client_name="Greer Industrial Park",
    delivery_date="2026-10-15",
    amount=17500000
)
print(p)

cl = Checklists()
print(cl.create_project_checklist(p["project"]["id"], industry="construction"))
PY
```

Expected output: project `PROJ-001` and a phase checklist (pre-construction, construction, closeout) written to `partenon-core/data/projects.json` and `data/checklists.json`.

> **Gap:** The Strategist has no built-in construction checklist template yet. The generic consulting template is used as a placeholder.

### Diplomat: run daily follow-ups

```bash
python3 hermes/profiles/partenon-diplomatico/skills/relations/tools/followups.py
```

Actual output (with the sample `.relations` above):

```text
Daily Follow-ups — Diplomat
Date: 2026-06-27
Total pending: 1

[OVERDUE] Milestone MIL-001: Foundation pour (2026-07-15) — Confirm concrete delivery
```

> **Gap:** Follow-ups only work after clients and milestones are preloaded. There is no bulk import from a CRM export yet.

### Scribe: build a project-cost workbook

```bash
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/templates.py
```

This generates local budget/vendors/cash-flow templates. With real Google credentials, the Scribe would run `google_sheets.py` to publish the dashboard.

### Guardian: list keys and audit a profile

```bash
python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py
```

Expected output: a list of configured provider keys with status. In local mode most keys are `missing` because `.env` contains placeholders.

### Collector: create a progress-payment invoice

```bash
python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py
```

Local-mode output shows invoice creation, payment recording, and sync-with-Treasurer flag.

> **Gap:** The Collector runs in local mode without a real Stripe key. Live mode requires `STRIPE_SECRET_KEY` in `.env`.

---

## 6. First three missions per hero

### Strategist

1. **Create a project** for every active job with delivery date, amount, and assigned PM.
2. **Generate a phase checklist** (pre-construction, construction, closeout) for each project and assign owners/due dates.
3. **Schedule weekly site-review calendar events** with subcontractor cutoff reminders.

### Diplomat

1. **Register all clients, subcontractors, and suppliers** from the project list using `crm.py`.
2. **Add milestones** for permits, material deliveries, inspections, and punch-list sign-off; confirm each in writing.
3. **Run daily follow-ups** and draft reminder emails for any milestone within 3 days.

### Scribe

1. **Create a project cost workbook** with estimated vs. actual materials, labor, subcontractors, and permits.
2. **Classify office rent, insurance, and payroll** as fixed costs; tag all job-related spend as variable.
3. **Run a weekly budget review** and flag any project whose margin is below 15%.

### Guardian

1. **List all API keys** for Procore, QuickBooks, Stripe, and supplier portals.
2. **Audit permissions** for every active Partenon profile and note missing least-privilege rules.
3. **Set a 90-day rotation reminder** and append the audit to `data/audit/security.log`.

### Collector

1. **Create a Stripe invoice** for the first progress payment on the active project.
2. **Set up payment reminders** for retainers and progress payments.
3. **Generate the income report** for the month and flag any invoice overdue by more than 7 days.

---

## 7. Gaps found during simulation

| Gap | Severity | Evidence |
|-----|----------|----------|
| No construction-specific checklist template | MEDIUM | `checklists.py` falls back to a generic consulting template. |
| No field photo / document attachment flow | MEDIUM | Project notes are plain text; site photos and permits are not attached. |
| No live supplier-portal or Procore integration | HIGH | The Diplomat tracks milestones manually; real dispatch would need API credentials. |
| No project budget vs. actual-hours roll-up | HIGH | Scribe tracks budgets; Strategist tracks projects; no automatic cost-per-project roll-up exists. |
| No progress-payment schedule automation | MEDIUM | Collector can create invoices, but progress billing schedules are manual. |
