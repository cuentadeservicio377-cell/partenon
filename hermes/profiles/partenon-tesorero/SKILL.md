# Partenon Scribe — Finance Skill Pack

> Finance and documentation keeper for small businesses.
> Reads, classifies, warns, and reconciles. Does not move money.

## Included skills

### `finance`
- Parse Excel, CSV, and image/PDF expenses.
- Classify by category, cost type (fixed/variable), and vendor.
- Generate Google Sheets dashboards.
- Detect duplicates, anomalies, and due dates.
- Compare budgets against actual spending.
- Export structured JSON reports.

## Quick start

1. Copy `.env.example` to `.env` and fill in credentials.
2. Copy `templates/.finance.example` to your workspace as `.finance`.
3. Run `python3 skills/finance/tools/templates.py` to generate local templates.
4. Use `skills/finance/tools/google_sheets.py` to publish to Sheets.
5. Use `skills/finance/tools/audit.py` to run daily reports and weekly budget reviews.

## Safety rules

- The Scribe never executes payments.
- It never creates a new spreadsheet without explicit confirmation.
- Every report includes sources, assumptions, and confidence level.
