"""
Partenon Guardian — GPU Allocator

Helpers for allocating NVIDIA GPU resources for model inference,
validating API key presence, and returning a safe GPU configuration.

Python 3.12 compatible.
"""

import os
from typing import Any, Dict


_DEFAULT_NIM_ENDPOINT = "https://integrate.api.nvidia.com/v1"
_DEFAULT_MODELS = [
    "nvidia/nemotron-4-340b-instruct",
    "nvidia/llama-3.1-nemotron-70b-instruct",
]
_MAX_GPUS_PER_REQUEST = 8


def allocate_gpu(
    profile: str,
    model_name: str,
    requested_gpus: int = 1,
    region: str = "us-central",
) -> Dict[str, Any]:
    """
    Allocate NVIDIA GPU resources for a Partenon profile.

    Args:
        profile: name of the hero profile requesting GPU resources.
        model_name: NVIDIA model identifier.
        requested_gpus: number of GPUs requested (1-8).
        region: target compute region.

    Returns:
        Dict with allocation status, configuration, and usage limits.
    """
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        return {
            "profile": profile,
            "model": model_name,
            "status": "denied",
            "reason": "NVIDIA_API_KEY is not configured.",
        }

    if requested_gpus < 1 or requested_gpus > _MAX_GPUS_PER_REQUEST:
        return {
            "profile": profile,
            "model": model_name,
            "status": "denied",
            "reason": f"requested_gpus must be between 1 and {_MAX_GPUS_PER_REQUEST}.",
        }

    # In a real deployment, this would call the NVIDIA API to reserve quota.
    # Here we return a validated, deterministic configuration object.
    endpoint = os.environ.get("NVIDIA_NIM_ENDPOINT", _DEFAULT_NIM_ENDPOINT)
    allocated = requested_gpus
    quota_remaining = max(0, _MAX_GPUS_PER_REQUEST - allocated)

    return {
        "profile": profile,
        "model": model_name,
        "allocated_gpus": allocated,
        "region": region,
        "endpoint": endpoint,
        "status": "allocated",
        "rate_limits": {
            "requests_per_minute": int(os.environ.get("NVIDIA_RATE_LIMIT_RPM", "60")),
            "tokens_per_day": int(os.environ.get("NVIDIA_RATE_LIMIT_TPD", "1000000")),
        },
        "estimated_cost_per_hour": round(allocated * 0.75, 2),
        "quota_remaining": quota_remaining,
        "note": "GPU allocation is simulated. Replace with NVIDIA API call for production reservations.",
    }
