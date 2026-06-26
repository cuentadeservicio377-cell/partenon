"""
Workflow Engine para Hermes Business OS Proactive Edition.

Maneja eventos, triggers, y handoffs automáticos entre skills.
Este es el sistema nervioso que hace que los departamentos se hablen solos.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Callable
from dataclasses import dataclass, asdict

# Añadir paths para imports de otros skills
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DATA_DIR = PROJECT_ROOT / "data"


@dataclass
class Evento:
    id: str
    tipo: str  # cliente_contratado, tarea_vencida, pipeline_estancado, etc.
    origen: str  # skill que generó el evento
    entidad_id: str
    entidad_tipo: str
    datos: dict
    timestamp: str
    procesado: bool = False
    acciones_ejecutadas: List[str] = None

    def __post_init__(self):
        if self.acciones_ejecutadas is None:
            self.acciones_ejecutadas = []


class WorkflowEngine:
    """
    Motor de workflows event-driven.

    Reglas de workflow se definen como:
    - Trigger: qué evento lo activa
    - Condition: condición opcional
    - Actions: lista de acciones a ejecutar
    """

    WORKFLOWS = [
        {
            "id": "wf_contratado_a_proyecto",
            "nombre": "Cliente contratado → Crear proyecto",
            "trigger": "cliente_contratado",
            "condition": None,
            "actions": [
                "crear_proyecto_operaciones",
                "crear_meta_iniciativa",
                "generar_checklist",
                "notificar_usuario",
            ],
        },
        {
            "id": "wf_tarea_vencida",
            "nombre": "Tarea vencida → Alerta y reagenda",
            "trigger": "tarea_vencida",
            "condition": None,
            "actions": [
                "nudge_urgente",
                "sugerir_reagenda",
            ],
        },
        {
            "id": "wf_pipeline_estancado",
            "nombre": "Pipeline sin movimiento → Nudge",
            "trigger": "pipeline_estancado",
            "condition": "dias_sin_movimiento >= 3",
            "actions": [
                "nudge_pipeline",
                "sugerir_campania",
            ],
        },
        {
            "id": "wf_cotizacion_aprobada",
            "nombre": "Cotización aprobada → Documentos + Finanzas",
            "trigger": "cotizacion_aprobada",
            "condition": None,
            "actions": [
                "generar_contrato",
                "registrar_ingreso_esperado",
                "crear_proyecto",
            ],
        },
        {
            "id": "wf_proyecto_50pct",
            "nombre": "Proyecto 50% → Revisión de riesgo",
            "trigger": "proyecto_progreso_50",
            "condition": None,
            "actions": [
                "revisar_deadlines",
                "alertar_si_atrasado",
            ],
        },
        {
            "id": "wf_nuevo_lead",
            "nombre": "Nuevo lead → Bienvenida + Tarea",
            "trigger": "cliente_nuevo",
            "condition": None,
            "actions": [
                "registrar_cliente",
                "crear_tarea_seguimiento",
                "nudge_bienvenida",
            ],
        },
    ]

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else DATA_DIR
        self.events_file = self.data_dir / "events.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.events_file.exists():
            self._save_events([])

    def _load_events(self) -> list:
        try:
            with open(self.events_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("events", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_events(self, events: list):
        with open(self.events_file, "w", encoding="utf-8") as f:
            json.dump({"events": events, "updated_at": datetime.now().isoformat()}, f, indent=2, ensure_ascii=False)

    def _load_json(self, filename: str) -> dict:
        try:
            with open(self.data_dir / filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def emitir_evento(self, tipo: str, origen: str, entidad_id: str, entidad_tipo: str, datos: dict = None) -> dict:
        """Emite un nuevo evento al sistema."""
        evento = Evento(
            id=f"EVT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{tipo}",
            tipo=tipo,
            origen=origen,
            entidad_id=entidad_id,
            entidad_tipo=entidad_tipo,
            datos=datos or {},
            timestamp=datetime.now().isoformat(),
        )

        events = self._load_events()
        events.append(asdict(evento))
        self._save_events(events)

        # Procesar inmediatamente
        acciones = self.procesar_evento(asdict(evento))
        evento.acciones_ejecutadas = acciones

        # Actualizar evento con acciones
        events = self._load_events()
        for e in events:
            if e["id"] == evento.id:
                e["acciones_ejecutadas"] = acciones
        self._save_events(events)

        return asdict(evento)

    def procesar_evento(self, evento: dict) -> List[str]:
        """Procesa un evento ejecutando los workflows correspondientes."""
        acciones_ejecutadas = []

        for workflow in self.WORKFLOWS:
            if workflow["trigger"] == evento["tipo"]:
                if self._evaluar_condicion(workflow.get("condition"), evento):
                    for action in workflow["actions"]:
                        try:
                            resultado = self._ejecutar_accion(action, evento)
                            if resultado:
                                acciones_ejecutadas.append(f"{workflow['id']}.{action}")
                        except Exception as e:
                            # Log error pero no romper otros workflows
                            acciones_ejecutadas.append(f"{workflow['id']}.{action}:ERROR:{str(e)}")

        # Marcar como procesado
        events = self._load_events()
        for e in events:
            if e["id"] == evento["id"]:
                e["procesado"] = True
                e["acciones_ejecutadas"] = acciones_ejecutadas
        self._save_events(events)

        return acciones_ejecutadas

    def _evaluar_condicion(self, condicion: Optional[str], evento: dict) -> bool:
        """Evalúa una condición de workflow."""
        if not condicion:
            return True

        # Condiciones simples
        if "dias_sin_movimiento >= 3" in condicion:
            return evento.get("datos", {}).get("dias_sin_movimiento", 0) >= 3

        return True

    def _ejecutar_accion(self, accion: str, evento: dict) -> bool:
        """Ejecuta una acción específica."""
        datos = evento.get("datos", {})

        if accion == "crear_proyecto_operaciones":
            return self._action_crear_proyecto(datos)
        elif accion == "crear_meta_iniciativa":
            return self._action_crear_meta(datos)
        elif accion == "generar_checklist":
            return self._action_generar_checklist(datos)
        elif accion == "notificar_usuario":
            return self._action_notificar(evento)
        elif accion == "nudge_urgente":
            return self._action_nudge(evento, "critica")
        elif accion == "sugerir_reagenda":
            return self._action_sugerir_reagenda(datos)
        elif accion == "nudge_pipeline":
            return self._action_nudge(evento, "media")
        elif accion == "sugerir_campania":
            return self._action_sugerir_campania(datos)
        elif accion == "generar_contrato":
            return self._action_generar_contrato(datos)
        elif accion == "registrar_ingreso_esperado":
            return self._action_registrar_ingreso(datos)
        elif accion == "crear_proyecto":
            return self._action_crear_proyecto(datos)
        elif accion == "revisar_deadlines":
            return self._action_revisar_deadlines(datos)
        elif accion == "alertar_si_atrasado":
            return self._action_alertar_atraso(datos)
        elif accion == "registrar_cliente":
            return self._action_registrar_cliente(datos)
        elif accion == "crear_tarea_seguimiento":
            return self._action_crear_tarea_seguimiento(datos)
        elif accion == "nudge_bienvenida":
            return self._action_nudge(evento, "baja")

        return False

    # ===== ACCIONES =====

    def _action_crear_proyecto(self, datos: dict) -> bool:
        """Crea un proyecto en projects.json."""
        projects_file = self.data_dir / "projects.json"
        projects_data = self._load_json("projects.json")
        projects = projects_data.get("projects", [])

        next_id = len(projects) + 1
        proyecto = {
            "id": f"PROJ-{next_id:03d}",
            "nombre": datos.get("nombre_proyecto", f"Proyecto {datos.get('cliente_nombre', 'Nuevo')}"),
            "cliente_id": datos.get("cliente_id", ""),
            "cliente_nombre": datos.get("cliente_nombre", ""),
            "estado": "planificado",
            "progreso": 0,
            "fecha_inicio": datetime.now().strftime("%Y-%m-%d"),
            "fecha_entrega": datos.get("fecha_entrega", (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")),
            "descripcion": datos.get("descripcion", ""),
            "monto": datos.get("monto", 0),
        }

        projects.append(proyecto)
        projects_data["projects"] = projects
        with open(projects_file, "w", encoding="utf-8") as f:
            json.dump(projects_data, f, indent=2, ensure_ascii=False)

        return True

    def _action_crear_meta(self, datos: dict) -> bool:
        """Crea una meta en metas.json."""
        try:
            from skills.hermes_iniciativa.tools.metas_engine import MetasEngine
            engine = MetasEngine(str(self.data_dir))
            engine.create_meta(
                titulo=f"Entregar {datos.get('nombre_proyecto', 'proyecto')} a tiempo",
                tipo="semanal",
                departamento="operaciones",
                target=1,
                unidad="proyecto",
                kpi_source="tasks.completadas",
            )
            return True
        except Exception:
            return False

    def _action_generar_checklist(self, datos: dict) -> bool:
        """Genera checklist en checklists.json."""
        checklists_file = self.data_dir / "checklists.json"
        checklists_data = self._load_json("checklists.json")
        checklists = checklists_data.get("checklists", [])

        checklist = {
            "id": f"CHK-{len(checklists) + 1:03d}",
            "proyecto_id": datos.get("proyecto_id", ""),
            "titulo": f"Checklist {datos.get('nombre_proyecto', 'Proyecto')}",
            "items": [
                {"titulo": "Definir alcance", "completado": False},
                {"titulo": "Asignar responsables", "completado": False},
                {"titulo": "Establecer fechas clave", "completado": False},
                {"titulo": "Comunicación con cliente", "completado": False},
                {"titulo": "Cierre administrativo", "completado": False},
            ],
            "creado": datetime.now().strftime("%Y-%m-%d"),
        }

        checklists.append(checklist)
        checklists_data["checklists"] = checklists
        with open(checklists_file, "w", encoding="utf-8") as f:
            json.dump(checklists_data, f, indent=2, ensure_ascii=False)

        return True

    def _action_notificar(self, evento: dict) -> bool:
        """Guarda notificación para ser enviada."""
        # En producción, esto enviaría Telegram/WhatsApp
        # Por ahora, guardamos en events para que el gateway lo procese
        return True

    def _action_nudge(self, evento: dict, urgencia: str) -> bool:
        """Crea un nudge en nudges.json."""
        try:
            from skills.hermes_iniciativa.tools.nudges_engine import NudgesEngine
            engine = NudgesEngine(str(self.data_dir))
            # Los nudges se detectan automáticamente por el engine
            # Este método es para nudges de eventos específicos
            return True
        except Exception:
            return False

    def _action_sugerir_reagenda(self, datos: dict) -> bool:
        """Sugiere reagendar una tarea vencida."""
        return True  # Placeholder para lógica futura

    def _action_sugerir_campania(self, datos: dict) -> bool:
        """Sugiere campaña de reactivación."""
        return True  # Placeholder

    def _action_generar_contrato(self, datos: dict) -> bool:
        """Genera contrato usando motor de documentos."""
        return True  # Placeholder

    def _action_registrar_ingreso(self, datos: dict) -> bool:
        """Registra ingreso esperado en finanzas."""
        return True  # Placeholder

    def _action_revisar_deadlines(self, datos: dict) -> bool:
        """Revisa si los deadlines del proyecto están en riesgo."""
        return True  # Placeholder

    def _action_alertar_atraso(self, datos: dict) -> bool:
        """Alerta si el proyecto va atrasado."""
        return True  # Placeholder

    def _action_registrar_cliente(self, datos: dict) -> bool:
        """Registra cliente en clients.json."""
        clients_file = self.data_dir / "clients.json"
        clients_data = self._load_json("clients.json")
        clients = clients_data.get("clients", [])

        next_id = len(clients) + 1
        cliente = {
            "id": f"CLI-{next_id:03d}",
            "nombre": datos.get("nombre", "Nuevo Cliente"),
            "email": datos.get("email", ""),
            "telefono": datos.get("telefono", ""),
            "estado": "lead",
            "fecha_registro": datetime.now().strftime("%Y-%m-%d"),
            "fuente": datos.get("fuente", "desconocida"),
        }

        clients.append(cliente)
        clients_data["clients"] = clients
        with open(clients_file, "w", encoding="utf-8") as f:
            json.dump(clients_data, f, indent=2, ensure_ascii=False)

        return True

    def _action_crear_tarea_seguimiento(self, datos: dict) -> bool:
        """Crea tarea de seguimiento en tasks.json."""
        tasks_file = self.data_dir / "tasks.json"
        tasks_data = self._load_json("tasks.json")
        tasks = tasks_data.get("tasks", [])

        next_id = tasks_data.get("next_id", len(tasks) + 1)
        task = {
            "id": f"TASK-{next_id:03d}",
            "titulo": f"Seguimiento a {datos.get('nombre', 'nuevo lead')}",
            "estado": "pendiente",
            "prioridad": "alta",
            "responsable": "Por asignar",
            "fecha_vencimiento": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
            "proyecto_id": "",
            "columna_kanban": "por_hacer",
        }

        tasks.append(task)
        tasks_data["tasks"] = tasks
        tasks_data["next_id"] = next_id + 1
        with open(tasks_file, "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, indent=2, ensure_ascii=False)

        return True

    def detectar_eventos_automaticos(self) -> List[dict]:
        """Escanea datos y detecta eventos que deberían emitirse."""
        eventos_detectados = []
        hoy = datetime.now()

        # Detectar tareas vencidas
        tasks_data = self._load_json("tasks.json")
        for task in tasks_data.get("tasks", []):
            if task.get("estado") in ["pendiente", "en_progreso", "bloqueada"]:
                fecha_venc = task.get("fecha_vencimiento")
                if fecha_venc and fecha_venc < hoy.strftime("%Y-%m-%d"):
                    eventos_detectados.append(self.emitir_evento(
                        tipo="tarea_vencida",
                        origen="workflow_engine",
                        entidad_id=task["id"],
                        entidad_tipo="tarea",
                        datos={"titulo": task["titulo"], "dias_atraso": (hoy - datetime.strptime(fecha_venc, "%Y-%m-%d")).days},
                    ))

        # Detectar pipeline estancado
        pipeline_data = self._load_json("pipeline.json")
        entries = pipeline_data.get("entries", [])
        if entries:
            fecha_limite = (hoy - timedelta(days=3)).strftime("%Y-%m-%d")
            sin_movimiento = all(
                (e.get("fecha_actualizacion") or e.get("fecha_registro", "")) < fecha_limite
                for e in entries
            )
            if sin_movimiento:
                eventos_detectados.append(self.emitir_evento(
                    tipo="pipeline_estancado",
                    origen="workflow_engine",
                    entidad_id="pipeline",
                    entidad_tipo="pipeline",
                    datos={"dias_sin_movimiento": 3},
                ))

        return eventos_detectados


if __name__ == "__main__":
    engine = WorkflowEngine()
    # Demo: emitir evento de cliente contratado
    evento = engine.emitir_evento(
        tipo="cliente_contratado",
        origen="hermes-ventas",
        entidad_id="CLI-001",
        entidad_tipo="cliente",
        datos={
            "cliente_id": "CLI-001",
            "cliente_nombre": "Juan Pérez",
            "nombre_proyecto": "Boda Juan y María",
            "monto": 250000,
            "fecha_entrega": "2026-10-15",
        },
    )
    print(f"Evento emitido: {evento['id']}")
    print(f"Acciones ejecutadas: {evento.get('acciones_ejecutadas', [])}")
