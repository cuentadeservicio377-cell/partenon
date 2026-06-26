---
name: payments
version: 0.1.0
profile: partenon-cobrador
description: >
  Manages payments, subscriptions, invoices, payment links, reminders,
  revenue reports, fraud monitoring, and collection workflows through Stripe
  and Google Workspace.
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

### `create_invoice(customer, items)`

Creates and finalizes a Stripe invoice for a customer.

**Parameters:**
- `customer` (dict): `email` required, `name` optional.
- `items` (list): each item has `description`, `amount`, and optional `currency`.

**Return:**
- Dict with `success`, `invoice_id`, `amount`, `currency`, `status`, `hosted_invoice_url`, `message`.

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
- Dict with `success`, `payment_id`, `synced_with_treasurer`, `message`.

### `list_charges(start_date, end_date)`

Lists Stripe charges for a date range.

**Parameters:**
- `start_date` (str): ISO 8601 date, for example `2026-06-01`.
- `end_date` (str): ISO 8601 date, for example `2026-06-30`.

**Return:**
- Dict with `success`, `count`, `charges`.

### `generate_income_report(start_date, end_date)`

Generates an income report for a date range.

**Parameters:**
- `start_date` (str): ISO 8601, for example `2026-06-01`.
- `end_date` (str): ISO 8601, for example `2026-06-30`.

**Return:**
- Dict with `total_collected`, `pending`, `overdue`, `by_customer`, `by_product`.

### `read_pending_payments()`

Returns all pending payments and open invoices.

**Return:**
- Dict with `success`, `count`, `payments`, `invoices`.

### `read_overdue_payments()`

Returns overdue payments grouped by days past due.

**Return:**
- Dict with `success`, `count`, `overdue`.

### `get_upcoming_payments(days)`

Returns payments and invoices due in the next N days.

**Parameters:**
- `days` (int): number of days to look ahead (default 3).

**Return:**
- List of payment or invoice dicts.

### `get_failed_subscriptions()`

Returns subscriptions with failed charge attempts.

**Return:**
- List of subscription dicts.

### `classify_risk(overdue_payments)`

Classifies overdue accounts as low, medium, or high risk.

**Parameters:**
- `overdue_payments` (list): optional list of overdue payment dicts.

**Return:**
- Dict with `success`, `count`, `low`, `medium`, `high`.

### `schedule_followup(payment)`

Schedules the next contact for an overdue account based on risk and policy.

**Parameters:**
- `payment` (dict): `id`, `customer_email`, `days_overdue`.

**Return:**
- Dict with `success`, `payment_id`, `next_contact_date`, `channel`, `message`.

### `monitor_fraud(charge)`

Monitors a Stripe charge for suspicious patterns.

**Parameters:**
- `charge` (dict): optional charge dict.

**Return:**
- Dict with `success`, `risk_score`, `flags`.

### `notify(message, level)`

Notifies the operator through the configured channel.

**Parameters:**
- `message` (str): notification body.
- `level` (str): `info`, `warning`, or `error`.

**Return:**
- Dict with `success`, `level`, `message`.

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
- **NEVER** ignore a failed subscription; review the payment method before the next attempt.

## Files

- `.payments`: master file of products, prices, links, subscriptions, customers, invoices, payments, and reminders.
- `templates/.payments.example`: initial template for the master file.
- `cron/daily-collection.json`: daily collection review configuration.
- `cron/daily-followups.json`: daily follow-up and escalation configuration.

## Dependencies

- `stripe_tools.py`: implementation of the main functions.
- `google_workspace` MCP: sending reminders and recording in Sheets.
- `gbrain` MCP: recording missions and client context.
