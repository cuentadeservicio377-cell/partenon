"""Tests for the Slack notification adapter."""

import unittest

from mcp_servers.notifications.server import slack_notify_task_overdue, slack_send_message
from mcp_servers.notifications.slack import send_message


class SlackAdapterTestCase(unittest.TestCase):
    def test_send_message_dry_run(self):
        result = send_message("#general", "Hello")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["channel"], "#general")

    def test_slack_send_message_tool(self):
        result = slack_send_message("#alerts", "System alert")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])

    def test_slack_notify_task_overdue_tool(self):
        result = slack_notify_task_overdue("TASK-001", "Fix billing", "2026-06-25")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])
        self.assertIn("TASK-001", result["message"])


if __name__ == "__main__":
    unittest.main()
