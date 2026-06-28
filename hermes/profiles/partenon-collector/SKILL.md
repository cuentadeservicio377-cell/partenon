# Partenon Collector — Payments Skill Pack

> Payments, collections, and revenue agent for small businesses.
> Creates links, invoices, and subscriptions; tracks overdue accounts; monitors fraud.

## Included skills

### `payments`
- Create payment links, subscriptions, and invoices.
- Send payment reminders.
- Record confirmed payments and sync with the Scribe.
- List charges and generate income reports.
- Track pending, overdue, upcoming, and failed payments.
- Classify customer risk and monitor fraud.

## Quick start

1. Copy `.env.example` to `.env` and set `STRIPE_SECRET_KEY`.
2. Copy `templates/.payments.example` to your workspace as `.payments`.
3. Use `skills/payments/tools/payment_link.py` to create a link.
4. Use `skills/payments/tools/invoice.py` to create an invoice.
5. Start the webhook handler: `python -m mcp_servers.payments.webhook`.

## Safety rules

- The Collector never executes a payment; it only creates links/invoices.
- Every confirmed payment is synced with the Scribe via the `payment_confirmed` workflow event.
- Reminders escalate to the Diplomat after three contacts.
- Fraud flags are forwarded to the Guardian.

## MCP Tools

The Collector exposes the `partenon-payments` MCP server. Available tools:

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

## Dry-run vs live

| Tool | Dry-run behavior | Live requirement |
|---|---|---|
| `payments_create_payment_link` | Returns example URL | `STRIPE_SECRET_KEY` |
| `payments_create_subscription` | Returns mock subscription id | `STRIPE_SECRET_KEY` |
| `payments_create_invoice` | Returns mock invoice id | `STRIPE_SECRET_KEY` |
| `payments_record_payment` | Simulates Scribe sync | `STRIPE_SECRET_KEY` and valid PaymentIntent |
| `payments_list_charges` | Returns empty list | `STRIPE_SECRET_KEY` |
| `payments_generate_income_report` | Returns zero | `STRIPE_SECRET_KEY` |
| `payments_monitor_fraud` | Returns empty flags | `STRIPE_SECRET_KEY` |
| `payments_get_upcoming_payments` | Returns empty list | `STRIPE_SECRET_KEY` |
| `payments_get_failed_subscriptions` | Returns empty list | `STRIPE_SECRET_KEY` |

Live mode is opt-in via `.env`. The default dry-run mode never creates real Stripe objects or sends messages.
