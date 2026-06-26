---
name: payments
version: 0.1.0
profile: partenon-cobrador
description: >
  Gestiona pagos, suscripciones, links de pago, recordatorios y reportes de ingresos
  mediante Stripe y Google Workspace.
---

# Skill: Payments — Partenon Cobrador

## Rol

Soy la capa de pagos del Cobrador. Conecto Stripe con el resto del Partenón para que cada cobro tenga origen, destino y registro.

## Funciones

### `create_payment_link(product, price)`

Genera un link de pago de Stripe para un producto y precio.

**Parámetros:**
- `product` (dict): `name`, `description` opcional.
- `price` (dict): `amount` (entero en centavos), `currency` (default `mxn`), `recurring` opcional.

**Retorno:**
- Dict con `success`, `url`, `payment_link_id`, `message`.

### `create_subscription(customer, price)`

Crea una suscripción de Stripe para un cliente y un precio recurrente.

**Parámetros:**
- `customer` (dict): `email` requerido, `name` opcional.
- `price` (dict): `id` del precio de Stripe o `amount`/`currency`/`interval` para crearlo.

**Retorno:**
- Dict con `success`, `subscription_id`, `status`, `next_payment`, `message`.

### `send_payment_reminder(customer)`

Envía un recordatorio de pago al cliente por el canal configurado (Gmail primero, luego Google Chat si aplica).

**Parámetros:**
- `customer` (dict): `email`, `name`, `amount_due`, `currency`, `due_date`, `payment_link` opcional.

**Retorno:**
- Dict con `success`, `channel`, `message_id` (si aplica), `message`.

### `record_payment(intent)`

Registra un pago confirmado por Stripe en el archivo `.payments` y notifica al Tesorero.

**Parámetros:**
- `intent` (dict): `payment_intent_id`, `amount`, `currency`, `customer_email`, `status`, `created`.

**Retorno:**
- Dict con `success`, `payment_id`, `synced_to_treasurer`, `message`.

### `generate_income_report(start_date, end_date)`

Genera un reporte de ingresos para un rango de fechas.

**Parámetros:**
- `start_date` (str): ISO 8601, por ejemplo `2026-06-01`.
- `end_date` (str): ISO 8601, por ejemplo `2026-06-30`.

**Retorno:**
- Dict con `total_collected`, `pending`, `overdue`, `by_customer`, `by_product`.

## Estados de Cobranza

```
Pendiente → Recordatorio enviado → Pagado → Registrado → Sincronizado con Tesorero
     ↓
Vencido → Segundo recordatorio → Tercer recordatorio → Escalado a Diplomático
     ↓
Fallido → Reintentar método → Cancelar suscripción
```

## Reglas

- **SIEMPRE** validar que existe un registro de cobro antes de crear un link.
- **SIEMPRE** usar `record_payment` después de confirmar un pago en Stripe.
- **SIEMPRE** notificar al Tesorero cuando un pago se confirme.
- **NUNCA** enviar más de tres recordatorios sin escalar.
- **NUNCA** crear una suscripción sin consentimiento documentado del cliente.

## Archivos

- `.payments`: archivo maestro de productos, precios, links, suscripciones, clientes y pagos.
- `templates/.payments.example`: plantilla inicial del archivo maestro.
- `cron/daily-collection.json`: configuración de revisión diaria de cobranza.

## Dependencias

- `stripe_tools.py`: implementación de las funciones principales.
- `google_workspace` MCP: envío de recordatorios y registro en Sheets.
- `gbrain` MCP: registro de misiones y contexto del cliente.
