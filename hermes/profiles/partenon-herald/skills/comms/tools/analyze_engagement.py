#!/usr/bin/env python3
"""
Partenon Herald — Analyze Engagement
Reads social metrics and produces an engagement report with opportunities and replies.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


def load_metrics(path: Path) -> Dict[str, Any]:
    """Load metrics from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_summary(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Compute aggregate engagement metrics."""
    posts = metrics.get("posts", [])
    if not posts:
        return {"posts_analyzed": 0, "engagement_rate": 0.0, "top_post": None}

    total_engagement = sum(p.get("likes", 0) + p.get("comments", 0) + p.get("shares", 0) for p in posts)
    total_impressions = sum(p.get("impressions", 1) for p in posts)
    engagement_rate = round(total_engagement / total_impressions * 100, 2) if total_impressions else 0.0
    top_post = max(posts, key=lambda p: p.get("likes", 0) + p.get("comments", 0) + p.get("shares", 0))

    return {
        "posts_analyzed": len(posts),
        "total_engagement": total_engagement,
        "total_impressions": total_impressions,
        "engagement_rate": engagement_rate,
        "top_post": {
            "id": top_post.get("id"),
            "channel": top_post.get("channel"),
            "copy": top_post.get("copy", "")[:120],
            "engagement": top_post.get("likes", 0) + top_post.get("comments", 0) + top_post.get("shares", 0),
        },
    }


def find_opportunities(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify high-engagement posts and unanswered comments."""
    opportunities = []
    for post in metrics.get("posts", []):
        comments = post.get("comments", 0)
        if comments > 0 and not post.get("replies", 0):
            opportunities.append({
                "type": "unanswered_comments",
                "post_id": post.get("id"),
                "channel": post.get("channel"),
                "comments": comments,
                "suggested_action": "Reply to comments within 24 hours",
            })
        if post.get("shares", 0) > 5:
            opportunities.append({
                "type": "high_shares",
                "post_id": post.get("id"),
                "channel": post.get("channel"),
                "shares": post.get("shares"),
                "suggested_action": "Repurpose this post into a carousel, email, or blog",
            })
    return opportunities


def analyze(metrics_path: Path) -> Dict[str, Any]:
    """Run engagement analysis."""
    metrics = load_metrics(metrics_path)
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": compute_summary(metrics),
        "opportunities": find_opportunities(metrics),
        "recommendations": [
            "Post at the times when the top-performing content was published.",
            "Reply to all comments within one day to boost reach.",
            "Repurpose the top post into at least two additional formats.",
        ],
    }
    return report


def save_report(report: Dict[str, Any], output_dir: Path = Path("output/copy")) -> Path:
    """Persist engagement report to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"engagement-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return path


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python3 analyze_engagement.py <metrics.json>",
            "example": "python3 analyze_engagement.py output/copy/metrics.json",
            "schema": {
                "posts": [
                    {"id": "string", "channel": "string", "likes": 0, "comments": 0, "shares": 0, "impressions": 0, "replies": 0, "copy": "string"},
                ],
            },
        }, ensure_ascii=False, indent=2))
        return 0

    metrics_path = Path(sys.argv[1])
    if not metrics_path.exists():
        print(json.dumps({"success": False, "error": f"File not found: {metrics_path}"}, ensure_ascii=False, indent=2))
        return 1

    report = analyze(metrics_path)
    path = save_report(report)
    report["success"] = True
    report["output_path"] = str(path.resolve())
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
