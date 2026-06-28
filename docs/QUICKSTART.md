# Partenon Quickstart

Get a working Partenon demo on your laptop in about 15 minutes. This guide uses only the code in this repository — no live Stripe charges, no real Google credentials, and no Hermes Agent CLI required.

For business-oriented rollout guidance, read [`ENTREPRENEUR_PLAYBOOK.md`](ENTREPRENEUR_PLAYBOOK.md). For deep technical detail, read [`HERO_GUIDE.md`](HERO_GUIDE.md).

---

## What you will have at the end

- A Python virtual environment with dependencies installed.
- A sample expense workbook at `data/sample_expenses.xlsx`.
- A JSON audit report at `data/sample_expenses_report.json`.
- A local Next.js dashboard running on [http://localhost:3000](http://localhost:3000).
- A copy of `.env` ready for your real credentials.

---

## Prerequisites

- Python 3.12 or newer
- Node.js 20 or newer
- npm
- Git

---

## Step 1: Clone the repository

```bash
git clone https://github.com/cuentadeservicio377-cell/partenon.git
cd partenon
```

Expected result: you are in the `partenon/` directory with `README.md`, `install.sh`, and `dashboard/` visible.

---

## Step 2: Run the installer

```bash
./install.sh
```

`install.sh` does the following:

1. Creates `.venv` and installs `openpyxl`, `fastmcp`, `python-dotenv`.
2. Checks for the Hermes CLI (not required for the demo).
3. Copies `partenon_core/SKILL.md` to `~/.hermes/skills/partenon_core/`.
4. Copies `.env.example` to `.env`.
5. Creates `data/` and `logs/`.
6. Runs `scripts/demo_scribe.py`.

Expected output:

```text
Partenon v0.1.0 installer
========================================
Creating Python virtual environment...
...
=== Partenon Scribe Demo ===
Workbook: /.../partenon/data/sample_expenses.xlsx
Report: /.../partenon/data/sample_expenses_report.json
{
  "timestamp": "2026-06-26T...Z",
  "income": 4000.0,
  "fixed_expenses": 609.0,
  "variable_expenses": 1030.0,
  "margin": 2361.0,
  "margin_pct": 59.03,
  "alerts": []
}
```

---

## Step 3: Inspect the generated files

Open `data/sample_expenses.xlsx` in Excel, LibreOffice, or Google Sheets. It contains five sheets:

- **Dashboard** — formulas that summarize income, fixed expenses, variable expenses, margin, and active suppliers.
- **Income** — two sample income rows.
- **Fixed Expenses** — three sample fixed-cost rows.
- **Variable Expenses** — three sample variable-cost rows.
- **Suppliers** — five sample suppliers with ratings.

Open `data/sample_expenses_report.json`:

```json
{
  "timestamp": "2026-06-26T...Z",
  "income": 4000.0,
  "fixed_expenses": 609.0,
  "variable_expenses": 1030.0,
  "margin": 2361.0,
  "margin_pct": 59.03,
  "alerts": []
}
```

---

## Step 4: Run the intent router

Test how Partenon routes plain-language messages to heroes.

```bash
python3 partenon_core/tools/router.py
```

Expected output:

```text
'Organize my numbers'                         -> partenon-scribe
'Create a campaign for next week'              -> partenon-herald
'Generate a payment link'                      -> partenon-collector
'Rotate my OpenAI API key'                     -> partenon-guardian
'What do I have this week?'                    -> partenon-strategist
'Follow up with client Acme Inc'               -> partenon-diplomat
'What did we decide last month?'               -> partenon-brain
```

---

## Step 5: Run a hero tool directly

Try the Herald's copy generator without any API credentials:

```bash
# Create a minimal .design first
python3 hermes/profiles/partenon-herald/skills/comms/tools/brand_intake.py
```

Answer the prompts, or press Enter to accept defaults. It writes `.design` in the current directory.

Then generate a post:

```bash
python3 hermes/profiles/partenon-herald/skills/comms/tools/copy_generator.py post "payment automation" linkedin
```

Expected output: a JSON object with three ad variants and a `qa` block showing whether any banned patterns were found.

---

## Step 6: Try the Collector in local mode

No Stripe key is required. The Collector falls back to local `.payments` records.

```bash
python3 hermes/profiles/partenon-collector/skills/payments/tools/stripe_tools.py
```

Expected output: several JSON objects showing a test payment link, subscription, invoice, reminder, and payment record.

---

## Step 7: Create a project and task with the Strategist

```bash
python - <<'PY'
import sys
sys.path.insert(0, "hermes/profiles/partenon-strategist/skills/ops/tools")
from projects import get_projects
from tasks import get_tasks

p = get_projects().create_project(
    name="Acme Website Redesign",
    client_id="CLI-001",
    delivery_date="2026-08-15"
)
print(p)

t = get_tasks().create_task(
    project_id=p["project"]["id"],
    title="Audit current site",
    assignee="Ana",
    due_date="2026-07-04",
    priority="high"
)
print(t)
PY
```

Expected output: project `PROJ-001` and task `TASK-001` are created in `partenon_core/data/projects.json` and `partenon_core/data/tasks.json`.

---

## Step 8: Start the dashboard

```bash
cd dashboard
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in a browser. Log in with:

- Username: `admin`
- Password: `partenon`

The dashboard reads `data/tasks.json` and `data/cron.json` from the project root. It shows:

- KPI cards for active missions.
- A mission kanban filtered by hero profile.
- A cron job manager.

To build the production bundle:

```bash
npm run build
```

Expected result: `next build` completes with no TypeScript errors.

---

## Step 9: Edit your environment variables

Open `.env` and replace the placeholder values with real ones when you are ready:

```bash
# Required to talk to models through OpenRouter
OPENROUTER_API_KEY=sk-or-v1-...

# Required for Google Sheets, Docs, Calendar, Gmail
GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/google-service-account.json

# Required only if you use the Collector
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Required only if you use the Brain with G-Brain
GBRAIN_DATABASE_URL=postgresql://localhost:5432/gbrain

# Dashboard credentials
DASHBOARD_APP_USERNAME=admin
DASHBOARD_APP_PASSWORD=partenon
```

> **Warning:** `gbrain/server.py` and `partenon_core/config/mcp/servers.yaml` read `GBrain_DATABASE_URL` by default. Use the exact variable name required by the component you run.

---

## Screenshot placeholders

Add your own screenshots here after running the steps above:

| Step | Suggested filename | What to capture |
|------|--------------------|-----------------|
| 3 | `docs/assets/screenshot-scribe-demo.png` | `data/sample_expenses_report.json` output |
| 4 | `docs/assets/screenshot-router.png` | `python3 partenon_core/tools/router.py` output |
| 5 | `docs/assets/screenshot-herald-copy.png` | `copy_generator.py` JSON output |
| 8 | `docs/assets/screenshot-dashboard.png` | Dashboard at `http://localhost:3000` |

---

## Common first issues

### `install.sh` fails because Python is not found

Make sure `python3` is on your PATH. On macOS, install Python from [python.org](https://www.python.org/) or via Homebrew:

```bash
brew install python
```

### The dashboard fails to read `data/tasks.json`

The dashboard expects `data/tasks.json` to be in the project root, one directory above `dashboard/`. Run `npm run dev` from inside `dashboard/`; the file paths are resolved relative to the project root.

### No `.env` file was created

If `.env` already existed, the installer skips it. Run:

```bash
cp .env.example .env
```

### The Collector says Stripe is not available

That is expected in local mode. Install the Stripe Python library and add a test key when ready:

```bash
source .venv/bin/activate
pip install stripe
```

---

## Next steps

1. Read [`ENTREPRENEUR_PLAYBOOK.md`](ENTREPRENEUR_PLAYBOOK.md) to choose which heroes to activate for your business.
2. Read [`SECURITY.md`](SECURITY.md) before adding real credentials.
3. Read [`API.md`](API.md) for command and API reference.
4. Read [`HERO_GUIDE.md`](HERO_GUIDE.md) for a full tool breakdown.
