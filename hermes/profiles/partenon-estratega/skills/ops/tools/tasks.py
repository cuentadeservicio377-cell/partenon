"""
Partenon Estratega — Tasks Tool
Manages tasks within projects.
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


class Tareas:
    """Task management tool."""

    TASK_STATUSES = [
        "pendiente",
        "en_progreso",
        "bloqueada",
        "completada",
        "cancelada",
    ]

    PRIORITIES = {
        "baja": 1,
        "media": 2,
        "alta": 3,
        "urgente": 4,
    }

    def __init__(self):
        self.data_dir = _resolve_data_dir()
        self.tasks_file = self.data_dir / "tasks.json"
        self._tasks = None
        self._next_id = 1

    def _load(self) -> List[Dict[str, Any]]:
        """Load tasks from JSON."""
        if self._tasks is not None:
            return self._tasks

        if self.tasks_file.exists():
            try:
                with open(self.tasks_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._tasks = data.get("tasks", [])
                    self._next_id = data.get("next_id", 1)
                    return self._tasks
            except Exception:
                pass

        self._tasks = []
        self._next_id = 1
        return self._tasks

    def _save(self):
        """Save tasks to JSON."""
        data = {
            "tasks": self._tasks,
            "next_id": self._next_id,
            "updated_at": datetime.now().isoformat(),
        }
        with open(self.tasks_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _generate_task_id(self) -> str:
        """Generate task ID (TASK-001, TASK-002, etc.)."""
        task_id = f"TASK-{self._next_id:03d}"
        self._next_id += 1
        return task_id

    def create_task(
        self,
        proyecto_id: str,
        titulo: str,
        descripcion: str = None,
        responsable: str = None,
        fecha_vencimiento: str = None,
        prioridad: str = "media",
        dependencias: List[str] = None,
        etiquetas: List[str] = None,
    ) -> Dict[str, Any]:
        """Create a new task."""
        self._load()

        if prioridad not in self.PRIORITIES:
            prioridad = "media"

        if fecha_vencimiento and isinstance(fecha_vencimiento, str):
            try:
                fecha_vencimiento_dt = datetime.fromisoformat(fecha_vencimiento.replace("Z", "+00:00"))
            except ValueError:
                fecha_vencimiento_dt = datetime.now() + timedelta(days=7)
        else:
            fecha_vencimiento_dt = datetime.now() + timedelta(days=7)

        task = {
            "id": self._generate_task_id(),
            "proyecto_id": proyecto_id,
            "titulo": titulo,
            "descripcion": descripcion or "",
            "responsable": responsable or "No asignado",
            "estado": "pendiente",
            "prioridad": prioridad,
            "prioridad_valor": self.PRIORITIES[prioridad],
            "fecha_creacion": datetime.now().isoformat(),
            "fecha_vencimiento": fecha_vencimiento_dt.isoformat(),
            "fecha_completado": None,
            "dependencias": dependencias or [],
            "etiquetas": etiquetas or [],
            "comentarios": [],
        }

        self._tasks.append(task)
        self._save()

        return {
            "success": True,
            "tarea": task,
            "message": f"Tarea creada: {titulo} ({task['id']})",
        }

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task by ID."""
        self._load()

        for task in self._tasks:
            if task["id"].lower() == task_id.lower():
                return task

        return None

    def update_task(self, task_id: str, **updates) -> Dict[str, Any]:
        """Update task fields."""
        self._load()

        for task in self._tasks:
            if task["id"].lower() == task_id.lower():
                safe_updates = {
                    k: v
                    for k, v in updates.items()
                    if k not in ["id", "proyecto_id", "fecha_creacion"]
                }
                task.update(safe_updates)
                self._save()

                return {
                    "success": True,
                    "tarea": task,
                    "message": f"Tarea {task_id} actualizada",
                }

        return {
            "success": False,
            "error": f"Tarea {task_id} no encontrada",
        }

    def complete_task(self, task_id: str, comentario: str = None) -> Dict[str, Any]:
        """Mark task as completed."""
        result = self.update_task(
            task_id,
            estado="completada",
            fecha_completado=datetime.now().isoformat(),
        )

        if result["success"] and comentario:
            task = result["tarea"]
            task["comentarios"].append({
                "tipo": "completado",
                "texto": comentario,
                "fecha": datetime.now().isoformat(),
            })
            self._save()

        if result["success"]:
            result["message"] = f"Tarea {task_id} completada"

        return result

    def list_tasks(
        self,
        proyecto_id: str = None,
        estado: str = None,
        responsable: str = None,
        prioridad: str = None,
    ) -> List[Dict[str, Any]]:
        """List tasks with optional filters."""
        self._load()

        tasks = self._tasks

        if proyecto_id:
            tasks = [t for t in tasks if t["proyecto_id"].lower() == proyecto_id.lower()]

        if estado:
            tasks = [t for t in tasks if t["estado"] == estado]

        if responsable:
            tasks = [t for t in tasks if responsable.lower() in t["responsable"].lower()]

        if prioridad:
            tasks = [t for t in tasks if t["prioridad"] == prioridad]

        tasks.sort(key=lambda t: (-t["prioridad_valor"], t["fecha_vencimiento"]))

        return tasks

    def get_pending_tasks(self, proyecto_id: str = None) -> List[Dict[str, Any]]:
        """Get pending tasks."""
        return self.list_tasks(proyecto_id=proyecto_id, estado="pendiente")

    def get_tasks_by_project(self, proyecto_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a project."""
        return self.list_tasks(proyecto_id=proyecto_id)

    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """Get overdue tasks."""
        self._load()
        now = datetime.now()

        overdue = []
        for task in self._tasks:
            if task["estado"] in ["pendiente", "en_progreso", "bloqueada"]:
                fecha_vencimiento = datetime.fromisoformat(task["fecha_vencimiento"])
                if fecha_vencimiento < now:
                    overdue.append(task)

        overdue.sort(key=lambda t: -t["prioridad_valor"])
        return overdue

    def get_tasks_summary(self, proyecto_id: str = None) -> Dict[str, Any]:
        """Get tasks summary."""
        tasks = self.list_tasks(proyecto_id=proyecto_id)

        total = len(tasks)
        pendientes = len([t for t in tasks if t["estado"] == "pendiente"])
        en_progreso = len([t for t in tasks if t["estado"] == "en_progreso"])
        bloqueadas = len([t for t in tasks if t["estado"] == "bloqueada"])
        completadas = len([t for t in tasks if t["estado"] == "completada"])
        vencidas = len([
            t for t in tasks
            if t["estado"] in ["pendiente", "en_progreso", "bloqueada"]
            and datetime.fromisoformat(t["fecha_vencimiento"]) < datetime.now()
        ])

        completion_rate = (completadas / total * 100) if total > 0 else 0

        return {
            "total": total,
            "pendientes": pendientes,
            "en_progreso": en_progreso,
            "bloqueadas": bloqueadas,
            "completadas": completadas,
            "vencidas": vencidas,
            "tasa_completado": round(completion_rate, 1),
            "proximas_vencimientos": self._get_upcoming_deadlines(proyecto_id),
        }

    def _get_upcoming_deadlines(
        self, proyecto_id: str = None, days: int = 3
    ) -> List[Dict[str, Any]]:
        """Get tasks with deadlines in the next N days."""
        self._load()
        now = datetime.now()
        upcoming = []

        for task in self._tasks:
            if task["estado"] in ["pendiente", "en_progreso", "bloqueada"]:
                if proyecto_id and task["proyecto_id"].lower() != proyecto_id.lower():
                    continue

                fecha_vencimiento = datetime.fromisoformat(task["fecha_vencimiento"])
                days_left = (fecha_vencimiento - now).days

                if 0 <= days_left <= days:
                    upcoming.append({
                        "tarea": task,
                        "dias_restantes": days_left,
                        "fecha_vencimiento": fecha_vencimiento.strftime("%Y-%m-%d"),
                    })

        upcoming.sort(key=lambda x: x["dias_restantes"])
        return upcoming

    def format_task_list(self, tasks: List[Dict[str, Any]], title: str = "Tareas") -> str:
        """Format task list for display."""
        if not tasks:
            return f"No hay {title.lower()}."

        lines = [f"{title} ({len(tasks)})", ""]

        status_markers = {
            "pendiente": "[ ]",
            "en_progreso": "[~]",
            "bloqueada": "[B]",
            "completada": "[x]",
            "cancelada": "[-]",
        }

        priority_markers = {
            "baja": "",
            "media": "",
            "alta": "ALTA",
            "urgente": "URGENTE",
        }

        for task in tasks:
            status_marker = status_markers.get(task["estado"], "•")
            priority_marker = priority_markers.get(task["prioridad"], "")

            fecha_vencimiento = datetime.fromisoformat(task["fecha_vencimiento"])
            is_overdue = (
                fecha_vencimiento < datetime.now()
                and task["estado"] not in ["completada", "cancelada"]
            )
            overdue_marker = " VENCIDA" if is_overdue else ""

            lines.append(
                f"{status_marker} {priority_marker} {task['titulo']} ({task['id']}){overdue_marker}"
            )
            lines.append(f"   Estado: {task['estado']} | Prioridad: {task['prioridad']}")
            lines.append(
                f"   Responsable: {task['responsable']} | Vence: {fecha_vencimiento.strftime('%Y-%m-%d')}"
            )

            if task["descripcion"]:
                lines.append(f"   {task['descripcion'][:80]}...")

            lines.append("")

        return "\n".join(lines)

    def format_tasks_summary(self, summary: Dict[str, Any]) -> str:
        """Format tasks summary for display."""
        lines = [
            "Resumen de Tareas",
            "",
            f"Total: {summary['total']}",
            f"Pendientes: {summary['pendientes']}",
            f"En progreso: {summary['en_progreso']}",
            f"Bloqueadas: {summary['bloqueadas']}",
            f"Completadas: {summary['completadas']}",
            f"Vencidas: {summary['vencidas']}",
            f"Tasa de completado: {summary['tasa_completado']}%",
        ]

        if summary["proximas_vencimientos"]:
            lines.extend(["", "Proximas vencimientos:"])
            for item in summary["proximas_vencimientos"]:
                task = item["tarea"]
                marker = "URGENTE" if item["dias_restantes"] <= 1 else "proximo"
                lines.append(
                    f"{marker} {task['titulo']} — {item['dias_restantes']} dias ({item['fecha_vencimiento']})"
                )

        return "\n".join(lines)


# Singleton
_tareas_instance = None


def get_tareas() -> Tareas:
    """Get or create singleton Tareas instance."""
    global _tareas_instance
    if _tareas_instance is None:
        _tareas_instance = Tareas()
    return _tareas_instance
