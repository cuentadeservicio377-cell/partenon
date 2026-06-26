"""
Partenon Diplomat — Proposal Generator Tool
Drafts structured proposals for clients based on `.relations` data.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from crm import RelationsCRM, get_relations_crm


DEFAULT_CURRENCY = os.getenv("PARTENON_CURRENCY", "MXN")


def _format_currency(amount: float, currency: str = DEFAULT_CURRENCY) -> str:
    """Format amount with currency code."""
    return f"{currency} {amount:,.2f}"


def _build_scope_items(items: Optional[List[Dict[str, Any]]]) -> str:
    """Render scope items as a markdown list."""
    if not items:
        return "- Scope to be defined with the client."
    lines = []
    for item in items:
        name = item.get("name", "Unnamed item")
        description = item.get("description", "")
        lines.append(f"- **{name}**: {description}")
    return "\n".join(lines)


def generate_proposal(
    entity_id: str,
    title: str,
    scope_items: Optional[List[Dict[str, Any]]] = None,
    amount: float = 0,
    currency: str = DEFAULT_CURRENCY,
    duration_days: int = 30,
    notes: str = "",
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """
    Generate a proposal draft for a client.

    Args:
        entity_id: Client ID from `.relations`.
        title: Proposal title.
        scope_items: List of {"name", "description"} scope items.
        amount: Proposed amount.
        currency: Currency code.
        duration_days: Estimated delivery duration in days.
        notes: Additional terms or notes.
        crm: RelationsCRM instance.

    Returns:
        Structured proposal object and markdown text.
    """
    crm = crm or get_relations_crm()
    summary = crm.get_relationship_summary(entity_id)

    if not summary.get("success"):
        return {
            "success": False,
            "error": summary.get("error", f"Entity {entity_id} not found"),
        }

    entity = summary.get("entity", {})
    entity_name = entity.get("name", "Client")
    contact = entity.get("main_contact", {}) or {}
    contact_name = contact.get("name") or entity_name

    today = datetime.now()
    valid_until = today + timedelta(days=15)
    estimated_delivery = today + timedelta(days=duration_days)

    scope_md = _build_scope_items(scope_items)

    proposal = {
        "id": f"PROP-{entity_id}-{today.strftime('%Y%m%d')}",
        "entity_id": entity_id,
        "entity_name": entity_name,
        "title": title,
        "date": today.isoformat(),
        "valid_until": valid_until.isoformat(),
        "scope_items": scope_items or [],
        "amount": amount,
        "currency": currency,
        "duration_days": duration_days,
        "estimated_delivery": estimated_delivery.isoformat(),
        "notes": notes,
        "status": "draft",
    }

    markdown = f"""# Proposal: {title}

**To:** {contact_name} — {entity_name}  
**Date:** {today.strftime('%Y-%m-%d')}  
**Valid until:** {valid_until.strftime('%Y-%m-%d')}

## Scope

{scope_md}

## Investment

**Total:** {_format_currency(amount, currency)}

## Timeline

- **Estimated duration:** {duration_days} business days
- **Estimated delivery:** {estimated_delivery.strftime('%Y-%m-%d')}

## Terms

{notes if notes else "Standard terms apply. Payment schedule to be confirmed with The Collector."}

## Next Steps

1. Review and approve this proposal.
2. Confirm milestone dates with the Strategist.
3. The Collector will issue the formal invoice.

---
*Prepared by The Diplomat — Partenon*
"""

    proposal["markdown"] = markdown

    # Save to output directory for persistence
    output_dir = Path("output/proposals")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{proposal['id']}.md"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)
        proposal["output_file"] = str(output_file)
    except Exception as e:
        proposal["output_file_error"] = str(e)

    return {
        "success": True,
        "proposal": proposal,
        "message": f"Proposal draft generated for {entity_name}: {proposal['id']}",
    }


if __name__ == "__main__":
    print(
        generate_proposal(
            entity_id="CLI-001",
            title="Operations Consulting Package",
            scope_items=[
                {"name": "Process audit", "description": "Map current workflows and bottlenecks."},
                {"name": "Improvement plan", "description": "Deliver prioritized recommendations."},
            ],
            amount=50000,
            duration_days=45,
            notes="50% upfront, 50% on delivery. Travel expenses billed separately.",
        )
    )
