"""
Partenon — Intent Router
Routes user messages to the appropriate hero profile.
"""

import re
from typing import Optional, Dict, Any


class IntentRouter:
    """Routes natural language intents to Partenon hero profiles."""

    INTENT_PATTERNS = {
        "partenon-tesorero": {
            "keywords": [
                "finance", "finances", "budget", "expense", "expenses", "income",
                "cost", "costs", "excel", "sheet", "spreadsheet", "dashboard", "number",
                "numbers", "payment", "payments", "collection", "collections",
                "invoice", "invoices", "account statement", "cash flow", "margin",
                "profitability", "tax", "fixed cost", "variable cost",
            ],
            "patterns": [
                r"\b(organize|review|sort out)\s+(my\s+)?(finances|numbers|expenses|accounts)\b",
                r"\b(fixed\s+cost|variable\s+cost)\b",
                r"\b(how\s+much\s+(did\s+we\s+(invoice|earn|spend)|do\s+we\s+owe))\b",
            ]
        },
        "partenon-mensajero": {
            "keywords": [
                "brand", "branding", "communication", "marketing", "social", "content",
                "campaign", "calendar", "seo", "geo", "post", "copy", "message",
                "presentation", "letter", "mail", "email", "landing", "site",
                "wordpress", "blog", "lead magnet",
            ],
            "patterns": [
                r"\b(create|make|generate)\s+(a\s+)?(campaign|presentation|publication)\b",
                r"\b(content\s+calendar|content\s+plan)\b",
                r"\b(brand\s+voice|brand\s+message)\b",
            ]
        },
        "partenon-cobrador": {
            "keywords": [
                "collect", "collection", "collections", "payment", "payments", "stripe",
                "payment link", "subscription", "invoice", "bill", "card", "customer owes",
                "balance", "debt", "payment reminder", "recurring",
            ],
            "patterns": [
                r"\b(generate|create|send)\s+(a\s+)?(payment\s+link|link)\b",
                r"\b(subscription|recurring|monthly)\b",
                r"\b(payment\s+reminder|collect\s+from)\b",
            ]
        },
        "partenon-guardian": {
            "keywords": [
                "security", "api key", "api keys", "key", "token", "permission", "permissions",
                "model", "models", "nvidia", "openai", "kimi", "account", "access",
                "audit", "sandbox", "nemotron", "neoclaw",
            ],
            "patterns": [
                r"\b(rotate|change|revoke)\s+(the\s+)?(api\s+key|key|token)\b",
                r"\b(which\s+models|configure\s+models|manage\s+access)\b",
                r"\b(permissions\s+of\s+(treasurer|messenger|collector|guardian|strategist|diplomat))\b",
            ]
        },
        "partenon-estratega": {
            "keywords": [
                "project", "projects", "task", "tasks", "pending", "backlog",
                "checklist", "milestone", "milestones", "deadline", "date", "calendar", "agenda",
                "reminder", "reminders", "assign", "owner", "team", "goals",
                "objectives", "okr", "plan", "planning", "week", "month",
            ],
            "patterns": [
                r"\b(create|new|start)\s+(a\s+)?(project|milestone)\b",
                r"\b(pending\s+tasks?|what\s+do\s+we\s+have\s+pending)\b",
                r"\b(calendar|agenda|reminder)\b",
                r"\b(briefing|weekly\s+plan|weekly\s+review)\b",
            ]
        },
        "partenon-diplomatico": {
            "keywords": [
                "client", "clients", "vendor", "vendors", "partner", "partners",
                "relationship", "relationships", "follow-up", "follow up", "contract", "contracts",
                "milestone", "milestones", "negotiation", "agreement", "agreements",
                "satisfaction", "meeting", "call",
            ],
            "patterns": [
                r"\b(follow\s+up\s+on|how\s+is)\s+(the\s+)?(client|vendor)\b",
                r"\b(negotiate|coordinate)\s+(with\s+)?(client|vendor)\b",
                r"\b(milestones?\s+of\s+(the\s+)?(client|vendor))\b",
            ]
        },
        "partenon-brain": {
            "keywords": [
                "memory", "context", "insight", "insights", "pattern", "patterns",
                "remember", "recall", "history", "learn", "learned",
                "decision", "decisions", "knowledge",
            ],
            "patterns": [
                r"\b(what\s+did\s+we\s+decid(e|ed)|what\s+was\s+said|remember\s+that)\b",
                r"\b(recall|summarize|search)\s+(my\s+)?(memory|context|history)\b",
                r"\b(insights?|patterns?|trends?|findings?)\b",
            ]
        },
    }

    def __init__(self):
        # All Partenon profiles are active by default.
        self.active_profiles = set(self.INTENT_PATTERNS.keys())

    def route(self, message: str) -> Optional[str]:
        """Route a message to the appropriate profile. Returns profile name or None."""
        message_lower = message.lower()
        scores = {}

        for profile_name, patterns in self.INTENT_PATTERNS.items():
            if profile_name not in self.active_profiles:
                continue

            score = 0
            for keyword in patterns["keywords"]:
                if keyword in message_lower:
                    score += 1

            for pattern in patterns["patterns"]:
                if re.search(pattern, message_lower):
                    score += 3

            if score > 0:
                scores[profile_name] = score

        if not scores:
            return None

        return max(scores, key=scores.get)

    def route_with_context(
        self,
        message: str,
        last_profile: str = None,
        last_entity: str = None,
    ) -> Dict[str, Any]:
        """Route with conversation context."""
        result = {
            "profile": None,
            "entity": last_entity,
            "confidence": 0.0,
        }

        entity_match = re.search(r"\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b", message)
        if entity_match:
            result["entity"] = entity_match.group(1)

        routed = self.route(message)
        if routed:
            result["profile"] = routed
            result["confidence"] = 0.8
        elif last_profile:
            result["profile"] = last_profile
            result["confidence"] = 0.5

        return result


_router_instance = None


def get_router() -> IntentRouter:
    """Get or create singleton router instance."""
    global _router_instance
    if _router_instance is None:
        _router_instance = IntentRouter()
    return _router_instance


def route_intent(message: str) -> Optional[str]:
    """Convenience function."""
    return get_router().route(message)


if __name__ == "__main__":
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
