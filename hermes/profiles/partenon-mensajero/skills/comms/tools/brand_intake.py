#!/usr/bin/env python3
"""
Partenon Mensajero — Brand Intake Tool
Adaptacion del cuestionario de marca. Genera el archivo .design de la empresa.
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
            "id": "nombre_marca",
            "question": "Nombre publico de la marca o empresa",
            "required": True,
        },
        {
            "id": "website",
            "question": "Sitio web principal (URL)",
            "required": False,
        },
        {
            "id": "que_vendes",
            "question": "Que vendes en una oracion",
            "required": True,
        },
        {
            "id": "a_quien_ayudas",
            "question": "A quien ayudas (buyer primario: rol, industria, tamano)",
            "required": True,
        },
        {
            "id": "como_lo_haces",
            "question": "Como lo haces (mecanismo, proceso o diferenciador clave)",
            "required": True,
        },
        {
            "id": "mercado",
            "question": "Mercado o geografia que atiendes",
            "required": True,
        },
        {
            "id": "tono",
            "question": "Tono de la marca (formal, cercano, tecnico, directo, premium, etc.)",
            "required": True,
        },
        {
            "id": "forma_trato",
            "question": "Forma de trato (tu, usted, ustedes)",
            "required": True,
        },
        {
            "id": "claims_prohibidos",
            "question": "Claims o promesas que debemos evitar hasta tener evidencia",
            "required": False,
        },
        {
            "id": "aprobador_final",
            "question": "Quien aprueba el copy y las campanas finalmente",
            "required": True,
        },
    ]


def p1_questions() -> List[Dict[str, Any]]:
    """Strong strategy fields."""
    return [
        {
            "id": "posicionamiento",
            "question": "En una oracion: que eres, para quien y que resultado creas",
            "required": False,
        },
        {
            "id": "diferenciador",
            "question": "Por que alguien deberia elegirte en lugar de un competidor",
            "required": False,
        },
        {
            "id": "proof_points",
            "question": "Puntos de prueba que ya tienes (testimonios, metricas, casos)",
            "required": False,
        },
        {
            "id": "objeciones",
            "question": "Objeciones principales que frenan la compra",
            "required": False,
        },
        {
            "id": "canales",
            "question": "Canales activos o prioritarios (lista separada por comas)",
            "required": False,
        },
        {
            "id": "kpis",
            "question": "KPIs que definen exito para comunicaciones",
            "required": False,
        },
        {
            "id": "palabras_siempre",
            "question": "Palabras o frases que siempre deben aparecer",
            "required": False,
        },
        {
            "id": "palabras_nunca",
            "question": "Palabras o frases que nunca deben usarse",
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
            "nombre_marca": "",
            "website": "",
            "industria": "",
            "mercado": "",
            "etapa": "",
        },
        "positioning": {
            "que_vendes": "",
            "a_quien_ayudas": "",
            "como_lo_haces": "",
            "posicionamiento": "",
            "diferenciador": "",
        },
        "voice": {
            "tono": "",
            "forma_trato": "tu",
            "estilo": "directo, claro, sin relleno",
            "emojis": False,
            "slang": False,
        },
        "audience": {
            "primary": {
                "rol": "",
                "industria": "",
                "tamano": "",
                "dolor": "",
                "outcome": "",
                "objeciones": [],
            },
            "secondary": [],
        },
        "channels": [],
        "messaging": {
            "key_messages": [],
            "claims_prohibidos": [],
            "proof_points": [],
            "cta_matrix": {
                "awareness": "Conoce como funciona",
                "consideration": "Agenda una llamada",
                "decision": "Compra ahora",
            },
        },
        "content": {
            "pillars": [],
            "topics_to_own": [],
            "topics_to_avoid": [],
        },
        "operations": {
            "aprobador_final": "",
            "autonomia": {
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
    brand["nombre_marca"] = answers.get("nombre_marca", brand.get("nombre_marca", ""))
    brand["website"] = answers.get("website", brand.get("website", ""))
    brand["mercado"] = answers.get("mercado", brand.get("mercado", ""))

    positioning = design.setdefault("positioning", {})
    positioning["que_vendes"] = answers.get("que_vendes", positioning.get("que_vendes", ""))
    positioning["a_quien_ayudas"] = answers.get("a_quien_ayudas", positioning.get("a_quien_ayudas", ""))
    positioning["como_lo_haces"] = answers.get("como_lo_haces", positioning.get("como_lo_haces", ""))
    positioning["posicionamiento"] = answers.get("posicionamiento", positioning.get("posicionamiento", ""))
    positioning["diferenciador"] = answers.get("diferenciador", positioning.get("diferenciador", ""))

    voice = design.setdefault("voice", {})
    voice["tono"] = answers.get("tono", voice.get("tono", ""))
    voice["forma_trato"] = answers.get("forma_trato", voice.get("forma_trato", "tu"))

    audience = design.setdefault("audience", {})
    primary = audience.setdefault("primary", {})
    primary["rol"] = answers.get("a_quien_ayudas", primary.get("rol", ""))
    if "objeciones" in answers:
        objeciones = answers["objeciones"]
        if isinstance(objeciones, str):
            primary["objeciones"] = [o.strip() for o in objeciones.split("\n") if o.strip()]
        elif isinstance(objeciones, list):
            primary["objeciones"] = objeciones

    design["channels"] = parse_channels(answers.get("canales", design.get("channels", [])))

    messaging = design.setdefault("messaging", {})
    if "proof_points" in answers:
        proof = answers["proof_points"]
        if isinstance(proof, str):
            messaging["proof_points"] = [p.strip() for p in proof.split("\n") if p.strip()]
        elif isinstance(proof, list):
            messaging["proof_points"] = proof

    if "claims_prohibidos" in answers:
        claims = answers["claims_prohibidos"]
        if isinstance(claims, str):
            messaging["claims_prohibidos"] = [c.strip() for c in claims.split("\n") if c.strip()]
        elif isinstance(claims, list):
            messaging["claims_prohibidos"] = claims

    if "palabras_siempre" in answers:
        words = answers["palabras_siempre"]
        if isinstance(words, str):
            messaging.setdefault("key_messages", []).extend(
                [w.strip() for w in words.split("\n") if w.strip()]
            )

    if "kpis" in answers:
        design.setdefault("kpis", {}).setdefault("comms", parse_channels(answers["kpis"]))

    operations = design.setdefault("operations", {})
    operations["aprobador_final"] = answers.get("aprobador_final", operations.get("aprobador_final", ""))

    design["meta"]["updated_at"] = datetime.now().isoformat()
    return design


def validate_p0(design: Dict[str, Any]) -> List[str]:
    """Return missing P0 fields."""
    missing = []
    positioning = design.get("positioning", {})
    voice = design.get("voice", {})
    brand = design.get("brand", {})
    operations = design.get("operations", {})

    if not positioning.get("que_vendes"):
        missing.append("positioning.que_vendes")
    if not positioning.get("a_quien_ayudas"):
        missing.append("positioning.a_quien_ayudas")
    if not positioning.get("como_lo_haces"):
        missing.append("positioning.como_lo_haces")
    if not voice.get("tono"):
        missing.append("voice.tono")
    if not voice.get("forma_trato"):
        missing.append("voice.forma_trato")
    if not brand.get("mercado"):
        missing.append("brand.mercado")
    if not operations.get("aprobador_final"):
        missing.append("operations.aprobador_final")

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

    print("\n=== Entrevista de marca (P0) ===")
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

    print("\n=== Entrevista de marca (P1, opcional) ===")
    for q in p1_questions():
        value = input(f"{q['question']} (Enter para omitir): ").strip()
        if value:
            answers[q["id"]] = value

    design = update_design_from_answers(design, answers)
    missing = validate_p0(design)

    save_design(design, path)

    result = {
        "success": len(missing) == 0,
        "path": str(path.resolve()),
        "missing_p0": missing,
        "brand_name": design.get("brand", {}).get("nombre_marca", ""),
    }

    if missing:
        print(f"\n.design guardado, pero faltan campos P0: {', '.join(missing)}")
    else:
        print(f"\n.design guardado correctamente en {path}")

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
        "brand_name": design.get("brand", {}).get("nombre_marca", ""),
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
