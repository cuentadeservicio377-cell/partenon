"""Tests for the Partenon onboarding engine."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

from partenon_core.tools.onboarding_engine import OnboardingEngine


class OnboardingEngineTestCase(unittest.TestCase):
    def test_engine_runs_without_crash(self):
        engine = OnboardingEngine()
        result = engine.run_full_onboarding()

        self.assertIsInstance(result, dict)
        self.assertIn("success", result)
        self.assertIn("steps", result)
        self.assertIn("errors", result)

    def test_engine_creates_local_data_files(self):
        engine = OnboardingEngine()
        engine.run_full_onboarding()

        for filename in [
            "clients.json",
            "projects.json",
            "tasks.json",
            "quotes.json",
            "pipeline.json",
            "checklists.json",
            "catalog.json",
            "events.json",
            "nudges.json",
            "goals.json",
        ]:
            path = REPO_ROOT / "data" / filename
            self.assertTrue(path.exists(), f"{filename} should be created")

    def test_welcome_document_created(self):
        engine = OnboardingEngine()
        engine.run_full_onboarding()

        welcome_path = REPO_ROOT / "docs" / "WELCOME.md"
        self.assertTrue(welcome_path.exists(), "Welcome document should be created")
        content = welcome_path.read_text(encoding="utf-8")
        self.assertIn("Welcome to Partenon", content)


if __name__ == "__main__":
    unittest.main()
