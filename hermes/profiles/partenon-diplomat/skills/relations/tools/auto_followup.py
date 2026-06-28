"""
Partenon Diplomat — Auto Follow-up Tool
Runs the daily follow-up report and returns recommended actions for clients
and vendors. This is the MCP-facing entry point for automated follow-ups.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from crm import RelationsCRM, get_relations_crm
from followups import get_pending_followups, run_daily_followups


def auto_followup(
    alert_days: Optional[List[int]] = None,
    channels: Optional[List[str]] = None,
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """
    Run automated follow-ups and return a structured report.

    Args:
        alert_days: Day thresholds for urgency scoring (default [1, 3, 7]).
        channels: Suggested channels for actions (default ["gmail", "google_workspace"]).
        crm: RelationsCRM instance.

    Returns:
        Follow-up report with total count and recommended actions.
    """
    return run_daily_followups(alert_days=alert_days, channels=channels, crm=crm)


def auto_followup_for_entity(
    entity_id: str,
    alert_days: Optional[List[int]] = None,
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """Run follow-up detection filtered to a single entity."""
    crm = crm or get_relations_crm()
    followups = get_pending_followups(crm=crm, alert_days=alert_days)
    filtered = [f for f in followups if f.get("entity_id", "").lower() == entity_id.lower()]
    return {
        "success": True,
        "entity_id": entity_id,
        "total": len(filtered),
        "followups": filtered,
    }


if __name__ == "__main__":
    print(auto_followup())
