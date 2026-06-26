#!/usr/bin/env python3
"""
Partenon Herald — Read Brand Config
Loads the .design file and returns the brand voice, audience, and messaging context.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict

import yaml


def load_design(path: Path = Path(".design")) -> Dict[str, Any]:
    """Load brand design file if present."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            pass
    return {}


def main() -> int:
    """CLI entry point."""
    design_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".design")
    design = load_design(design_path)

    context = {
        "success": bool(design),
        "brand_name": design.get("brand", {}).get("brand_name", ""),
        "what_you_sell": design.get("positioning", {}).get("what_you_sell", ""),
        "who_you_help": design.get("positioning", {}).get("who_you_help", ""),
        "how_you_do_it": design.get("positioning", {}).get("how_you_do_it", ""),
        "tone": design.get("voice", {}).get("tone", ""),
        "addressing": design.get("voice", {}).get("addressing", ""),
        "channels": design.get("channels", []),
        "key_messages": design.get("messaging", {}).get("key_messages", []),
        "claims_to_avoid": design.get("messaging", {}).get("claims_to_avoid", []),
    }
    print(json.dumps(context, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
