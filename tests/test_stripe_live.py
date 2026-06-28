"""Tests for Stripe live-mode behavior in the Payments MCP server."""

import os
import unittest
from unittest import mock

from mcp_servers.payments.server import (
    payments_create_invoice,
    payments_create_payment_link,
    payments_generate_income_report,
    payments_list_charges,
    payments_record_payment,
)


class StripeLiveTestCase(unittest.TestCase):
    def setUp(self):
        self.env_patcher = mock.patch.dict(os.environ, {"STRIPE_SECRET_KEY": "sk_test_xxx"}, clear=False)
        self.env_patcher.start()

    def tearDown(self):
        self.env_patcher.stop()

    @mock.patch("mcp_servers.payments.server._stripe_client")
    def test_create_payment_link_live(self, mock_client_factory):
        mock_client = mock_client_factory.return_value
        mock_client.products.create.return_value = mock.Mock(id="prod_123")
        mock_client.prices.create.return_value = mock.Mock(id="price_123")
        mock_client.payment_links.create.return_value = mock.Mock(url="https://pay.stripe.test/link_123")

        result = payments_create_payment_link(100.0, "USD", dry_run=False)
        self.assertTrue(result["ok"])
        self.assertFalse(result["dry_run"])
        self.assertIn("url", result)

    @mock.patch("mcp_servers.payments.server._stripe_client")
    def test_create_invoice_live(self, mock_client_factory):
        mock_client = mock_client_factory.return_value
        mock_client.customers.list.return_value = mock.Mock(data=[mock.Mock(id="cus_123")])
        mock_client.invoices.create.return_value = mock.Mock(id="inv_123", auto_advance=True)
        mock_client.invoiceitems.create.return_value = mock.Mock(id="ii_123")
        mock_client.invoices.finalize_invoice.return_value = mock.Mock(
            id="inv_123", hosted_invoice_url="https://invoice.stripe.test/inv_123"
        )

        result = payments_create_invoice("client@example.test", 250.0, dry_run=False)
        self.assertTrue(result["ok"])
        self.assertFalse(result["dry_run"])
        self.assertEqual(result["invoice_id"], "inv_123")

    @mock.patch("mcp_servers.payments.server._stripe_client")
    def test_record_payment_live_succeeded(self, mock_client_factory):
        mock_client = mock_client_factory.return_value
        mock_client.payment_intents.retrieve.return_value = mock.Mock(status="succeeded", amount_received=10000)

        result = payments_record_payment("pi_123", 100.0, dry_run=False)
        self.assertTrue(result["ok"])
        self.assertFalse(result["dry_run"])
        self.assertTrue(result["synced_with_scribe"])

    @mock.patch("mcp_servers.payments.server._stripe_client")
    def test_record_payment_live_not_succeeded(self, mock_client_factory):
        mock_client = mock_client_factory.return_value
        mock_client.payment_intents.retrieve.return_value = mock.Mock(status="requires_payment_method")

        result = payments_record_payment("pi_123", 100.0, dry_run=False)
        self.assertFalse(result["ok"])

    @mock.patch("mcp_servers.payments.server._stripe_client")
    def test_list_charges_live(self, mock_client_factory):
        mock_client = mock_client_factory.return_value
        charge = mock.Mock(
            id="ch_123",
            amount=5000,
            currency="usd",
            status="succeeded",
            customer="cus_123",
            created=1700000000,
        )
        mock_client.charges.list.return_value = mock.Mock(data=[charge])

        result = payments_list_charges("2024-01-01", "2024-01-31", dry_run=False)
        self.assertTrue(result["ok"])
        self.assertFalse(result["dry_run"])
        self.assertEqual(len(result["charges"]), 1)

    @mock.patch("mcp_servers.payments.server._stripe_client")
    def test_generate_income_report_live(self, mock_client_factory):
        mock_client = mock_client_factory.return_value
        charge = mock.Mock(status="succeeded", amount=20000)
        mock_client.charges.list.return_value = mock.Mock(data=[charge])

        result = payments_generate_income_report("month", dry_run=False)
        self.assertTrue(result["ok"])
        self.assertFalse(result["dry_run"])
        self.assertEqual(result["income"], 200.0)


if __name__ == "__main__":
    unittest.main()
