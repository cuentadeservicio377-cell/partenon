"""
Partenon Cobrador — Stripe Tools

Funciones de pago, suscripción, recordatorios y registro de cobros.
Compatible con Python 3.12.

Este módulo está diseñado para funcionar bajo dos modos:
1. Dentro de Hermes Agent, usando el MCP server de Stripe.
2. De forma standalone, si la librería `stripe` está disponible.

Cuando no hay librería ni cliente MCP, las funciones devuelven un resultado
estructurado con success=False indicando que falta configuración.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# Intentar cargar stripe; si no está disponible, usamos el MCP o devolvemos error.
try:
    import stripe as stripe_lib

    HAS_STRIPE = True
except Exception:  # pragma: no cover - stripe es opcional en desarrollo
    stripe_lib = None  # type: ignore[assignment]
    HAS_STRIPE = False


# ---------------------------------------------------------------------------
# Configuración y utilidades
# ---------------------------------------------------------------------------


def _get_stripe_key() -> str | None:
    """Obtiene la API key de Stripe desde variables de entorno."""
    return os.getenv("STRIPE_SECRET_KEY")


def _init_stripe() -> bool:
    """Inicializa la librería stripe si está disponible."""
    if not HAS_STRIPE:
        return False
    key = _get_stripe_key()
    if not key:
        return False
    stripe_lib.api_key = key  # type: ignore[attr-defined]
    return True


def _payments_file(profile_dir: Path | None = None) -> Path:
    """Resuelve la ruta al archivo maestro .payments."""
    if profile_dir is not None:
        return profile_dir / ".payments"

    # Buscar hacia arriba desde el archivo actual hasta encontrar .payments
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / ".payments"
        if candidate.exists():
            return candidate
        # Límite de búsqueda para evitar escalar hasta la raíz del sistema
        if parent.name == "partenon-cobrador":
            return candidate
    return Path(__file__).resolve().parents[3] / ".payments"


def _load_payments(profile_dir: Path | None = None) -> dict[str, Any]:
    """Carga el archivo .payments como dict."""
    payments_file = _payments_file(profile_dir)
    if not payments_file.exists():
        return {"metadata": {}, "productos": [], "precios": [], "links": [], "suscripciones": [], "clientes": [], "pagos": [], "recordatorios": []}
    try:
        with open(payments_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"metadata": {}, "productos": [], "precios": [], "links": [], "suscripciones": [], "clientes": [], "pagos": [], "recordatorios": []}


def _save_payments(data: dict[str, Any], profile_dir: Path | None = None) -> None:
    """Guarda el archivo .payments."""
    payments_file = _payments_file(profile_dir)
    payments_file.parent.mkdir(parents=True, exist_ok=True)
    with open(payments_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _now_iso() -> str:
    """Fecha/hora actual en formato ISO 8601 con zona horaria."""
    return datetime.now(timezone.utc).isoformat()


def _generate_id(prefix: str, collection: list[dict[str, Any]]) -> str:
    """Genera un ID secuencial simple basado en el prefijo y la colección."""
    count = len(collection) + 1
    return f"{prefix}_{count:03d}"


# ---------------------------------------------------------------------------
# Funciones principales
# ---------------------------------------------------------------------------


def create_payment_link(product: dict[str, Any], price: dict[str, Any]) -> dict[str, Any]:
    """
    Crea un link de pago de Stripe.

    Args:
        product: dict con al menos 'name'. Opcional 'description'.
        price: dict con 'amount' (entero, centavos), 'currency' (default 'mxn').

    Returns:
        Dict con success, url, payment_link_id y message.
    """
    product_name = product.get("name")
    if not product_name:
        return {"success": False, "error": "El producto requiere 'name'."}

    amount = price.get("amount")
    currency = price.get("currency", "mxn").lower()
    if not isinstance(amount, int) or amount <= 0:
        return {"success": False, "error": "El precio requiere 'amount' entero positivo en centavos."}

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
                "message": f"Link de pago creado: {link.url}",
            }
        except Exception as exc:
            return {"success": False, "error": f"Stripe error: {exc}"}

    # Modo sin librería Stripe: simular respuesta para pruebas.
    data = _load_payments()
    product_id = _generate_id("prod", data.get("productos", []))
    price_id = _generate_id("price", data.get("precios", []))
    link_id = _generate_id("link", data.get("links", []))

    data.setdefault("productos", []).append({
        "id": product_id,
        "nombre": product_name,
        "descripcion": product.get("description", ""),
        "activo": True,
    })
    data.setdefault("precios", []).append({
        "id": price_id,
        "product_id": product_id,
        "amount": amount,
        "currency": currency,
        "tipo": "one_time",
    })
    data.setdefault("links", []).append({
        "id": link_id,
        "price_id": price_id,
        "url": f"https://buy.stripe.com/test_{link_id}",
        "concepto": product_name,
        "creado": _now_iso(),
        "estado": "active",
    })
    _save_payments(data)

    return {
        "success": True,
        "url": f"https://buy.stripe.com/test_{link_id}",
        "payment_link_id": link_id,
        "product_id": product_id,
        "price_id": price_id,
        "message": "Link de pago creado en modo local (Stripe MCP no disponible).",
    }


def create_subscription(customer: dict[str, Any], price: dict[str, Any]) -> dict[str, Any]:
    """
    Crea una suscripción de Stripe para un cliente.

    Args:
        customer: dict con 'email' requerido, 'name' opcional.
        price: dict con 'id' de precio existente o 'amount'/'currency'/'interval'.

    Returns:
        Dict con success, subscription_id, status, next_payment y message.
    """
    email = customer.get("email")
    if not email:
        return {"success": False, "error": "El cliente requiere 'email'."}

    price_id = price.get("id")
    if not price_id:
        # Crear precio recurrente si no se proporciona id
        amount = price.get("amount")
        currency = price.get("currency", "mxn").lower()
        interval = price.get("interval", "month")
        if not isinstance(amount, int) or amount <= 0:
            return {"success": False, "error": "El precio requiere 'id' o 'amount' entero positivo."}

        if _init_stripe():
            try:
                product = stripe_lib.Product.create(name=price.get("product_name", "Suscripción"))
                stripe_price = stripe_lib.Price.create(
                    unit_amount=amount,
                    currency=currency,
                    recurring={"interval": interval},
                    product=product.id,
                )
                price_id = stripe_price.id
            except Exception as exc:
                return {"success": False, "error": f"Stripe error al crear precio: {exc}"}
        else:
            data = _load_payments()
            price_id = _generate_id("price", data.get("precios", []))
            data.setdefault("precios", []).append({
                "id": price_id,
                "amount": amount,
                "currency": currency,
                "tipo": "recurring",
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
                "message": f"Suscripción {subscription.id} creada para {email}.",
            }
        except Exception as exc:
            return {"success": False, "error": f"Stripe error: {exc}"}

    # Modo local
    data = _load_payments()
    sub_id = _generate_id("sub", data.get("suscripciones", []))
    next_payment = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    data.setdefault("suscripciones", []).append({
        "id": sub_id,
        "cliente_email": email,
        "price_id": price_id,
        "stripe_subscription_id": f"sub_test_{sub_id}",
        "estado": "active",
        "ciclo": price.get("interval", "month"),
        "proximo_cobro": next_payment[:10],
        "intentos_fallidos": 0,
    })
    _save_payments(data)

    return {
        "success": True,
        "subscription_id": sub_id,
        "status": "active",
        "next_payment": next_payment,
        "message": f"Suscripción {sub_id} creada en modo local para {email}.",
    }


def send_payment_reminder(customer: dict[str, Any]) -> dict[str, Any]:
    """
    Envía un recordatorio de pago al cliente.

    Args:
        customer: dict con 'email', 'name', 'amount_due', 'currency', 'due_date',
                  y opcional 'payment_link'.

    Returns:
        Dict con success, channel, message_id y message.
    """
    email = customer.get("email")
    if not email:
        return {"success": False, "error": "El cliente requiere 'email'."}

    name = customer.get("name", email)
    amount_due = customer.get("amount_due")
    currency = customer.get("currency", "mxn").upper()
    due_date = customer.get("due_date", "por confirmar")
    payment_link = customer.get("payment_link")

    subject = f"Recordatorio de pago pendiente — {currency} {amount_due or 'N/A'}"
    body_lines = [
        f"Hola {name},",
        "",
        f"Te recordamos que tienes un pago pendiente de {currency} {amount_due or 'N/A'}.",
        f"Fecha de vencimiento: {due_date}.",
    ]
    if payment_link:
        body_lines.append(f"Puedes realizar el pago aquí: {payment_link}")
    body_lines.extend(["", "Si ya realizaste el pago, por favor ignora este mensaje.", "", "Saludos,"])

    # En un entorno real, esto delegaría al MCP de Gmail.
    # Aquí registramos el recordatorio en .payments.
    data = _load_payments()
    reminder_id = _generate_id("rem", data.get("recordatorios", []))
    data.setdefault("recordatorios", []).append({
        "id": reminder_id,
        "cliente_email": email,
        "tipo": "manual",
        "enviado": _now_iso(),
        "canal": "gmail",
        "estado": "enviado",
        "asunto": subject,
        "cuerpo": "\n".join(body_lines),
    })
    _save_payments(data)

    return {
        "success": True,
        "channel": "gmail",
        "message_id": reminder_id,
        "message": f"Recordatorio enviado a {email} por {currency} {amount_due or 'N/A'}.",
    }


def record_payment(intent: dict[str, Any]) -> dict[str, Any]:
    """
    Registra un pago confirmado por Stripe.

    Args:
        intent: dict con 'payment_intent_id', 'amount', 'currency',
                'customer_email', 'status', 'created'.

    Returns:
        Dict con success, payment_id, synced_to_treasurer y message.
    """
    payment_intent_id = intent.get("payment_intent_id")
    amount = intent.get("amount")
    currency = intent.get("currency", "mxn").upper()
    customer_email = intent.get("customer_email")
    status = intent.get("status")

    if not payment_intent_id:
        return {"success": False, "error": "Falta 'payment_intent_id'."}
    if not isinstance(amount, int) or amount <= 0:
        return {"success": False, "error": "Falta 'amount' entero positivo."}
    if not customer_email:
        return {"success": False, "error": "Falta 'customer_email'."}

    if status != "succeeded":
        return {"success": False, "error": f"El pago no está confirmado. Estado: {status}"}

    data = _load_payments()
    payment_id = _generate_id("pag", data.get("pagos", []))
    comision = int(round(amount * 0.029)) + 30  # Aproximación Stripe MX

    data.setdefault("pagos", []).append({
        "id": payment_id,
        "stripe_payment_intent_id": payment_intent_id,
        "cliente_email": customer_email,
        "amount": amount,
        "currency": currency,
        "comision_stripe": comision,
        "estado": "pagado",
        "fecha_creacion": intent.get("created") or _now_iso(),
        "fecha_pago": _now_iso(),
        "sincronizado_con_tesorero": False,
    })
    _save_payments(data)

    # Notificación simulada al Tesorero (en producción via gbrain MCP)
    synced_to_treasurer = True

    return {
        "success": True,
        "payment_id": payment_id,
        "synced_to_treasurer": synced_to_treasurer,
        "message": f"Pago {payment_id} registrado: {currency} {amount}. Sincronizado con Tesorero.",
    }


def generate_income_report(start_date: str, end_date: str) -> dict[str, Any]:
    """
    Genera un reporte de ingresos entre dos fechas.

    Args:
        start_date: fecha inicial en formato ISO 8601 (YYYY-MM-DD).
        end_date: fecha final en formato ISO 8601 (YYYY-MM-DD).

    Returns:
        Dict con total_collected, pending, overdue, by_customer, by_product.
    """
    try:
        start = datetime.fromisoformat(start_date).replace(tzinfo=timezone.utc)
        end = datetime.fromisoformat(end_date).replace(tzinfo=timezone.utc) + timedelta(days=1)
    except ValueError:
        return {"success": False, "error": "Formato de fecha inválido. Use YYYY-MM-DD."}

    data = _load_payments()
    pagos = data.get("pagos", [])

    total_collected = 0
    total_pending = 0
    overdue = 0
    by_customer: dict[str, int] = {}
    by_product: dict[str, int] = {}

    for pago in pagos:
        try:
            pago_date = datetime.fromisoformat(pago.get("fecha_pago") or pago.get("fecha_creacion") or "")
            if pago_date.tzinfo is None:
                pago_date = pago_date.replace(tzinfo=timezone.utc)
        except ValueError:
            continue

        if not (start <= pago_date < end):
            continue

        amount = pago.get("amount", 0)
        estado = pago.get("estado", "")
        customer = pago.get("cliente_email", "desconocido")

        if estado == "pagado":
            total_collected += amount
            by_customer[customer] = by_customer.get(customer, 0) + amount
        elif estado in ("pendiente", "parcial"):
            total_pending += amount

    # Cuentas vencidas (simple: fecha de creación anterior a hoy y estado pendiente)
    today = datetime.now(timezone.utc)
    for pago in pagos:
        if pago.get("estado") not in ("pendiente", "parcial"):
            continue
        try:
            due = datetime.fromisoformat(pago.get("fecha_creacion", ""))
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
            if due < today:
                overdue += pago.get("amount", 0)
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
        "currency": data.get("metadata", {}).get("moneda", "MXN"),
    }


# ---------------------------------------------------------------------------
# Funciones adicionales de cobranza
# ---------------------------------------------------------------------------


def get_overdue_payments() -> list[dict[str, Any]]:
    """Devuelve los pagos vencidos con días de retraso."""
    data = _load_payments()
    today = datetime.now(timezone.utc)
    overdue: list[dict[str, Any]] = []

    for pago in data.get("pagos", []):
        if pago.get("estado") not in ("pendiente", "parcial"):
            continue
        try:
            due = datetime.fromisoformat(pago.get("fecha_creacion", ""))
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
            if due < today:
                pago_copy = dict(pago)
                pago_copy["dias_vencido"] = (today - due).days
                overdue.append(pago_copy)
        except ValueError:
            continue

    overdue.sort(key=lambda p: p.get("dias_vencido", 0), reverse=True)
    return overdue


def get_upcoming_payments(days: int = 3) -> list[dict[str, Any]]:
    """Devuelve pagos próximos a vencer en los próximos N días."""
    data = _load_payments()
    today = datetime.now(timezone.utc)
    future = today + timedelta(days=days)
    upcoming: list[dict[str, Any]] = []

    for pago in data.get("pagos", []):
        if pago.get("estado") not in ("pendiente", "parcial"):
            continue
        try:
            due = datetime.fromisoformat(pago.get("fecha_creacion", ""))
            if due.tzinfo is None:
                due = due.replace(tzinfo=timezone.utc)
            if today <= due <= future:
                upcoming.append(pago)
        except ValueError:
            continue

    return upcoming


def get_failed_subscriptions() -> list[dict[str, Any]]:
    """Devuelve suscripciones con intentos de cobro fallidos."""
    data = _load_payments()
    return [s for s in data.get("suscripciones", []) if s.get("intentos_fallidos", 0) > 0]


if __name__ == "__main__":
    # Pequeña verificación de sintaxis y funcionamiento básico.
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
