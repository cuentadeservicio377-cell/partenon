"""MCP orchestration tools for the Partenon Brain."""

import json
from typing import Any

from .gbrain_client import GBrainClient


def _client() -> GBrainClient:
    return GBrainClient()


def share_context(
    context_type: str,
    data: dict[str, Any],
    access: list[str],
    ttl: str = "30d",
) -> dict[str, Any]:
    """Publish shared context that other heroes can request."""
    client = _client()
    payload = {
        "type": context_type,
        "access": access,
        "ttl": ttl,
        "data": data,
    }
    slug = f"context/{context_type}"
    result = client.put_page(
        slug,
        json.dumps(payload, ensure_ascii=False),
        tags=["context", context_type, *access],
    )
    return {"ok": True, "slug": slug, "gbrain": result}


def find_patterns(pattern: str, sources: list[str]) -> dict[str, Any]:
    """Search G-Brain for a pattern across named sources."""
    client = _client()
    matches = []
    for source in sources:
        response = client.search(f"{pattern} {source}", limit=10)
        matches.append({"source": source, "response": response})
    return {"ok": True, "pattern": pattern, "sources": sources, "matches": matches}


def orchestrate_agents(agents: list[str], task: str) -> dict[str, Any]:
    """Register an orchestration plan for a set of agents."""
    client = _client()
    slug = f"orchestration/{task.replace(' ', '_').lower()}"
    payload = {"agents": agents, "task": task, "status": "planned"}
    result = client.put_page(
        slug,
        json.dumps(payload, ensure_ascii=False),
        tags=["orchestration", *agents],
    )
    return {"ok": True, "slug": slug, "agents": agents, "gbrain": result}


def register_agent(agent: str, config: dict[str, Any]) -> dict[str, Any]:
    """Register or update an agent configuration in G-Brain."""
    client = _client()
    slug = f"agents/{agent}"
    result = client.put_page(
        slug,
        json.dumps(config, ensure_ascii=False),
        tags=["agent", agent],
    )
    return {"ok": True, "slug": slug, "agent": agent, "gbrain": result}


def generate_insight(
    pattern: str,
    sources: list[str],
    output: str = "optimization_report",
) -> dict[str, Any]:
    """Generate a strategic insight from cross-agent patterns."""
    matches = find_patterns(pattern, sources)
    insight = {
        "pattern": pattern,
        "sources": sources,
        "output": output,
        "summary": f"Cross-agent analysis for '{pattern}' completed.",
        "recommendations": ["Review matching pages in G-Brain."],
    }
    return {"ok": True, "insight": insight, "matches": matches["matches"]}
