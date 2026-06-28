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


if __name__ == "__main__":
    mcp.run()
