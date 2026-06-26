"""
Partenon General Onboarding Flow.

Asks business questions, creates profile files, and generates initial kanban missions.
"""

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = Path(__file__).resolve().parents[2]
PROFILE_EXAMPLES = REPO_ROOT / "hermes" / "profiles"
PROFILE_FILES = {
    "scribe": ".finance",
    "herald": ".design",
    "collector": ".payments",
    "guardian": ".security",
    "strategist": ".ops",
    "diplomat": ".relations",
}


def load_questions() -> str:
    """Load onboarding questions markdown."""
    path = REPO_ROOT / "partenon-core" / "templates" / "onboarding_questions.md"
    return path.read_text(encoding="utf-8")


def load_initial_tasks() -> List[Dict[str, Any]]:
    """Load default mission templates."""
    path = REPO_ROOT / "partenon-core" / "data" / "initial_tasks.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def create_profile_files(answers: Dict[str, str], workspace: Path) -> Dict[str, Path]:
    """Create .finance, .design, .payments, .security, .ops, .relations from examples."""
    created = {}
    for profile, filename in PROFILE_FILES.items():
        example = PROFILE_EXAMPLES / f"partenon-{profile}" / "templates" / f"{filename}.example"
        target = workspace / filename
        if example.exists():
            shutil.copy(example, target)
            content = target.read_text(encoding="utf-8")
            content = content.replace("{{EMPRESA_NOMBRE}}", answers.get("name", "My Company"))
            content = content.replace("{{INDUSTRIA}}", answers.get("industry", "services"))
            content = content.replace("{{MONEDA}}", answers.get("currency", "USD"))
            target.write_text(content, encoding="utf-8")
        created[filename] = target
    return created


def generate_missions(answers: Dict[str, str]) -> List[Dict[str, Any]]:
    """Generate initial missions from templates, optionally customized by answers."""
    missions = load_initial_tasks()
    for m in missions:
        m["created_at"] = datetime.now(timezone.utc).isoformat()
        m["updated_at"] = m["created_at"]
    return missions


def run_onboarding(answers: Dict[str, str], workspace: Path) -> Dict[str, Any]:
    """
    Run the general onboarding.

    Args:
        answers: dict with keys like name, industry, currency, etc.
        workspace: directory where profile files and tasks will be written.

    Returns:
        dict with profile_files, missions, and summary.
    """
    workspace.mkdir(parents=True, exist_ok=True)
    profile_files = create_profile_files(answers, workspace)
    missions = generate_missions(answers)

    tasks_path = workspace / "tasks.json"
    with open(tasks_path, "w", encoding="utf-8") as f:
        json.dump(missions, f, ensure_ascii=False, indent=2)

    summary = {
        "company": answers.get("name", "My Company"),
        "industry": answers.get("industry", "services"),
        "active_profiles": list(PROFILE_FILES.values()),
        "missions_generated": len(missions),
        "workspace": str(workspace),
    }

    return {
        "profile_files": {k: str(v) for k, v in profile_files.items()},
        "missions": missions,
        "summary": summary,
    }


if __name__ == "__main__":
    sample_answers = {
        "name": "Aurora Coffee",
        "industry": "food",
        "currency": "USD",
        "size": "2-5",
        "country": "Mexico",
    }
    result = run_onboarding(sample_answers, REPO_ROOT / "data" / "workspaces" / "demo")
    print(json.dumps(result, ensure_ascii=False, indent=2))
