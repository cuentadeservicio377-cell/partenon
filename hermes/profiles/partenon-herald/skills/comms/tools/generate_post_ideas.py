#!/usr/bin/env python3
"""
Partenon Herald — Generate Post Ideas
Suggests social post ideas aligned with the brand .design file and content pillars.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


CONTENT_PILLARS = {
    "educational": "Teach something useful",
    "behind_the_scenes": "Show the real process",
    "social_proof": "Results, testimonials, credibility",
    "engagement": "Start conversations",
    "promotional": "Direct promotion (use sparingly)",
}


def load_design(path: Path = Path(".design")) -> Dict[str, Any]:
    """Load brand design file if present."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            pass
    return {}


def generate_ideas(design: Dict[str, Any], count: int = 5) -> List[Dict[str, Any]]:
    """Generate post ideas from brand context."""
    what_you_sell = design.get("positioning", {}).get("what_you_sell", "your offer")
    who_you_help = design.get("positioning", {}).get("who_you_help", "your audience")
    how_you_do_it = design.get("positioning", {}).get("how_you_do_it", "your process")
    pillars = list(CONTENT_PILLARS.keys())

    templates = [
        {"pillar": "educational", "prompt": f"Explain one thing {who_you_help} gets wrong about {what_you_sell} and how to fix it."},
        {"pillar": "behind_the_scenes", "prompt": f"Show a step from {how_you_do_it} without filters."},
        {"pillar": "social_proof", "prompt": f"Share a result or testimonial related to {what_you_sell}."},
        {"pillar": "engagement", "prompt": f"Ask {who_you_help} about their biggest challenge with {what_you_sell}."},
        {"pillar": "promotional", "prompt": f"Highlight the main benefit of {what_you_sell} for {who_you_help}."},
    ]

    ideas = []
    for i in range(count):
        template = templates[i % len(templates)]
        ideas.append({
            "id": f"IDEA-{datetime.now().strftime('%Y%m%d')}-{i+1:03d}",
            "pillar": template["pillar"],
            "pillar_description": CONTENT_PILLARS[template["pillar"]],
            "prompt": template["prompt"],
            "suggested_channels": design.get("channels", ["linkedin", "instagram"])[:2],
        })
    return ideas


def main() -> int:
    """CLI entry point."""
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    design = load_design()
    ideas = generate_ideas(design, count)

    result = {
        "success": True,
        "generated_at": datetime.now().isoformat(),
        "count": len(ideas),
        "ideas": ideas,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
