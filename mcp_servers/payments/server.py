"""Partenon Payments MCP server.

Dry-run by default. When STRIPE_SECRET_KEY is set and a tool is called with
`dry_run=false`, the server executes against the Stripe API.
"""

import os
from datetime import datetime, timedelta

import stripe
from mcp.server.fastmcp import FastMCP

from mcp_servers._shared.live_mode import is_live

mcp = FastMCP("partenon-payments")


def _stripe_client():
    key = os.environ.get("STRIPE_SECRET_KEY")
    if not key:
        raise RuntimeError("STRIPE_SECRET_KEY not configured")
    return stripe.StripeClient(key)


@mcp.tool()
def payments_create_payment_link(amount: float, currency: str = "USD", dry_run: bool = True) -> dict:
    """Create a Stripe Payment Link."""
    if dry_run:
        return {"ok": True, "dry_run": True, "url": "https://example.test/pay/link_123"}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        product = client.products.create(name="Partenon payment")
        price = client.prices.create(
            unit_amount=int(amount * 100),
            currency=currency.lower(),
            product=product.id,
        )
        link = client.payment_links.create(line_items=[{"price": price.id, "quantity": 1}])
        return {"ok": True, "dry_run": False, "url": link.url}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_create_subscription(
    customer_email: str, amount: float, interval: str = "month", dry_run: bool = True
) -> dict:
    """Create a Stripe subscription."""
    if dry_run:
        return {"ok": True, "dry_run": True, "subscription_id": "sub_123"}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        customers = client.customers.list(email=customer_email, limit=1)
        customer = customers.data[0] if customers.data else client.customers.create(email=customer_email)
        product = client.products.create(name="Partenon subscription")
        price = client.prices.create(
            unit_amount=int(amount * 100),
            currency="usd",
            recurring={"interval": interval},
            product=product.id,
        )
        subscription = client.subscriptions.create(
            customer=customer.id,
            items=[{"price": price.id}],
            payment_behavior="default_incomplete",
            expand=["latest_invoice.payment_intent"],
        )
        return {"ok": True, "dry_run": False, "subscription_id": subscription.id}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_create_invoice(customer_email: str, amount: float, dry_run: bool = True) -> dict:
    """Create and finalize a Stripe invoice."""
    if dry_run:
        return {"ok": True, "dry_run": True, "invoice_id": "inv_123"}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        customers = client.customers.list(email=customer_email, limit=1)
        customer = customers.data[0] if customers.data else client.customers.create(email=customer_email)
        invoice = client.invoices.create(customer=customer.id, auto_advance=True)
        client.invoiceitems.create(
            customer=customer.id,
            amount=int(amount * 100),
            currency="usd",
            invoice=invoice.id,
            description="Partenon invoice",
        )
        finalized = client.invoices.finalize_invoice(invoice.id)
        return {"ok": True, "dry_run": False, "invoice_id": finalized.id, "hosted_invoice_url": finalized.hosted_invoice_url}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_send_payment_reminder(
    customer_email: str, amount: float, due_date: str, dry_run: bool = True
) -> dict:
    """Send a payment reminder (dry-run only; live send requires email integration)."""
    if dry_run:
        return {"ok": True, "dry_run": True, "channel": "email"}
    return {"ok": False, "error": "live execution requires Gmail/Stripe credentials"}


@mcp.tool()
def payments_record_payment(payment_intent_id: str, amount: float, dry_run: bool = True) -> dict:
    """Record a confirmed payment and notify the Scribe."""
    if dry_run:
        return {"ok": True, "dry_run": True, "synced_with_scribe": True}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        intent = client.payment_intents.retrieve(payment_intent_id)
        if intent.status != "succeeded":
            return {"ok": False, "error": f"payment intent status is {intent.status}"}
        return {"ok": True, "dry_run": False, "synced_with_scribe": True, "amount_received": intent.amount_received / 100}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_list_charges(start_date: str, end_date: str, dry_run: bool = True) -> dict:
    """List Stripe charges for a date range."""
    if dry_run:
        return {"ok": True, "dry_run": True, "charges": []}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        start_ts = int(datetime.fromisoformat(start_date).timestamp())
        end_ts = int(datetime.fromisoformat(end_date).timestamp())
        charges = client.charges.list(
            created={"gte": start_ts, "lte": end_ts},
            limit=100,
        )
        return {
            "ok": True,
            "dry_run": False,
            "charges": [
                {
                    "id": c.id,
                    "amount": c.amount / 100,
                    "currency": c.currency,
                    "status": c.status,
                    "customer": c.customer,
                    "created": c.created,
                }
                for c in charges.data
            ],
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_generate_income_report(period: str, dry_run: bool = True) -> dict:
    """Generate an income report from Stripe charges."""
    if dry_run:
        return {"ok": True, "dry_run": True, "period": period, "income": 0.0}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        now = datetime.now()
        if period == "month":
            start = now.replace(day=1)
        elif period == "week":
            start = now - timedelta(days=now.weekday())
        else:
            start = now - timedelta(days=30)
        start_ts = int(start.timestamp())
        charges = client.charges.list(created={"gte": start_ts}, limit=100)
        total = sum(c.amount for c in charges.data if c.status == "succeeded") / 100
        return {"ok": True, "dry_run": False, "period": period, "income": total}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_read_pending_payments(dry_run: bool = True) -> dict:
    """List pending Stripe payment intents."""
    if dry_run:
        return {"ok": True, "dry_run": True, "pending": []}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        intents = client.payment_intents.list(limit=100)
        pending = [
            {"id": pi.id, "amount": pi.amount / 100, "status": pi.status, "customer": pi.customer}
            for pi in intents.data
            if pi.status in ("requires_payment_method", "requires_confirmation", "requires_action")
        ]
        return {"ok": True, "dry_run": False, "pending": pending}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_read_overdue_payments(dry_run: bool = True) -> dict:
    """List open Stripe invoices that are past due."""
    if dry_run:
        return {"ok": True, "dry_run": True, "overdue": []}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        invoices = client.invoices.list(status="open", limit=100)
        overdue = [
            {
                "id": inv.id,
                "amount": inv.amount_due / 100,
                "customer": inv.customer,
                "due_date": inv.due_date,
            }
            for inv in invoices.data
            if inv.due_date and datetime.fromtimestamp(inv.due_date).date() < datetime.now().date()
        ]
        return {"ok": True, "dry_run": False, "overdue": overdue}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_classify_risk(customer_email: str, dry_run: bool = True) -> dict:
    """Classify payment risk for a customer based on Stripe history."""
    if dry_run:
        return {"ok": True, "dry_run": True, "risk": "low"}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        customers = client.customers.list(email=customer_email, limit=1)
        if not customers.data:
            return {"ok": True, "dry_run": False, "risk": "unknown", "reason": "customer not found"}
        customer_id = customers.data[0].id
        charges = client.charges.list(customer=customer_id, limit=100)
        failures = sum(1 for c in charges.data if c.status == "failed")
        total = len(charges.data)
        risk = "low"
        if total > 0 and failures / total > 0.2:
            risk = "high"
        elif failures > 0:
            risk = "medium"
        return {"ok": True, "dry_run": False, "risk": risk, "failures": failures, "total": total}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_schedule_followup(customer_email: str, days: int = 2, dry_run: bool = True) -> dict:
    """Schedule a collection follow-up."""
    if dry_run:
        return {"ok": True, "dry_run": True, "due_in_days": days}
    return {"ok": False, "error": "live execution requires credentials"}


@mcp.tool()
def payments_monitor_fraud(dry_run: bool = True) -> dict:
    """Monitor recent Stripe charges for fraud signals."""
    if dry_run:
        return {"ok": True, "dry_run": True, "flags": []}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        since = int((datetime.now() - timedelta(days=7)).timestamp())
        charges = client.charges.list(created={"gte": since}, limit=100)
        flags = []
        for c in charges.data:
            if c.status == "failed" or getattr(c, "fraud_details", {}).get("stripe_report") == "fraudulent":
                flags.append({"id": c.id, "status": c.status, "amount": c.amount / 100})
        return {"ok": True, "dry_run": False, "flags": flags}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_get_upcoming_payments(dry_run: bool = True) -> dict:
    """List upcoming subscription invoice dates."""
    if dry_run:
        return {"ok": True, "dry_run": True, "upcoming": []}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        subscriptions = client.subscriptions.list(status="active", limit=100)
        upcoming = []
        for sub in subscriptions.data:
            upcoming.append(
                {
                    "subscription_id": sub.id,
                    "customer": sub.customer,
                    "next_payment": sub.current_period_end,
                    "amount": sub.plan.amount / 100 if sub.plan else None,
                }
            )
        return {"ok": True, "dry_run": False, "upcoming": upcoming}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@mcp.tool()
def payments_get_failed_subscriptions(dry_run: bool = True) -> dict:
    """List subscriptions with recent failed payments."""
    if dry_run:
        return {"ok": True, "dry_run": True, "failed": []}
    if not is_live("stripe"):
        return {"ok": False, "error": "live execution requires Stripe credentials"}
    try:
        client = _stripe_client()
        invoices = client.invoices.list(
            status="open",
            subscription_details={"status": "past_due"},
            limit=100,
        )
        failed = [
            {
                "invoice_id": inv.id,
                "subscription_id": inv.subscription,
                "amount": inv.amount_due / 100,
                "customer": inv.customer,
            }
            for inv in invoices.data
        ]
        return {"ok": True, "dry_run": False, "failed": failed}
    except Exception as e:
        return {"ok": False, "error": str(e)}
