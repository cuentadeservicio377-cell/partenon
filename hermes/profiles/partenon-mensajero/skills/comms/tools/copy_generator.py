#!/usr/bin/env python3
"""
Partenon Mensajero — Copy Generator Tool
Genera copy para ads, emails, posts y landing. Anti-AI-slop.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


BANNED_PATTERNS = [
    "revolucionario",
    "game changer",
    "transforma tu vida",
    "sin esfuerzo",
    "100% garantizado",
    "resultados inmediatos",
    "unico en el mercado",
    "descubre el secreto",
    "aprovecha ya",
    "no te lo pierdas",
    "la mejor solucion",
]


def load_design(path: Path = Path(".design")) -> Dict[str, Any]:
    """Load brand design file if present."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            pass
    return {}


def get_brand_context(design: Dict[str, Any]) -> Dict[str, Any]:
    """Extract relevant fields for copy generation."""
    positioning = design.get("positioning", {})
    voice = design.get("voice", {})
    messaging = design.get("messaging", {})
    audience = design.get("audience", {})

    return {
        "brand_name": design.get("brand", {}).get("nombre_marca", "Tu marca"),
        "que_vendes": positioning.get("que_vendes", ""),
        "a_quien_ayudas": positioning.get("a_quien_ayudas", ""),
        "como_lo_haces": positioning.get("como_lo_haces", ""),
        "tono": voice.get("tono", "directo"),
        "forma_trato": voice.get("forma_trato", "tu"),
        "key_messages": messaging.get("key_messages", []),
        "claims_prohibidos": messaging.get("claims_prohibidos", []),
        "proof_points": messaging.get("proof_points", []),
        "cta_matrix": messaging.get("cta_matrix", {}),
        "primary_dolor": audience.get("primary", {}).get("dolor", ""),
        "primary_outcome": audience.get("primary", {}).get("outcome", ""),
    }


def sanitize_text(text: str, banned: List[str]) -> str:
    """Remove or flag banned patterns from copy."""
    flagged = []
    lower_text = text.lower()
    for pattern in banned:
        if pattern in lower_text:
            flagged.append(pattern)
    return flagged


def generate_hook(brand: Dict[str, Any], topic: str, channel: str) -> str:
    """Generate a channel-aware hook."""
    dolor = brand["primary_dolor"] or "el problema que no deja crecer tu negocio"
    outcome = brand["primary_outcome"] or "un resultado claro y medible"
    que_vendes = brand["que_vendes"] or topic

    if channel in ["linkedin", "blog"]:
        return f"La mayoria de empresas lidian con {dolor}. Aqui hay una forma mas directa de llegar a {outcome}."
    if channel in ["instagram", "tiktok"]:
        return f"Si {dolor}, esto cambia como piensas sobre {que_vendes}."
    if channel == "email":
        return f"Hablemos de {dolor}. Hay una forma de acercarte a {outcome} sin complicar el dia a dia."
    return f"{dolor}? Existe una forma mas clara de resolverlo."


def generate_body(brand: Dict[str, Any], topic: str) -> str:
    """Generate a concise body paragraph."""
    parts = [
        f"Ayudamos a {brand['a_quien_ayudas']} a {brand['primary_outcome']}." if brand["a_quien_ayudas"] and brand["primary_outcome"] else "",
        f"Lo hacemos a traves de {brand['como_lo_haces']}." if brand["como_lo_haces"] else "",
        f"El punto central: {topic}." if topic else "",
    ]
    return " ".join(p for p in parts if p)


def generate_cta(brand: Dict[str, Any], stage: str = "consideration") -> str:
    """Generate a stage-appropriate CTA."""
    cta_matrix = brand.get("cta_matrix", {})
    return cta_matrix.get(stage, "Conoce mas")


def generate_ad_copy(brand: Dict[str, Any], topic: str, channel: str) -> Dict[str, Any]:
    """Generate ad copy variants."""
    hook = generate_hook(brand, topic, channel)
    body = generate_body(brand, topic)
    cta = generate_cta(brand, "consideration")

    variants = [
        {"name": "Directa", "headline": hook, "body": body, "cta": cta},
        {"name": "Dolor", "headline": f"Cansado de {brand['primary_dolor']}?", "body": body, "cta": cta},
        {"name": "Resultado", "headline": f"Como llegar a {brand['primary_outcome']}", "body": body, "cta": cta},
    ]

    return {
        "type": "ad",
        "channel": channel,
        "topic": topic,
        "variants": variants,
    }


def generate_email_copy(brand: Dict[str, Any], topic: str, email_type: str = "outreach") -> Dict[str, Any]:
    """Generate email copy."""
    subject = f"Sobre {topic}"
    if email_type == "follow_up":
        subject = f"Seguimiento: {topic}"
    elif email_type == "newsletter":
        subject = f"Este mes: {topic}"

    saludo = "Estimado/a" if brand["forma_trato"] == "usted" else "Hola"
    cta = generate_cta(brand, "decision") if email_type == "follow_up" else generate_cta(brand, "consideration")

    body_lines = [
        f"{saludo}",
        "",
        generate_hook(brand, topic, "email"),
        "",
        generate_body(brand, topic),
        "",
        f"{cta}.",
        "",
        "Saludos,",
        brand["brand_name"],
    ]

    return {
        "type": "email",
        "email_type": email_type,
        "subject": subject,
        "body": "\n".join(body_lines),
    }


def generate_post_copy(brand: Dict[str, Any], topic: str, channel: str) -> Dict[str, Any]:
    """Generate social post copy."""
    hook = generate_hook(brand, topic, channel)
    body = generate_body(brand, topic)
    cta = generate_cta(brand, "awareness")

    return {
        "type": "post",
        "channel": channel,
        "topic": topic,
        "copy": f"{hook}\n\n{body}\n\n{cta}.",
    }


def generate_landing_copy(brand: Dict[str, Any], topic: str) -> Dict[str, Any]:
    """Generate landing page copy structure."""
    return {
        "type": "landing",
        "topic": topic,
        "hero": {
            "headline": f"{brand['brand_name']} ayuda a {brand['a_quien_ayudas']} a {brand['primary_outcome']}",
            "subheadline": generate_body(brand, topic),
            "cta": generate_cta(brand, "decision"),
        },
        "problem": brand["primary_dolor"],
        "solution": brand["como_lo_haces"],
        "proof": brand["proof_points"][:3],
        "faq_cta": generate_cta(brand, "consideration"),
    }


def generate_copy(
    piece_type: str,
    topic: str,
    channel: str = "linkedin",
    email_type: str = "outreach",
    design: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Main dispatcher for copy generation."""
    design = design or load_design()
    brand = get_brand_context(design)

    if piece_type == "ad":
        result = generate_ad_copy(brand, topic, channel)
    elif piece_type == "email":
        result = generate_email_copy(brand, topic, email_type)
    elif piece_type == "post":
        result = generate_post_copy(brand, topic, channel)
    elif piece_type == "landing":
        result = generate_landing_copy(brand, topic)
    else:
        return {
            "success": False,
            "error": f"Tipo de pieza no soportado: {piece_type}",
        }

    all_text = json.dumps(result, ensure_ascii=False)
    flagged = sanitize_text(all_text, BANNED_PATTERNS + brand["claims_prohibidos"])

    result["success"] = True
    result["qa"] = {
        "banned_patterns_found": flagged,
        "passed": len(flagged) == 0,
    }

    return result


def save_copy(result: Dict[str, Any], output_dir: Path = Path("output/copy")) -> Path:
    """Persist copy pack to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{result['type']}-{timestamp}.json"
    path = output_dir / filename

    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    return path


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 3:
        print(json.dumps({
            "usage": "python3 copy_generator.py <tipo> <tema> [canal|email_type]",
            "types": ["ad", "email", "post", "landing"],
            "example": "python3 copy_generator.py ad 'automatizacion de cobros' linkedin",
        }, ensure_ascii=False, indent=2))
        return 0

    piece_type = sys.argv[1]
    topic = sys.argv[2]
    channel_or_email_type = sys.argv[3] if len(sys.argv) > 3 else "linkedin"

    kwargs = {"piece_type": piece_type, "topic": topic}
    if piece_type == "email":
        kwargs["email_type"] = channel_or_email_type
    else:
        kwargs["channel"] = channel_or_email_type

    result = generate_copy(**kwargs)
    path = save_copy(result)

    result["output_path"] = str(path.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("success") else 1


if __name__ == "__main__":
    sys.exit(main())
