"""
Partenon — Intent Router
Routes user messages to the appropriate hero profile.
"""

import re
from typing import Optional, Dict, Any


class IntentRouter:
    """Routes natural language intents to Partenon hero profiles."""

    INTENT_PATTERNS = {
        "partenon-tesorero": {
            "keywords": [
                "finanza", "finanzas", "presupuesto", "gasto", "gastos", "ingreso", "ingresos",
                "costo", "costos", "excel", "sheet", "spreadsheet", "dashboard", "numero",
                "numeros", "pago", "pagos", "cobro", "cobros", "factura", "facturas",
                "estado de cuenta", "flujo de caja", "margen", "rentabilidad", "iva",
            ],
            "patterns": [
                r"\b(ordena|acomoda|revisa)\s+(mis\s+)?(finanzas|numeros|gastos|cuentas)\b",
                r"\b(costo\s+fijo|costo\s+variable|gasto\s+fijo|gasto\s+variable)\b",
                r"\b(cuanto\s+(facturamos|ganamos|gastamos|debemos))\b",
            ]
        },
        "partenon-mensajero": {
            "keywords": [
                "marca", "branding", "comunicacion", "marketing", "redes", "social", "contenido",
                "campana", "campaña", "calendario", "seo", "geo", "post", "copy", "mensaje",
                "presentacion", "presentación", "carta", "mail", "email", "landing", "sitio",
                "wordpress", "blog", "lead magnet", "lead magnet",
            ],
            "patterns": [
                r"\b(crea|haz|genera)\s+(una\s+)?(campana|campaña|presentacion|presentación|publicacion|publicación)\b",
                r"\b(calendario\s+de\s+contenido|plan\s+de\s+contenido)\b",
                r"\b(voz\s+de\s+marca|mensaje\s+de\s+marca)\b",
            ]
        },
        "partenon-cobrador": {
            "keywords": [
                "cobrar", "cobranza", "cobro", "cobros", "pago", "pagos", "stripe", "link de pago",
                "suscripcion", "suscripción", "factura", "facturar", "tarjeta", "cliente\s+debe",
                "saldo", "adeudo", "recordatorio de pago",
            ],
            "patterns": [
                r"\b(genera|crea|envia)\s+(un\s+)?(link|enlace)\s+de\s+pago\b",
                r"\b(suscripcion|suscripción|recurrente|mensualidad)\b",
                r"\b(recordatorio\s+de\s+pago|cobrar\s+a)\b",
            ]
        },
        "partenon-guardian": {
            "keywords": [
                "seguridad", "api key", "api keys", "clave", "token", "permiso", "permisos",
                "modelo", "modelos", "nvidia", "openai", "kimi", "cuenta", "acceso", "accesos",
                "audit", "auditoria", "sandbox", "nemotron", "neoclaw",
            ],
            "patterns": [
                r"\b(rota|cambia|revoca)\s+(la\s+)?(api\s+key|clave|token)\b",
                r"\b(que\s+modelos|configura\s+modelos|administra\s+accesos)\b",
                r"\b(permisos\s+de\s+(tesorero|mensajero|cobrador|guardian|estratega|diplomatico))\b",
            ]
        },
        "partenon-estratega": {
            "keywords": [
                "proyecto", "proyectos", "tarea", "tareas", "pendiente", "pendientes",
                "checklist", "hito", "hitos", "deadline", "fecha", "calendario", "agenda",
                "recordatorio", "recordatorios", "asignar", "responsable", "equipo", "metas",
                "objetivos", "okr", "plan", "planeacion", "planificación", "semana", "mes",
            ],
            "patterns": [
                r"\b(crea|nuevo|inicia)\s+(un\s+)?(proyecto|hito)\b",
                r"\b(tareas?\s+pendientes?|que\s+tenemos\s+pendiente)\b",
                r"\b(calendario|agenda|recordatorio)\b",
                r"\b(briefing|plan\s+semanal|review\s+semanal)\b",
            ]
        },
        "partenon-diplomatico": {
            "keywords": [
                "cliente", "clientes", "proveedor", "proveedores", "aliado", "aliados",
                "relacion", "relación", "relaciones", "seguimiento", "contrato", "contratos",
                "hito", "hitos", "negociacion", "negociación", "acuerdo", "acuerdos",
                "satisfaccion", "satisfacción", "reunion", "reunión", "llamada",
            ],
            "patterns": [
                r"\b(dame\s+seguimiento\s+a|como\s+va)\s+(el\s+)?(cliente|proveedor)\b",
                r"\b(negocia|coordina)\s+(con\s+)?(cliente|proveedor)\b",
                r"\b(hitos?\s+del\s+(cliente|proveedor))\b",
            ]
        },
    }

    def __init__(self):
        # All Partenon profiles are active by default.
        self.active_profiles = set(self.INTENT_PATTERNS.keys())

    def route(self, message: str) -> Optional[str]:
        """Route a message to the appropriate profile. Returns profile name or None."""
        message_lower = message.lower()
        scores = {}

        for profile_name, patterns in self.INTENT_PATTERNS.items():
            if profile_name not in self.active_profiles:
                continue

            score = 0
            for keyword in patterns["keywords"]:
                if keyword in message_lower:
                    score += 1

            for pattern in patterns["patterns"]:
                if re.search(pattern, message_lower):
                    score += 3

            if score > 0:
                scores[profile_name] = score

        if not scores:
            return None

        return max(scores, key=scores.get)

    def route_with_context(
        self,
        message: str,
        last_profile: str = None,
        last_entity: str = None,
    ) -> Dict[str, Any]:
        """Route with conversation context."""
        result = {
            "profile": None,
            "entity": last_entity,
            "confidence": 0.0,
        }

        entity_match = re.search(r"\b([A-Z][a-z]+\s+[A-Z][a-z]+)\b", message)
        if entity_match:
            result["entity"] = entity_match.group(1)

        routed = self.route(message)
        if routed:
            result["profile"] = routed
            result["confidence"] = 0.8
        elif last_profile:
            result["profile"] = last_profile
            result["confidence"] = 0.5

        return result


_router_instance = None


def get_router() -> IntentRouter:
    """Get or create singleton router instance."""
    global _router_instance
    if _router_instance is None:
        _router_instance = IntentRouter()
    return _router_instance


def route_intent(message: str) -> Optional[str]:
    """Convenience function."""
    return get_router().route(message)
