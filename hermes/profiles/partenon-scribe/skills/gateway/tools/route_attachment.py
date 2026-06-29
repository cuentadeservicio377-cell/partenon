"""
Gateway attachment router.

Routes incoming files to the Partenon hero best suited to process them.
"""

import os
from typing import Any, Dict


def _mime_category(mime_type: str) -> str:
    """Normalize a MIME type into a broad category."""
    mime_lower = (mime_type or "").lower().strip()
    if mime_lower in {"application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "text/csv", "application/vnd.oasis.opendocument.spreadsheet"}:
        return "spreadsheet"
    if mime_lower.startswith("image/"):
        return "image"
    if mime_lower == "application/pdf":
        return "pdf"
    if mime_lower in {"text/plain", "text/markdown", "application/json"}:
        return "text"
    return "unknown"


def _looks_like_contract(filename: str) -> bool:
    """Detect contract/proposal/invoice hints in a filename."""
    lowered = os.path.basename(filename).lower()
    return any(hint in lowered for hint in ("contract", "proposal", "invoice"))


def route_attachment(file_name: str, mime_type: str, context: str = "") -> Dict[str, Any]:
    """
    Route an attachment to the appropriate Partenon profile.

    Returns a dict with keys:
        profile: target Partenon profile name.
        action: always "process_attachment".
        summary: human-readable routing explanation.
        dry_run: True to keep the gateway non-destructive.
    """
    category = _mime_category(mime_type)

    if category == "spreadsheet":
        profile = "partenon-scribe"
        summary = f"Spreadsheet '{file_name}' routed to the Scribe for finance/records processing."
    elif category == "image":
        profile = "partenon-herald"
        summary = f"Image '{file_name}' routed to the Herald for brand/comms use."
    elif category == "pdf":
        if _looks_like_contract(file_name):
            profile = "partenon-diplomat"
            summary = f"PDF '{file_name}' looks like a contract/proposal/invoice; routed to the Diplomat."
        else:
            profile = "partenon-brain"
            summary = f"PDF '{file_name}' routed to the Brain for general indexing."
    elif category == "text":
        profile = "partenon-brain"
        summary = f"Text document '{file_name}' routed to the Brain for context/memory indexing."
    else:
        # Unknown type: send to Brain as a safe default.
        profile = "partenon-brain"
        summary = f"Attachment '{file_name}' (type '{mime_type}') routed to the Brain for triage."

    return {
        "profile": profile,
        "action": "process_attachment",
        "summary": summary,
        "dry_run": True,
    }


if __name__ == "__main__":  # pragma: no cover
    import sys

    if len(sys.argv) >= 3:
        print(route_attachment(sys.argv[1], sys.argv[2], " ".join(sys.argv[3:])))
    else:
        print(route_attachment("report.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))
