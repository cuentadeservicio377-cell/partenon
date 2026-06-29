"""
Gateway progressive onboarding conversation tool.

Guides a new user through a short questionnaire and, on completion, creates
company files and initial missions.
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict

# Allow the tool to be loaded standalone from a profile directory.
try:
    from mcp_servers.memory.tools import GBrainStore
except ImportError:  # pragma: no cover
    _repo_root = Path(__file__).resolve().parents[6]
    if str(_repo_root) not in sys.path:
        sys.path.insert(0, str(_repo_root))
    from mcp_servers.memory.tools import GBrainStore

try:
    from partenon_core.tools.onboarding_engine import OnboardingEngine
    from partenon_core.tools.onboarding_flow import run_onboarding
except ImportError:  # pragma: no cover
    from partenon_core.tools.onboarding_engine import OnboardingEngine
    from partenon_core.tools.onboarding_flow import run_onboarding


ONBOARDING_STEPS = [
    "welcome",
    "company_name",
    "industry",
    "team_size",
    "main_pain",
    "confirm",
    "done",
]


_ANSWER_KEYS = {
    "company_name": "name",
    "industry": "industry",
    "team_size": "size",
    "main_pain": "main_pain",
}


def _get_store() -> GBrainStore:
    """Return a GBrainStore instance using the configured database URL."""
    return GBrainStore(os.getenv("GBRAIN_DATABASE_URL"))


def _load_state(user_id: str) -> Dict[str, Any]:
    """Load onboarding state from memory, or return a fresh welcome state."""
    page = _get_store().get_page(f"onboarding/{user_id}")
    if page and page.get("content"):
        try:
            return json.loads(page["content"])
        except json.JSONDecodeError:
            pass
    return {"step": "welcome", "answers": {}}


def _save_state(user_id: str, state: Dict[str, Any]) -> None:
    """Persist onboarding state to memory."""
    _get_store().put_page(
        f"onboarding/{user_id}",
        json.dumps(state, ensure_ascii=False),
        tags=["onboarding", "gateway"],
    )


def _next_step(current: str) -> str:
    """Return the next step in the state machine."""
    try:
        idx = ONBOARDING_STEPS.index(current)
    except ValueError:
        return "done"
    if idx + 1 < len(ONBOARDING_STEPS):
        return ONBOARDING_STEPS[idx + 1]
    return "done"


def _confirmation_message(answers: Dict[str, str]) -> str:
    """Build the confirmation prompt from collected answers."""
    lines = [
        "Please confirm your answers:",
        f"- Company name: {answers.get('name', '')}",
        f"- Industry: {answers.get('industry', '')}",
        f"- Team size: {answers.get('size', '')}",
        f"- Main pain: {answers.get('main_pain', '')}",
        "",
        "Reply 'yes' to create your workspace, or 'no' to start over.",
    ]
    return "\n".join(lines)


def _run_onboarding_completion(answers: Dict[str, str]) -> Dict[str, Any]:
    """
    Create company files and first missions using the onboarding engine.

    Runs in a temporary workspace so the gateway does not pollute the repository.
    """
    workspace = Path(tempfile.mkdtemp(prefix="partenon-onboarding-"))
    config_dir = workspace / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "company.yaml"

    company_yaml = f"""company:
  name: {answers.get('name', 'My Company')}
  industry: {answers.get('industry', 'services')}
  currency: USD
  language: en
  timezone: UTC
"""
    config_path.write_text(company_yaml, encoding="utf-8")

    engine = OnboardingEngine(config_path=str(config_path))
    engine.project_root = workspace
    engine.data_dir = workspace / "data"
    engine.data_dir.mkdir(exist_ok=True)
    engine_result = engine.run_full_onboarding()

    flow_result = run_onboarding(answers, workspace)

    return {
        "success": engine_result.get("success", False),
        "workspace": str(workspace),
        "company": answers.get("name", "My Company"),
        "industry": answers.get("industry", "services"),
        "missions_generated": flow_result.get("summary", {}).get("missions_generated", 0),
        "profile_files": flow_result.get("profile_files", {}),
    }


def onboarding_reply(user_id: str, text: str) -> Dict[str, Any]:
    """
    Advance the onboarding conversation for a user.

    Returns a dict with keys:
        reply: text to send back to the user.
        step: current onboarding step.
        done: True when onboarding has completed.
    """
    state = _load_state(user_id)
    current_step = state.get("step", "welcome")
    answers = state.get("answers", {})
    cleaned = text.strip()

    if current_step == "welcome":
        next_step = _next_step(current_step)
        reply = (
            "Welcome to Partenon. I will help you set up your company in a few steps.\n"
            "What is your company name?"
        )
        state["step"] = next_step
        _save_state(user_id, state)
        return {"reply": reply, "step": next_step, "done": False}

    if current_step in _ANSWER_KEYS:
        key = _ANSWER_KEYS[current_step]
        answers[key] = cleaned
        state["answers"] = answers
        next_step = _next_step(current_step)
        state["step"] = next_step

        if next_step == "industry":
            reply = f"Nice to meet you, {answers.get('name', '')}. What industry are you in?"
        elif next_step == "team_size":
            reply = "How many people are on your team? (e.g., 1, 2-5, 6-20)"
        elif next_step == "main_pain":
            reply = "What is the main pain you want Partenon to solve first?"
        elif next_step == "confirm":
            reply = _confirmation_message(answers)
        else:
            reply = "Thanks. Let's continue."

        _save_state(user_id, state)
        return {"reply": reply, "step": next_step, "done": False}

    if current_step == "confirm":
        if cleaned.lower() in {"yes", "y", "confirm", "ok"}:
            state["step"] = "done"
            _save_state(user_id, state)
            summary = _run_onboarding_completion(answers)
            reply = (
                f"Workspace created for {summary['company']}.\n"
                f"Generated {summary['missions_generated']} initial missions.\n"
                "You can now talk to any Partenon hero."
            )
            return {"reply": reply, "step": "done", "done": True, "summary": summary}

        # Anything other than yes keeps the user at the confirm step.
        reply = "Please reply 'yes' to confirm, or 'no' to start over."
        return {"reply": reply, "step": "confirm", "done": False}

    # Already done; just acknowledge.
    return {
        "reply": "Your onboarding is already complete. How can Partenon help today?",
        "step": "done",
        "done": True,
    }


if __name__ == "__main__":  # pragma: no cover
    import sys

    uid = sys.argv[1] if len(sys.argv) > 1 else "demo-user"
    txt = sys.argv[2] if len(sys.argv) > 2 else ""
    print(onboarding_reply(uid, txt))
