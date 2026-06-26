---
name: finance
description: Finance skill for the Partenon Treasurer profile. Classifies fixed and variable costs, builds dashboards, analyzes expenses, and detects inconsistencies in Google Sheets.
version: 0.1.0
metadata:
  partenon:
    profile: partenon-tesorero
    tags: [finance, google-sheets, budgets, vendors, costs, dashboards]
    related_skills: [business-core, marketing, operations]
    depends_on: [google_workspace]
    status: draft
---

# Skill: Finance — Partenon Treasurer v0.1

## Role

I am the Treasurer's finance skill. I keep Hermes' numbers organized, visible, and auditable in Google Sheets.

## Activation

I activate when:
- An expense or income needs to be recorded.
- A cost needs to be classified as fixed or variable.
- A project or campaign budget is requested.
- A dashboard needs to be built or updated.
- An inconsistency or duplicate is detected.
- A due date is approaching.

## Python tools

### `tools/google_sheets.py`
- `GoogleSheets.read_sheet(spreadsheet_id, range_name)` - Reads a Sheets range.
- `GoogleSheets.write_sheet(spreadsheet_id, range_name, values)` - Writes a range to Sheets.
- `GoogleSheets.append_row(spreadsheet_id, range_name, row)` - Appends a row at the end.
- `GoogleSheets.create_dashboard(title, sheets)` - Creates a master spreadsheet with base sheets.
- `GoogleSheets.get_or_create_spreadsheet(title)` - Finds or creates a spreadsheet by title.

### `tools/parsers.py`
- `ExpenseParser.parse_excel(filepath)` - Extracts expenses from an Excel or CSV file.
- `ExpenseParser.parse_csv(filepath)` - Extracts expenses from CSV.
- `ExpenseParser.normalize_amount(value)` - Normalizes amounts to numbers.
- `ExpenseParser.infer_category(description)` - Suggests a category from a description.

### `tools/templates.py`
- `Templates.create_budget(filepath, period, items)` - Generates a budget template.
- `Templates.create_vendors(filepath)` - Generates a vendor directory.
- `Templates.create_cash_flow(filepath, months)` - Generates a cash flow template.

### `tools/audit.py`
- `Audit.read_spending()` - Reads fixed and variable expenses from the master sheet.
- `Audit.read_cash_flow()` - Calculates current cash flow and short-term projection.
- `Audit.read_budgets()` - Loads active budgets from the sheet or `.finance` file.
- `Audit.compare_budget_vs_actual()` - Calculates variance and flags areas exceeding budget.
- `Audit.detect_anomalies()` - Identifies anomalies, duplicates, and budget overruns.
- `Audit.notify(message, channel)` - Sends a report notification.
- `Audit.export_report(report, output_path)` - Writes a JSON report file.
- `Audit.run_daily_report(output_path)` - Runs the complete daily report workflow.
- `Audit.run_weekly_review(output_path)` - Runs the complete weekly budget review workflow.

## Main functions

### 1. Classify fixed and variable costs

Every expense is tagged at the time of registration:
- Fixed: rent, base salaries, recurring services.
- Variable: materials, advertising, shipping, commissions.
- Ambiguous: left for review and the user is asked.

### 2. Build dashboard

The master dashboard includes these sheets:
- Monthly Summary
- Cash Flow
- Income
- Fixed Costs
- Variable Costs
- Vendors
- Budget vs Actual
- Alerts

### 3. Analyze expenses

- Compare actual expenses against budget.
- Calculate percentage variance.
- Identify top vendors by amount.
- Group expenses by category and period.

### 4. Detect inconsistencies

- Duplicate transactions.
- Negative or null amounts.
- Empty or unknown categories.
- Upcoming due dates without recorded payment.
- Price variations greater than the configured threshold.

## Flow: Record an expense

1. Receive description, amount, date, and method.
2. Normalize amount and date.
3. Infer category.
4. Classify as fixed or variable.
5. If ambiguous, ask the user.
6. Write the row in the corresponding Sheets sheet.
7. Update the dashboard if applicable.

## Flow: Campaign budget

1. Receive campaign parameters from the Messenger.
2. Calculate expected variable costs.
3. Verify availability against the marketing budget.
4. Create or update the budget in Sheets.
5. Share the link with the Messenger.

## Rules

- Always write to Google Sheets.
- Ask before categorizing ambiguous expenses.
- Do not modify past transactions; create reversals.
- Maintain consistent currency and rounding.
- Alert due dates 3 days in advance.
- Connect with the Messenger for campaign budgets.
