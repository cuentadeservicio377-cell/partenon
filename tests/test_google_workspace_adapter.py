"""Tests for the Google Workspace MCP server adapter."""

import unittest

from mcp_servers.google_workspace.server import (
    workspace_create_calendar_event,
    workspace_create_document,
    workspace_create_presentation,
    workspace_create_spreadsheet,
    workspace_read_sheet,
    workspace_send_email,
    workspace_write_to_sheets,
)


class GoogleWorkspaceAdapterTestCase(unittest.TestCase):
    def test_create_spreadsheet_dry_run(self):
        result = workspace_create_spreadsheet("Budget 2026")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["title"], "Budget 2026")

    def test_write_to_sheets_dry_run(self):
        result = workspace_write_to_sheets("sheet_123", "A1:B2", '[["a", "b"], ["c", "d"]]')
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["updated_cells"], 4)

    def test_read_sheet_dry_run(self):
        result = workspace_read_sheet("sheet_123", "A1:B2")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])
        self.assertEqual(result["values"], [])

    def test_create_document_dry_run(self):
        result = workspace_create_document("Brand brief", "Content here")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])

    def test_create_presentation_dry_run(self):
        result = workspace_create_presentation("Pitch deck")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])

    def test_create_calendar_event_dry_run(self):
        result = workspace_create_calendar_event("Kickoff", "2026-07-01T10:00:00", "2026-07-01T11:00:00")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])

    def test_send_email_dry_run(self):
        result = workspace_send_email("client@example.test", "Subject", "Body")
        self.assertTrue(result["ok"])
        self.assertTrue(result["dry_run"])


if __name__ == "__main__":
    unittest.main()
