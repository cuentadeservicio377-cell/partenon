#!/usr/bin/env python3
"""
Partenon Herald — Presentation Builder
Generates a slide deck outline and JSON structure for a pitch or proposal.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def build_slides(topic: str, design: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return a standard slide structure."""
    brand_name = design.get("brand", {}).get("brand_name", "Your company")
    positioning = design.get("positioning", {})
    what_you_sell = positioning.get("what_you_sell", topic)
    who_you_help = positioning.get("who_you_help", "your audience")
    how_you_do_it = positioning.get("how_you_do_it", "our process")
    proof_points = design.get("messaging", {}).get("proof_points", [])
    cta = design.get("messaging", {}).get("cta_matrix", {}).get("decision", "Get started")

    slides = [
        {
            "slide": 1,
            "type": "title",
            "title": topic,
            "subtitle": f"A proposal by {brand_name}",
        },
        {
            "slide": 2,
            "type": "problem",
            "title": "The problem",
            "bullets": [
                f"{who_you_help} faces a specific, costly challenge.",
                "Existing solutions are slow, expensive, or hard to adopt.",
                "The cost of inaction grows every week.",
            ],
        },
        {
            "slide": 3,
            "type": "solution",
            "title": "The solution",
            "bullets": [
                what_you_sell,
                f"Built for {who_you_help}.",
                "Clear outcomes without unnecessary complexity.",
            ],
        },
        {
            "slide": 4,
            "type": "how_it_works",
            "title": "How it works",
            "bullets": [
                how_you_do_it,
                "Step 1: discovery and setup.",
                "Step 2: execution with weekly visibility.",
                "Step 3: measurement and iteration.",
            ],
        },
        {
            "slide": 5,
            "type": "proof",
            "title": "Proof",
            "bullets": proof_points if proof_points else ["Case studies and testimonials available on request."],
        },
        {
            "slide": 6,
            "type": "next_steps",
            "title": "Next steps",
            "bullets": [
                "Schedule a diagnostic call.",
                "Receive a tailored plan within 48 hours.",
                f"{cta}.",
            ],
        },
    ]
    return slides


def build_presentation(topic: str, design: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Build a complete presentation package."""
    design = design or load_design()
    slides = build_slides(topic, design)
    return {
        "title": topic,
        "brand": design.get("brand", {}).get("brand_name", ""),
        "slides": slides,
        "speaker_notes": "Keep each slide to one idea. Use numbers when you have them.",
    }


def save_presentation(presentation: Dict[str, Any], output_dir: Path = Path("output/copy")) -> Path:
    """Persist presentation structure to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_title = "".join(c if c.isalnum() else "_" for c in presentation["title"]).lower()
    path = output_dir / f"presentation-{safe_title}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(presentation, f, ensure_ascii=False, indent=2)
    return path


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python3 presentation_builder.py <topic>",
            "example": "python3 presentation_builder.py 'Automation for SMEs'",
        }, ensure_ascii=False, indent=2))
        return 0

    topic = sys.argv[1]
    presentation = build_presentation(topic)
    path = save_presentation(presentation)
    presentation["success"] = True
    presentation["output_path"] = str(path.resolve())
    print(json.dumps(presentation, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
