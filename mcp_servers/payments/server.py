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
def payments_create_subscription(customer_email: str, amount: float, interval: str = "month", dry_run: bool = True) -> dict:
    """Create a subscription."""
    if dry_run:
        return {"ok": True, "dry_run": True, "subscription_id": "sub_123"}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_create_invoice(customer_email: str, amount: float, dry_run: bool = True) -> dict:
    """Create an invoice."""
    if dry_run:
        return {"ok": True, "dry_run": True, "invoice_id": "inv_123"}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_send_payment_reminder(customer_email: str, amount: float, due_date: str, dry_run: bool = True) -> dict:
    """Send a payment reminder."""
    if dry_run:
        return {"ok": True, "dry_run": True, "channel": "email"}
    return {"ok": False, "error": "live execution requires Gmail/Stripe credentials"}


@mcp.tool()
def payments_record_payment(payment_intent_id: str, amount: float, dry_run: bool = True) -> dict:
    """Record a confirmed payment and notify the Scribe."""
    if dry_run:
        return {"ok": True, "dry_run": True, "synced_with_scribe": True}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_list_charges(start_date: str, end_date: str, dry_run: bool = True) -> dict:
    """List charges for a date range."""
    if dry_run:
        return {"ok": True, "dry_run": True, "charges": []}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_generate_income_report(period: str, dry_run: bool = True) -> dict:
    """Generate an income report."""
    if dry_run:
        return {"ok": True, "dry_run": True, "period": period, "income": 0.0}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_read_pending_payments(dry_run: bool = True) -> dict:
    """List pending payments."""
    if dry_run:
        return {"ok": True, "dry_run": True, "pending": []}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_read_overdue_payments(dry_run: bool = True) -> dict:
    """List overdue payments."""
    if dry_run:
        return {"ok": True, "dry_run": True, "overdue": []}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_classify_risk(customer_email: str, dry_run: bool = True) -> dict:
    """Classify payment risk for a customer."""
    if dry_run:
        return {"ok": True, "dry_run": True, "risk": "low"}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_schedule_followup(customer_email: str, days: int = 2, dry_run: bool = True) -> dict:
    """Schedule a collection follow-up."""
    if dry_run:
        return {"ok": True, "dry_run": True, "due_in_days": days}
    return {"ok": False, "error": "live execution requires credentials"}


@mcp.tool()
def payments_monitor_fraud(dry_run: bool = True) -> dict:
    """Monitor recent charges for fraud signals."""
    if dry_run:
        return {"ok": True, "dry_run": True, "flags": []}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_get_upcoming_payments(dry_run: bool = True) -> dict:
    """List upcoming subscription payments."""
    if dry_run:
        return {"ok": True, "dry_run": True, "upcoming": []}
    return {"ok": False, "error": "live execution requires Stripe credentials"}


@mcp.tool()
def payments_get_failed_subscriptions(dry_run: bool = True) -> dict:
    """List failed subscription payments."""
    if dry_run:
        return {"ok": True, "dry_run": True, "failed": []}
    return {"ok": False, "error": "live execution requires Stripe credentials"}
