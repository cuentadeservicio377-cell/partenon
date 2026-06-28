"""Stripe webhook handler for Partenon.

Receives `checkout.session.completed` and `invoice.paid` events from Stripe,
verifies the signature when `STRIPE_WEBHOOK_SECRET` is set, and emits a
`payment_confirmed` event into the workflow engine so the Scribe can reconcile.
"""

import json
import os

import stripe
import uvicorn
from fastapi import FastAPI, HTTPException, Request

from partenon_core.tools.workflow_engine import WorkflowEngine

app = FastAPI(title="Partenon Stripe Webhook")


@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET")

    if secret:
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, secret)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail="Invalid payload") from exc
        except stripe.error.SignatureVerificationError as exc:
            raise HTTPException(status_code=400, detail="Invalid signature") from exc
    else:
        event = json.loads(payload)

    event_type = event.get("type")
    if event_type in ("checkout.session.completed", "invoice.paid"):
        data = event.get("data", {}).get("object", {})
        engine = WorkflowEngine()
        engine.emit_event(
            type="payment_confirmed",
            source="stripe-webhook",
            entity_id=data.get("id", "unknown"),
            entity_type="payment",
            data={
                "amount": data.get("amount_total", data.get("amount_due", 0)) / 100,
                "currency": data.get("currency", "usd"),
                "customer_email": data.get("customer_email", ""),
                "customer": data.get("customer", ""),
                "stripe_event_type": event_type,
            },
        )

    return {"status": "processed", "type": event.get("type")}


@app.get("/health")
async def health():
    return {"ok": True}


def main():
    port = int(os.environ.get("STRIPE_WEBHOOK_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
