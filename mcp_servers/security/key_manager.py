"""Guardian key audit and model recommendation utilities."""

import math
import re
from typing import Optional


def detect_key_provider(key: str) -> str:
    """Guess the provider from an API key prefix."""
    prefixes = {
        "sk_": "stripe",
        "pk_": "stripe",
        "rk_": "stripe",
        "sk-or-v1-": "openrouter",
        "sk-": "openai",
        "nvapi-": "nvidia",
        "AIza": "google",
        "xoxb-": "slack",
        "xoxp-": "slack",
    }
    for prefix, provider in prefixes.items():
        if key.startswith(prefix):
            return provider
    return "unknown"


def estimate_entropy(key: str) -> float:
    """Estimate Shannon entropy of a key string."""
    if not key:
        return 0.0
    prob = [float(key.count(c)) / len(key) for c in dict.fromkeys(list(key))]
    return -sum(p * math.log2(p) for p in prob)


def audit_key_strength(key: str) -> dict:
    """Audit an API key and return a strength report."""
    issues = []
    provider = detect_key_provider(key)
    entropy = estimate_entropy(key)

    if len(key) < 32:
        issues.append("key is shorter than 32 characters")
    if key in {"admin", "password", "123456", "secret", "test"}:
        issues.append("key is a known weak value")
    if re.search(r"(test|example|demo|sample)", key, re.IGNORECASE):
        issues.append("key contains a weak/test substring")
    if entropy < 4.0:
        issues.append("low entropy")

    score = 100
    score -= max(0, (32 - len(key))) * 2
    score -= len(issues) * 20
    score = max(0, min(100, score))

    recommendation = "ok"
    if score < 50:
        recommendation = "rotate immediately"
    elif score < 80:
        recommendation = "review and consider rotation"

    return {
        "provider": provider,
        "length": len(key),
        "entropy": round(entropy, 2),
        "score": score,
        "issues": issues,
        "recommendation": recommendation,
    }


def recommend_model(provider: str, budget_tier: str = "standard", latency: str = "normal") -> dict:
    """Recommend an AI model given provider, budget tier, and latency preference."""
    catalog = {
        "openai": {
            "cheap": {"model": "gpt-4.1-mini", "reason": "low cost, fast"},
            "standard": {"model": "gpt-4.1", "reason": "balanced capability and cost"},
            "premium": {"model": "gpt-4.1-2025-04-14", "reason": "highest reasoning quality"},
        },
        "anthropic": {
            "cheap": {"model": "claude-sonnet-4-20250514", "reason": "lower price than opus"},
            "standard": {"model": "claude-sonnet-4-20250514", "reason": "best cost/quality balance"},
            "premium": {"model": "claude-opus-4", "reason": "maximum capability"},
        },
        "google": {
            "cheap": {"model": "gemini-2.5-flash-preview-05-20", "reason": "fast and cheap"},
            "standard": {"model": "gemini-2.5-pro-preview-05-06", "reason": "strong multimodal"},
            "premium": {"model": "gemini-2.5-pro-preview-05-06", "reason": "top Google model"},
        },
        "nvidia": {
            "cheap": {"model": "meta/llama3-8b-instruct", "reason": "cheap local GPU inference"},
            "standard": {"model": "meta/llama3-70b-instruct", "reason": "strong open model"},
            "premium": {"model": "nvidia/nemotron-4-340b-instruct", "reason": "highest NVIDIA model quality"},
        },
        "openrouter": {
            "cheap": {"model": "openrouter/google/gemini-2.5-flash-preview-05-20", "reason": "low cost"},
            "standard": {"model": "openrouter/anthropic/claude-sonnet-4-20250514", "reason": "balanced"},
            "premium": {"model": "openrouter/anthropic/claude-opus-4", "reason": "maximum quality"},
        },
    }
    selected = catalog.get(provider.lower(), {}).get(
        budget_tier.lower(),
        {"model": "unknown", "reason": "no recommendation for this provider/tier"},
    )
    if latency.lower() == "low":
        selected["note"] = "prefer smaller context windows and flash/mini variants for lowest latency"
    return {"provider": provider, "budget_tier": budget_tier, "latency": latency, **selected}


def rotate_key_live(service: str) -> dict:
    """Placeholder for live key rotation. Requires explicit approval; does not rotate alone."""
    return {
        "ok": True,
        "rotated": False,
        "service": service,
        "note": "live rotation requires explicit operator approval and provider API access",
    }
