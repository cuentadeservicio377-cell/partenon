"""Tests for the gateway command parser."""

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL_PATH = REPO_ROOT / "hermes" / "profiles" / "partenon-scribe" / "skills" / "gateway" / "tools" / "parse_command.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location("gateway_parse_command", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def parser():
    return _load_tool()


def test_parse_command_explicit_profile(parser):
    result = parser.parse_command("/scribe review last month expenses")
    assert result["profile"] == "partenon-scribe"
    assert result["action"] == "review"
    assert result["args"] == ["last", "month", "expenses"]
    assert result["confidence"] == 1.0
    assert result["prefix_used"] is True


def test_parse_command_alias_scribe(parser):
    result = parser.parse_command("/s classify expenses")
    assert result["profile"] == "partenon-scribe"
    assert result["action"] == "classify"
    assert result["args"] == ["expenses"]
    assert result["prefix_used"] is True


def test_parse_command_full_profile_name(parser):
    result = parser.parse_command("/partenon-herald create campaign")
    assert result["profile"] == "partenon-herald"
    assert result["action"] == "create"
    assert result["args"] == ["campaign"]


def test_parse_command_all_aliases(parser):
    expected = {
        "/h": "partenon-herald",
        "/c": "partenon-collector",
        "/g": "partenon-guardian",
        "/st": "partenon-strategist",
        "/d": "partenon-diplomat",
        "/b": "partenon-brain",
    }
    for command, profile in expected.items():
        result = parser.parse_command(f"{command} do something")
        assert result["profile"] == profile, command


def test_parse_command_no_prefix_fallback(parser):
    result = parser.parse_command("Organize my numbers")
    assert result["profile"] == "partenon-scribe"
    assert result["prefix_used"] is False
    assert result["confidence"] == 0.7


def test_parse_command_unknown_prefix_uses_fallback(parser):
    result = parser.parse_command("/unknown send invoice")
    assert result["profile"] == "partenon-collector"
    assert result["prefix_used"] is False


def test_parse_command_unroutable_message(parser):
    result = parser.parse_command("asdfghjkl")
    assert result["profile"] is None
    assert result["confidence"] == 0.0
