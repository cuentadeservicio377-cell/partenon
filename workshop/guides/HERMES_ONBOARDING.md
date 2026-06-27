# Hermes Agent Onboarding Guide

> How Hermes should guide a new company through its first Partenon setup.
> This guide is grounded in the actual code and profiles in this repository.

---

## Pre-Flight Checklist

Before starting onboarding, Hermes verifies the following:

| # | Requirement | How to verify | Gap if missing |
|---|-------------|---------------|----------------|
| 1 | Python 3.10+ installed | `python3 --version` or `./install.sh` | Onboarding scripts will fail. |
| 2 | Hermes CLI available | `hermes --version` | Profiles cannot be loaded into Hermes; Hermes prints install instructions. |
| 3 | `.env` configured from template | `.env` exists with real keys | Integrations stay in local/demo mode. |
| 4 | Google service account JSON | `GOOGLE_SERVICE_ACCOUNT_JSON` points to a valid file | Sheets/Drive integration is disabled. |
| 5 | Stripe test key | `STRIPE_SECRET_KEY=sk_test_...` | Collector runs in local mode only. |
| 6 | Partenon repo cloned and installed | `./install.sh` ran successfully | `data/`, `logs/`, `.venv/` created; demo ran. |
| 7 | G-Brain available (optional) | `gbrain` binary in PATH or MCP configured | Brain memory stays local. |

If any required item is missing, Hermes logs it as a gap and continues in local/demo mode rather than blocking the entire onboarding.

---

## Step 1: Hermes Asks Business Questions and Writes `client.yaml`

Hermes switches to the onboarding profile and asks a standard set of questions. Answers are written to `config/company.yaml`.

### Example prompts

**Hermes:**
```text
Welcome to Partenon. I am Hermes, your company's operating system.
I need 10 minutes of context to choose the right heroes and configure your workspace.
```

**Hermes:**
```text
1. What is your company name?
2. What industry are you in? (food, retail, consulting, saas, construction, legal, events, other)
3. What currency do you use?
4. What timezone should I use for daily briefings?
5. How many employees do you have?
6. What are your top 3 operational pains right now?
7. Which tools are you already using? (Google Workspace, Stripe, Square, Shopify, QuickBooks, etc.)
8. Who is the final approver for brand, finance, and operations decisions?
9. Do you want to start with a 15-minute Scribe demo?
10. Which heroes sound most useful today? (If unsure, I will recommend based on your industry.)
```

### Expected Hermes response

Hermes writes `config/company.yaml`:

```yaml
company:
  name: "Example Company"
  industry: "consulting"
  currency: "USD"
  timezone: "America/Chicago"
  fiscal_year: 2026
  employees: 12

integrations:
  google_workspace: true
  stripe: true

profiles_active:
  - strategist
  - diplomat
  - scribe
  - collector
```

Then Hermes runs the onboarding engine:

```bash
python3 partenon-core/tools/onboarding_engine.py
```

Expected output:
```text
[success] Company configured: Example Company
[success] Created: data/clients.json
[success] Created: data/projects.json
[success] Service catalog created for industry: consulting
[success] Welcome guide created: docs/WELCOME.md
```

### Gaps

- If the company name is still "My Company", the engine warns and sets `success: false`.
- Google Workspace setup is skipped if credentials are missing.

---

## Step 2: Hermes Selects Heroes and Creates Their Config Files

Hermes recommends heroes based on industry and pain points, then copies templates from `hermes/profiles/<profile>/templates/`.

### Industry selection matrix (from `docs/ENTREPRENEUR_PLAYBOOK.md`)

| Industry | Recommended first heroes |
|----------|--------------------------|
| Coffee shop / food | Scribe → Strategist → Herald → Collector |
| Marketing agency | Strategist → Diplomat → Scribe → Herald → Collector |
| Construction / events | Strategist → Diplomat → Scribe → Guardian |
| SaaS / tech startup | Guardian → Scribe → Collector → Strategist → Brain |
| Retail / e-commerce | Scribe → Collector → Herald → Strategist |

### CLI commands

```bash
hermes profile use partenon-tesorero    # Scribe
hermes profile use partenon-mensajero   # Herald
hermes profile use partenon-cobrador    # Collector
hermes profile use partenon-guardian    # Guardian
hermes profile use partenon-estratega   # Strategist
hermes profile use partenon-diplomatico # Diplomat
hermes profile use partenon-brain       # Brain
```

### Config files created

```bash
cp hermes/profiles/partenon-tesorero/templates/.finance.example .finance
cp hermes/profiles/partenon-mensajero/templates/.design.example .design
cp hermes/profiles/partenon-cobrador/templates/.payments.example .payments
cp hermes/profiles/partenon-guardian/templates/.security.example .security
cp hermes/profiles/partenon-estratega/templates/.ops.example .ops
cp hermes/profiles/partenon-diplomatico/templates/.relations.example .relations
cp hermes/profiles/partenon-brain/templates/.brain.example .brain
```

Hermes then asks follow-up questions to fill the config files:
- Fixed costs, variable budgets, vendors (Scribe)
- Brand positioning, voice, channels, claims to avoid (Herald)
- Products, prices, payment policies (Collector)
- API keys and rotation policy (Guardian)
- Project defaults and briefing times (Strategist)
- Top clients/vendors and milestones (Diplomat)
- Memory structure and indexing rules (Brain)

### Expected Hermes response

```text
I have created your company files:
- .finance — fixed/variable costs and vendors
- .design — brand voice and messaging rules
- .payments — products, prices, and collection policies
- .security — API keys and permissions
- .ops — project defaults and briefing schedule
- .relations — clients, vendors, and milestones
- .brain — memory rules

Next I will run the Scribe demo to validate finance access.
```

---

## Step 3: Hermes Runs the Scribe Demo to Validate Finance Access

Hermes runs the Treasurer demo and checks that the workbook is created.

```bash
python3 scripts/demo_tesorero.py
```

### Expected output

```text
=== Partenon Scribe Demo ===
Workbook: /path/to/partenon/data/sample_expenses.xlsx
Report: /path/to/partenon/data/sample_expenses_report.json
{
  "timestamp": "2026-06-27T...",
  "income": 4000.0,
  "fixed_expenses": 609.0,
  "variable_expenses": 1030.0,
  "margin": 2361.0,
  "margin_pct": 59.03,
  "alerts": []
}
```

Hermes explains:
- The demo created a sample workbook with Income, Fixed Expenses, Variable Expenses, and Suppliers sheets.
- The margin is healthy; if it were negative, the Scribe would flag it.
- To publish to Google Sheets, set `GOOGLE_SERVICE_ACCOUNT_JSON` in `.env`.

### Gaps

- The demo is local-only unless Google credentials are present.
- The parser's `CATEGORY_KEYWORDS` are English-only.

---

## Step 4: Hermes Runs a Smoke Test for Each Hero

Hermes runs a quick smoke test per active hero and records results.

### Scribe smoke test

```bash
hermes profile use partenon-tesorero
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/templates.py
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/parsers.py data/sample_expenses.xlsx
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/audit.py --week 2026-W26
```

Expected: templates generated, parser returns categories, audit returns report.

### Herald smoke test

```bash
hermes profile use partenon-mensajero
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/brand_intake.py --review .design
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py --type post --channel linkedin --offer "Our first week with Partenon"
```

Expected: `.design` validated; 3 copy variants generated.

### Collector smoke test

```bash
hermes profile use partenon-cobrador
python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py create_payment_link --product "Test service" --amount 10000 --currency usd
python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py read_pending_payments
```

Expected: local-mode link placeholder and pending payments list.

### Guardian smoke test

```bash
hermes profile use partenon-guardian
python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py list_keys
python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py audit_access --profile partenon-tesorero
```

Expected: key table and permission audit.

### Strategist smoke test

```bash
hermes profile use partenon-estratega
python3 hermes/profiles/partenon-estratega/skills/ops/tools/projects.py create "Onboarding test project" --type consulting
python3 hermes/profiles/partenon-estratega/skills/ops/tools/tasks.py create "Confirm onboarding complete" --project "Onboarding test project" --owner owner@example.com --due 2026-07-04
python3 hermes/profiles/partenon-estratega/skills/ops/tools/briefings.py morning
```

Expected: project, task, and briefing output.

### Diplomat smoke test

```bash
hermes profile use partenon-diplomatico
python3 hermes/profiles/partenon-diplomatico/skills/relations/tools/crm.py add_client --name "Test Client" --email "client@example.com" --rating B
python3 hermes/profiles/partenon-diplomatico/skills/relations/tools/followups.py run_daily
```

Expected: client added to `.relations`; follow-up report generated.

### Brain smoke test

```bash
hermes profile use partenon-brain
python3 hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py put_page --slug "example/learnings/onboarding-test" --content "Partenon onboarding completed." --tags ["onboarding"]
python3 hermes/profiles/partenon-brain/skills/memory/tools/gbrain_client.py search --query "onboarding"
```

Expected: page slug returned (or local stub if G-Brain unavailable); search returns matches.

---

## Step 5: Handoff to Dashboard and First Mission

Hermes starts the Next.js dashboard:

```bash
cd dashboard
npm install
npm run dev
```

Default login: `admin` / `partenon` (change in `.env`).

Hermes then publishes the first mission:

```text
Your Partenon workspace is ready.

Open the dashboard at http://localhost:3000
Login: admin / partenon

Your first missions:
1. Scribe: upload last month's expenses and classify them.
2. Strategist: create your first project and assign 3 tasks.
3. Diplomat: register your top 3 clients/vendors and set milestones.

Run any time:
- python3 scripts/demo_tesorero.py
- python3 partenon-core/tools/router.py
- hermes profile use <hero>
```

---

## Example Full Onboarding Conversation

**Owner:**
```text
Hermes, set up Partenon for my marketing agency.
```

**Hermes:**
```text
I will guide you through the setup. First, I am checking the pre-flight requirements...
[PASS] Python 3.12
[PASS] .env exists
[WARNING] Hermes CLI not found — I will copy profiles locally.
[INFO] Google Workspace credentials not configured — Sheets integration disabled.

Let me ask a few questions about your agency.
```

After questions:

**Hermes:**
```text
Based on your answers, I recommend starting with these heroes:
1. Strategist — project deadlines and resource allocation
2. Diplomat — client milestones and follow-ups
3. Scribe — project budgets and cash flow
4. Herald — case-study content and calendar
5. Collector — retainer invoicing

I will create config/company.yaml and copy the profile templates now.
```

After config creation:

**Hermes:**
```text
Running the Scribe demo to validate finance access...
Demo passed. Margin: 59.03%

Running hero smoke tests...
[PASS] Scribe
[PASS] Herald
[PASS] Collector (local mode)
[PASS] Strategist
[PASS] Diplomat
[PARTIAL] Brain — G-Brain not configured, local stub used.

Starting dashboard...
Your workspace is ready at http://localhost:3000
```

---

## Onboarding Completion Checklist

- [ ] `config/company.yaml` created and valid
- [ ] `.finance`, `.design`, `.payments`, `.security`, `.ops`, `.relations`, `.brain` created
- [ ] `python3 scripts/demo_tesorero.py` passes
- [ ] All active heroes pass smoke tests
- [ ] Dashboard starts at `http://localhost:3000`
- [ ] First missions assigned in dashboard or `.ops`
- [ ] Gaps documented in `MISSING_IMPLEMENTATION.md` or local notes

---

## Common Onboarding Gaps

| Gap | How Hermes handles it |
|-----|----------------------|
| Hermes CLI not installed | Copies profiles to `~/.hermes/profiles/` and instructs owner to install Hermes later. |
| Google service account missing | Skips Drive/Sheets setup; uses local Excel/JSON. |
| Stripe test key missing | Collector runs in local mode; owner sees placeholder links. |
| G-Brain missing | Brain uses local stub; memory is not persistent across sessions. |
| Industry not in catalog | Falls back to `consulting` catalog. |
