#!/usr/bin/env python3
"""
Partenon Herald — Read Content Calendar
Loads the most recent content calendar or a specific calendar file.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def find_latest_calendar(folder: Path = Path("output/campaigns")) -> Optional[Path]:
    """Find the most recent content-calendar.json under the campaigns folder."""
    candidates = list(folder.rglob("content-calendar.json"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) > 1:
        calendar_path = Path(sys.argv[1])
    else:
        calendar_path = find_latest_calendar()

    if calendar_path is None or not calendar_path.exists():
        print(json.dumps({"success": False, "error": "No content calendar found."}, ensure_ascii=False, indent=2))
        return 1

    with open(calendar_path, "r", encoding="utf-8") as f:
        calendar: Dict[str, Any] = json.load(f)

    calendar["success"] = True
    calendar["source_path"] = str(calendar_path.resolve())
    print(json.dumps(calendar, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
