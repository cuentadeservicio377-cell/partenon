# Hermes Onboarding Guide

This guide describes how the Hermes Agent should guide a new company through Partenon setup. It is written for workshop facilitators, developers packaging Partenon for clients, and operators running onboarding calls.

For a 15-minute local demo without Hermes, see [`docs/QUICKSTART.md`](../../docs/QUICKSTART.md). For business-type hero selection, see [`docs/ENTREPRENEUR_PLAYBOOK.md`](../../docs/ENTREPRENEUR_PLAYBOOK.md).

---

## Pre-flight checklist

Before Hermes starts the onboarding conversation, confirm the environment:

| Requirement | How to verify | Expected result |
|-------------|---------------|-----------------|
| Python 3.10+ | `python3 --version` | `Python 3.10.x` or newer |
| Hermes CLI | `hermes --version` | Version string returned |
| Git | `git --version` | Any recent version |
| `.env` file | `ls -la .env` | File exists after `cp .env.example .env` |
| Google service account JSON | `cat /path/to/google-service-account.json` | Valid JSON with client_email |
| Stripe test key (optional) | `echo $STRIPE_SECRET_KEY` | `sk_test_...` if Collector is used |
| Node.js 20+ (dashboard) | `node --version` | `v20.x` or newer |

> **Note:** Hermes Agent CLI is distributed separately by Nous Research. `install.sh` detects it and prints instructions if it is missing.

---

## Step 1: Hermes asks the business questions and writes `client.yaml`

Hermes opens the onboarding by asking the founder or operations lead the questions below. The answers are written to `config/client.yaml`.

### Interview script

```text
Hermes: I will set up Partenon for your company. First, a few questions:

1. What is your company name and industry?
2. What currency and timezone do you operate in?
3. How many employees and locations do you have?
4. Which tools do you already use? (Google Workspace, Stripe, Shopify, Procore, etc.)
5. What is your biggest operational pain right now? (cash flow, deadlines, marketing, payments, security)
6. Who should I contact for finance, operations, and marketing decisions?
7. Do you have a Google service account JSON and Stripe test key ready?
```

### Example Hermes response

```text
Hermes: Thank you. Based on your answers, I am writing config/client.yaml with
your company profile, active integrations, and the hero profiles we will activate
first. I will also copy the corresponding templates to your workspace.
```

### Generated `config/client.yaml`

```yaml
company:
  name: "Acme Coffee"
  industry: "food"
  currency: "USD"
  timezone: "America/New_York"
  employees: 12
  locations: 2

contacts:
  owner: "Owner"
  finance: "owner@acmecoffee.example.com"
  operations: "manager@acmecoffee.example.com"

integrations:
  google_workspace: true
  stripe: true
  gbrain: false

active_profiles:
  - partenon-tesorero
  - partenon-estratega
  - partenon-mensajero
  - partenon-cobrador
```

---

## Step 2: Hermes selects heroes and creates their config files

Hermes uses the company's industry and pain points to pick 2–4 heroes first. It copies templates from `hermes/profiles/<profile>/templates/` to the workspace root.

### Decision rules

| Industry / pain | First heroes | Config files |
|-----------------|--------------|--------------|
| Coffee shop, retail, food | Scribe → Strategist → Herald → Collector | `.finance`, `.ops`, `.design`, `.payments` |
| Agency, consulting, legal | Strategist → Diplomat → Scribe → Herald | `.ops`, `.relations`, `.finance`, `.design` |
| Construction, events, logistics | Strategist → Diplomat → Scribe → Guardian | `.ops`, `.relations`, `.finance`, `.security` |
| SaaS, tech startup | Guardian → Scribe → Collector → Strategist | `.security`, `.finance`, `.payments`, `.ops` |

### Example Hermes commands

```bash
hermes profile use partenon-tesorero
hermes profile use partenon-estratega
hermes profile use partenon-mensajero
hermes profile use partenon-cobrador
```

### Config files created

```bash
cp hermes/profiles/partenon-tesorero/templates/.finance.example .finance
cp hermes/profiles/partenon-estratega/templates/.ops.example .ops
cp hermes/profiles/partenon-mensajero/templates/.design.example .design
cp hermes/profiles/partenon-cobrador/templates/.payments.example .payments
```

### Example Hermes response

```text
Hermes: For a coffee shop, I am starting with the Scribe (finance), Strategist
(operations), Herald (marketing), and Collector (payments). I have copied their
templates to your workspace. Next we will customize each file with your real
numbers.
```

---

## Step 3: Hermes runs the Scribe demo to validate finance access

Hermes runs the Scribe demo to confirm Python dependencies, Excel generation, and audit logic work.

### Command

```bash
python3 scripts/demo_tesorero.py
```

### Expected output

```text
=== Partenon Scribe Demo ===
Workbook: /.../partenon/data/sample_expenses.xlsx
Report: /.../partenon/data/sample_expenses_report.json
{
  "timestamp": "2026-06-27T00:27:21.122822+00:00Z",
  "income": 4000.0,
  "fixed_expenses": 609.0,
  "variable_expenses": 1030.0,
  "margin": 2361.0,
  "margin_pct": 59.03,
  "alerts": []
}
```

### Example Hermes response

```text
Hermes: The Scribe demo passed. It created a sample workbook and an audit report.
Now we will replace the sample data with your fixed costs, variable budgets, and
vendors in .finance.
```

---

## Step 4: Hermes runs a smoke test for each hero

Hermes verifies that each activated hero can run its primary tool in local mode before connecting live credentials.

### Scribe smoke test

```bash
python3 hermes/profiles/partenon-tesorero/skills/finance/tools/templates.py
```

Expected result: local budget/vendor/cash-flow templates are generated.

### Strategist smoke test

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-estratega/skills/ops/tools")
from projects import get_projects
print(get_projects().create_project(
    name="Smoke Test Project",
    delivery_date="2026-12-31"
))
PY
```

Expected result: `PROJ-001` created in `partenon-core/data/projects.json`.

### Herald smoke test

```bash
python3 hermes/profiles/partenon-mensajero/skills/comms/tools/copy_generator.py post "smoke test" linkedin
```

Expected result: JSON with copy and a `qa` block showing no banned patterns.

### Collector smoke test

```bash
python3 hermes/profiles/partenon-cobrador/skills/payments/tools/stripe_tools.py
```

Expected result: local-mode payment link, subscription, invoice, and income report.

### Diplomat smoke test

```bash
python3 hermes/profiles/partenon-diplomatico/skills/relations/tools/followups.py
```

Expected result: daily follow-up report (empty if no `.relations` data yet).

### Guardian smoke test

```bash
python3 hermes/profiles/partenon-guardian/skills/security/tools/key_manager.py
```

Expected result: key list and rotation status from `.security`.

### Brain smoke test

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-brain/skills/memory/tools")
from gbrain_client import GBrainClient
c = GBrainClient()
print(c.put_page("onboarding/smoke-test", "Partenon onboarding smoke test", ["test"]))
PY
```

> **Gap:** If `gbrain` is not running or `GBRAIN_DATABASE_URL` is not set, this step fails. Hermes should explain that G-Brain is optional for local onboarding.

### Example Hermes response

```text
Hermes: All four heroes passed their smoke tests in local mode. The Scribe can
build workbooks, the Strategist can create projects, the Herald can generate copy,
and the Collector can create payment links. Live integrations will be enabled when
you add real credentials to .env.
```

---

## Step 5: Handoff to dashboard and first mission

Hermes starts the dashboard and assigns the company's first mission.

### Start the dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open http://localhost:3000 and log in with the credentials from `.env` (default `admin` / `partenon`).

### Create the first mission

Hermes creates a mission card in `data/tasks.json` or via the dashboard:

```json
{
  "id": "MISSION-001",
  "title": "Build the first margin dashboard",
  "hero": "partenon-tesorero",
  "status": "todo",
  "description": "Use the Scribe to create a finance workbook with the company's fixed costs, variable budgets, and vendors."
}
```

### Example Hermes response

```text
Hermes: Your dashboard is running at http://localhost:3000. Your first mission is
"Build the first margin dashboard" with the Scribe. I will remind you when it is
due and escalate if it gets blocked.
```

---

## Day 1–30 checklist

- [ ] Choose a business type and read the matching company card.
- [ ] Run the matching simulation step by step.
- [ ] Create `config/company.yaml` with name, industry, currency, and timezone.
- [ ] Complete the brand interview (`.design`).
- [ ] Create the first project in the Strategist.
- [ ] Register the top 5 clients/vendors in the Diplomat.
- [ ] Build a finance template or run `python3 scripts/demo_tesorero.py`.
- [ ] Run the Guardian key audit and fill missing credentials.
- [ ] Generate a 7-day content calendar with the Herald.

---

## Day 31–90 checklist

- [ ] Connect live Google Workspace, Stripe, and G-Brain credentials.
- [ ] Move from local-mode invoices to real Stripe invoicing.
- [ ] Automate weekly reports from the Scribe and Collector.
- [ ] Build reusable checklists for the company's industry.
- [ ] Use the Brain to index validated decisions.
- [ ] Review the Guardian audit weekly and rotate keys older than 90 days.

---

## Common onboarding mistakes

1. **Turning on all heroes at once.** Start with 2–4. The others add noise before data exists.
2. **Skipping `.design`.** The Herald refuses to publish without a brand file for good reason.
3. **Forgetting task owners.** The Strategist rejects tasks without an owner and due date.
4. **Storing keys in profile files.** Keys belong in `.env` or a secrets manager, never in `.security`.
5. **Treating local-mode outputs as live.** Payment links, invoices, and calendars are drafts until real credentials are connected.

---

## Example prompt → Hermes response pairs

### Prompt: "Set up Partenon for my coffee shop"

```text
Hermes: I will guide you through setup for your coffee shop. I need a few details:
company name, currency, number of locations, and your top operational pain. Based
on that, I will activate the Scribe, Strategist, Herald, and Collector.
```

### Prompt: "Which heroes should I activate first?"

```text
Hermes: For a coffee shop, I recommend Scribe first to see your margins, then
Strategist for scheduling and checklists, Herald for local social content, and
Collector for catering payments. We can add Guardian and Diplomat later.
```

### Prompt: "The Scribe demo failed"

```text
Hermes: Let me check. The most common causes are Python older than 3.10 or a
missing dependency. Please run python3 --version and then ./install.sh. If it
still fails, share the error message.
```

### Prompt: "How do I add my real Stripe key?"

```text
Hermes: Open .env and set STRIPE_SECRET_KEY=sk_test_... for test mode or
sk_live_... for production. Then run the Collector smoke test again. Keep .env out
of version control; it is already in .gitignore.
```

---

## Common onboarding failures and responses

| Failure | Likely cause | Hermes response |
|---------|--------------|-----------------|
| `hermes: command not found` | Hermes CLI not installed | Print Nous Research install link and offer manual profile copy. |
| `ModuleNotFoundError: openpyxl` | Virtualenv not activated | Run `./install.sh` to create `.venv` and install dependencies. |
| `GOOGLE_SERVICE_ACCOUNT_JSON` missing | `.env` not filled | Prompt user to paste the JSON path; do not store the key in chat. |
| Stripe tools return local mode | `STRIPE_SECRET_KEY` missing or invalid | Explain local-mode fallback and request a test key. |
| G-Brain smoke test fails | `gbrain` binary or database missing | Mark Brain as inactive until G-Brain is configured. |
| Copy generator output is generic | `.design` file incomplete | Run `brand_intake.py` interactively to fill brand context. |

---

## Checklist for a complete onboarding

- [ ] `config/client.yaml` created and validated
- [ ] `.finance`, `.ops`, `.design`, `.payments` (and others) copied and customized
- [ ] `.env` filled with safe placeholders or real credentials
- [ ] `python3 scripts/demo_tesorero.py` passes
- [ ] Each activated hero passes its smoke test
- [ ] Dashboard starts at http://localhost:3000
- [ ] First mission created and assigned to the right hero
- [ ] Guardian audit scheduled if live credentials are used

---

## Where to go next

- [`docs/ENTREPRENEUR_PLAYBOOK.md`](../../docs/ENTREPRENEUR_PLAYBOOK.md) — copy-paste prompts for each hero.
- [`docs/HERO_GUIDE.md`](../../docs/HERO_GUIDE.md) — every tool, env var, and cron job per hero.
- [`workshop/simulations/`](../simulations/) — run the five simulations end to end.
- [`workshop/checklists/PRODUCTION_READINESS.md`](../checklists/PRODUCTION_READINESS.md) — verify the system is production-ready.
