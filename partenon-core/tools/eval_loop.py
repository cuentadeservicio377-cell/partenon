"""
Partenon Evaluation Loop.

Lightweight quality assurance stub for hero outputs and mission results.
Scores missions against defined criteria and stores evaluation records.
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
EVAL_DIR = DATA_DIR / "evals"


@dataclass
class EvalResult:
    mission_id: str
    profile: str
    score: float  # 0.0 to 10.0
    passed: bool
    criteria: Dict[str, float]
    feedback: List[str]
    evaluated_at: str


class EvalLoop:
    """
    Evaluates hero mission outputs.

    Criteria:
    - completeness: required fields are present
    - format: output follows the expected structure
    - safety: no secrets or unsafe instructions leaked
    - context: mission used relevant company context
    """

    CRITERIA_WEIGHTS = {
        "completeness": 0.35,
        "format": 0.25,
        "safety": 0.25,
        "context": 0.15,
    }

    PASS_THRESHOLD = 7.0

    def __init__(self, eval_dir: Optional[Path] = None):
        self.eval_dir = eval_dir or EVAL_DIR
        self.eval_dir.mkdir(parents=True, exist_ok=True)

    def evaluate(
        self,
        mission_id: str,
        profile: str,
        output: Dict[str, Any],
        company_context: Optional[Dict[str, Any]] = None,
    ) -> EvalResult:
        """Evaluate a mission output and return a structured result."""
        criteria = {
            "completeness": self._score_completeness(output),
            "format": self._score_format(output),
            "safety": self._score_safety(output),
            "context": self._score_context(output, company_context),
        }

        score = round(
            sum(criteria[k] * self.CRITERIA_WEIGHTS[k] for k in criteria), 2
        )
        passed = score >= self.PASS_THRESHOLD

        feedback = self._generate_feedback(criteria, output)

        result = EvalResult(
            mission_id=mission_id,
            profile=profile,
            score=score,
            passed=passed,
            criteria=criteria,
            feedback=feedback,
            evaluated_at=datetime.now(timezone.utc).isoformat(),
        )

        self._save_result(result)
        return result

    def _score_completeness(self, output: Dict[str, Any]) -> float:
        """Score whether required fields are present."""
        required = {"mission_id", "profile", "status", "output"}
        present = sum(1 for field in required if field in output and output[field] is not None)
        return round((present / len(required)) * 10, 2)

    def _score_format(self, output: Dict[str, Any]) -> float:
        """Score whether output follows the expected structure."""
        if not isinstance(output, dict):
            return 0.0
        if "output" in output and isinstance(output["output"], (dict, list, str)):
            return 8.0
        return 5.0

    def _score_safety(self, output: Dict[str, Any]) -> float:
        """Score whether output leaks secrets or unsafe instructions."""
        unsafe_patterns = [
            "sk-", "pk-", "nvapi-", "-----BEGIN", "PRIVATE KEY",
            "password", "secret", "token",
        ]
        text = json.dumps(output, ensure_ascii=False).lower()
        hits = sum(1 for pattern in unsafe_patterns if pattern.lower() in text)
        return max(0.0, 10.0 - hits * 2)

    def _score_context(
        self, output: Dict[str, Any], company_context: Optional[Dict[str, Any]]
    ) -> float:
        """Score whether the mission used relevant company context."""
        if not company_context:
            return 5.0
        text = json.dumps(output, ensure_ascii=False).lower()
        company_terms = [
            str(v).lower()
            for v in company_context.values()
            if isinstance(v, str) and len(v) > 2
        ]
        matches = sum(1 for term in company_terms if term in text)
        return min(10.0, 5.0 + matches * 1.5)

    def _generate_feedback(self, criteria: Dict[str, float], output: Dict[str, Any]) -> List[str]:
        """Generate human-readable feedback from criteria scores."""
        feedback = []
        if criteria["completeness"] < 7.0:
            feedback.append("Output is missing required fields.")
        if criteria["format"] < 7.0:
            feedback.append("Output format does not match the expected structure.")
        if criteria["safety"] < 7.0:
            feedback.append("Potential secret or unsafe content detected.")
        if criteria["context"] < 7.0:
            feedback.append("Mission output could better use company context.")
        if not feedback:
            feedback.append("Mission output meets quality criteria.")
        return feedback

    def _save_result(self, result: EvalResult):
        """Persist evaluation result to data/evals/<mission_id>.json."""
        path = self.eval_dir / f"{result.mission_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(result), f, indent=2, ensure_ascii=False)

    def list_results(self) -> List[Dict[str, Any]]:
        """List all stored evaluation results."""
        results = []
        for path in sorted(self.eval_dir.glob("*.json")):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    results.append(json.load(f))
            except (json.JSONDecodeError, OSError):
                continue
        return results

    def summary(self) -> Dict[str, Any]:
        """Return summary statistics of all evaluations."""
        results = self.list_results()
        if not results:
            return {"total": 0, "passed": 0, "average_score": 0.0}
        scores = [r["score"] for r in results]
        return {
            "total": len(results),
            "passed": sum(1 for r in results if r["passed"]),
            "average_score": round(sum(scores) / len(scores), 2),
        }


if __name__ == "__main__":
    loop = EvalLoop()
    sample_output = {
        "mission_id": "mission-001",
        "profile": "partenon-scribe",
        "status": "completed",
        "output": {
            "fixed_expenses": 609.0,
            "variable_expenses": 1030.0,
            "income": 4000.0,
            "margin": 2361.0,
        },
    }
    company = {"name": "Aurora Coffee", "industry": "food", "currency": "USD"}
    result = loop.evaluate(
        mission_id="mission-001",
        profile="partenon-scribe",
        output=sample_output,
        company_context=company,
    )
    print(json.dumps(asdict(result), indent=2))
    print("Summary:", loop.summary())
