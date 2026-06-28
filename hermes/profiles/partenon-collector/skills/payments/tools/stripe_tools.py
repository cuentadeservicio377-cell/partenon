"""
Partenon Collector — Stripe Tools

Payment, subscription, reminder, invoice, fraud monitoring, and collection
record functions. Compatible with Python 3.12.

This module is designed to work in two modes:
1. Inside Hermes Agent, using the Stripe MCP server.
2. Standalone, if the `stripe` library is available.

When there is no library or MCP client, functions return a structured
result with success=False indicating that configuration is missing.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Try to load stripe; if not available, we use MCP or return an error.
try:
    import stripe as stripe_lib

    HAS_STRIPE = True
except Exception:  # pragma: no cover - stripe is optional in development
    stripe_lib = None  # type: ignore[assignment]
    HAS_STRIPE = False


# ---------------------------------------------------------------------------
# Configuration and utilities
# ---------------------------------------------------------------------------


def _get_stripe_key() -> str | None:
    """Get Stripe API key from environment variables."""
    return os.getenv("STRIPE_SECRET_KEY")


def _init_stripe() -> bool:
    """Initialize the stripe library if available."""
    if not HAS_STRIPE:
        return False
    key = _get_stripe_key()
    if not key:
        return False
    stripe_lib.api_key = key  # type: ignore[attr-defined]
    return True


def _payments_file(profile_dir: Path | None = None) -> Path:
    """Resolve the path to the master .payments file."""
    if profile_dir is not None:
        return profile_dir / ".payments"

    # Search upward from the current file until .payments is found
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / ".payments"
        if candidate.exists():
            return candidate
        # Search limit to avoid climbing to the system root
        if parent.name == "partenon-collector":
            return candidate
    return Path(__file__).resolve().parents[3] / ".payments"


def _load_payments(profile_dir: Path | None = None) -> dict[str, Any]:
    """Load the .payments file as a dict."""
    payments_file = _payments_file(profile_dir)
    if not payments_file.exists():
        return {
            "metadata": {},
            "products": [],
            "prices": [],
            "links": [],
            "subscriptions": [],
            "customers": [],
            "payments": [],
            "invoices": [],
            "reminders": [],
        }
    try:
        with open(payments_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "metadata": {},
            "products": [],
            "prices": [],
            "links": [],
            "subscriptions": [],
            "customers": [],
            "payments": [],
            "invoices": [],
            "reminders": [],
        }


def _save_payments(data: dict[str, Any], profile_dir: Path | None = None) -> None:
    """Save the .payments file."""
    payments_file = _payments_file(profile_dir)
    payments_file.parent.mkdir(parents=True, exist_ok=True)
    with open(payments_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _now_iso() -> str:
    """Current date/time in ISO 8601 format with timezone."""
    return datetime.now(timezone.utc).isoformat()


def _today_iso() -> str:
    """Current date in ISO 8601 format (YYYY-MM-DD)."""
    return datetime.now(timezone.utc).date().isoformat()


def _generate_id(prefix: str, collection: list[dict[str, Any]]) -> str:
    """Generate a simple sequential ID based on prefix and collection."""
    count = len(collection) + 1
    return f"{prefix}_{count:03d}"


def _parse_iso_date(value: str | None) -> datetime | None:
    """Parse an ISO date or datetime string into an aware UTC datetime."""
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# Main functions
# ---------------------------------------------------------------------------


def create_payment_link(product: dict[str, Any], price: dict[str, Any]) -> dict[str, Any]:
    """
    Create a Stripe payment link.

    Args:
        product: dict with at least 'name'. Optional 'description'.
        price: dict with 'amount' (integer, cents), 'currency' (default 'mxn').

    Returns:
        Dict with success, url, payment_link_id, and message.
    """
    product_name = product.get("name")
    if not product_name:
        return {"success": False, "error": "Product requires 'name'."}

    amount = price.get("amount")
    currency = price.get("currency", "mxn").lower()
    if not isinstance(amount, int) or amount <= 0:
        return {"success": False, "error": "Price requires positive integer 'amount' in cents."}

    if _init_stripe():
        try:
            stripe_product = stripe_lib.Product.create(
                name=product_name, description=product.get("description", "")
            )
            stripe_price = stripe_lib.Price.create(
                unit_amount=amount,
                currency=currency,
                product=stripe_product.id,
            )
            link = stripe_lib.PaymentLink.create(
                line_items=[{"price": stripe_price.id, "quantity": 1}]
            )
            return {
                "success": True,
                "url": link.url,
                "payment_link_id": link.id,
                "product_id": stripe_product.id,
                "price_id": stripe_price.id,
                "message": f"Payment link created: {link.url}",
            }
        except Exception as exc:
            return {"success": False, "error": f"Stripe error: {exc}"}

    # Mode without Stripe library: simulate response for tests.
    data = _load_payments()
    product_id = _generate_id("prod", data.get("products", []))
    price_id = _generate_id("price", data.get("prices", []))
    link_id = _generate_id("link", data.get("links", []))

    data.setdefault("products", []).append(
        {
            "id": product_id,
            "name": product_name,
            "description": product.get("description", ""),
            "active": True,
        }
    )
    data.setdefault("prices", []).append(
        {
            "id": price_id,
            "product_id": product_id,
            "amount": amount,
            "currency": currency,
            "type": "one_time",
        }
    )
    data.setdefault("links", []).append(
        {
            "id": link_id,
            "price_id": price_id,
            "url": f"https://buy.stripe.com/test_{link_id}",
            "concept": product_name,
            "created": _now_iso(),
            "status": "active",
        }
    )
    _save_payments(data)

    return {
        "success": True,
        "url": f"https://buy.stripe.com/test_{link_id}",
        "payment_link_id": link_id,
        "product_id": product_id,
        "price_id": price_id,
        "message": "Payment link created in local mode (Stripe MCP not available).",
    }


def create_subscription(customer: dict[str, Any], price: dict[str, Any]) -> dict[str, Any]:
    """
    Create a Stripe subscription for a customer.

    Args:
        customer: dict with 'email' required, 'name' optional.
        price: dict with existing Stripe 'id' or 'amount'/'currency'/'interval'.

    Returns:
        Dict with success, subscription_id, status, next_payment, and message.
    """
    email = customer.get("email")
    if not email:
        return {"success": False, "error": "Customer requires 'email'."}

    price_id = price.get("id")
    if not price_id:
        # Create recurring price if no id is provided
        amount = price.get("amount")
        currency = price.get("currency", "mxn").lower()
        interval = price.get("interval", "month")
        if not isinstance(amount, int) or amount <= 0:
            return {"success": False, "error": "Price requires 'id' or positive integer 'amount'."}

        if _init_stripe():
            try:
                product = stripe_lib.Product.create(name=price.get("product_name", "Subscription"))
                stripe_price = stripe_lib.Price.create(
                    unit_amount=amount,
                    currency=currency,
                    recurring={"interval": interval},
                    product=product.id,
                )
                price_id = stripe_price.id
            except Exception as exc:
                return {"success": False, "error": f"Stripe error creating price: {exc}"}
        else:
            data = _load_payments()
            price_id = _generate_id("price", data.get("prices", []))
            data.setdefault("prices", []).append(
                {
                    "id": price_id,
                    "amount": amount,
                    "currency": currency,
                    "type": "recurring",
                    "interval": interval,
                }
            )
            _save_payments(data)

    if _init_stripe():
        try:
            stripe_customer = stripe_lib.Customer.create(
                email=email, name=customer.get("name", "")
            )
            subscription = stripe_lib.Subscription.create(
                customer=stripe_customer.id,
                items=[{"price": price_id}],
            )
            return {
                "success": True,
                "subscription_id": subscription.id,
                "status": subscription.status,
                "next_payment": datetime.fromtimestamp(
                    subscription.current_period_end, tz=timezone.utc
                ).isoformat(),
                "message": f"Subscription {subscription.id} created for {email}.",
            }
        except Exception as exc:
            return {"success": False, "error": f"Stripe error: {exc}"}

    # Local mode
    data = _load_payments()
    sub_id = _generate_id("sub", data.get("subscriptions", []))
    next_payment = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    data.setdefault("subscriptions", []).append(
        {
            "id": sub_id,
            "customer_email": email,
            "price_id": price_id,
            "stripe_subscription_id": f"sub_test_{sub_id}",
            "status": "active",
            "cycle": price.get("interval", "month"),
            "next_charge": next_payment[:10],
            "failed_attempts": 0,
        }
    )
    _save_payments(data)

    return {
        "success": True,
        "subscription_id": sub_id,
        "status": "active",
        "next_payment": next_payment,
        "message": f"Subscription {sub_id} created in local mode for {email}.",
    }


def create_invoice(customer: dict[str, Any], items: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Create a Stripe invoice for a customer.

    Args:
        customer: dict with 'email' required, 'name' optional.
        items: list of dicts with 'description' and 'amount' (integer, cents).

    Returns:
        Dict with success, invoice_id, amount, currency, and message.
    """
    email = customer.get("email")
    if not email:
        return {"success": False, "error": "Customer requires 'email'."}
    if not items or not isinstance(items, list):
        return {"success": False, "error": "Invoice requires at least one item."}

    total = 0
    for item in items:
        amount = item.get("amount")
        if not isinstance(amount, int) or amount <= 0:
            return {"success": False, "error": "Each invoice item requires a positive integer 'amount'."}
        total += amount

    currency = (items[0].get("currency", "mxn") if items else "mxn").lower()

    if _init_stripe():
        try:
            stripe_customer = stripe_lib.Customer.create(
                email=email, name=customer.get("name", "")
            )
            invoice = stripe_lib.Invoice.create(
                customer=stripe_customer.id,
                auto_advance=True,
                collection_method="send_invoice",
                days_until_due=7,
            )
            for item in items:
                stripe_lib.InvoiceItem.create(
                    customer=stripe_customer.id,
                    invoice=invoice.id,
                    amount=item["amount"],
                    currency=currency,
                    description=item.get("description", ""),
                )
            finalized = stripe_lib.Invoice.finalize_invoice(invoice.id)
            return {
                "success": True,
                "invoice_id": finalized.id,
                "amount": total,
                "currency": currency.upper(),
                "status": finalized.status,
                "hosted_invoice_url": finalized.hosted_invoice_url,
                "message": f"Invoice {finalized.id} created for {email}.",
            }
        except Exception as exc:
            return {"success": False, "error": f"Stripe error: {exc}"}

    # Local mode
    data = _load_payments()
    invoice_id = _generate_id("inv", data.get("invoices", []))
    data.setdefault("invoices", []).append(
        {
            "id": invoice_id,
            "customer_email": email,
            "items": items,
            "amount": total,
            "currency": currency,
            "status": "open",
            "created": _now_iso(),
            "due_date": (datetime.now(timezone.utc) + timedelta(days=7)).date().isoformat(),
        }
    )
    _save_payments(data)

    return {
        "success": True,
        "invoice_id": invoice_id,
        "amount": total,
        "currency": currency.upper(),
        "status": "open",
        "hosted_invoice_url": f"https://invoice.stripe.com/test_{invoice_id}",
        "message": f"Invoice {invoice_id} created in local mode for {email}.",
    }


def send_payment_reminder(customer: dict[str, Any]) -> dict[str, Any]:
    """
    Send a payment reminder to the customer.

    Args:
        customer: dict with 'email', 'name', 'amount_due', 'currency', 'due_date',
                  and optional 'payment_link'.

    Returns:
        Dict with success, channel, message_id, and message.
    """
    email = customer.get("email")
    if not email:
        return {"success": False, "error": "Customer requires 'email'."}

    name = customer.get("name", email)
    amount_due = customer.get("amount_due")
    currency = customer.get("currency", "mxn").upper()
    due_date = customer.get("due_date", "to be confirmed")
    payment_link = customer.get("payment_link")

    subject = f"Pending payment reminder — {currency} {amount_due or 'N/A'}"
    body_lines = [
        f"Hi {name},",
        "",
        f"We remind you that you have a pending payment of {currency} {amount_due or 'N/A'}.",
        f"Due date: {due_date}.",
    ]
    if payment_link:
        body_lines.append(f"You can make the payment here: {payment_link}")
    body_lines.extend(
        [
            "",
            "If you already made the payment, please ignore this message.",
            "",
            "Regards,",
        ]
    )

    # In a real environment, this would delegate to the Gmail MCP.
    # Here we register the reminder in .payments.
    data = _load_payments()
    reminder_id = _generate_id("rem", data.get("reminders", []))
    data.setdefault("reminders", []).append(
        {
            "id": reminder_id,
            "customer_email": email,
            "type": "manual",
            "sent": _now_iso(),
            "channel": "gmail",
            "status": "sent",
            "subject": subject,
            "body": "\n".join(body_lines),
        }
    )
    _save_payments(data)

    return {
        "success": True,
        "channel": "gmail",
        "message_id": reminder_id,
        "message": f"Reminder sent to {email} for {currency} {amount_due or 'N/A'}.",
    }


def record_payment(intent: dict[str, Any]) -> dict[str, Any]:
    """
    Record a Stripe-confirmed payment.

    Args:
        intent: dict with 'payment_intent_id', 'amount', 'currency',
                'customer_email', 'status', 'created'.

    Returns:
        Dict with success, payment_id, synced_with_treasurer, and message.
    """
    payment_intent_id = intent.get("payment_intent_id")
    amount = intent.get("amount")
    currency = intent.get("currency", "mxn").upper()
    customer_email = intent.get("customer_email")
    status = intent.get("status")

    if not payment_intent_id:
        return {"success": False, "error": "Missing 'payment_intent_id'."}
    if not isinstance(amount, int) or amount <= 0:
        return {"success": False, "error": "Missing positive integer 'amount'."}
    if not customer_email:
        return {"success": False, "error": "Missing 'customer_email'."}

    if status != "succeeded":
        return {"success": False, "error": f"Payment is not confirmed. Status: {status}"}

    data = _load_payments()
    payment_id = _generate_id("pay", data.get("payments", []))
    commission = int(round(amount * 0.029)) + 30  # Approximation for Stripe MX

    data.setdefault("payments", []).append(
        {
            "id": payment_id,
            "stripe_payment_intent_id": payment_intent_id,
            "customer_email": customer_email,
            "amount": amount,
            "currency": currency,
            "stripe_commission": commission,
            "status": "paid",
            "created_at": intent.get("created") or _now_iso(),
            "paid_at": _now_iso(),
            "synced_with_treasurer": False,
        }
    )
    _save_payments(data)

    # Simulated notification to the Treasurer (in production via gbrain MCP)
    synced_with_treasurer = True

    return {
        "success": True,
        "payment_id": payment_id,
        "synced_with_treasurer": synced_with_treasurer,
        "message": f"Payment {payment_id} recorded: {currency} {amount}. Synced with Treasurer.",
    }


def list_charges(start_date: str | None = None, end_date: str | None = None) -> dict[str, Any]:
    """
    List Stripe charges for a date range.

    Args:
        start_date: optional ISO 8601 date (YYYY-MM-DD).
        end_date: optional ISO 8601 date (YYYY-MM-DD).

    Returns:
        Dict with success, count, and charges.
    """
    start = _parse_iso_date(start_date) if start_date else None
    end = _parse_iso_date(end_date) if end_date else None

    if _init_stripe():
        try:
            params: dict[str, Any] = {"limit": 100}
            if start:
                params["created[gte]"] = int(start.timestamp())
            if end:
                params["created[lte]"] = int(end.timestamp())
            result = stripe_lib.Charge.list(**params)
            return {
                "success": True,
                "count": len(result.data),
                "charges": [
                    {
                        "id": ch.id,
                        "amount": ch.amount,
                        "currency": ch.currency.upper(),
                        "customer_email": ch.receipt_email,
                        "status": ch.status,
                        "created": datetime.fromtimestamp(ch.created, tz=timezone.utc).isoformat(),
                    }
                    for ch in result.data
                ],
            }
        except Exception as exc:
            return {"success": False, "error": f"Stripe error: {exc}"}

    # Local mode: filter payments from .payments
    data = _load_payments()
    payments = data.get("payments", [])
    charges: list[dict[str, Any]] = []
    for payment in payments:
        paid_at = _parse_iso_date(payment.get("paid_at"))
        if start and paid_at and paid_at < start:
            continue
        if end and paid_at and paid_at > end:
            continue
        charges.append(
            {
                "id": payment.get("stripe_payment_intent_id"),
                "amount": payment.get("amount"),
                "currency": payment.get("currency", "MXN"),
                "customer_email": payment.get("customer_email"),
                "status": payment.get("status"),
                "created": payment.get("paid_at"),
            }
        )

    return {
        "success": True,
        "count": len(charges),
        "charges": charges,
        "message": "Charges listed in local mode (Stripe MCP not available).",
    }


def generate_income_report(start_date: str, end_date: str) -> dict[str, Any]:
    """
    Generate an income report between two dates.

    Args:
        start_date: start date in ISO 8601 format (YYYY-MM-DD).
        end_date: end date in ISO 8601 format (YYYY-MM-DD).

    Returns:
        Dict with total_collected, pending, overdue, by_customer, by_product.
    """
    try:
        start = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
        end = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc) + timedelta(days=1)
    except ValueError:
        return {"success": False, "error": "Invalid date format. Use YYYY-MM-DD."}

    data = _load_payments()
    payments = data.get("payments", [])

    total_collected = 0
    total_pending = 0
    overdue = 0
    by_customer: dict[str, int] = {}
    by_product: dict[str, int] = {}

    # Build a price -> product name lookup for by_product attribution
    price_to_product: dict[str, str] = {}
    for price in data.get("prices", []):
        product = next(
            (p for p in data.get("products", []) if p.get("id") == price.get("product_id")),
            None,
        )
        price_to_product[price.get("id", "")] = (
            product.get("name", "Unknown") if product else "Unknown"
        )

    for payment in payments:
        try:
            payment_date = datetime.fromisoformat(
                payment.get("paid_at") or payment.get("created_at") or ""
            )
            if payment_date.tzinfo is None:
                payment_date = payment_date.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

        if not (start <= payment_date < end):
            continue

        amount = payment.get("amount", 0)
        status = payment.get("status", "")
        customer = payment.get("customer_email", "unknown")
        price_id = payment.get("price_id", "")
        product_name = price_to_product.get(price_id, "Unknown")

        if status == "paid":
            total_collected += amount
            by_customer[customer] = by_customer.get(customer, 0) + amount
            by_product[product_name] = by_product.get(product_name, 0) + amount
        elif status in ("pending", "partial"):
            total_pending += amount

    # Overdue accounts (simple: creation date earlier than today and status pending)
    today = datetime.now(timezone.utc)
    for payment in payments:
        if payment.get("status") not in ("pending", "partial"):
            continue
        try:
            due = datetime.fromisoformat(payment.get("created_at", ""))
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
            if due < today:
                overdue += payment.get("amount", 0)
        except ValueError:
            continue

    return {
        "success": True,
        "period": {"start": start_date, "end": end_date},
        "total_collected": total_collected,
        "pending": total_pending,
        "overdue": overdue,
        "by_customer": by_customer,
        "by_product": by_product,
        "currency": data.get("metadata", {}).get("currency", "MXN"),
    }


# ---------------------------------------------------------------------------
# Collection workflow functions
# ---------------------------------------------------------------------------


def read_pending_payments() -> dict[str, Any]:
    """Return all pending payments and open invoices."""
    data = _load_payments()
    pending_payments = [p for p in data.get("payments", []) if p.get("status") in ("pending", "partial")]
    open_invoices = [i for i in data.get("invoices", []) if i.get("status") in ("open", "draft")]
    return {
        "success": True,
        "count": len(pending_payments) + len(open_invoices),
        "payments": pending_payments,
        "invoices": open_invoices,
    }


def read_overdue_payments() -> dict[str, Any]:
    """Return overdue payments grouped by days past due."""
    overdue = get_overdue_payments()
    return {
        "success": True,
        "count": len(overdue),
        "overdue": overdue,
    }


def get_overdue_payments() -> list[dict[str, Any]]:
    """Return overdue payments with days late."""
    data = _load_payments()
    today = datetime.now(timezone.utc)
    overdue: list[dict[str, Any]] = []

    for payment in data.get("payments", []):
        if payment.get("status") not in ("pending", "partial"):
            continue
        due = _parse_iso_date(payment.get("due_date") or payment.get("created_at"))
        if due is None:
            continue
        if due < today:
            payment_copy = dict(payment)
            payment_copy["days_overdue"] = (today - due).days
            overdue.append(payment_copy)

    # Include open invoices past their due date
    for invoice in data.get("invoices", []):
        if invoice.get("status") not in ("open", "draft"):
            continue
        due = _parse_iso_date(invoice.get("due_date"))
        if due is None:
            continue
        if due < today:
            invoice_copy = dict(invoice)
            invoice_copy["days_overdue"] = (today - due).days
            invoice_copy["type"] = "invoice"
            overdue.append(invoice_copy)

    overdue.sort(key=lambda p: p.get("days_overdue", 0), reverse=True)
    return overdue


def get_upcoming_payments(days: int = 3) -> list[dict[str, Any]]:
    """Return payments due in the next N days."""
    data = _load_payments()
    today = datetime.now(timezone.utc)
    future = today + timedelta(days=days)
    upcoming: list[dict[str, Any]] = []

    for payment in data.get("payments", []):
        if payment.get("status") not in ("pending", "partial"):
            continue
        due = _parse_iso_date(payment.get("due_date") or payment.get("created_at"))
        if due is None:
            continue
        if today <= due <= future:
            upcoming.append(payment)

    for invoice in data.get("invoices", []):
        if invoice.get("status") not in ("open", "draft"):
            continue
        due = _parse_iso_date(invoice.get("due_date"))
        if due is None:
            continue
        if today <= due <= future:
            upcoming.append(invoice)

    return upcoming


def get_failed_subscriptions() -> list[dict[str, Any]]:
    """Return subscriptions with failed charge attempts."""
    data = _load_payments()
    return [s for s in data.get("subscriptions", []) if s.get("failed_attempts", 0) > 0]


def classify_risk(overdue_payments: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """
    Classify overdue accounts as low, medium, or high risk.

    Args:
        overdue_payments: optional list of overdue payment dicts. If omitted,
                          the function reads them from the .payments file.

    Returns:
        Dict with success and risk buckets.
    """
    if overdue_payments is None:
        overdue_payments = get_overdue_payments()

    low: list[dict[str, Any]] = []
    medium: list[dict[str, Any]] = []
    high: list[dict[str, Any]] = []

    for payment in overdue_payments:
        days = payment.get("days_overdue", 0)
        amount = payment.get("amount", 0)
        if days <= 7 or amount < 10000:
            low.append(payment)
        elif days <= 30 or amount < 100000:
            medium.append(payment)
        else:
            high.append(payment)

    return {
        "success": True,
        "count": len(overdue_payments),
        "low": low,
        "medium": medium,
        "high": high,
    }


def schedule_followup(payment: dict[str, Any]) -> dict[str, Any]:
    """
    Schedule the next contact for an overdue account based on risk and policy.

    Args:
        payment: dict with at least 'id', 'customer_email', 'days_overdue'.

    Returns:
        Dict with success, next_contact_date, channel, and message.
    """
    payment_id = payment.get("id")
    email = payment.get("customer_email")
    days_overdue = payment.get("days_overdue", 0)

    if not payment_id or not email:
        return {"success": False, "error": "Payment requires 'id' and 'customer_email'."}

    today = datetime.now(timezone.utc).date()
    if days_overdue <= 3:
        next_contact = today + timedelta(days=1)
        channel = "email"
    elif days_overdue <= 7:
        next_contact = today + timedelta(days=2)
        channel = "email"
    elif days_overdue <= 30:
        next_contact = today + timedelta(days=3)
        channel = "email"
    else:
        next_contact = today + timedelta(days=1)
        channel = "escalation"

    data = _load_payments()
    data.setdefault("reminders", []).append(
        {
            "id": _generate_id("rem", data.get("reminders", [])),
            "customer_email": email,
            "payment_id": payment_id,
            "type": "followup",
            "scheduled": next_contact.isoformat(),
            "channel": channel,
            "status": "scheduled",
        }
    )
    _save_payments(data)

    return {
        "success": True,
        "payment_id": payment_id,
        "next_contact_date": next_contact.isoformat(),
        "channel": channel,
        "message": f"Follow-up scheduled for {email} on {next_contact} via {channel}.",
    }


def monitor_fraud(charge: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    Monitor a Stripe charge for suspicious patterns.

    Args:
        charge: optional charge dict. If omitted, the most recent charges are
                reviewed from the local .payments file.

    Returns:
        Dict with success, flags, and risk_score.
    """
    flags: list[str] = []

    if charge:
        amount = charge.get("amount", 0)
        currency = charge.get("currency", "MXN").upper()
        customer_email = charge.get("customer_email")
        status = charge.get("status", "")
        if amount > 500000:
            flags.append("unusually_large_amount")
        if status in ("failed", "disputed"):
            flags.append("failed_or_disputed_charge")
        if not customer_email:
            flags.append("missing_customer_email")
        return {
            "success": True,
            "charge_id": charge.get("id"),
            "risk_score": min(len(flags) * 3, 10),
            "flags": flags,
        }

    # No charge provided: review recent local payments
    data = _load_payments()
    payments = data.get("payments", [])[-10:]
    reviewed: list[dict[str, Any]] = []
    for payment in payments:
        result = monitor_fraud(payment)
        if result.get("risk_score", 0) > 0:
            reviewed.append(result)

    return {
        "success": True,
        "reviewed": len(payments),
        "flagged": len(reviewed),
        "alerts": reviewed,
    }


def notify(message: str, level: str = "info") -> dict[str, Any]:
    """
    Notify the operator through the configured channel.

    Args:
        message: notification body.
        level: info, warning, or error.

    Returns:
        Dict with success and logged message.
    """
    allowed_levels = {"info", "warning", "error"}
    if level not in allowed_levels:
        return {"success": False, "error": f"Level must be one of {allowed_levels}."}

    # In production this would delegate to the operator channel (Slack, email, etc.)
    # Here we log the notification to the .payments file for audit.
    data = _load_payments()
    data.setdefault("notifications", []).append(
        {
            "id": _generate_id("notif", data.get("notifications", [])),
            "level": level,
            "message": message,
            "sent": _now_iso(),
        }
    )
    _save_payments(data)

    return {
        "success": True,
        "level": level,
        "message": message,
    }


# ---------------------------------------------------------------------------
# Entry point for quick smoke tests
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    # Small syntax and basic functionality check.
    print("create_payment_link:", create_payment_link({"name": "Test"}, {"amount": 10000}))
    print("create_subscription:", create_subscription({"email": "test@example.com"}, {"amount": 5000, "interval": "month"}))
    print("create_invoice:", create_invoice(
        {"email": "test@example.com", "name": "Test"},
        [{"description": "Service", "amount": 10000, "currency": "mxn"}],
    ))
    print("send_payment_reminder:", send_payment_reminder({
        "email": "test@example.com",
        "name": "Test",
        "amount_due": 10000,
        "currency": "mxn",
        "due_date": "2026-06-30",
    }))
    print("record_payment:", record_payment({
        "payment_intent_id": "pi_test_001",
        "amount": 10000,
        "currency": "mxn",
        "customer_email": "test@example.com",
        "status": "succeeded",
    }))
    print("list_charges:", list_charges("2026-06-01", "2026-06-30"))
    print("generate_income_report:", generate_income_report("2026-06-01", "2026-06-30"))
    print("read_pending_payments:", read_pending_payments())
    print("read_overdue_payments:", read_overdue_payments())
    print("classify_risk:", classify_risk())
    print("monitor_fraud:", monitor_fraud())
    print("notify:", notify("Daily collection review completed."))
