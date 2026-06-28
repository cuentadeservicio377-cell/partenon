#!/usr/bin/env python3
"""
Partenon Herald — Schedule Content
Reads a content calendar and prepares a schedule of posts with optional publish times.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional


def find_latest_calendar(folder: Path = Path("output/campaigns")) -> Optional[Path]:
    """Find the most recent content-calendar.json under the campaigns folder."""
    candidates = list(folder.rglob("content-calendar.json"))
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def schedule_posts(
    calendar: Dict[str, Any],
    start_time: str = "09:00",
    interval_hours: int = 24,
) -> Dict[str, Any]:
    """Build a schedule from a content calendar."""
    entries = calendar.get("calendar", [])
    channels = calendar.get("channels", [])
    base_date = datetime.strptime(calendar.get("start_date", datetime.now().strftime("%Y-%m-%d")), "%Y-%m-%d")
    hour, minute = map(int, start_time.split(":"))

    scheduled = []
    for idx, entry in enumerate(entries):
        publish_time = base_date + timedelta(days=idx, hours=hour - base_date.hour, minutes=minute - base_date.minute)
        for channel in channels:
            scheduled.append({
                "day": entry.get("day"),
                "date": entry.get("date"),
                "publish_at": publish_time.isoformat(),
                "channel": channel,
                "pillar": entry.get("pillar"),
                "format": entry.get("format"),
                "topic_angle": entry.get("topic_angle"),
                "status": "scheduled",
            })

    return {
        "campaign_id": calendar.get("campaign_id"),
        "topic": calendar.get("topic"),
        "schedule": scheduled,
        "total_posts": len(scheduled),
    }


def save_schedule(schedule: Dict[str, Any], output_dir: Path = Path("output/campaigns")) -> Path:
    """Persist schedule next to its source calendar or in the output root."""
    campaign_id = schedule.get("campaign_id", "unknown")
    folder = output_dir / campaign_id
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "schedule.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    return path


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(json.dumps({
            "usage": "python3 schedule_content.py [calendar-path] [start-time] [interval-hours]",
            "example": "python3 schedule_content.py output/campaigns/CAL-.../content-calendar.json 08:00 24",
        }, ensure_ascii=False, indent=2))
        return 0

    calendar_path = Path(sys.argv[1]) if len(sys.argv) > 1 else find_latest_calendar()
    if calendar_path is None or not calendar_path.exists():
        print(json.dumps({
            "success": False,
            "error": "No content calendar found. Generate one with content_calendar.py first.",
        }, ensure_ascii=False, indent=2))
        return 1

    start_time = sys.argv[2] if len(sys.argv) > 2 else "09:00"
    interval_hours = int(sys.argv[3]) if len(sys.argv) > 3 else 24

    with open(calendar_path, "r", encoding="utf-8") as f:
        calendar = json.load(f)

    schedule = schedule_posts(calendar, start_time, interval_hours)
    path = save_schedule(schedule)
    schedule["success"] = True
    schedule["output_path"] = str(path.resolve())
    print(json.dumps(schedule, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
