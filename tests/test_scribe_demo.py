"""Tests for the Scribe finance demo."""

import json
import sys
import unittest
from pathlib import Path

# Make repo root importable.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.demo_scribe import main as demo_main  # noqa: E402


class ScribeDemoTestCase(unittest.TestCase):
    def test_demo_creates_workbook_and_report(self):
        demo_main()

        workbook_path = REPO_ROOT / "data" / "sample_expenses.xlsx"
        report_path = REPO_ROOT / "data" / "sample_expenses_report.json"

        self.assertTrue(workbook_path.exists(), "Sample workbook should be created")
        self.assertTrue(report_path.exists(), "Sample report should be created")

        report = json.loads(report_path.read_text(encoding="utf-8"))
        self.assertIn("income", report)
        self.assertIn("fixed_expenses", report)
        self.assertIn("variable_expenses", report)
        self.assertIn("margin", report)
        self.assertIn("margin_pct", report)
        self.assertIn("alerts", report)

        self.assertEqual(report["income"], 4000.0)
        self.assertEqual(report["fixed_expenses"], 609.0)
        self.assertEqual(report["variable_expenses"], 1030.0)
        self.assertEqual(report["margin"], 2361.0)
        self.assertEqual(report["margin_pct"], 59.03)
        self.assertEqual(report["alerts"], [])


if __name__ == "__main__":
    unittest.main()
