---
name: payments
version: 0.1.0
profile: partenon-collector
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

## MCP Tools

All operations are exposed through the `partenon-payments` MCP server:

- `payments_create_payment_link`
- `payments_create_subscription`
- `payments_create_invoice`
- `payments_send_payment_reminder`
- `payments_record_payment`
- `payments_list_charges`
- `payments_generate_income_report`
- `payments_read_pending_payments`
- `payments_read_overdue_payments`
- `payments_classify_risk`
- `payments_schedule_followup`
- `payments_monitor_fraud`
- `payments_get_upcoming_payments`
- `payments_get_failed_subscriptions`

> Roadmap: `notify` is currently a local helper, not an MCP tool. It will be replaced by `partenon-comms` or `partenon-herald` publishing/notification tools when available.

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|------|------------------|------------------|
| `payments_create_payment_link` | Simulates link creation and logs payload. | `STRIPE_SECRET_KEY` |
| `payments_create_subscription` | Simulates subscription creation and logs payload. | `STRIPE_SECRET_KEY` |
| `payments_create_invoice` | Simulates invoice creation and logs payload. | `STRIPE_SECRET_KEY` |
| `payments_send_payment_reminder` | Generates draft reminder; does not send email. | `GMAIL_ACCESS_TOKEN` |
| `payments_record_payment` | Writes to local `.payments` file; does not call Stripe. | `GOOGLE_SERVICE_ACCOUNT_JSON` (for Sheets sync) |
| `payments_list_charges` | Returns simulated or locally cached charges. | `STRIPE_SECRET_KEY` |
| `payments_generate_income_report` | Generates report from local data. | `GOOGLE_SERVICE_ACCOUNT_JSON` (to write to Sheets) |
| `payments_read_pending_payments` | Reads from local `.payments` file. | None (local read) |
| `payments_read_overdue_payments` | Reads from local `.payments` file. | None (local read) |
| `payments_classify_risk` | Classifies from local overdue data. | None (local analysis) |
| `payments_schedule_followup` | Schedules next contact in local cron file. | `GMAIL_ACCESS_TOKEN` (when live send is enabled) |
| `payments_monitor_fraud` | Flags suspicious patterns from local charge data. | None (local analysis) |
| `payments_get_upcoming_payments` | Reads from local `.payments` file. | None (local read) |
| `payments_get_failed_subscriptions` | Reads from local `.payments` file or simulated cache. | `STRIPE_SECRET_KEY` |

## Files

- `.payments`: master file of products, prices, links, subscriptions, customers, invoices, payments, and reminders.
- `templates/.payments.example`: initial template for the master file.
- `cron/daily-collection.json`: daily collection review configuration.
- `cron/daily-followups.json`: daily follow-up and escalation configuration.

## Dependencies

- `partenon-payments` MCP server: source of truth for all payment, subscription, invoice, reminder, report, and fraud-monitoring tools.
- `partenon-brain` MCP server: records collection missions and client context.
- `stripe_tools.py`: local implementation helpers used by the MCP server.
- `google_workspace` integration (via MCP): sends reminders and records collections in Sheets when live mode is enabled.
