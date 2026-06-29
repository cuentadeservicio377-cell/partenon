"""Tests for the gateway guard tool."""

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL_PATH = REPO_ROOT / "hermes" / "profiles" / "partenon-scribe" / "skills" / "gateway" / "tools" / "check_guard.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location("gateway_check_guard", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def guard(monkeypatch):
    monkeypatch.setenv("GATEWAY_ALLOWED_USERS", "user-1,user-2")
    monkeypatch.setenv("TELEGRAM_ALLOWED_USERS", "telegram-1")
    module = _load_tool()
    module._RATE_LIMIT_LOG.clear()
    return module


def test_guard_denies_when_no_allow_list(monkeypatch):
    monkeypatch.delenv("GATEWAY_ALLOWED_USERS", raising=False)
    monkeypatch.delenv("TELEGRAM_ALLOWED_USERS", raising=False)
    module = _load_tool()
    result = module.check_guard("user-1", "hello")
    assert result["allowed"] is False
    assert "allow-list" in result["reason"]


def test_guard_allows_allowed_user(guard):
    result = guard.check_guard("user-1", "hello")
    assert result["allowed"] is True
    assert result["reason"] == "Message accepted."


def test_guard_allows_telegram_user(guard):
    result = guard.check_guard("telegram-1", "hello")
    assert result["allowed"] is True


def test_guard_denies_unknown_user(guard):
    result = guard.check_guard("user-99", "hello")
    assert result["allowed"] is False
    assert "not in the allow-list" in result["reason"]


def test_guard_requires_mention_in_group(guard):
    result = guard.check_guard("user-1", "do something", is_group=True, bot_username="partenon_bot")
    assert result["allowed"] is False
    assert "mention" in result["reason"]


def test_guard_allows_group_with_mention(guard):
    result = guard.check_guard("user-1", "@partenon_bot do something", is_group=True, bot_username="partenon_bot")
    assert result["allowed"] is True


def test_guard_allows_literal_botname_mention(guard):
    result = guard.check_guard("user-1", "@botname do something", is_group=True)
    assert result["allowed"] is True


def test_guard_rate_limit(guard, monkeypatch):
    monkeypatch.setenv("GATEWAY_RATE_LIMIT_PER_MINUTE", "3")
    for i in range(3):
        result = guard.check_guard("user-1", f"msg {i}")
        assert result["allowed"] is True
    result = guard.check_guard("user-1", "msg over")
    assert result["allowed"] is False
    assert "Rate limit exceeded" in result["reason"]


def test_guard_rate_limit_is_per_user(guard, monkeypatch):
    monkeypatch.setenv("GATEWAY_RATE_LIMIT_PER_MINUTE", "1")
    assert guard.check_guard("user-1", "first")["allowed"] is True
    assert guard.check_guard("user-2", "first")["allowed"] is True
    assert guard.check_guard("user-1", "second")["allowed"] is False
