"""Tests for the gateway attachment router."""

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL_PATH = REPO_ROOT / "hermes" / "profiles" / "partenon-scribe" / "skills" / "gateway" / "tools" / "route_attachment.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location("gateway_route_attachment", TOOL_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def router():
    return _load_tool()


def test_spreadsheet_routes_to_scribe(router):
    result = router.route_attachment("report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    assert result["profile"] == "partenon-scribe"
    assert result["action"] == "process_attachment"
    assert result["dry_run"] is True


def test_csv_routes_to_scribe(router):
    result = router.route_attachment("transactions.csv", "text/csv")
    assert result["profile"] == "partenon-scribe"


def test_ods_routes_to_scribe(router):
    result = router.route_attachment("budget.ods", "application/vnd.oasis.opendocument.spreadsheet")
    assert result["profile"] == "partenon-scribe"


def test_image_routes_to_herald(router):
    result = router.route_attachment("banner.png", "image/png")
    assert result["profile"] == "partenon-herald"


@pytest.mark.parametrize("mime", ["image/jpeg", "image/webp", "image/gif"])
def test_image_mime_variants_routes_to_herald(router, mime):
    result = router.route_attachment(f"file.{mime.split('/')[-1]}", mime)
    assert result["profile"] == "partenon-herald"


def test_contract_pdf_routes_to_diplomat(router):
    result = router.route_attachment("Acme_contract_2026.pdf", "application/pdf")
    assert result["profile"] == "partenon-diplomat"


def test_proposal_pdf_routes_to_diplomat(router):
    result = router.route_attachment("Web_design_proposal.pdf", "application/pdf")
    assert result["profile"] == "partenon-diplomat"


def test_invoice_pdf_routes_to_diplomat(router):
    result = router.route_attachment("invoice_001.pdf", "application/pdf")
    assert result["profile"] == "partenon-diplomat"


def test_generic_pdf_routes_to_brain(router):
    result = router.route_attachment("notes.pdf", "application/pdf")
    assert result["profile"] == "partenon-brain"


def test_text_routes_to_brain(router):
    result = router.route_attachment("README.md", "text/markdown")
    assert result["profile"] == "partenon-brain"


def test_json_routes_to_brain(router):
    result = router.route_attachment("clients.json", "application/json")
    assert result["profile"] == "partenon-brain"


def test_unknown_type_routes_to_brain(router):
    result = router.route_attachment("archive.zip", "application/zip")
    assert result["profile"] == "partenon-brain"
