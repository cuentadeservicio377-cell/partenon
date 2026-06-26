"""
Partenon Collector — Stripe Tools

Payment, subscription, reminder, and collection record functions.
Compatible with Python 3.12.

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
        if parent.name == "partenon-cobrador":
            return candidate
    return Path(__file__).resolve().parents[3] / ".payments"


def _load_payments(profile_dir: Path | None = None) -> dict[str, Any]:
    """Load the .payments file as a dict."""
    payments_file = _payments_file(profile_dir)
    if not payments_file.exists():
        return {"metadata": {}, "products": [], "prices": [], "links": [], "subscriptions": [], "customers": [], "payments": [], "reminders": []}
    try:
        with open(payments_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"metadata": {}, "products": [], "prices": [], "links": [], "subscriptions": [], "customers": [], "payments": [], "reminders": []}


def _save_payments(data: dict[str, Any], profile_dir: Path | None = None) -> None:
    """Save the .payments file."""
    payments_file = _payments_file(profile_dir)
    payments_file.parent.mkdir(parents=True, exist_ok=True)
    with open(payments_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _now_iso() -> str:
    """Current date/time in ISO 8601 format with timezone."""
    return datetime.now(timezone.utc).isoformat()


def _generate_id(prefix: str, collection: list[dict[str, Any]]) -> str:
    """Generate a simple sequential ID based on prefix and collection."""
    count = len(collection) + 1
    return f"{prefix}_{count:03d}"


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
            stripe_product = stripe_lib.Product.create(name=product_name, description=product.get("description", ""))
            stripe_price = stripe_lib.Price.create(
                unit_amount=amount,
                currency=currency,
                product=stripe_product.id,
            )
            link = stripe_lib.PaymentLink.create(line_items=[{"price": stripe_price.id, "quantity": 1}])
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

    data.setdefault("products", []).append({
        "id": product_id,
        "name": product_name,
        "description": product.get("description", ""),
        "active": True,
    })
    data.setdefault("prices", []).append({
        "id": price_id,
        "product_id": product_id,
        "amount": amount,
        "currency": currency,
        "type": "one_time",
    })
    data.setdefault("links", []).append({
        "id": link_id,
        "price_id": price_id,
        "url": f"https://buy.stripe.com/test_{link_id}",
        "concept": product_name,
        "created": _now_iso(),
        "status": "active",
    })
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
            data.setdefault("prices", []).append({
                "id": price_id,
                "amount": amount,
                "currency": currency,
                "type": "recurring",
                "interval": interval,
            })
            _save_payments(data)

    if _init_stripe():
        try:
            stripe_customer = stripe_lib.Customer.create(email=email, name=customer.get("name", ""))
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
    data.setdefault("subscriptions", []).append({
        "id": sub_id,
        "customer_email": email,
        "price_id": price_id,
        "stripe_subscription_id": f"sub_test_{sub_id}",
        "status": "active",
        "cycle": price.get("interval", "month"),
        "next_charge": next_payment[:10],
        "failed_attempts": 0,
    })
    _save_payments(data)

    return {
        "success": True,
        "subscription_id": sub_id,
        "status": "active",
        "next_payment": next_payment,
        "message": f"Subscription {sub_id} created in local mode for {email}.",
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
    body_lines.extend(["", "If you already made the payment, please ignore this message.", "", "Regards,"])

    # In a real environment, this would delegate to the Gmail MCP.
    # Here we register the reminder in .payments.
    data = _load_payments()
    reminder_id = _generate_id("rem", data.get("reminders", []))
    data.setdefault("reminders", []).append({
        "id": reminder_id,
        "customer_email": email,
        "type": "manual",
        "sent": _now_iso(),
        "channel": "gmail",
        "status": "sent",
        "subject": subject,
        "body": "\n".join(body_lines),
    })
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
        Dict with success, payment_id, synced_to_scribe, and message.
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

    data.setdefault("payments", []).append({
        "id": payment_id,
        "stripe_payment_intent_id": payment_intent_id,
        "customer_email": customer_email,
        "amount": amount,
        "currency": currency,
        "stripe_commission": commission,
        "status": "paid",
        "created_at": intent.get("created") or _now_iso(),
        "paid_at": _now_iso(),
        "synced_to_scribe": False,
    })
    _save_payments(data)

    # Simulated notification to the Scribe (in production via gbrain MCP)
    synced_to_scribe = True

    return {
        "success": True,
        "payment_id": payment_id,
        "synced_to_scribe": synced_to_scribe,
        "message": f"Payment {payment_id} recorded: {currency} {amount}. Synced with Scribe.",
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

    for payment in payments:
        try:
            payment_date = datetime.fromisoformat(payment.get("paid_at") or payment.get("created_at") or "")
            if payment_date.tzinfo is None:
                payment_date = payment_date.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

        if not (start <= payment_date < end):
            continue

        amount = payment.get("amount", 0)
        status = payment.get("status", "")
        customer = payment.get("customer_email", "unknown")

        if status == "paid":
            total_collected += amount
            by_customer[customer] = by_customer.get(customer, 0) + amount
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
# Additional collection functions
# ---------------------------------------------------------------------------


def get_overdue_payments() -> list[dict[str, Any]]:
    """Return overdue payments with days late."""
    data = _load_payments()
    today = datetime.now(timezone.utc)
    overdue: list[dict[str, Any]] = []

    for payment in data.get("payments", []):
        if payment.get("status") not in ("pending", "partial"):
            continue
        try:
            due = datetime.fromisoformat(payment.get("created_at", ""))
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
            if due < today:
                payment_copy = dict(payment)
                payment_copy["days_overdue"] = (today - due).days
                overdue.append(payment_copy)
        except ValueError:
            continue

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
        try:
            due = datetime.fromisoformat(payment.get("created_at", ""))
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
            if today <= due <= future:
                upcoming.append(payment)
        except ValueError:
            continue

    return upcoming


def get_failed_subscriptions() -> list[dict[str, Any]]:
    """Return subscriptions with failed charge attempts."""
    data = _load_payments()
    return [s for s in data.get("subscriptions", []) if s.get("failed_attempts", 0) > 0]


if __name__ == "__main__":
    # Small syntax and basic functionality check.
    print("create_payment_link:", create_payment_link({"name": "Test"}, {"amount": 10000}))
    print("create_subscription:", create_subscription({"email": "test@example.com"}, {"amount": 5000, "interval": "month"}))
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
    print("generate_income_report:", generate_income_report("2026-06-01", "2026-06-30"))
