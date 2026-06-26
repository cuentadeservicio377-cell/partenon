#!/usr/bin/env python3
"""
Partenon Herald — SEO/GEO Optimizer
Analyzes a topic for traditional search (SEO) and generative engine optimization (GEO).
"""

import json
import sys
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


def generate_keywords(topic: str, brand: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate a small keyword map for the topic."""
    brand_name = brand.get("brand_name", "")
    what_you_sell = brand.get("what_you_sell", "")
    who_you_help = brand.get("who_you_help", "")

    primary = topic.lower()
    variants = [
        f"{primary} for {who_you_help}" if who_you_help else primary,
        f"{primary} services",
        f"{primary} guide",
        f"best {primary}",
        f"{primary} vs alternative",
    ]
    if brand_name:
        variants.append(f"{brand_name} {primary}")
    if what_you_sell:
        variants.append(f"{what_you_sell} {primary}")

    keywords = []
    for kw in variants:
        keywords.append({
            "keyword": kw,
            "intent": "informational" if "guide" in kw or "vs" in kw else "commercial",
            "priority": "high" if kw == variants[0] else "medium",
        })
    return keywords


def generate_recommendations(topic: str, brand: Dict[str, Any]) -> List[str]:
    """Return SEO content recommendations."""
    what_you_sell = brand.get("what_you_sell", "")
    who_you_help = brand.get("who_you_help", "")
    how_you_do_it = brand.get("how_you_do_it", "")

    recommendations = [
        f"Use the primary keyword '{topic}' in the title, first paragraph, and at least one H2.",
        "Add a clear meta description under 160 characters.",
        "Include internal links to related service or product pages.",
        "Add structured data (FAQ or HowTo) if the content answers steps or questions.",
    ]
    if who_you_help:
        recommendations.append(f"Address the reader directly as {who_you_help}.")
    if what_you_sell:
        recommendations.append(f"State what you sell ({what_you_sell}) in the first 100 words.")
    if how_you_do_it:
        recommendations.append(f"Explain how you do it ({how_you_do_it}) to build credibility.")
    return recommendations


def generate_geo_recommendations(topic: str, brand: Dict[str, Any]) -> List[str]:
    """Return GEO recommendations for AI-driven search."""
    what_you_sell = brand.get("what_you_sell", "")
    who_you_help = brand.get("who_you_help", "")

    recommendations = [
        "Answer the target question directly in the first two sentences.",
        "Use clear headings that match how people ask AI assistants.",
        "Include concise bullets with facts, not marketing fluff.",
        "Add an explicit 'Who this is for' and 'What you get' section.",
    ]
    if what_you_sell:
        recommendations.append(f"Mention the core offer ({what_you_sell}) in a plain statement an AI can quote.")
    if who_you_help:
        recommendations.append(f"Describe the buyer ({who_you_help}) so the model can map relevance.")
    return recommendations


def analyze(
    topic: str,
    content: Optional[str] = None,
    design: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Run SEO/GEO analysis for a topic."""
    design = design or load_design()
    brand_context = {
        "brand_name": design.get("brand", {}).get("brand_name", ""),
        "what_you_sell": design.get("positioning", {}).get("what_you_sell", ""),
        "who_you_help": design.get("positioning", {}).get("who_you_help", ""),
        "how_you_do_it": design.get("positioning", {}).get("how_you_do_it", ""),
        "tone": design.get("voice", {}).get("tone", "direct"),
    }

    result = {
        "topic": topic,
        "content_provided": bool(content),
        "keywords": generate_keywords(topic, brand_context),
        "seo_recommendations": generate_recommendations(topic, brand_context),
        "geo_recommendations": generate_geo_recommendations(topic, brand_context),
    }

    if content:
        word_count = len(content.split())
        result["content_metrics"] = {
            "word_count": word_count,
            "has_heading": "#" in content,
            "has_bullets": "\n- " in content or "\n* " in content,
            "has_cta": any(cta in content.lower() for cta in ["contact", "book", "schedule", "start", "learn more"]),
        }
    return result


def save_report(result: Dict[str, Any], output_dir: Path = Path("output/copy")) -> Path:
    """Persist the SEO/GEO report to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_topic = "".join(c if c.isalnum() else "_" for c in result["topic"]).lower()
    path = output_dir / f"seo-geo-{safe_topic}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return path


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python3 seo_geo_optimizer.py <topic> [content-file]",
            "example": "python3 seo_geo_optimizer.py 'payment automation for SMEs'",
        }, ensure_ascii=False, indent=2))
        return 0

    topic = sys.argv[1]
    content = None
    if len(sys.argv) > 2:
        content_path = Path(sys.argv[2])
        if content_path.exists():
            content = content_path.read_text(encoding="utf-8")

    result = analyze(topic, content)
    path = save_report(result)
    result["output_path"] = str(path.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
