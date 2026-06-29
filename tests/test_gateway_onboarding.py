"""Tests for the gateway progressive onboarding tool."""

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL_PATH = REPO_ROOT / "hermes" / "profiles" / "partenon-scribe" / "skills" / "gateway" / "tools" / "onboarding_reply.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location("gateway_onboarding_reply", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def onboarding(temp_data_dir):
    return _load_tool()


def test_onboarding_welcome_asks_company_name(onboarding):
    result = onboarding.onboarding_reply("user-a", "")
    assert result["step"] == "company_name"
    assert result["done"] is False
    assert "company name" in result["reply"]


def test_onboarding_collects_answers_and_reaches_confirm(onboarding):
    onboarding.onboarding_reply("user-b", "")
    assert onboarding.onboarding_reply("user-b", "Aurora Coffee")["step"] == "industry"
    assert onboarding.onboarding_reply("user-b", "food")["step"] == "team_size"
    assert onboarding.onboarding_reply("user-b", "2-5")["step"] == "main_pain"
    confirm = onboarding.onboarding_reply("user-b", "keeping track of finances")
    assert confirm["step"] == "confirm"
    assert "Aurora Coffee" in confirm["reply"]
    assert "food" in confirm["reply"]


def test_onboarding_confirm_creates_workspace(onboarding):
    user_id = "user-c"
    onboarding.onboarding_reply(user_id, "")
    onboarding.onboarding_reply(user_id, "Aurora Coffee")
    onboarding.onboarding_reply(user_id, "food")
    onboarding.onboarding_reply(user_id, "2-5")
    onboarding.onboarding_reply(user_id, "keeping track of finances")
    result = onboarding.onboarding_reply(user_id, "yes")
    assert result["done"] is True
    assert result["step"] == "done"
    assert "summary" in result
    summary = result["summary"]
    assert summary["success"] is True
    assert summary["company"] == "Aurora Coffee"
    assert summary["industry"] == "food"
    assert summary["missions_generated"] > 0
    assert summary["profile_files"]
    workspace = Path(summary["workspace"])
    assert workspace.exists()
    assert (workspace / "data" / "clients.json").exists()


def test_onboarding_done_is_idempotent(onboarding):
    user_id = "user-d"
    onboarding.onboarding_reply(user_id, "")
    onboarding.onboarding_reply(user_id, "Aurora Coffee")
    onboarding.onboarding_reply(user_id, "food")
    onboarding.onboarding_reply(user_id, "2-5")
    onboarding.onboarding_reply(user_id, "keeping track of finances")
    onboarding.onboarding_reply(user_id, "yes")
    result = onboarding.onboarding_reply(user_id, "hello again")
    assert result["done"] is True
    assert result["step"] == "done"


def test_onboarding_state_persists_between_calls(onboarding):
    user_id = "user-e"
    onboarding.onboarding_reply(user_id, "")
    onboarding.onboarding_reply(user_id, "Stellar Legal")
    fresh = _load_tool()
    result = fresh.onboarding_reply(user_id, "legal")
    assert result["step"] == "team_size"
