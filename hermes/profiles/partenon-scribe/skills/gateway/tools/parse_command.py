"""
Gateway command parser.

Detects explicit `/profile action args...` commands (and short aliases) and
falls back to the natural-language intent router when no prefix is present.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Allow the tool to be loaded standalone from a profile directory.
try:
    from partenon_core.tools.intent_router import route_intent
except ImportError:  # pragma: no cover
    try:
        from partenon_core.tools.router import route_intent
    except ImportError:
        _repo_root = Path(__file__).resolve().parents[6]
        if str(_repo_root) not in sys.path:
            sys.path.insert(0, str(_repo_root))
        from partenon_core.tools.intent_router import route_intent


# Short aliases used in Telegram-style command prefixes.
PROFILE_ALIASES: Dict[str, str] = {
    "s": "scribe",
    "h": "herald",
    "c": "collector",
    "g": "guardian",
    "st": "strategist",
    "d": "diplomat",
    "b": "brain",
}

_PROFILE_NAMES = {
    "scribe",
    "herald",
    "collector",
    "guardian",
    "strategist",
    "diplomat",
    "brain",
}


def _resolve_profile(token: str) -> Optional[str]:
    """Return canonical profile name from a command token, or None."""
    token = token.lstrip("/").lower()
    if token in _PROFILE_NAMES:
        return token
    if token.startswith("partenon-") and token[9:] in _PROFILE_NAMES:
        return token[9:]
    return PROFILE_ALIASES.get(token)


def _split_command(message: str) -> tuple[Optional[str], Optional[str], List[str]]:
    """Split a command into profile, action and args."""
    tokens = message.strip().split()
    if not tokens:
        return None, None, []

    first = tokens[0]
    if not first.startswith("/"):
        return None, None, tokens

    profile = _resolve_profile(first)
    if profile is None:
        # Unknown prefix: treat everything as a free-form message.
        return None, None, tokens

    if len(tokens) == 1:
        return profile, None, []

    return profile, tokens[1], tokens[2:]


def parse_command(message: str) -> Dict[str, Any]:
    """
    Parse a gateway command.

    Returns a dict with keys:
        profile: canonical Partenon profile name (without prefix) or None.
        action: the requested action, or None.
        args: list of remaining arguments.
        confidence: routing confidence between 0 and 1.
        prefix_used: True when an explicit `/profile` prefix was matched.
        reply: short human-readable routing summary.
    """
    profile, action, args = _split_command(message)

    if profile is not None:
        full_profile = f"partenon-{profile}"
        action_text = f"action '{action}'" if action else "no explicit action"
        return {
            "profile": full_profile,
            "action": action,
            "args": args,
            "confidence": 1.0,
            "prefix_used": True,
            "reply": f"Routing to {full_profile} ({action_text}).",
        }

    # No explicit prefix: use the natural-language router as fallback.
    routed = route_intent(message)
    if routed:
        return {
            "profile": routed,
            "action": None,
            "args": [],
            "confidence": 0.7,
            "prefix_used": False,
            "reply": f"No prefix found; routed to {routed} by intent.",
        }

    return {
        "profile": None,
        "action": None,
        "args": [],
        "confidence": 0.0,
        "prefix_used": False,
        "reply": "No prefix matched and intent could not be determined.",
    }


if __name__ == "__main__":  # pragma: no cover
    import sys as _sys

    sample = " ".join(_sys.argv[1:]) if len(_sys.argv) > 1 else "Organize my numbers"
    print(parse_command(sample))
