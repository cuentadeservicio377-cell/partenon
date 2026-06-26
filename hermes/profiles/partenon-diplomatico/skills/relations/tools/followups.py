"""
Partenon Diplomatico — Follow-ups Tool
Generates reminders and daily follow-up reports for clients and suppliers.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Allow importing crm.py from the same directory
sys.path.insert(0, str(Path(__file__).parent))

from crm import RelationsCRM, get_relations_crm


# Default follow-up windows in days
DEFAULT_FOLLOW_UP_WINDOWS = [1, 3, 7]


def _parse_date(value: str) -> Optional[datetime]:
    """Parse an ISO date string into a datetime object."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            return None


def _format_date(value: str) -> str:
    """Return a human-readable date string."""
    parsed = _parse_date(value)
    if parsed is None:
        return value
    return parsed.strftime("%Y-%m-%d")


def _today() -> datetime:
    """Return current datetime; overridable via PARTENON_TODAY for tests."""
    env_today = os.getenv("PARTENON_TODAY")
    if env_today:
        parsed = _parse_date(env_today)
        if parsed:
            return parsed
    return datetime.now()


def get_pending_followups(
    crm: Optional[RelationsCRM] = None,
    dias_alerta: Optional[List[int]] = None,
) -> List[Dict[str, Any]]:
    """
    Return pending reminders and milestones that need attention.

    Logic:
    - Reminders with fecha <= today and estado 'pendiente'.
    - Milestones with fecha <= today and estado not in closed/cancelled.
    - Urgency grows as the date passes.
    """
    crm = crm or get_relations_crm()
    data = crm._load()
    hoy = _today()
    ventanas = sorted(dias_alerta or DEFAULT_FOLLOW_UP_WINDOWS)
    followups: List[Dict[str, Any]] = []

    # Check explicit reminders
    for reminder in data.get("recordatorios", []):
        if reminder.get("estado") != "pendiente":
            continue

        fecha = _parse_date(reminder.get("fecha", ""))
        if fecha is None:
            continue

        dias_diferencia = (hoy - fecha).days
        if dias_diferencia < 0:
            continue

        urgencia = "baja"
        for umbral in ventanas:
            if dias_diferencia >= umbral:
                urgencia = "alta" if umbral == ventanas[-1] else "media"

        entity = crm._find_entity(data, reminder.get("entidad_id", ""))
        followups.append({
            "tipo": "recordatorio",
            "id": reminder["id"],
            "entidad": entity["nombre"] if entity else reminder.get("entidad_id", ""),
            "entidad_id": reminder.get("entidad_id", ""),
            "mensaje": reminder.get("mensaje", ""),
            "canal": reminder.get("canal", "email"),
            "fecha_objetivo": reminder.get("fecha", ""),
            "dias_retraso": dias_diferencia,
            "urgencia": urgencia,
            "accion_recomendada": _recommend_action(reminder.get("mensaje", ""), entity, dias_diferencia),
        })

    # Check milestones without written confirmation or past due
    for section in ["clientes", "proveedores"]:
        for entity in data.get(section, []):
            entity_id = entity.get("id", "")
            for hito in entity.get("hitos", []):
                estado = hito.get("estado", "")
                if estado in {"completado", "cerrado", "cancelado"}:
                    continue

                fecha = _parse_date(hito.get("fecha", ""))
                if fecha is None:
                    continue

                dias_diferencia = (hoy - fecha).days
                if dias_diferencia < -ventanas[-1]:
                    continue

                urgencia = "baja"
                if not hito.get("confirmado_escrito", False):
                    urgencia = "media"
                for umbral in ventanas:
                    if dias_diferencia >= umbral:
                        urgencia = "alta" if umbral == ventanas[-1] else "media"

                followups.append({
                    "tipo": "hito",
                    "id": hito["id"],
                    "entidad": entity.get("nombre", ""),
                    "entidad_id": entity_id,
                    "mensaje": hito.get("descripcion", ""),
                    "fecha_objetivo": hito.get("fecha", ""),
                    "estado_hito": estado,
                    "confirmado_escrito": hito.get("confirmado_escrito", False),
                    "dias_retraso": max(0, dias_diferencia),
                    "urgencia": urgencia,
                    "accion_recomendada": _recommend_hito_action(hito, entity, dias_diferencia),
                })

    followups.sort(key=lambda x: (x["urgencia"] != "alta", x["urgencia"] != "media", -x["dias_retraso"]))
    return followups


def _recommend_action(mensaje: str, entity: Optional[Dict[str, Any]], dias: int) -> str:
    """Recommend a follow-up action for a reminder."""
    nombre = entity["nombre"] if entity else "la entidad"
    if dias == 0:
        return f"Contactar hoy a {nombre}: {mensaje}"
    if dias <= 3:
        return f"Enviar recordatorio a {nombre}: {mensaje}"
    return f"Escalar seguimiento con {nombre}: {mensaje}"


def _recommend_hito_action(hito: Dict[str, Any], entity: Dict[str, Any], dias: int) -> str:
    """Recommend a follow-up action for a milestone."""
    nombre = entity.get("nombre", "la entidad")
    descripcion = hito.get("descripcion", "")
    confirmado = hito.get("confirmado_escrito", False)

    if not confirmado:
        return f"Solicitar confirmación escrita a {nombre} para: {descripcion}"

    if dias <= 0:
        return f"Verificar avance con {nombre} antes de: {hito.get('fecha', '')}"

    return f"Revisar bloqueo con {nombre} para: {descripcion}"


def build_reminder_message(followup: Dict[str, Any], firma: str = "") -> str:
    """Build a formal reminder message for a follow-up item."""
    nombre = followup.get("entidad", "")
    mensaje = followup.get("mensaje", "")
    fecha = _format_date(followup.get("fecha_objetivo", ""))
    dias = followup.get("dias_retraso", 0)
    tipo = followup.get("tipo", "seguimiento")

    subject = f"Seguimiento: {mensaje[:60]}"
    body_lines = [
        f"Estimado/a {nombre},",
        "",
        f"Nos ponemos en contacto para dar seguimiento a: {mensaje}.",
    ]

    if tipo == "hito":
        if not followup.get("confirmado_escrito", False):
            body_lines.append(f"La fecha acordada es {fecha}. Solicitamos confirmación por escrito para cerrar este punto.")
        else:
            body_lines.append(f"El hito está programado para {fecha}. Agradecemos validar el avance.")
    else:
        body_lines.append(f"Este recordatorio está programado para {fecha}.")

    if dias > 0:
        body_lines.append(f"Llevamos {dias} día(s) de diferencia con la fecha prevista.")

    body_lines.extend([
        "",
        "Quedamos atentos a tu respuesta.",
        "",
        "Saludos,",
        "El equipo de Partenon",
    ])

    if firma:
        body_lines.append(firma)

    return {
        "subject": subject,
        "body": "\n".join(body_lines),
    }


def schedule_reminder(
    entity_id: str,
    mensaje: str,
    fecha: str,
    canal: str = "email",
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """Schedule a new follow-up reminder."""
    crm = crm or get_relations_crm()
    return crm.add_recordatorio(entity_id, mensaje, fecha, canal=canal, tipo="seguimiento")


def run_daily_followups(
    dias_alerta: Optional[List[int]] = None,
    canales: Optional[List[str]] = None,
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """
    Daily cron entry point: list pending follow-ups and suggest actions.

    Returns a structured report. Sending emails or calendar events is left
    to the caller / MCP layer.
    """
    crm = crm or get_relations_crm()
    canales = canales or ["gmail", "google_workspace"]
    followups = get_pending_followups(crm=crm, dias_alerta=dias_alerta)

    report_lines = [
        "Seguimientos del día — Diplomático",
        f"Fecha: {_today().strftime('%Y-%m-%d')}",
        f"Total pendientes: {len(followups)}",
        "",
    ]

    actions = []
    for item in followups:
        urgencia = item["urgencia"].upper()
        entidad = item["entidad"]
        mensaje = item["mensaje"]
        accion = item["accion_recomendada"]

        report_lines.append(f"[{urgencia}] {entidad}: {mensaje}")
        report_lines.append(f"    Acción: {accion}")
        report_lines.append("")

        actions.append({
            "urgencia": item["urgencia"],
            "tipo": item["tipo"],
            "entidad_id": item["entidad_id"],
            "entidad": entidad,
            "mensaje": mensaje,
            "accion_recomendada": accion,
            "canales_sugeridos": canales,
        })

    if not followups:
        report_lines.append("No hay seguimientos pendientes por hoy.")

    return {
        "success": True,
        "total": len(followups),
        "fecha": _today().isoformat(),
        "report": "\n".join(report_lines),
        "actions": actions,
    }


if __name__ == "__main__":
    result = run_daily_followups()
    print(result["report"])
