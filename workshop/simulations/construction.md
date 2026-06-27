# Construction Simulation — D&M Construction

This document walks through a simulated Partenon onboarding for D&M Construction, a residential and commercial contractor in Hoover, Alabama. See the company card in [`workshop/companies/construction--dm-construction.md`](../companies/construction--dm-construction.md).

## 1. Company interview

| Question | Answer |
|----------|--------|
| Company name | D&M Construction |
| Industry | Residential and commercial construction / remodeling |
| Team size | Small local team plus subcontractors |
| Currency and fiscal year | USD, calendar year |
| Annual revenue | $6.3M+ (advertised) |
| Biggest operational pain | Project scheduling, subcontractor coordination, and change-order tracking |
| Tools already in use | QuickBooks, Google Workspace, iPhone/email for site communication, company website lead form |
| Payment terms | Deposits + progress draws; final payment on completion |
| Who approves quotes and change orders | Owner |

## 2. Hero selection

Following the Entrepreneur Playbook priority for construction / events / logistics, Hermes recommends:

1. **Strategist** — phase checklists, scheduling, permit tracking.
2. **Diplomat** — client and subcontractor milestones, contracts, follow-ups.
3. **Scribe** — per-project costing (materials, labor, subcontractors, permits).
4. **Guardian** — secure access to shared accounts, CAD files, and subcontractor portals.

Collector and Herald are added after the first two projects are stabilized.

## 3. Config files created

### `.ops` (Strategist)

```yaml
profile: partenon-estratega
owner: "Owner"
assistant_name: "Strategist"

calendar:
  morning_briefing: "06:30"
  midday_pulse: "12:00"
  evening_wrap: "16:30"
  weekly_planning: "monday 07:00"
  weekly_retro: "saturday 18:00"
  timezone: "America/Chicago"

projects:
  default_duration_days: 45
  auto_checklist: true
  notify_diplomat_on_milestones: true

tasks:
  default_priority: high
  default_duration_days: 5
  escalate_blocked_after_hours: 24

goals:
  review_day: saturday
  default_type: weekly
  departments:
    - operations
    - sales
```

### `.relations` (Diplomat)

```json
{
  "company": "D&M Construction",
  "updated": "2026-06-26T00:00:00",
  "clients": [
    {
      "id": "CLI-001",
      "name": "Johnson Residence",
      "main_contact": { "name": "Mark Johnson", "email": "mark@example.com", "phone": "+1 205 555 0100" },
      "category": "residential",
      "status": "active",
      "rating": "A",
      "milestones": [
        {
          "id": "MIL-001",
          "description": "Kitchen remodel contract signed",
          "date": "2026-06-25",
          "status": "confirmed",
          "confirmed_in_writing": true,
          "next_step": "Schedule pre-construction walkthrough"
        },
        {
          "id": "MIL-002",
          "description": "Cabinet delivery and install",
          "date": "2026-07-15",
          "status": "proposed",
          "confirmed_in_writing": false,
          "next_step": "Confirm cabinet lead time with supplier"
        }
      ]
    }
  ],
  "vendors": [
    {
      "id": "VEN-001",
      "name": "Cabinets Direct",
      "main_contact": { "name": "Sarah Lee", "email": "sarah@cabinetsdirect.example.com", "phone": "+1 205 555 0200" },
      "category": "cabinetry",
      "status": "active",
      "rating": "B",
      "milestones": [
        {
          "id": "MIL-VEN-001",
          "description": "Confirm cabinet lead time for Johnson Residence",
          "date": "2026-06-30",
          "status": "proposed",
          "confirmed_in_writing": false,
          "next_step": "Call and email confirmation"
        }
      ]
    }
  ],
  "contracts": [],
  "communications": [],
  "reminders": []
}
```

### `.finance` (Scribe)

```toml
[company]
name = "D&M Construction"
currency = "USD"
fiscal_year = 2026
responsible = "Scribe"

[fixed_costs]
[[fixed_costs.item]]
name = "Office and storage rent"
amount = 4500.00
frequency = "monthly"
category = "office"
due_day = 1

[[fixed_costs.item]]
name = "Insurance (liability + vehicle)"
amount = 2800.00
frequency = "monthly"
category = "insurance"
due_day = 10

[[fixed_costs.item]]
name = "Owner and admin payroll"
amount = 18000.00
frequency = "biweekly"
category = "payroll"
due_day = 15

[variable_costs]
[[variable_costs.item]]
name = "Project materials"
category = "materials"
monthly_budget = 180000.00

[[variable_costs.item]]
name = "Subcontractor labor"
category = "labor"
monthly_budget = 120000.00

[[variable_costs.item]]
name = "Permits and inspections"
category = "permits"
monthly_budget = 8000.00

[vendors]
[[vendors.item]]
id = "P001"
name = "Cabinets Direct"
contact = "Sarah Lee"
payment_terms = "net 30"
lead_time = "3-4 weeks"
rating = 4

[[vendors.item]]
id = "P002"
name = "Hoover Lumber"
contact = "Mike Ross"
payment_terms = "net 15"
lead_time = "1 week"
rating = 5

[rules]
minimum_expected_margin = 25.0
alert_days_before_due = 3
```

### `.security` (Guardian)

```yaml
metadata:
  profile: partenon-guardian
  version: "1.0.0"

providers:
  quickbooks:
    env_var: QUICKBOOKS_API_KEY
    pattern: "^[A-Za-z0-9_-]+$"
    required: true
    key_reference: "env://QUICKBOOKS_API_KEY"
    rotation_days: 90

  google_workspace:
    env_var: GOOGLE_SERVICE_ACCOUNT_JSON
    required: true
    key_reference: "env://GOOGLE_SERVICE_ACCOUNT_JSON"
    rotation_days: 365

permissions_by_profile:
  partenon-estratega:
    tools: [terminal, file, google_workspace]
    skills: [ops]
    files: [".ops", "projects/*"]

  partenon-diplomatico:
    tools: [file, google_workspace]
    skills: [relations]
    files: [".relations"]

policies:
  least_privilege: true
  default_deny: true
  log_all_access: true
  mask_secrets_in_logs: true
  rotation_reminder_days: 90
  audit_retention_days: 365
```

## 4. First missions

### Mission 1 — Strategist: kitchen remodel project checklist

```bash
hermes profile use partenon-estratega
```

Prompt:

```text
Strategist, create a project "Johnson Residence kitchen remodel" for client
Johnson Residence with delivery 2026-08-15 and amount $45,000. Generate a
construction checklist with phases pre-construction, construction, and closeout.
```

Actual Python equivalent:

```bash
python3 hermes/profiles/partenon-estratega/skills/ops/tools/projects.py \
  --create "Johnson Residence kitchen remodel" \
  --client "Johnson Residence" \
  --amount 45000 \
  --due 2026-08-15

python3 hermes/profiles/partenon-estratega/skills/ops/tools/checklists.py \
  --project "Johnson Residence kitchen remodel" \
  --type construction
```

**Expected output:**

```json
{
  "project_id": "PROJ-001",
  "title": "Johnson Residence kitchen remodel",
  "client": "Johnson Residence",
  "amount": 45000,
  "checklist": {
    "pre-construction": [
      "Finalize contract and deposit",
      "Pull permits",
      "Order cabinets and materials",
      "Schedule rough-in subcontractors"
    ],
    "construction": [
      "Demolition",
      "Electrical and plumbing rough-in",
      "Cabinet install",
      "Countertop measure and install",
      "Flooring and paint",
      "Final fixtures"
    ],
    "closeout": [
      "Final inspection",
      "Punch list completion",
      "Final invoice",
      "Warranty documentation"
    ]
  }
}
```

**Actual gap:** `checklists.py` does not include a `construction` template out of the box. The items above must be supplied or added to the tool.

### Mission 2 — Diplomat: confirm cabinet lead time

```bash
hermes profile use partenon-diplomatico
```

Prompt:

```text
Diplomat, update vendor Cabinets Direct with milestone "Confirm cabinet lead
time for Johnson Residence" due 2026-06-30, and run follow-ups for any vendor
milestone in the next 3 days.
```

Actual Python equivalent:

```bash
python3 hermes/profiles/partenon-diplomatico/skills/relations/tools/crm.py \
  --add-vendor "Cabinets Direct" \
  --email "sarah@cabinetsdirect.example.com" \
  --category cabinetry

python3 hermes/profiles/partenon-diplomatico/skills/relations/tools/followups.py \
  --window-days 3
```

**Expected output:**

```json
{
  "vendors_with_upcoming_milestones": ["Cabinets Direct"],
  "drafts": [
    {
      "vendor": "Cabinets Direct",
      "milestone": "Confirm cabinet lead time for Johnson Residence",
      "draft_subject": "Confirming cabinet lead time — Johnson Residence",
      "draft_body": "Hi Sarah, can you confirm the lead time and delivery date for the Johnson Residence cabinets? We need to lock the install schedule by July 3."
    }
  ],
  "status": "drafts_ready_for_review"
}
```

**Actual gap:** No live Gmail or Google Contacts integration; drafts are local only.

### Mission 3 — Scribe: per-project cost tracking

```bash
hermes profile use partenon-tesorero
```

Prompt:

```text
Scribe, create a project cost sheet for "Johnson Residence kitchen remodel"
with budget categories materials $18,000, subcontractor labor $15,000, permits
$2,000, and overhead $3,000. Flag if total estimated cost exceeds 75% of the
$45,000 contract.
```

Actual Python equivalent:

```bash
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/templates.py \
  --project "Johnson Residence kitchen remodel"

python3 hermes/profiles/partenon-tesorero/skills/finance/tools/audit.py \
  --project "Johnson Residence kitchen remodel" \
  --budget 45000 \
  --breakdown "materials=18000,labor=15000,permits=2000,overhead=3000"
```

**Expected output:**

```json
{
  "project": "Johnson Residence kitchen remodel",
  "contract": 45000,
  "estimated_cost": 38000,
  "estimated_margin": 7000,
  "margin_pct": 15.6,
  "alerts": [
    "Estimated margin is 15.6%, below the 25% minimum expected margin."
  ],
  "status": "needs_review"
}
```

**Actual gap:** The project cost sheet is not automatically linked to the project in `.ops`. The user must manually track actuals against the estimate.

## 5. Smoke test summary

| Hero | Command | Expected result | Status |
|------|---------|-----------------|--------|
| Strategist | `python3 .../projects.py --create` + `checklists.py` | Project and checklist JSON | PASS (manual template) |
| Diplomat | `python3 .../crm.py --add-vendor` + `followups.py` | Draft follow-up | PASS (draft only) |
| Scribe | `python3 .../audit.py --project` | Margin report | PARTIAL (manual input) |
| Guardian | `python3 .../key_manager.py --list` | Key inventory | PASS (local env scan) |

## 6. Gaps documented

- **No construction checklist template.** The Strategist's checklist tool needs a construction/industry template.
- **No permit deadline tracking.** The Strategist tracks tasks but does not integrate with municipal permit APIs or calendars.
- **No change-order workflow.** Scope changes must be logged manually in `.relations` and `.finance`.
- **No subcontractor portal integration.** The Diplomat cannot automatically sync with subcontractor scheduling tools.
- **No live QuickBooks sync.** The Scribe must import/export CSV or Excel from QuickBooks.
