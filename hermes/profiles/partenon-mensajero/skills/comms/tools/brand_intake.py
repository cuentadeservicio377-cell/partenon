#!/usr/bin/env python3
"""
Partenon Herald — Brand Intake Tool
Adaptation of the brand questionnaire. Generates the company's .design file.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


DEFAULT_DESIGN_PATH = Path(".design")


def p0_questions() -> List[Dict[str, Any]]:
    """Minimum required fields to unlock real campaigns."""
    return [
        {
            "id": "brand_name",
            "question": "Public brand or company name",
            "required": True,
        },
        {
            "id": "website",
            "question": "Main website URL",
            "required": False,
        },
        {
            "id": "what_you_sell",
            "question": "What you sell in one sentence",
            "required": True,
        },
        {
            "id": "who_you_help",
            "question": "Who you help (primary buyer: role, industry, size)",
            "required": True,
        },
        {
            "id": "how_you_do_it",
            "question": "How you do it (mechanism, process, or key differentiator)",
            "required": True,
        },
        {
            "id": "market",
            "question": "Market or geography you serve",
            "required": True,
        },
        {
            "id": "tone",
            "question": "Brand tone (formal, close, technical, direct, premium, etc.)",
            "required": True,
        },
        {
            "id": "addressing",
            "question": "Form of address (you formal, you informal, plural)",
            "required": True,
        },
        {
            "id": "claims_to_avoid",
            "question": "Claims or promises to avoid until evidence exists",
            "required": False,
        },
        {
            "id": "final_approver",
            "question": "Who finally approves copy and campaigns",
            "required": True,
        },
    ]


def p1_questions() -> List[Dict[str, Any]]:
    """Strong strategy fields."""
    return [
        {
            "id": "positioning",
            "question": "In one sentence: what you are, for whom, and what result you create",
            "required": False,
        },
        {
            "id": "differentiator",
            "question": "Why someone should choose you over a competitor",
            "required": False,
        },
        {
            "id": "proof_points",
            "question": "Proof points you already have (testimonials, metrics, cases)",
            "required": False,
        },
        {
            "id": "objections",
            "question": "Main objections that stop the purchase",
            "required": False,
        },
        {
            "id": "channels",
            "question": "Active or priority channels (comma-separated list)",
            "required": False,
        },
        {
            "id": "kpis",
            "question": "KPIs that define success for communications",
            "required": False,
        },
        {
            "id": "words_always",
            "question": "Words or phrases that must always appear",
            "required": False,
        },
        {
            "id": "words_never",
            "question": "Words or phrases that must never be used",
            "required": False,
        },
    ]


def empty_design() -> Dict[str, Any]:
    """Return a fresh .design skeleton."""
    return {
        "meta": {
            "version": "0.1.0",
            "profile": "partenon-mensajero",
            "updated_at": datetime.now().isoformat(),
        },
        "brand": {
            "brand_name": "",
            "website": "",
            "industry": "",
            "market": "",
            "stage": "",
        },
        "positioning": {
            "what_you_sell": "",
            "who_you_help": "",
            "how_you_do_it": "",
            "positioning": "",
            "differentiator": "",
        },
        "voice": {
            "tone": "",
            "addressing": "you informal",
            "style": "direct, clear, no filler",
            "emojis": False,
            "slang": False,
        },
        "audience": {
            "primary": {
                "role": "",
                "industry": "",
                "size": "",
                "pain": "",
                "outcome": "",
                "objections": [],
            },
            "secondary": [],
        },
        "channels": [],
        "messaging": {
            "key_messages": [],
            "claims_to_avoid": [],
            "proof_points": [],
            "cta_matrix": {
                "awareness": "See how it works",
                "consideration": "Book a diagnostic call",
                "decision": "Start this week",
            },
        },
        "content": {
            "pillars": [],
            "topics_to_own": [],
            "topics_to_avoid": [],
        },
        "operations": {
            "final_approver": "",
            "autonomy": {
                "draft_copy": True,
                "create_calendar": True,
                "publish_social": False,
                "send_email": False,
                "launch_ads": False,
            },
        },
    }


def parse_channels(value: Any) -> List[str]:
    """Parse a comma-separated string or list into a clean list."""
    if isinstance(value, list):
        return [str(v).strip().lower() for v in value if str(v).strip()]
    if isinstance(value, str):
        return [v.strip().lower() for v in value.split(",") if v.strip()]
    return []


def update_design_from_answers(design: Dict[str, Any], answers: Dict[str, Any]) -> Dict[str, Any]:
    """Map interview answers into the .design structure."""
    brand = design.setdefault("brand", {})
    brand["brand_name"] = answers.get("brand_name", brand.get("brand_name", ""))
    brand["website"] = answers.get("website", brand.get("website", ""))
    brand["market"] = answers.get("market", brand.get("market", ""))

    positioning = design.setdefault("positioning", {})
    positioning["what_you_sell"] = answers.get("what_you_sell", positioning.get("what_you_sell", ""))
    positioning["who_you_help"] = answers.get("who_you_help", positioning.get("who_you_help", ""))
    positioning["how_you_do_it"] = answers.get("how_you_do_it", positioning.get("how_you_do_it", ""))
    positioning["positioning"] = answers.get("positioning", positioning.get("positioning", ""))
    positioning["differentiator"] = answers.get("differentiator", positioning.get("differentiator", ""))

    voice = design.setdefault("voice", {})
    voice["tone"] = answers.get("tone", voice.get("tone", ""))
    voice["addressing"] = answers.get("addressing", voice.get("addressing", "you informal"))

    audience = design.setdefault("audience", {})
    primary = audience.setdefault("primary", {})
    primary["role"] = answers.get("who_you_help", primary.get("role", ""))
    if "objections" in answers:
        objections = answers["objections"]
        if isinstance(objections, str):
            primary["objections"] = [o.strip() for o in objections.split("\n") if o.strip()]
        elif isinstance(objections, list):
            primary["objections"] = objections

    design["channels"] = parse_channels(answers.get("channels", design.get("channels", [])))

    messaging = design.setdefault("messaging", {})
    if "proof_points" in answers:
        proof = answers["proof_points"]
        if isinstance(proof, str):
            messaging["proof_points"] = [p.strip() for p in proof.split("\n") if p.strip()]
        elif isinstance(proof, list):
            messaging["proof_points"] = proof

    if "claims_to_avoid" in answers:
        claims = answers["claims_to_avoid"]
        if isinstance(claims, str):
            messaging["claims_to_avoid"] = [c.strip() for c in claims.split("\n") if c.strip()]
        elif isinstance(claims, list):
            messaging["claims_to_avoid"] = claims

    if "words_always" in answers:
        words = answers["words_always"]
        if isinstance(words, str):
            messaging.setdefault("key_messages", []).extend(
                [w.strip() for w in words.split("\n") if w.strip()]
            )

    if "kpis" in answers:
        design.setdefault("kpis", {}).setdefault("comms", parse_channels(answers["kpis"]))

    operations = design.setdefault("operations", {})
    operations["final_approver"] = answers.get("final_approver", operations.get("final_approver", ""))

    design["meta"]["updated_at"] = datetime.now().isoformat()
    return design


def validate_p0(design: Dict[str, Any]) -> List[str]:
    """Return missing P0 fields."""
    missing = []
    positioning = design.get("positioning", {})
    voice = design.get("voice", {})
    brand = design.get("brand", {})
    operations = design.get("operations", {})

    if not positioning.get("what_you_sell"):
        missing.append("positioning.what_you_sell")
    if not positioning.get("who_you_help"):
        missing.append("positioning.who_you_help")
    if not positioning.get("how_you_do_it"):
        missing.append("positioning.how_you_do_it")
    if not voice.get("tone"):
        missing.append("voice.tone")
    if not voice.get("addressing"):
        missing.append("voice.addressing")
    if not brand.get("market"):
        missing.append("brand.market")
    if not operations.get("final_approver"):
        missing.append("operations.final_approver")

    return missing


def load_design(path: Path = DEFAULT_DESIGN_PATH) -> Dict[str, Any]:
    """Load existing .design or return a fresh skeleton."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or empty_design()
        except Exception:
            pass
    return empty_design()


def save_design(design: Dict[str, Any], path: Path = DEFAULT_DESIGN_PATH) -> None:
    """Write .design to disk as YAML."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(
            design,
            f,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )


def interactive_intake(path: Path = DEFAULT_DESIGN_PATH) -> Dict[str, Any]:
    """Run an interactive interview and write .design."""
    design = load_design(path)
    answers: Dict[str, Any] = {}

    print("\n=== Brand interview (P0) ===")
    for q in p0_questions():
        current = design
        for key in q["id"].split("."):
            current = current.get(key, {}) if isinstance(current, dict) else ""
        default = current if isinstance(current, str) else ""
        prompt = f"{q['question']}"
        if default:
            prompt += f" [{default}]"
        prompt += ": "
        value = input(prompt).strip()
        if value:
            answers[q["id"]] = value
        elif default:
            answers[q["id"]] = default

    print("\n=== Brand interview (P1, optional) ===")
    for q in p1_questions():
        value = input(f"{q['question']} (Enter to skip): ").strip()
        if value:
            answers[q["id"]] = value

    design = update_design_from_answers(design, answers)
    missing = validate_p0(design)

    save_design(design, path)

    result = {
        "success": len(missing) == 0,
        "path": str(path.resolve()),
        "missing_p0": missing,
        "brand_name": design.get("brand", {}).get("brand_name", ""),
    }

    if missing:
        print(f"\n.design saved, but P0 fields are missing: {', '.join(missing)}")
    else:
        print(f"\n.design saved successfully at {path}")

    return result


def generate_design_from_dict(answers: Dict[str, Any], path: Path = DEFAULT_DESIGN_PATH) -> Dict[str, Any]:
    """Programmatic entry point to generate .design from a dict."""
    design = load_design(path)
    design = update_design_from_answers(design, answers)
    missing = validate_p0(design)
    save_design(design, path)

    return {
        "success": len(missing) == 0,
        "path": str(path.resolve()),
        "missing_p0": missing,
        "brand_name": design.get("brand", {}).get("brand_name", ""),
    }


def main() -> int:
    """CLI entry point."""
    path = DEFAULT_DESIGN_PATH
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])

    if len(sys.argv) > 2 and sys.argv[2] == "--json":
        answers = json.loads(sys.stdin.read())
        result = generate_design_from_dict(answers, path)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["success"] else 1

    result = interactive_intake(path)
    return 0 if result["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
