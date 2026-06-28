"""
Partenon Scribe - Audit and Reporting Tools
Implements the daily/weekly cron workflows:
  read_spending, read_cash_flow, detect_anomalies,
  read_budgets, compare_budget_vs_actual, notify, export_report.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# TOML parser (Python 3.11+ has tomllib built-in)
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

from .google_sheets import GoogleSheets, get_google_sheets
from .parsers import ExpenseParser, get_parser


DEFAULT_SHEET_RANGES = {
    "fixed_costs": "Fixed Costs!A2:G",
    "variable_costs": "Variable Costs!A2:G",
    "income": "Income!A2:E",
    "budgets": "Budget vs Actual!A2:G",
    "vendors": "Vendors!A2:H",
    "alerts": "Alerts!A2:G",
}


class Audit:
    """Audit and reporting engine for the Scribe's finance workflow."""

    def __init__(
        self,
        spreadsheet_id: Optional[str] = None,
        service_account_path: Optional[str] = None,
        finance_file: Optional[str] = None,
    ):
        self.spreadsheet_id = spreadsheet_id or os.environ.get("PARTENON_TESORERO_SHEET_ID", "")
        self.finance_file = finance_file or ".finance"
        self.sheets = get_google_sheets(service_account_path=service_account_path)
        self.parser = get_parser()
        self.errors: List[str] = []

    def _sheet_values(self, range_name: str) -> List[List[Any]]:
        """Read values from Sheets if a spreadsheet ID is configured."""
        if not self.spreadsheet_id:
            self.errors.append("No spreadsheet ID configured")
            return []
        return self.sheets.read_range(self.spreadsheet_id, range_name)

    def _load_finance_config(self) -> Dict[str, Any]:
        """Load the local .finance TOML config file."""
        path = Path(self.finance_file)
        if not path.exists():
            return {}
        if tomllib is None:
            self.errors.append("TOML parser not available (install tomli or use Python 3.11+)")
            return {}
        try:
            with open(path, "rb") as f:
                return tomllib.load(f)
        except Exception as e:
            self.errors.append(f"Failed to parse .finance file: {e}")
            return {}

    def read_spending(self) -> Dict[str, Any]:
        """Read fixed and variable expenses from the master sheet."""
        fixed = self._sheet_values(DEFAULT_SHEET_RANGES["fixed_costs"])
        variable = self._sheet_values(DEFAULT_SHEET_RANGES["variable_costs"])

        fixed_total = sum(self._row_amount(row, 2) for row in fixed)
        variable_total = sum(self._row_amount(row, 2) for row in variable)

        return {
            "fixed_costs": {
                "count": len(fixed),
                "total": round(fixed_total, 2),
                "rows": fixed,
            },
            "variable_costs": {
                "count": len(variable),
                "total": round(variable_total, 2),
                "rows": variable,
            },
            "total_expenses": round(fixed_total + variable_total, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def read_cash_flow(self) -> Dict[str, Any]:
        """Calculate current cash flow from income and expenses."""
        income_rows = self._sheet_values(DEFAULT_SHEET_RANGES["income"])
        spending = self.read_spending()

        income_total = sum(self._row_amount(row, 2) for row in income_rows)
        expenses_total = spending.get("total_expenses", 0.0)
        balance = income_total - expenses_total

        return {
            "income": round(income_total, 2),
            "expenses": round(expenses_total, 2),
            "balance": round(balance, 2),
            "income_count": len(income_rows),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def read_budgets(self) -> Dict[str, Any]:
        """Load active budgets from the master sheet or .finance file."""
        config = self._load_finance_config()
        budgets_from_file = config.get("budgets", {}).get("area", [])
        sheet_budgets = self._sheet_values(DEFAULT_SHEET_RANGES["budgets"])

        parsed_budgets = []
        for row in sheet_budgets:
            if len(row) >= 3:
                try:
                    parsed_budgets.append({
                        "area": row[0],
                        "period": row[1],
                        "budget": float(row[2]),
                        "actual": float(row[3]) if len(row) > 3 else 0.0,
                    })
                except (ValueError, TypeError):
                    continue

        return {
            "budgets": parsed_budgets or budgets_from_file,
            "source": "sheet" if parsed_budgets else "finance_file",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def compare_budget_vs_actual(self) -> Dict[str, Any]:
        """Compare budgeted amounts against actual spending by area."""
        spending = self.read_spending()
        budgets = self.read_budgets()

        variable_rows = spending.get("variable_costs", {}).get("rows", [])
        fixed_rows = spending.get("fixed_costs", {}).get("rows", [])
        all_expenses = variable_rows + fixed_rows

        area_actuals: Dict[str, float] = {}
        for row in all_expenses:
            if len(row) < 4:
                continue
            area = str(row[3]).strip() if row[3] else "uncategorized"
            amount = self._row_amount(row, 2)
            area_actuals[area] = area_actuals.get(area, 0.0) + amount

        comparisons = []
        for budget in budgets.get("budgets", []):
            area = budget.get("name") or budget.get("area") or "unknown"
            budget_amount = float(budget.get("amount", 0.0))
            actual = area_actuals.get(area, 0.0)
            difference = budget_amount - actual
            variance_pct = round((difference / budget_amount) * 100, 2) if budget_amount else 0.0
            comparisons.append({
                "area": area,
                "period": budget.get("period", ""),
                "budget": budget_amount,
                "actual": round(actual, 2),
                "difference": round(difference, 2),
                "variance_pct": variance_pct,
                "status": "over_budget" if difference < 0 else "on_track",
            })

        return {
            "comparisons": comparisons,
            "total_budget": round(sum(b.get("budget", 0.0) for b in comparisons), 2),
            "total_actual": round(sum(b.get("actual", 0.0) for b in comparisons), 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def detect_anomalies(self) -> Dict[str, Any]:
        """Detect anomalies in expenses and budget overruns."""
        spending = self.read_spending()
        budget = self.compare_budget_vs_actual()

        expenses: List[Dict[str, Any]] = []
        for row in spending.get("fixed_costs", {}).get("rows", []):
            expenses.append(self._sheet_row_to_expense(row, "fixed"))
        for row in spending.get("variable_costs", {}).get("rows", []):
            expenses.append(self._sheet_row_to_expense(row, "variable"))

        parser_anomalies = self.parser.detect_anomalies(expenses)
        duplicates = self.parser.detect_duplicates(expenses)

        over_budget = [b for b in budget.get("comparisons", []) if b.get("status") == "over_budget"]

        return {
            "anomalies": parser_anomalies,
            "duplicates": duplicates,
            "over_budget_areas": over_budget,
            "total_flags": len(parser_anomalies) + len(duplicates) + len(over_budget),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def notify(self, message: str, channel: str = "console") -> bool:
        """Send a notification to the configured channel."""
        if channel == "console":
            print(f"[SCRIBE NOTIFY] {message}")
            return True
        if channel == "file":
            log_path = Path("scribe_notifications.log")
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now(timezone.utc).isoformat()} {message}\n")
            return True
        self.errors.append(f"Notification channel not implemented: {channel}")
        return False

    def export_report(self, report: Dict[str, Any], output_path: str) -> bool:
        """Export a report dict to a JSON file."""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.errors.append(f"Failed to export report: {e}")
            return False

    def run_daily_report(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Run the complete daily report workflow."""
        cash_flow = self.read_cash_flow()
        anomalies = self.detect_anomalies()

        report = {
            "type": "daily_report",
            "cash_flow": cash_flow,
            "anomalies": anomalies,
            "errors": list(self.errors),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

        self.notify(f"Daily report generated. Balance: {cash_flow.get('balance', 0.0)}")

        if output_path:
            self.export_report(report, output_path)

        return report

    def run_weekly_review(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Run the complete weekly budget vs actuals workflow."""
        comparison = self.compare_budget_vs_actual()

        report = {
            "type": "weekly_budget_review",
            "comparison": comparison,
            "errors": list(self.errors),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

        over_budget = comparison.get("comparisons", [])
        flagged = [c for c in over_budget if c.get("status") == "over_budget"]
        self.notify(f"Weekly review generated. {len(flagged)} areas over budget.")

        if output_path:
            self.export_report(report, output_path)

        return report

    @staticmethod
    def _row_amount(row: List[Any], index: int) -> float:
        """Safely extract a numeric amount from a row."""
        if index >= len(row):
            return 0.0
        value = row[index]
        if isinstance(value, (int, float)):
            return float(value)
        try:
            return float(str(value).replace(",", "").replace("$", ""))
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _sheet_row_to_expense(row: List[Any], cost_type: str) -> Dict[str, Any]:
        """Convert a sheet row to the parser's expense dict format."""
        return {
            "date": row[0] if len(row) > 0 else None,
            "description": row[1] if len(row) > 1 else "No description",
            "amount": Audit._row_amount(row, 2),
            "category": row[3] if len(row) > 3 else "",
            "provider": row[4] if len(row) > 4 else "",
            "type": cost_type,
            "source": "sheet",
        }


# Singleton
_audit_instance = None


def get_audit(
    spreadsheet_id: Optional[str] = None,
    service_account_path: Optional[str] = None,
    finance_file: Optional[str] = None,
) -> Audit:
    """Get or create singleton Audit instance."""
    global _audit_instance
    if _audit_instance is None:
        _audit_instance = Audit(
            spreadsheet_id=spreadsheet_id,
            service_account_path=service_account_path,
            finance_file=finance_file,
        )
    return _audit_instance
