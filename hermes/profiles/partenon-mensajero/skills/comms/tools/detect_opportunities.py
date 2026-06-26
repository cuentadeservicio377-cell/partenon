#!/usr/bin/env python3
"""
Partenon Herald — Detect Opportunities
Reads social metrics and returns high-engagement posts and reply opportunities.
This is a thin wrapper around analyze_engagement for cron workflows.
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


def run_analysis(metrics_path: Path) -> Dict[str, Any]:
    """Call analyze_engagement.py and return its report."""
    tool = Path(__file__).with_name("analyze_engagement.py")
    result = subprocess.run(
        [sys.executable, str(tool), str(metrics_path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return {"success": False, "error": result.stderr or "analyze_engagement failed"}
    return json.loads(result.stdout)


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": True,
            "generated_at": datetime.now().isoformat(),
            "opportunities": [],
            "note": "Provide a metrics JSON file to detect real opportunities.",
        }, ensure_ascii=False, indent=2))
        return 0

    metrics_path = Path(sys.argv[1])
    report = run_analysis(metrics_path)
    opportunities = report.get("opportunities", [])
    output = {
        "success": report.get("success", True),
        "generated_at": datetime.now().isoformat(),
        "opportunities": opportunities,
        "recommendations": report.get("recommendations", []),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
