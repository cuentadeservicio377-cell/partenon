#!/usr/bin/env python3
"""
Partenon Herald — Read Social Metrics
Reads a metrics snapshot for social channels. If no file is provided, returns an empty template.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict


def empty_metrics() -> Dict[str, Any]:
    """Return an empty metrics template."""
    return {
        "success": True,
        "channels": ["linkedin", "twitter", "instagram"],
        "posts": [],
        "note": "Provide a metrics JSON file as the first argument to load real data.",
    }


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(json.dumps(empty_metrics(), ensure_ascii=False, indent=2))
        return 0

    metrics_path = Path(sys.argv[1])
    if not metrics_path.exists():
        print(json.dumps({"success": False, "error": f"File not found: {metrics_path}"}, ensure_ascii=False, indent=2))
        return 1

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics: Dict[str, Any] = json.load(f)

    metrics["success"] = True
    print(json.dumps(metrics, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
