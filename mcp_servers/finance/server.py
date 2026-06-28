"""Partenon Finance MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("partenon-finance")


@mcp.tool()
def finance_parse_expense(text: str, dry_run: bool = True) -> dict:
    """Parse a free-text expense into structured fields."""
    if dry_run:
        return {"ok": True, "dry_run": True, "parsed": {"description": text, "amount": 0.0}}
    return {"ok": False, "error": "live execution requires credentials"}


@mcp.tool()
def finance_classify_expense(description: str, amount: float, dry_run: bool = True) -> dict:
    """Classify an expense as fixed or variable."""
    if dry_run:
        category = "variable" if amount < 1000 else "fixed"
        return {"ok": True, "dry_run": True, "category": category}
    return {"ok": False, "error": "live execution requires credentials"}


@mcp.tool()
def finance_generate_dashboard(period: str, dry_run: bool = True) -> dict:
    """Generate a finance dashboard summary for the period."""
    if dry_run:
        return {
            "ok": True,
            "dry_run": True,
            "period": period,
            "income": 0.0,
            "fixed_expenses": 0.0,
            "variable_expenses": 0.0,
            "margin": 0.0,
        }
    return {"ok": False, "error": "live execution requires credentials"}


@mcp.tool()
def finance_detect_anomaly(dry_run: bool = True) -> dict:
    """Detect anomalies, duplicates, or budget overruns."""
    if dry_run:
        return {"ok": True, "dry_run": True, "anomalies": []}
    return {"ok": False, "error": "live execution requires credentials"}


@mcp.tool()
def finance_compare_budget(dry_run: bool = True) -> dict:
    """Compare budget vs actual spending."""
    if dry_run:
        return {"ok": True, "dry_run": True, "variances": []}
    return {"ok": False, "error": "live execution requires credentials"}


@mcp.tool()
def finance_export_report(format: str = "json", dry_run: bool = True) -> dict:
    """Export a finance report."""
    if dry_run:
        return {"ok": True, "dry_run": True, "format": format, "path": "data/reports/finance_report.json"}
    return {"ok": False, "error": "live execution requires credentials"}


@mcp.tool()
def finance_write_to_sheets(data: str, dry_run: bool = True) -> dict:
    """Write data to Google Sheets. Data must be a JSON string."""
    if dry_run:
        return {"ok": True, "dry_run": True, "rows_written": 0}
    return {"ok": False, "error": "live execution requires Google Workspace credentials"}


@mcp.tool()
def finance_create_spreadsheet(title: str, dry_run: bool = True) -> dict:
    """Create a Google Sheets spreadsheet."""
    if dry_run:
        return {"ok": True, "dry_run": True, "spreadsheet_id": "spreadsheet_123", "title": title}
    return {"ok": False, "error": "live execution requires Google Workspace credentials"}
