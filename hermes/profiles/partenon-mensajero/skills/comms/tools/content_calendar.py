#!/usr/bin/env python3
"""
Partenon Mensajero — Content Calendar Tool
Adaptacion de social_calendar.py. Genera calendarios de contenido con contexto de marca.
"""

import json
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


CONTENT_PILLARS = {
    "educational": {
        "name": "Educativo",
        "description": "Ensena algo util a la audiencia",
        "formats": [
            "How-to directo",
            "Tip rapido",
            "Mito vs realidad",
            "Framework o metodo",
            "Recomendacion de herramienta",
            "Dato del sector",
        ],
    },
    "behind_the_scenes": {
        "name": "Detras de escena",
        "description": "Muestra el proceso real sin filtros",
        "formats": [
            "Dia de trabajo",
            "Stack de herramientas",
            "Proceso paso a paso",
            "Leccion aprendida",
            "Metricas compartidas",
        ],
    },
    "social_proof": {
        "name": "Prueba social",
        "description": "Resultados, testimonios y credibilidad",
        "formats": [
            "Caso de cliente",
            "Testimonio",
            "Antes y despues",
            "Hito alcanzado",
            "Contenido generado por usuarios",
        ],
    },
    "engagement": {
        "name": "Engagement",
        "description": "Inicia conversaciones y construye comunidad",
        "formats": [
            "Opinion contundente",
            "Pregunta abierta",
            "Encuesta",
            "Esto o aquello",
            "Completa la frase",
        ],
    },
    "promotional": {
        "name": "Promocional",
        "description": "Promocion directa del producto o servicio (uso moderado)",
        "formats": [
            "Demo de producto",
            "Destacado de beneficio",
            "Oferta especial",
            "Promo de evento o webinar",
            "Recurso gratuito",
        ],
    },
}


POSTING_FREQUENCY = {
    "linkedin": {"ideal": "3-5x/semana", "minimum": "2x/semana"},
    "twitter": {"ideal": "3-5x/dia", "minimum": "1x/dia"},
    "instagram": {"ideal": "4-7x/semana", "minimum": "3x/semana"},
    "tiktok": {"ideal": "1-3x/dia", "minimum": "3x/semana"},
    "youtube": {"ideal": "2-3x/semana", "minimum": "1x/semana"},
    "facebook": {"ideal": "3-5x/semana", "minimum": "2x/semana"},
    "blog": {"ideal": "2-4x/mes", "minimum": "1x/mes"},
    "newsletter": {"ideal": "1-2x/semana", "minimum": "2x/mes"},
}


PILLAR_DISTRIBUTION = {
    "educational": 0.40,
    "behind_the_scenes": 0.15,
    "social_proof": 0.15,
    "engagement": 0.20,
    "promotional": 0.10,
}


def load_design(path: Path = Path(".design")) -> Dict[str, Any]:
    """Load brand design file if present."""
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            pass
    return {}


def pick_pillar_for_day(day_index: int) -> str:
    """Select a pillar based on distribution and rotation."""
    rotation = [
        "educational",
        "engagement",
        "educational",
        "behind_the_scenes",
        "educational",
        "social_proof",
        "promotional",
    ]
    return rotation[day_index % len(rotation)]


def generate_calendar(
    topic: str,
    channels: Optional[List[str]] = None,
    days: int = 7,
    brand_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Generate a content calendar with brand-aware angles."""
    if channels is None:
        channels = ["linkedin", "instagram"]

    brand_context = brand_context or {}
    positioning = brand_context.get("positioning", {})
    brand_name = brand_context.get("brand", {}).get("nombre_marca", topic)
    key_messages = brand_context.get("messaging", {}).get("key_messages", [])
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    calendar: Dict[str, Any] = {
        "campaign_id": f"CAL-{start_date.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}",
        "topic": topic,
        "brand": brand_name,
        "positioning": positioning,
        "channels": channels,
        "duration_days": days,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": (start_date + timedelta(days=days - 1)).strftime("%Y-%m-%d"),
        "posting_schedule": {p: POSTING_FREQUENCY.get(p, {}) for p in channels},
        "pillar_distribution": PILLAR_DISTRIBUTION,
        "calendar": [],
    }

    for day in range(days):
        date = start_date + timedelta(days=day)
        pillar_key = pick_pillar_for_day(day)
        pillar = CONTENT_PILLARS[pillar_key]
        formats = pillar["formats"]
        content_format = formats[day % len(formats)]

        message_angle = topic
        if key_messages:
            message_angle = key_messages[day % len(key_messages)]

        day_entry: Dict[str, Any] = {
            "day": day + 1,
            "date": date.strftime("%Y-%m-%d"),
            "day_of_week": date.strftime("%A"),
            "pillar": pillar["name"],
            "format": content_format,
            "topic_angle": f"{content_format} sobre {message_angle}",
            "channels": {},
            "status": "planned",
        }

        for channel in channels:
            guidance = f"{content_format} adaptado a {channel}"
            if channel in ["linkedin", "blog"]:
                guidance += ". Priorizar valor educativo y estructura escaneable."
            elif channel in ["instagram", "tiktok"]:
                guidance += ". Primero el gancho visual, despues la idea."
            elif channel == "newsletter":
                guidance += ". Un solo tema, una sola accion."

            day_entry["channels"][channel] = {
                "guidance": guidance,
                "copy": "",
                "status": "pending",
            }

        calendar["calendar"].append(day_entry)

    calendar["repurposing_notes"] = [
        "Cada pieza larga genera al menos 3 piezas cortas.",
        "Reutilizar el gancho mas fuerte para stories o reels.",
        "Un caso de cliente se convierte en post, email y carrusel.",
        "Republicar el contenido mejorado 2-4 semanas despues.",
    ]

    return calendar


def save_calendar(calendar: Dict[str, Any], output_dir: Path = Path("output/campaigns")) -> Path:
    """Persist calendar to disk."""
    campaign_id = calendar["campaign_id"]
    folder = output_dir / campaign_id
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "content-calendar.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(calendar, f, ensure_ascii=False, indent=2)

    return path


def main() -> int:
    """CLI entry point."""
    design = load_design()

    if len(sys.argv) < 2:
        print(json.dumps({
            "usage": "python3 content_calendar.py <topic> [canal1,canal2,...] [dias]",
            "example": "python3 content_calendar.py 'automatizacion para pymes' linkedin,instagram 14",
            "available_channels": list(POSTING_FREQUENCY.keys()),
        }, ensure_ascii=False, indent=2))
        return 0

    topic = sys.argv[1]
    channels = sys.argv[2].split(",") if len(sys.argv) > 2 else ["linkedin", "instagram"]
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 7

    calendar = generate_calendar(topic, channels, days, design)
    path = save_calendar(calendar)

    result = {
        "success": True,
        "campaign_id": calendar["campaign_id"],
        "calendar_path": str(path.resolve()),
        "days": days,
        "channels": channels,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
