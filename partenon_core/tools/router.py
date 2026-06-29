"""
Partenon — Intent Router

Thin wrapper that exposes the reusable IntentRouter and provides a CLI entry point.
"""

import sys
from pathlib import Path

# Support running this file directly as a script.
if __name__ == "__main__" and __package__ is None:
    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from partenon_core.tools.intent_router import get_router, route_intent
else:
    from partenon_core.tools.intent_router import get_router, route_intent


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for the intent router."""
    args = argv if argv is not None else sys.argv[1:]
    if args:
        message = " ".join(args)
        print(route_intent(message))
        return 0

    samples = [
        "Organize my numbers",
        "Create a campaign for next week",
        "Generate a payment link",
        "Rotate my OpenAI API key",
        "What do I have this week?",
        "Follow up with client Acme Inc",
        "What did we decide last month?",
    ]
    router = get_router()
    for s in samples:
        print(f"{s!r:45} -> {router.route(s)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
