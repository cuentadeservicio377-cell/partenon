---
name: payments
version: 0.1.0
profile: partenon-cobrador
description: >
  Manages payments, subscriptions, payment links, reminders, and income reports
  through Stripe and Google Workspace.
---

# Skill: Payments — Partenon Collector

## Role

I am the Collector's payments layer. I connect Stripe with the rest of Partenon so that every charge has origin, destination, and record.

## Functions

### `create_payment_link(product, price)`

Generates a Stripe payment link for a product and price.

**Parameters:**
- `product` (dict): `name`, optional `description`.
- `price` (dict): `amount` (integer in smallest currency unit), `currency` (default `mxn`), optional `recurring`.

**Return:**
- Dict with `success`, `url`, `payment_link_id`, `message`.

### `create_subscription(customer, price)`

Creates a Stripe subscription for a customer and a recurring price.

**Parameters:**
- `customer` (dict): `email` required, `name` optional.
- `price` (dict): Stripe price `id` or `amount`/`currency`/`interval` to create it.

**Return:**
- Dict with `success`, `subscription_id`, `status`, `next_payment`, `message`.

### `send_payment_reminder(customer)`

Sends a payment reminder to the customer through the configured channel (Gmail first, then Google Chat if applicable).

**Parameters:**
- `customer` (dict): `email`, `name`, `amount_due`, `currency`, `due_date`, optional `payment_link`.

**Return:**
- Dict with `success`, `channel`, `message_id` (if applicable), `message`.

### `record_payment(intent)`

Records a Stripe-confirmed payment in the `.payments` file and notifies the Treasurer.

**Parameters:**
- `intent` (dict): `payment_intent_id`, `amount`, `currency`, `customer_email`, `status`, `created`.

**Return:**
- Dict with `success`, `payment_id`, `synced_to_treasurer`, `message`.

### `generate_income_report(start_date, end_date)`

Generates an income report for a date range.

**Parameters:**
- `start_date` (str): ISO 8601, for example `2026-06-01`.
- `end_date` (str): ISO 8601, for example `2026-06-30`.

**Return:**
- Dict with `total_collected`, `pending`, `overdue`, `by_customer`, `by_product`.

## Collection states

```
Pending → Reminder sent → Paid → Recorded → Synced with Treasurer
   ↓
Overdue → Second reminder → Third reminder → Escalated to Diplomat
   ↓
Failed → Retry method → Cancel subscription
```

## Rules

- **ALWAYS** validate that a charge record exists before creating a link.
- **ALWAYS** use `record_payment` after confirming a payment in Stripe.
- **ALWAYS** notify the Treasurer when a payment is confirmed.
- **NEVER** send more than three reminders without escalating.
- **NEVER** create a subscription without documented customer consent.

## Files

- `.payments`: master file of products, prices, links, subscriptions, clients, and payments.
- `templates/.payments.example`: initial template for the master file.
- `cron/daily-collection.json`: daily collection review configuration.

## Dependencies

- `stripe_tools.py`: implementation of the main functions.
- `google_workspace` MCP: sending reminders and recording in Sheets.
- `gbrain` MCP: recording missions and client context.
