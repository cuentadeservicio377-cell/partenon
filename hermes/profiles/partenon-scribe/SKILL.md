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

## MCP Tools

The Scribe exposes the `partenon-finance` MCP server. Available tools:

- `finance_parse_expense`
- `finance_classify_expense`
- `finance_generate_dashboard`
- `finance_detect_anomaly`
- `finance_compare_budget`
- `finance_export_report`
- `finance_write_to_sheets`
- `finance_create_spreadsheet`

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|---|---|---|
| `finance_parse_expense` | Parses the input locally and returns structured fields; no external API call. | None. |
| `finance_classify_expense` | Classifies locally using local rules; no external service called. | None. |
| `finance_generate_dashboard` | Generates the dashboard structure locally; simulates spreadsheet creation. | `GOOGLE_SERVICE_ACCOUNT_JSON` to create a live Google Sheet. |
| `finance_detect_anomaly` | Detects anomalies from local data; no external call. | None. |
| `finance_compare_budget` | Compares local budget vs actual; no external call. | None. |
| `finance_export_report` | Exports the report to a local JSON or markdown file. | None. |
| `finance_write_to_sheets` | Simulates the write and returns a preview; no Sheet is modified. | `GOOGLE_SERVICE_ACCOUNT_JSON` to write to a live Google Sheet. |
| `finance_create_spreadsheet` | Simulates spreadsheet creation and returns a mock ID. | `GOOGLE_SERVICE_ACCOUNT_JSON` to create a live Google Sheet. |
