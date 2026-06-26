#!/usr/bin/env python3
"""
Partenon Herald — Publish Post
Validates and records a social post for a connected channel.
Real publishing is delegated to the Social APIs MCP; this tool handles validation,
approval gating, and local record keeping.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


SUPPORTED_CHANNELS = ["linkedin", "twitter", "instagram", "facebook", "tiktok"]


def load_design(path: Path = Path(".design")) -> Dict[str, Any]:
    """Load brand design file if present."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            pass
    return {}


def can_publish(design: Dict[str, Any]) -> bool:
    """Check whether the profile is authorized to publish without approval."""
    autonomy = design.get("operations", {}).get("autonomy", {})
    return bool(autonomy.get("publish_social", False))


def validate_post(channel: str, copy: str, media: List[str]) -> List[str]:
    """Return a list of validation errors."""
    errors = []
    if channel not in SUPPORTED_CHANNELS:
        errors.append(f"Unsupported channel: {channel}. Supported: {', '.join(SUPPORTED_CHANNELS)}")
    if not copy or len(copy.strip()) < 5:
        errors.append("Post copy is too short.")
    if len(copy) > 2200:
        errors.append("Post copy exceeds 2200 characters.")
    for m in media:
        if not Path(m).exists() and not m.startswith(("http://", "https://")):
            errors.append(f"Media reference not found: {m}")
    return errors


def publish(
    channel: str,
    copy: str,
    media: Optional[List[str]] = None,
    design: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Validate and record a post."""
    design = design or load_design()
    media = media or []
    errors = validate_post(channel, copy, media)
    if errors:
        return {"success": False, "errors": errors}

    approved = can_publish(design)
    status = "published" if approved else "pending_approval"

    record = {
        "success": True,
        "post_id": f"POST-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "channel": channel,
        "copy": copy,
        "media": media,
        "status": status,
        "published_at": datetime.now().isoformat() if approved else None,
        "requires_approval": not approved,
        "note": "Sent to Social APIs MCP" if approved else "Waiting for owner approval before publishing",
    }
    return record


def save_record(record: Dict[str, Any], output_dir: Path = Path("output/copy")) -> Path:
    """Persist post record to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_channel = record.get("channel", "unknown")
    path = output_dir / f"post-{safe_channel}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return path


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 3:
        print(json.dumps({
            "usage": "python3 publish_post.py <channel> <copy> [media-paths...]",
            "example": "python3 publish_post.py linkedin 'New guide on SME automation'",
            "supported_channels": SUPPORTED_CHANNELS,
        }, ensure_ascii=False, indent=2))
        return 0

    channel = sys.argv[1].lower()
    copy = sys.argv[2]
    media = sys.argv[3:] if len(sys.argv) > 3 else []

    result = publish(channel, copy, media)
    path = save_record(result)
    result["output_path"] = str(path.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
