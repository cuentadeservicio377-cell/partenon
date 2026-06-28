"""Partenon Payments MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("partenon-payments")


@mcp.tool()
def payments_create_payment_link(amount: float, currency: str = "USD", dry_run: bool = True) -> dict:
    """Create a payment link."""
    if dry_run:
        return {"ok": True, "dry_run": True, "url": "https://example.test/pay/link_123"}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_create_invoice(customer_email: str, amount: float, dry_run: bool = True) -> dict:
    """Create an invoice."""
    if dry_run:
        return {"ok": True, "dry_run": True, "invoice_id": "inv_123"}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_list_overdue(dry_run: bool = True) -> dict:
    """List overdue payments."""
    if dry_run:
        return {"ok": True, "dry_run": True, "overdue": []}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


if __name__ == "__main__":
    mcp.run()
