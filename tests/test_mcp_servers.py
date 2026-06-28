"""Tests for Partenon MCP server dry-run wrappers."""

import unittest

from mcp_servers.comms.server import (
    comms_brand_intake,
    comms_generate_copy,
    comms_plan_content_calendar,
)
from mcp_servers.finance.server import (
    finance_classify_expense,
    finance_generate_dashboard,
    finance_parse_expense,
)
from mcp_servers.memory.server import memory_get_page, memory_put_page, memory_search
from mcp_servers.ops.server import ops_create_project, ops_create_task, ops_generate_briefing
from mcp_servers.payments.server import (
    payments_create_invoice,
    payments_create_payment_link,
    payments_record_payment,
)
from mcp_servers.relations.server import (
    relations_register_client,
    relations_run_followups,
    relations_schedule_meeting,
)
from mcp_servers.security.server import (
    security_audit_access,
    security_list_keys,
    security_rotate_key,
)


class FinanceServerTestCase(unittest.TestCase):
    def test_parse_expense_dry_run(self):
        result = finance_parse_expense("office supplies")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])

    def test_classify_expense_dry_run(self):
        result = finance_classify_expense("rent", 500)
        self.assertTrue(result["ok"])
        self.assertIn(result["category"], ("fixed", "variable"))

    def test_generate_dashboard_dry_run(self):
        result = finance_generate_dashboard("2026-06")
        self.assertTrue(result["ok"])
        self.assertIn("income", result)


class PaymentsServerTestCase(unittest.TestCase):
    def test_create_payment_link_dry_run(self):
        result = payments_create_payment_link(100.0)
        self.assertTrue(result["ok"])
        self.assertIn("url", result)

    def test_create_invoice_dry_run(self):
        result = payments_create_invoice("client@example.test", 250.0)
        self.assertTrue(result["ok"])
        self.assertIn("invoice_id", result)

    def test_record_payment_dry_run(self):
        result = payments_record_payment("pi_123", 100.0)
        self.assertTrue(result["ok"])
        self.assertTrue(result["synced_with_scribe"])


class CommsServerTestCase(unittest.TestCase):
    def test_generate_copy_dry_run(self):
        result = comms_generate_copy("summer campaign", "email")
        self.assertTrue(result["ok"])
        self.assertIn("copy", result)

    def test_plan_content_calendar_dry_run(self):
        result = comms_plan_content_calendar("launch")
        self.assertTrue(result["ok"])
        self.assertIn("calendar", result)

    def test_brand_intake_dry_run(self):
        result = comms_brand_intake('{"name": "Acme"}')
        self.assertTrue(result["ok"])


class SecurityServerTestCase(unittest.TestCase):
    def test_list_keys_dry_run(self):
        result = security_list_keys()
        self.assertTrue(result["ok"])
        self.assertIn("keys", result)

    def test_rotate_key_dry_run(self):
        result = security_rotate_key("openai")
        self.assertTrue(result["ok"])
        self.assertFalse(result["rotated"])

    def test_audit_access_dry_run(self):
        result = security_audit_access("partenon-scribe")
        self.assertTrue(result["ok"])
        self.assertIn("violations", result)


class OpsServerTestCase(unittest.TestCase):
    def test_create_project_dry_run(self):
        result = ops_create_project("Website", "Acme")
        self.assertTrue(result["ok"])
        self.assertEqual(result["project_id"], "PROJ-001")

    def test_create_task_dry_run(self):
        result = ops_create_task("PROJ-001", "Design homepage")
        self.assertTrue(result["ok"])
        self.assertEqual(result["task_id"], "TASK-001")

    def test_generate_briefing_dry_run(self):
        result = ops_generate_briefing("partenon-scribe")
        self.assertTrue(result["ok"])
        self.assertIn("briefing", result)


class RelationsServerTestCase(unittest.TestCase):
    def test_register_client_dry_run(self):
        result = relations_register_client("Acme Inc", "acme@example.test")
        self.assertTrue(result["ok"])
        self.assertEqual(result["client_id"], "CLI-001")

    def test_run_followups_dry_run(self):
        result = relations_run_followups()
        self.assertTrue(result["ok"])
        self.assertIn("actions", result)

    def test_schedule_meeting_dry_run(self):
        result = relations_schedule_meeting("CLI-001", "Kickoff", "2026-07-01T10:00:00")
        self.assertTrue(result["ok"])
        self.assertEqual(result["meeting_id"], "MTG-001")


class MemoryServerTestCase(unittest.TestCase):
    def test_put_and_get_page(self):
        memory_put_page("test/page", "Test content", "test,example")
        result = memory_get_page("test/page")
        data = __import__("json").loads(result)
        self.assertEqual(data["slug"], "test/page")
        self.assertEqual(data["content"], "Test content")

    def test_search_pages(self):
        memory_put_page("test/searchable", "Searchable content", "test")
        result = memory_search("Searchable")
        data = __import__("json").loads(result)
        self.assertIsInstance(data, list)


if __name__ == "__main__":
    unittest.main()
