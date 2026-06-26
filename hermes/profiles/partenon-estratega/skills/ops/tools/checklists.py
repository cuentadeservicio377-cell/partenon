"""
Partenon Estratega — Checklists Tool
Manages project checklists by type and industry.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


def _resolve_data_dir() -> Path:
    """Resolve data directory relative to partenon-core."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "partenon-core":
            data_dir = parent / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            return data_dir
        candidate = parent / "partenon-core" / "data"
        if candidate.exists() and candidate.is_dir():
            return candidate
    for parent in current.parents:
        if (parent / "partenon-core").exists():
            data_dir = parent / "partenon-core" / "data"
            data_dir.mkdir(parents=True, exist_ok=True)
            return data_dir
    local = Path(__file__).resolve().parent / "data"
    local.mkdir(parents=True, exist_ok=True)
    return local


def _default_industry() -> str:
    """Read industry from empresa.yaml if available."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "partenon-core":
            config_path = parent / "config" / "empresa.yaml"
            break
        config_path = parent / "partenon-core" / "config" / "empresa.yaml"
        if config_path.exists():
            break
    else:
        return "consultoria"

    if not config_path.exists():
        return "consultoria"

    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("empresa", {}).get("industria", "consultoria")
    except Exception:
        return "consultoria"


class Checklists:
    """Checklist management with templates by industry."""

    CHECKLIST_TEMPLATES = {
        "eventos": {
            "pre-evento": [
                "Confirmar fecha y lugar con cliente",
                "Contratar proveedores (catering, musica, fotografo)",
                "Preparar mobiliario y decoracion",
                "Coordinar logistica de transporte",
                "Briefing con equipo de trabajo",
                "Confirmar asistencia de invitados",
                "Preparar checklist de equipo",
            ],
            "durante-evento": [
                "Setup en lugar del evento",
                "Recepcion de invitados",
                "Coordinacion en tiempo real",
                "Resolucion de imprevistos",
                "Documentacion fotografica",
            ],
            "post-evento": [
                "Desmontaje y recoleccion de equipo",
                "Inventario de mobiliario",
                "Facturacion final al cliente",
                "Evaluacion con cliente",
                "Archivar fotos y documentos",
            ],
        },
        "legal": {
            "pre-juicio": [
                "Revisar contrato y antecedentes del caso",
                "Investigar jurisprudencia relevante",
                "Preparar estrategia legal",
                "Calendarizar audiencias y plazos",
                "Recopilar documentacion",
            ],
            "durante-juicio": [
                "Preparar escritos y demandas",
                "Asistir a audiencias",
                "Comunicacion continua con cliente",
                "Actualizar expediente",
                "Dar seguimiento a resoluciones",
            ],
            "post-juicio": [
                "Analizar sentencia",
                "Ejecucion o apelacion segun corresponda",
                "Cierre administrativo del caso",
                "Informe final al cliente",
                "Archivar expediente",
            ],
        },
        "consultoria": {
            "pre-proyecto": [
                "Definir alcance y objetivos",
                "Asignar responsables",
                "Establecer fechas clave",
                "Confirmar recursos necesarios",
                "Reunion kickoff con cliente",
            ],
            "durante-proyecto": [
                "Seguimiento semanal de avances",
                "Comunicacion continua con cliente",
                "Control de calidad de entregables",
                "Documentacion de procesos",
                "Gestion de cambios",
            ],
            "post-proyecto": [
                "Entrega final de documentos",
                "Capacitacion al cliente",
                "Evaluacion de resultados",
                "Solicitar testimonio o referencia",
                "Cierre administrativo",
            ],
        },
        "retail": {
            "pre-venta": [
                "Verificar inventario disponible",
                "Confirmar precios vigentes",
                "Preparar cotizacion",
                "Verificar politicas de envio",
            ],
            "durante-venta": [
                "Confirmar pago",
                "Preparar pedido",
                "Coordinar envio o entrega",
                "Enviar confirmacion al cliente",
            ],
            "post-venta": [
                "Seguimiento de entrega",
                "Solicitar feedback",
                "Gestionar garantia si aplica",
                "Fidelizacion del cliente",
            ],
        },
    }

    def __init__(self):
        self.industria = _default_industry()
        self.data_dir = _resolve_data_dir()
        self.checklists_file = self.data_dir / "checklists.json"
        self._checklists = None

    def _load(self) -> Dict[str, Any]:
        """Load checklists from JSON."""
        if self._checklists is not None:
            return self._checklists

        if self.checklists_file.exists():
            try:
                with open(self.checklists_file, "r", encoding="utf-8") as f:
                    self._checklists = json.load(f)
                    return self._checklists
            except Exception:
                pass

        self._checklists = {}
        return self._checklists

    def _save(self):
        """Save checklists to JSON."""
        with open(self.checklists_file, "w", encoding="utf-8") as f:
            json.dump(self._checklists, f, ensure_ascii=False, indent=2)

    def get_template(self, industry: str = None, checklist_type: str = None) -> Dict[str, List[str]]:
        """Get checklist template for industry."""
        if not industry:
            industry = self.industria

        templates = self.CHECKLIST_TEMPLATES.get(industry, self.CHECKLIST_TEMPLATES["consultoria"])

        if checklist_type:
            return {checklist_type: templates.get(checklist_type, [])}

        return templates

    def create_project_checklist(
        self, proyecto_id: str, industry: str = None
    ) -> Dict[str, Any]:
        """Create checklist for a project based on industry templates."""
        self._load()

        templates = self.get_template(industry)

        checklist = {}
        for phase, items in templates.items():
            checklist[phase] = [
                {
                    "item": item,
                    "completado": False,
                    "fecha_completado": None,
                }
                for item in items
            ]

        self._checklists[proyecto_id] = {
            "proyecto_id": proyecto_id,
            "created_at": datetime.now().isoformat(),
            "phases": checklist,
        }
        self._save()

        total_items = sum(len(v) for v in checklist.values())
        return {
            "success": True,
            "checklist": self._checklists[proyecto_id],
            "message": f"Checklist creado para {proyecto_id} con {total_items} items",
        }

    def get_checklist(self, proyecto_id: str) -> Optional[Dict[str, Any]]:
        """Get checklist for a project."""
        self._load()
        return self._checklists.get(proyecto_id)

    def toggle_item(
        self, proyecto_id: str, phase: str, item_index: int
    ) -> Dict[str, Any]:
        """Toggle completion status of a checklist item."""
        self._load()

        checklist = self._checklists.get(proyecto_id)
        if not checklist:
            return {
                "success": False,
                "error": f"No hay checklist para {proyecto_id}",
            }

        phases = checklist.get("phases", {})
        if phase not in phases:
            return {
                "success": False,
                "error": f"Fase '{phase}' no encontrada",
            }

        items = phases[phase]
        if item_index < 0 or item_index >= len(items):
            return {
                "success": False,
                "error": f"Item {item_index} no valido",
            }

        item = items[item_index]
        item["completado"] = not item["completado"]
        item["fecha_completado"] = datetime.now().isoformat() if item["completado"] else None

        self._save()

        status = "completado" if item["completado"] else "pendiente"
        return {
            "success": True,
            "item": item,
            "message": f"'{item['item']}' marcado como {status}",
        }

    def add_custom_item(
        self, proyecto_id: str, phase: str, item_text: str
    ) -> Dict[str, Any]:
        """Add a custom item to a checklist."""
        self._load()

        checklist = self._checklists.get(proyecto_id)
        if not checklist:
            result = self.create_project_checklist(proyecto_id)
            if not result["success"]:
                return result
            checklist = self._checklists[proyecto_id]

        phases = checklist.setdefault("phases", {})
        phase_items = phases.setdefault(phase, [])

        phase_items.append({
            "item": item_text,
            "completado": False,
            "fecha_completado": None,
            "custom": True,
        })

        self._save()

        return {
            "success": True,
            "message": f"Item agregado a {phase}: {item_text}",
        }

    def get_progress(self, proyecto_id: str) -> Dict[str, Any]:
        """Get checklist progress for a project."""
        self._load()

        checklist = self._checklists.get(proyecto_id)
        if not checklist:
            return {
                "success": False,
                "error": f"No hay checklist para {proyecto_id}",
            }

        phases = checklist.get("phases", {})

        total_items = 0
        completed_items = 0
        phase_progress = {}

        for phase, items in phases.items():
            phase_total = len(items)
            phase_completed = sum(1 for item in items if item["completado"])
            total_items += phase_total
            completed_items += phase_completed

            phase_progress[phase] = {
                "total": phase_total,
                "completados": phase_completed,
                "progreso": round(phase_completed / phase_total * 100, 1) if phase_total > 0 else 0,
            }

        overall_progress = round(completed_items / total_items * 100, 1) if total_items > 0 else 0

        return {
            "success": True,
            "proyecto_id": proyecto_id,
            "total_items": total_items,
            "completados": completed_items,
            "progreso_general": overall_progress,
            "por_fase": phase_progress,
        }

    def format_checklist(self, proyecto_id: str) -> str:
        """Format checklist for display."""
        self._load()

        checklist = self._checklists.get(proyecto_id)
        if not checklist:
            return f"No hay checklist para {proyecto_id}."

        progress = self.get_progress(proyecto_id)
        lines = [
            f"Checklist — {proyecto_id}",
            f"Progreso: {progress['progreso_general']}% ({progress['completados']}/{progress['total_items']})",
            "",
        ]

        for phase, items in checklist.get("phases", {}).items():
            phase_prog = progress["por_fase"].get(phase, {})
            lines.append(
                f"{phase.replace('-', ' ').title()} ({phase_prog.get('completados', 0)}/{phase_prog.get('total', 0)})"
            )

            for item in items:
                check = "[x]" if item["completado"] else "[ ]"
                lines.append(f"  {check} {item['item']}")

            lines.append("")

        return "\n".join(lines)

    def format_progress(self, proyecto_id: str) -> str:
        """Format progress for display."""
        progress = self.get_progress(proyecto_id)

        if not progress["success"]:
            return progress["error"]

        lines = [
            f"Progreso — {proyecto_id}",
            "",
            f"{progress['completados']}/{progress['total_items']} items completados",
            f"Progreso general: {progress['progreso_general']}%",
            "",
        ]

        filled = int(progress['progreso_general'] / 10)
        bar = "=" * filled + "-" * (10 - filled)
        lines.append(f"[{bar}] {progress['progreso_general']}%")
        lines.append("")

        for phase, data in progress["por_fase"].items():
            phase_filled = int(data["progreso"] / 10)
            phase_bar = "=" * phase_filled + "-" * (10 - phase_filled)
            lines.append(f"{phase.replace('-', ' ').title()}: [{phase_bar}] {data['progreso']}%")

        return "\n".join(lines)


# Singleton
_checklists_instance = None


def get_checklists() -> Checklists:
    """Get or create singleton Checklists instance."""
    global _checklists_instance
    if _checklists_instance is None:
        _checklists_instance = Checklists()
    return _checklists_instance
