"""
Gateway guard tool.

Enforces allow-lists, group-chat mention requirements, and per-user rate limits
for inbound messages.
"""

import os
import time
from typing import Any, Dict, List, Set

# In-memory per-user call log for rate limiting.
# Keys are user IDs; values are lists of Unix timestamps.
_RATE_LIMIT_LOG: Dict[str, List[float]] = {}


def _parse_allowed_users() -> Set[str]:
    """Read GATEWAY_ALLOWED_USERS and TELEGRAM_ALLOWED_USERS from the environment."""
    raw = ""
    for key in ("GATEWAY_ALLOWED_USERS", "TELEGRAM_ALLOWED_USERS"):
        value = os.getenv(key, "")
        if value:
            raw = f"{raw},{value}" if raw else value
    return {u.strip() for u in raw.split(",") if u.strip()}


def _is_allowed_user(user_id: str) -> bool:
    """Check whether the user ID appears in any allow-list."""
    allowed = _parse_allowed_users()
    if not allowed:
        return False
    return user_id in allowed


def _has_group_mention(message: str, bot_username: str) -> bool:
    """Check that the message mentions the bot in a group context."""
    lowered = (message or "").lower()
    checks = ["@botname"]
    if bot_username:
        checks.append(f"@{bot_username.lower()}")
    return any(mention in lowered for mention in checks)


def _rate_limit(user_id: str, max_calls_per_minute: int) -> bool:
    """Return True if the call is within the per-user rate limit."""
    now = time.time()
    window_start = now - 60.0
    log = _RATE_LIMIT_LOG.get(user_id, [])
    log = [ts for ts in log if ts >= window_start]
    if len(log) >= max_calls_per_minute:
        return False
    log.append(now)
    _RATE_LIMIT_LOG[user_id] = log
    return True


def check_guard(
    user_id: str,
    message: str,
    is_group: bool = False,
    bot_username: str = "",
) -> Dict[str, Any]:
    """
    Validate whether an inbound message may be processed.

    Returns a dict with keys:
        allowed: True or False.
        reason: short explanation.
    """
    allowed_env = {
        u.strip()
        for key in ("GATEWAY_ALLOWED_USERS", "TELEGRAM_ALLOWED_USERS")
        for u in os.getenv(key, "").split(",")
        if u.strip()
    }

    if not allowed_env:
        return {
            "allowed": False,
            "reason": "No allow-list configured (GATEWAY_ALLOWED_USERS or TELEGRAM_ALLOWED_USERS).",
        }

    if user_id not in allowed_env:
        return {
            "allowed": False,
            "reason": f"User '{user_id}' is not in the allow-list.",
        }

    if is_group and not _has_group_mention(message, bot_username):
        return {
            "allowed": False,
            "reason": "Group messages must mention the bot (@botname or @<bot_username>).",
        }

    raw_limit = os.getenv("GATEWAY_RATE_LIMIT_PER_MINUTE", "30")
    try:
        max_calls = int(raw_limit)
    except ValueError:
        max_calls = 30

    if not _rate_limit(user_id, max_calls):
        return {
            "allowed": False,
            "reason": f"Rate limit exceeded ({max_calls} calls per minute).",
        }

    return {
        "allowed": True,
        "reason": "Message accepted.",
    }


if __name__ == "__main__":  # pragma: no cover
    import sys

    uid = sys.argv[1] if len(sys.argv) > 1 else "user-1"
    msg = sys.argv[2] if len(sys.argv) > 2 else "hello"
    print(check_guard(uid, msg))
