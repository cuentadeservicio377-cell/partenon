"""Tests for the Stripe webhook handler."""

import json
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

from mcp_servers.payments.webhook import app
from partenon_core.tools.workflow_engine import WorkflowEngine


client = TestClient(app)


def test_stripe_webhook_emits_payment_confirmed(monkeypatch):
    tmpdir = tempfile.TemporaryDirectory()
    monkeypatch.setattr(
        "partenon_core.tools.workflow_engine.WorkflowEngine.__init__",
        lambda self, data_dir=None: None,
    )
    monkeypatch.setattr(
        "partenon_core.tools.workflow_engine.WorkflowEngine._ensure_data_dir",
        lambda self: None,
    )
    monkeypatch.setattr(
        "partenon_core.tools.workflow_engine.WorkflowEngine._load_events",
        lambda self: [],
    )

    captured = {}

    def fake_emit(self, type, source, entity_id, entity_type, data):
        captured.update({"type": type, "source": source, "entity_id": entity_id, "data": data})
        return {"id": "evt_123", "actions_executed": []}

    monkeypatch.setattr(
        "partenon_core.tools.workflow_engine.WorkflowEngine.emit_event",
        fake_emit,
    )

    payload = {
        "id": "evt_123",
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_123",
                "amount_total": 10000,
                "currency": "usd",
                "customer_email": "client@example.test",
            }
        },
    }
    response = client.post("/webhooks/stripe", json=payload)
    assert response.status_code == 200
    assert captured["type"] == "payment_confirmed"
    assert captured["source"] == "stripe-webhook"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True
