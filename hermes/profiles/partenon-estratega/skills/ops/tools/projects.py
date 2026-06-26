"""
Partenon Estratega — Projects Tool
Manages projects, assignments, and project lifecycle.
"""

import json
from datetime import datetime, timedelta
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


class Proyectos:
    """Project management tool."""

    PROJECT_STATUSES = [
        "planificado",
        "en_progreso",
        "pausado",
        "completado",
        "cancelado",
        "entregado",
    ]

    def __init__(self):
        self.industria = _default_industry()
        self.data_dir = _resolve_data_dir()
        self.projects_file = self.data_dir / "projects.json"
        self._projects = None
        self._next_id = 1

    def _load(self) -> List[Dict[str, Any]]:
        """Load projects from JSON."""
        if self._projects is not None:
            return self._projects

        if self.projects_file.exists():
            try:
                with open(self.projects_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._projects = data.get("projects", [])
                    self._next_id = data.get("next_id", 1)
                    return self._projects
            except Exception:
                pass

        self._projects = []
        self._next_id = 1
        return self._projects

    def _save(self):
        """Save projects to JSON."""
        data = {
            "projects": self._projects,
            "next_id": self._next_id,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.projects_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _generate_project_id(self) -> str:
        """Generate project ID (PROJ-001, PROJ-002, etc.)."""
        project_id = f"PROJ-{self._next_id:03d}"
        self._next_id += 1
        return project_id

    def create_project(
        self,
        nombre: str,
        cliente_id: str = None,
        cliente_nombre: str = None,
        descripcion: str = None,
        fecha_inicio: str = None,
        fecha_entrega: str = None,
        monto: float = 0,
        tipo: str = None,
        notas: str = None,
    ) -> Dict[str, Any]:
        """Create a new project."""
        self._load()

        if fecha_inicio and isinstance(fecha_inicio, str):
            try:
                fecha_inicio_dt = datetime.fromisoformat(fecha_inicio.replace("Z", "+00:00"))
            except ValueError:
                fecha_inicio_dt = datetime.now()
        else:
            fecha_inicio_dt = datetime.now()

        if fecha_entrega and isinstance(fecha_entrega, str):
            try:
                fecha_entrega_dt = datetime.fromisoformat(fecha_entrega.replace("Z", "+00:00"))
            except ValueError:
                fecha_entrega_dt = fecha_inicio_dt + timedelta(days=30)
        else:
            fecha_entrega_dt = fecha_inicio_dt + timedelta(days=30)

        project = {
            "id": self._generate_project_id(),
            "nombre": nombre,
            "cliente_id": cliente_id,
            "cliente_nombre": cliente_nombre or "Cliente no especificado",
            "descripcion": descripcion or "",
            "tipo": tipo or self.industria,
            "estado": "planificado",
            "monto": monto,
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_inicio": fecha_inicio_dt.isoformat(),
            "fecha_entrega": fecha_entrega_dt.isoformat(),
            "fecha_completado": None,
            "progreso": 0,
            "tareas": [],
            "checklist": [],
            "notas": notas or "",
            "historial": [
                {"accion": "Creacion", "fecha": datetime.now().isoformat()}
            ],
        }

        self._projects.append(project)
        self._save()

        return {
            "success": True,
            "proyecto": project,
            "message": f"Proyecto creado: {nombre} ({project['id']})",
        }

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project by ID."""
        self._load()

        for project in self._projects:
            if project["id"].lower() == project_id.lower():
                return project

        return None

    def find_project(self, query: str) -> Optional[Dict[str, Any]]:
        """Find project by name or ID."""
        self._load()

        query_lower = query.lower()

        for project in self._projects:
            if project["id"].lower() == query_lower:
                return project
            if query_lower in project["nombre"].lower():
                return project

        return None

    def update_project(self, project_id: str, **updates) -> Dict[str, Any]:
        """Update project fields."""
        self._load()

        for project in self._projects:
            if project["id"].lower() == project_id.lower():
                safe_updates = {
                    k: v
                    for k, v in updates.items()
                    if k not in ["id", "historial", "tareas", "checklist"]
                }
                project.update(safe_updates)
                project["historial"].append({
                    "accion": f"Actualizacion: {', '.join(safe_updates.keys())}",
                    "fecha": datetime.now().isoformat(),
                })
                self._save()

                return {
                    "success": True,
                    "proyecto": project,
                    "message": f"Proyecto {project_id} actualizado",
                }

        return {
            "success": False,
            "error": f"Proyecto {project_id} no encontrado",
        }

    def update_status(
        self, project_id: str, nuevo_estado: str, notas: str = None
    ) -> Dict[str, Any]:
        """Update project status."""
        if nuevo_estado not in self.PROJECT_STATUSES:
            return {
                "success": False,
                "error": f"Estado invalido. Validos: {', '.join(self.PROJECT_STATUSES)}",
            }

        self._load()

        for project in self._projects:
            if project["id"].lower() == project_id.lower():
                estado_anterior = project["estado"]
                project["estado"] = nuevo_estado

                if nuevo_estado == "completado":
                    project["fecha_completado"] = datetime.now().isoformat()
                    project["progreso"] = 100

                project["historial"].append({
                    "accion": f"Cambio de estado: {estado_anterior} -> {nuevo_estado}",
                    "fecha": datetime.now().isoformat(),
                    "notas": notas or "",
                })
                self._save()

                return {
                    "success": True,
                    "proyecto": project,
                    "message": f"{project['nombre']}: {estado_anterior} -> {nuevo_estado}",
                }

        return {
            "success": False,
            "error": f"Proyecto {project_id} no encontrado",
        }

    def update_progress(self, project_id: str, progreso: int) -> Dict[str, Any]:
        """Update project progress percentage."""
        progreso = max(0, min(100, progreso))

        result = self.update_project(project_id, progreso=progreso)

        if result["success"]:
            result["message"] = f"Progreso de {project_id}: {progreso}%"

        return result

    def list_projects(
        self, estado: str = None, cliente_id: str = None
    ) -> List[Dict[str, Any]]:
        """List projects, optionally filtered."""
        self._load()

        projects = self._projects

        if estado:
            projects = [p for p in projects if p["estado"] == estado]

        if cliente_id:
            projects = [p for p in projects if p.get("cliente_id") == cliente_id]

        return projects

    def get_active_projects(self) -> List[Dict[str, Any]]:
        """Get active (non-completed) projects."""
        return self.list_projects()

    def get_overdue_projects(self) -> List[Dict[str, Any]]:
        """Get projects past their delivery date."""
        self._load()
        now = datetime.now()

        overdue = []
        for project in self._projects:
            if project["estado"] in ["planificado", "en_progreso", "pausado"]:
                fecha_entrega = datetime.fromisoformat(project["fecha_entrega"])
                if fecha_entrega < now:
                    overdue.append(project)

        return overdue

    def get_projects_summary(self) -> Dict[str, Any]:
        """Get projects summary."""
        self._load()

        total = len(self._projects)
        activos = len([p for p in self._projects if p["estado"] in ["planificado", "en_progreso", "pausado"]])
        completados = len([p for p in self._projects if p["estado"] in ["completado", "entregado"]])
        atrasados = len(self.get_overdue_projects())

        active_projects = [p for p in self._projects if p["estado"] in ["planificado", "en_progreso"]]
        avg_progress = (
            sum(p["progreso"] for p in active_projects) / len(active_projects)
            if active_projects
            else 0
        )

        return {
            "total": total,
            "activos": activos,
            "completados": completados,
            "atrasados": atrasados,
            "cancelados": len([p for p in self._projects if p["estado"] == "cancelado"]),
            "promedio_progreso": round(avg_progress, 1),
            "proximos_vencimientos": self._get_upcoming_deadlines(),
        }

    def _get_upcoming_deadlines(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get projects with deadlines in the next N days."""
        self._load()
        now = datetime.now()
        upcoming = []

        for project in self._projects:
            if project["estado"] in ["planificado", "en_progreso"]:
                fecha_entrega = datetime.fromisoformat(project["fecha_entrega"])
                days_left = (fecha_entrega - now).days

                if 0 <= days_left <= days:
                    upcoming.append({
                        "proyecto": project,
                        "dias_restantes": days_left,
                        "fecha_entrega": fecha_entrega.strftime("%Y-%m-%d"),
                    })

        upcoming.sort(key=lambda x: x["dias_restantes"])
        return upcoming

    def format_project_summary(self, summary: Dict[str, Any]) -> str:
        """Format projects summary for display."""
        lines = [
            "Resumen de Proyectos",
            "",
            f"Total: {summary['total']}",
            f"Activos: {summary['activos']}",
            f"Completados: {summary['completados']}",
            f"Atrasados: {summary['atrasados']}",
            f"Promedio de progreso: {summary['promedio_progreso']}%",
        ]

        if summary["proximos_vencimientos"]:
            lines.extend(["", "Proximos vencimientos:"])
            for item in summary["proximos_vencimientos"]:
                proyecto = item["proyecto"]
                marker = "URGENTE" if item["dias_restantes"] <= 2 else "proximo"
                lines.append(
                    f"{marker} {proyecto['nombre']} — {item['dias_restantes']} dias ({item['fecha_entrega']})"
                )

        return "\n".join(lines)


# Singleton
_proyectos_instance = None


def get_proyectos() -> Proyectos:
    """Get or create singleton Proyectos instance."""
    global _proyectos_instance
    if _proyectos_instance is None:
        _proyectos_instance = Proyectos()
    return _proyectos_instance
