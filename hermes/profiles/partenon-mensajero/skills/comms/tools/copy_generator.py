#!/usr/bin/env python3
"""
Partenon Herald — Copy Generator Tool
Generates copy for ads, emails, posts, and landing pages. Anti-AI-slop.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


BANNED_PATTERNS = [
    "revolutionary",
    "game changer",
    "transform your life",
    "effortless",
    "100% guaranteed",
    "instant results",
    "only one on the market",
    "discover the secret",
    "act now",
    "do not miss out",
    "the best solution",
]


def load_design(path: Path = Path(".design")) -> Dict[str, Any]:
    """Load brand design file if present."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            pass
    return {}


def get_brand_context(design: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields for copy generation."""
    positioning = design.get("positioning", {})
    voice = design.get("voice", {})
    messaging = design.get("messaging", {})
    audience = design.get("audience", {})

    return {
        "brand_name": design.get("brand", {}).get("brand_name", "Your brand"),
        "what_you_sell": positioning.get("what_you_sell", ""),
        "who_you_help": positioning.get("who_you_help", ""),
        "how_you_do_it": positioning.get("how_you_do_it", ""),
        "tone": voice.get("tone", "direct"),
        "addressing": voice.get("addressing", "you informal"),
        "key_messages": messaging.get("key_messages", []),
        "claims_to_avoid": messaging.get("claims_to_avoid", []),
        "proof_points": messaging.get("proof_points", []),
        "cta_matrix": messaging.get("cta_matrix", {}),
        "primary_pain": audience.get("primary", {}).get("pain", ""),
        "primary_outcome": audience.get("primary", {}).get("outcome", ""),
    }


def sanitize_text(text: str, banned: List[str]) -> List[str]:
    """Remove or flag banned patterns from copy."""
    flagged = []
    lower_text = text.lower()
    for pattern in banned:
        if pattern in lower_text:
            flagged.append(pattern)
    return flagged


def generate_hook(brand: Dict[str, Any], topic: str, channel: str) -> str:
    """Generate a channel-aware hook."""
    pain = brand["primary_pain"] or "the problem that keeps your business from growing"
    outcome = brand["primary_outcome"] or "a clear and measurable result"
    what_you_sell = brand["what_you_sell"] or topic

    if channel in ["linkedin", "blog"]:
        return f"Most businesses deal with {pain}. Here is a more direct way to reach {outcome}."
    if channel in ["instagram", "tiktok"]:
        return f"If {pain}, this changes how you think about {what_you_sell}."
    if channel == "email":
        return f"Let's talk about {pain}. There is a way to get closer to {outcome} without complicating your day."
    return f"{pain}? There is a clearer way to solve it."


def generate_body(brand: Dict[str, Any], topic: str) -> str:
    """Generate a concise body paragraph."""
    parts = [
        f"We help {brand['who_you_help']} to {brand['primary_outcome']}." if brand["who_you_help"] and brand["primary_outcome"] else "",
        f"We do it through {brand['how_you_do_it']}." if brand["how_you_do_it"] else "",
        f"The central point: {topic}." if topic else "",
    ]
    return " ".join(p for p in parts if p)


def generate_cta(brand: Dict[str, Any], stage: str = "consideration") -> str:
    """Generate a stage-appropriate CTA."""
    cta_matrix = brand.get("cta_matrix", {})
    return cta_matrix.get(stage, "Learn more")


def generate_ad_copy(brand: Dict[str, Any], topic: str, channel: str) -> Dict[str, Any]:
    """Generate ad copy variants."""
    hook = generate_hook(brand, topic, channel)
    body = generate_body(brand, topic)
    cta = generate_cta(brand, "consideration")

    variants = [
        {"name": "Direct", "headline": hook, "body": body, "cta": cta},
        {"name": "Pain", "headline": f"Tired of {brand['primary_pain']}?", "body": body, "cta": cta},
        {"name": "Outcome", "headline": f"How to reach {brand['primary_outcome']}", "body": body, "cta": cta},
    ]

    return {
        "type": "ad",
        "channel": channel,
        "topic": topic,
        "variants": variants,
    }


def generate_email_copy(brand: Dict[str, Any], topic: str, email_type: str = "outreach") -> Dict[str, Any]:
    """Generate email copy."""
    subject = f"About {topic}"
    if email_type == "follow_up":
        subject = f"Follow-up: {topic}"
    elif email_type == "newsletter":
        subject = f"This month: {topic}"

    greeting = "Dear" if brand["addressing"] == "you formal" else "Hi"
    cta = generate_cta(brand, "decision") if email_type == "follow_up" else generate_cta(brand, "consideration")

    body_lines = [
        f"{greeting}",
        "",
        generate_hook(brand, topic, "email"),
        "",
        generate_body(brand, topic),
        "",
        f"{cta}.",
        "",
        "Regards,",
        brand["brand_name"],
    ]

    return {
        "type": "email",
        "email_type": email_type,
        "subject": subject,
        "body": "\n".join(body_lines),
    }


def generate_post_copy(brand: Dict[str, Any], topic: str, channel: str) -> Dict[str, Any]:
    """Generate social post copy."""
    hook = generate_hook(brand, topic, channel)
    body = generate_body(brand, topic)
    cta = generate_cta(brand, "awareness")

    return {
        "type": "post",
        "channel": channel,
        "topic": topic,
        "copy": f"{hook}\n\n{body}\n\n{cta}.",
    }


def generate_landing_copy(brand: Dict[str, Any], topic: str) -> Dict[str, Any]:
    """Generate landing page copy structure."""
    return {
        "type": "landing",
        "topic": topic,
        "hero": {
            "headline": f"{brand['brand_name']} helps {brand['who_you_help']} to {brand['primary_outcome']}",
            "subheadline": generate_body(brand, topic),
            "cta": generate_cta(brand, "decision"),
        },
        "problem": brand["primary_pain"],
        "solution": brand["how_you_do_it"],
        "proof": brand["proof_points"][:3],
        "faq_cta": generate_cta(brand, "consideration"),
    }


def generate_copy(
    piece_type: str,
    topic: str,
    channel: str = "linkedin",
    email_type: str = "outreach",
    design: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Main dispatcher for copy generation."""
    design = design or load_design()
    brand = get_brand_context(design)

    if piece_type == "ad":
        result = generate_ad_copy(brand, topic, channel)
    elif piece_type == "email":
        result = generate_email_copy(brand, topic, email_type)
    elif piece_type == "post":
        result = generate_post_copy(brand, topic, channel)
    elif piece_type == "landing":
        result = generate_landing_copy(brand, topic)
    else:
        return {
            "success": False,
            "error": f"Unsupported piece type: {piece_type}",
        }

    all_text = json.dumps(result, ensure_ascii=False)
    flagged = sanitize_text(all_text, BANNED_PATTERNS + brand["claims_to_avoid"])

    result["success"] = True
    result["qa"] = {
        "banned_patterns_found": flagged,
        "passed": len(flagged) == 0,
    }

    return result


def save_copy(result: Dict[str, Any], output_dir: Path = Path("output/copy")) -> Path:
    """Persist copy pack to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{result['type']}-{timestamp}.json"
    path = output_dir / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return path


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 3:
        print(json.dumps({
            "usage": "python3 copy_generator.py <type> <topic> [channel|email_type]",
            "types": ["ad", "email", "post", "landing"],
            "example": "python3 copy_generator.py ad 'payment automation' linkedin",
        }, ensure_ascii=False, indent=2))
        return 0

    piece_type = sys.argv[1]
    topic = sys.argv[2]
    channel_or_email_type = sys.argv[3] if len(sys.argv) > 3 else "linkedin"

    kwargs = {"piece_type": piece_type, "topic": topic}
    if piece_type == "email":
        kwargs["email_type"] = channel_or_email_type
    else:
        kwargs["channel"] = channel_or_email_type

    result = generate_copy(**kwargs)
    path = save_copy(result)

    result["output_path"] = str(path.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
