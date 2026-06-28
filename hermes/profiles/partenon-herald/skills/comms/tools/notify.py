#!/usr/bin/env python3
"""
Partenon Herald — Notify
Records a notification for the operator. In production this routes to Gmail,
Slack, or an in-app channel via the appropriate MCP server.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def notify(message: str, channel: str = "console", payload: Dict[str, Any] = None) -> Dict[str, Any]:
    """Record a notification."""
    record = {
        "success": True,
        "sent_at": datetime.now().isoformat(),
        "channel": channel,
        "message": message,
        "payload": payload or {},
    }
    return record


def save_notification(record: Dict[str, Any], output_dir: Path = Path("output/copy")) -> Path:
    """Persist notification to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"notification-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return path


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python3 notify.py <message> [channel]",
            "example": "python3 notify.py 'Morning briefing ready' console",
        }, ensure_ascii=False, indent=2))
        return 0

    message = sys.argv[1]
    channel = sys.argv[2] if len(sys.argv) > 2 else "console"

    record = notify(message, channel)
    path = save_notification(record)
    record["output_path"] = str(path.resolve())
    print(json.dumps(record, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
