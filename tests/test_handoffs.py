"""Tests for Partenon hero collaboration handoffs via workflow engine."""

import json
import tempfile
import unittest
from pathlib import Path

from partenon_core.tools.workflow_engine import WorkflowEngine


class HandoffWorkflowTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.engine = WorkflowEngine(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def _nudges_for(self, target: str):
        nudges_path = Path(self.tmpdir.name) / "nudges.json"
        if not nudges_path.exists():
            return []
        data = json.loads(nudges_path.read_text(encoding="utf-8"))
        return [n for n in data.get("nudges", []) if n.get("target_profile") == target]

    def test_payment_confirmed_notifies_scribe(self):
        event = self.engine.emit_event(
            type="payment_confirmed",
            source="partenon-collector",
            entity_id="INV-001",
            entity_type="invoice",
            data={"amount": 500.0},
        )
        self.assertIn("wf_handoff_payment_confirmed.notify_scribe_of_payment", event["actions_executed"])
        self.assertTrue(self._nudges_for("scribe"))

    def test_campaign_budget_requested_notifies_scribe(self):
        event = self.engine.emit_event(
            type="campaign_budget_requested",
            source="partenon-herald",
            entity_id="CMP-001",
            entity_type="campaign",
            data={"requested_budget": 2000.0},
        )
        self.assertIn("wf_handoff_budget_requested.notify_scribe_of_budget_request", event["actions_executed"])
        self.assertTrue(self._nudges_for("scribe"))

    def test_agreement_reached_creates_project_and_notifies_strategist(self):
        event = self.engine.emit_event(
            type="agreement_reached",
            source="partenon-diplomat",
            entity_id="CLI-001",
            entity_type="client",
            data={"client_name": "Acme Inc", "project_name": "Redesign", "amount": 10000},
        )
        self.assertIn("wf_handoff_agreement_reached.create_operations_project", event["actions_executed"])
        self.assertIn("wf_handoff_agreement_reached.notify_strategist_of_deal", event["actions_executed"])
        self.assertTrue(self._nudges_for("strategist"))
        projects = json.loads((Path(self.tmpdir.name) / "projects.json").read_text(encoding="utf-8"))
        self.assertEqual(len(projects["projects"]), 1)

    def test_milestone_due_notifies_diplomat(self):
        event = self.engine.emit_event(
            type="milestone_due_soon",
            source="partenon-strategist",
            entity_id="PROJ-001",
            entity_type="project",
            data={"milestone": "Kickoff"},
        )
        self.assertIn("wf_handoff_milestone_due.notify_diplomat_of_milestone", event["actions_executed"])
        self.assertTrue(self._nudges_for("diplomat"))

    def test_key_rotation_notifies_all_profiles(self):
        event = self.engine.emit_event(
            type="key_rotation_required",
            source="partenon-guardian",
            entity_id="KEY-OPENAI",
            entity_type="api_key",
            data={"service": "openai"},
        )
        self.assertIn("wf_handoff_key_rotation.notify_profiles_of_key_rotation", event["actions_executed"])
        self.assertTrue(self._nudges_for("all"))

    def test_learning_recorded_notifies_target_hero(self):
        event = self.engine.emit_event(
            type="learning_recorded",
            source="partenon-brain",
            entity_id="LEARN-001",
            entity_type="learning",
            data={"target_profile": "scribe"},
        )
        self.assertIn("wf_handoff_learning_recorded.notify_relevant_hero_of_learning", event["actions_executed"])
        self.assertTrue(self._nudges_for("scribe"))


class CoreWorkflowTestCase(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.engine = WorkflowEngine(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_client_contracted_workflow_runs_all_actions(self):
        event = self.engine.emit_event(
            type="client_contracted",
            source="partenon-diplomat",
            entity_id="CLI-001",
            entity_type="client",
            data={"client_id": "CLI-001", "client_name": "Acme", "project_name": "Site"},
        )
        expected = {
            "wf_contracted_to_project.create_operations_project",
            "wf_contracted_to_project.create_initiative_goal",
            "wf_contracted_to_project.generate_checklist",
            "wf_contracted_to_project.notify_user",
        }
        self.assertTrue(expected.issubset(set(event["actions_executed"])))


if __name__ == "__main__":
    unittest.main()
