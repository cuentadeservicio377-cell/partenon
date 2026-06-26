"""
Partenon Estratega — Briefings Tool
Generates morning briefing, midday pulse, evening wrap, weekly planning and weekly retro.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

# Robust import for MetasEngine: works as package or standalone script.
try:
    from .metas import MetasEngine
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from metas import MetasEngine


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


def _load_json(data_dir: Path, filename: str) -> Dict[str, Any]:
    try:
        with open(data_dir / filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _default_currency(data_dir: Path) -> str:
    """Read currency from empresa.yaml if available."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if parent.name == "partenon-core":
            config_path = parent / "config" / "empresa.yaml"
            break
        config_path = parent / "partenon-core" / "config" / "empresa.yaml"
        if config_path.exists():
            break
    else:
        return "MXN"

    if not config_path.exists():
        return "MXN"

    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("empresa", {}).get("moneda", "MXN")
    except Exception:
        return "MXN"


class Briefings:
    """Generates proactive daily and weekly briefings."""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else _resolve_data_dir()
        self.moneda = _default_currency(self.data_dir)

    def generar_morning_briefing(self, nombre_usuario: str = "Jefe") -> str:
        """Generate the morning briefing."""
        hoy = datetime.now()
        hoy_str = hoy.strftime("%Y-%m-%d")

        metas_data = _load_json(self.data_dir, "metas.json")
        tasks_data = _load_json(self.data_dir, "tasks.json")
        pipeline_data = _load_json(self.data_dir, "pipeline.json")
        projects_data = _load_json(self.data_dir, "projects.json")
        quotes_data = _load_json(self.data_dir, "quotes.json")
        clients_data = _load_json(self.data_dir, "clients.json")

        # 1. Weekly goals
        metas = metas_data.get("metas", [])
        metas_activas = [m for m in metas if m["estado"] == "activa"]
        metas_texto = []
        for meta in metas_activas[:3]:
            progreso = meta["progreso"]
            target = meta["target"]
            pct = (progreso / target * 100) if target > 0 else 0
            estado = "cumplida" if pct >= 100 else "a tiempo" if pct >= 50 else "atrasada"
            metas_texto.append(
                f"   {meta['titulo']} -> {progreso:.0f}/{target:.0f} ({pct:.0f}%) — {estado}"
            )

        if not metas_texto:
            metas_texto = ["   No hay metas activas. Definimos una para esta semana?"]

        # 2. Critical today
        tasks = tasks_data.get("tasks", [])
        critico_hoy = []
        for task in tasks:
            if task.get("estado") in ["pendiente", "en_progreso", "bloqueada"]:
                fecha_venc = task.get("fecha_vencimiento")
                if fecha_venc == hoy_str:
                    critico_hoy.append(f"   {task['titulo']} (vence hoy)")

        for task in tasks:
            if task.get("estado") in ["pendiente", "en_progreso", "bloqueada"]:
                fecha_venc = task.get("fecha_vencimiento")
                if fecha_venc and fecha_venc < hoy_str:
                    dias = (hoy - datetime.strptime(fecha_venc, "%Y-%m-%d")).days
                    critico_hoy.append(f"   {task['titulo']} (vencida hace {dias} dias)")

        entries = pipeline_data.get("entries", [])
        for entry in entries:
            if entry.get("estado") == "cotizado":
                fecha = entry.get("fecha_actualizacion") or entry.get("fecha_registro")
                if fecha:
                    try:
                        fdt = datetime.strptime(fecha, "%Y-%m-%d")
                        dias = (hoy - fdt).days
                        if dias >= 3:
                            critico_hoy.append(
                                f"   {entry.get('cliente_nombre', 'Cliente')} cotizado hace {dias} dias"
                            )
                    except ValueError:
                        pass

        if not critico_hoy:
            critico_hoy = ["   Nada critico hoy. Buen momento para avanzar en proyectos."]

        # 3. Pipeline
        total_value = sum(e.get("monto", 0) for e in entries)
        num_opps = len(entries)
        por_estado: Dict[str, int] = {}
        for e in entries:
            est = e.get("estado", "otro")
            por_estado[est] = por_estado.get(est, 0) + 1

        pipeline_texto = f"{num_opps} oportunidades, {self.moneda} {total_value:,.0f} en juego"
        if por_estado:
            pipeline_texto += f" ({', '.join(f'{v} {k}' for k, v in list(por_estado.items())[:3])})"

        # 4. Finances
        quotes = quotes_data.get("quotes", [])
        por_cobrar = [q for q in quotes if q.get("estado") == "aprobada"]
        total_por_cobrar = sum(q.get("total", 0) for q in por_cobrar)
        vencidos = []
        for q in por_cobrar:
            fecha_pago = q.get("fecha_pago_esperada")
            if fecha_pago and fecha_pago < hoy_str:
                vencidos.append(q)

        finanzas_texto = f"{self.moneda} {total_por_cobrar:,.0f} por cobrar"
        if vencidos:
            finanzas_texto += f" ({len(vencidos)} vencido{'s' if len(vencidos) > 1 else ''})"

        # 5. Alerts
        projects = projects_data.get("projects", [])
        atrasados = 0
        for p in projects:
            if p.get("estado") in ["planificado", "en_progreso", "pausado"]:
                fecha_entrega = p.get("fecha_entrega")
                if fecha_entrega and fecha_entrega < hoy_str:
                    atrasados += 1

        alertas = []
        if atrasados > 0:
            alertas.append(f"{atrasados} proyecto{'s' if atrasados > 1 else ''} atrasado{'s' if atrasados > 1 else ''}")

        clients = clients_data.get("clients", [])
        inicio_semana = (hoy - timedelta(days=hoy.weekday())).strftime("%Y-%m-%d")
        nuevos_esta_semana = [c for c in clients if c.get("fecha_registro", "") >= inicio_semana]
        if not nuevos_esta_semana:
            alertas.append("0 clientes nuevos esta semana")

        lineas = [
            f"Buenos dias, {nombre_usuario}.",
            "",
            "Metas de esta semana:",
        ]
        lineas.extend(metas_texto)
        lineas.append("")
        lineas.append("Critico hoy:")
        lineas.extend(critico_hoy[:5])
        lineas.append("")
        lineas.append(f"Pipeline: {pipeline_texto}")
        lineas.append(f"Finanzas: {finanzas_texto}")

        if alertas:
            lineas.append(f"Alertas: {', '.join(alertas)}")

        lineas.append("")
        lineas.append("Por cual empezamos?")

        return "\n".join(lineas)

    def generar_midday_pulse(self, nombre_usuario: str = "Jefe") -> str:
        """Generate the midday pulse."""
        hoy = datetime.now()
        hoy_str = hoy.strftime("%Y-%m-%d")

        tasks_data = _load_json(self.data_dir, "tasks.json")
        tasks = tasks_data.get("tasks", [])

        hecho_hoy = [t for t in tasks if t.get("fecha_completado") == hoy_str]
        pendientes = [
            t for t in tasks
            if t.get("estado") in ["pendiente", "en_progreso"]
            and t.get("fecha_vencimiento") == hoy_str
        ]

        lineas = [
            f"Como va la manana, {nombre_usuario}?",
            "",
        ]

        if hecho_hoy:
            lineas.append(f"Hecho: {len(hecho_hoy)} tarea{'s' if len(hecho_hoy) > 1 else ''}")
            for t in hecho_hoy[:3]:
                lineas.append(f"   - {t['titulo']}")
        else:
            lineas.append("Aun nada marcado como hecho hoy.")

        if pendientes:
            lineas.append("")
            lineas.append(f"Pendiente para hoy: {len(pendientes)} tarea{'s' if len(pendientes) > 1 else ''}")
            for t in pendientes[:3]:
                lineas.append(f"   - {t['titulo']}")

        lineas.append("")
        if hecho_hoy:
            lineas.append("Si vas bien, genial. Si no, bloqueemos 30 min ahora para lo mas importante.")
        else:
            lineas.append("Necesitas que te ayude a priorizar lo que queda del dia?")

        return "\n".join(lineas)

    def generar_evening_wrap(self, nombre_usuario: str = "Jefe") -> str:
        """Generate the evening wrap."""
        hoy = datetime.now()
        hoy_str = hoy.strftime("%Y-%m-%d")
        manana = (hoy + timedelta(days=1)).strftime("%Y-%m-%d")

        tasks_data = _load_json(self.data_dir, "tasks.json")
        tasks = tasks_data.get("tasks", [])

        hecho_hoy = [t for t in tasks if t.get("fecha_completado") == hoy_str]
        pendientes_hoy = [
            t for t in tasks
            if t.get("estado") in ["pendiente", "en_progreso"]
            and t.get("fecha_vencimiento") == hoy_str
        ]
        para_manana = [
            t for t in tasks
            if t.get("estado") in ["pendiente", "en_progreso"]
            and t.get("fecha_vencimiento") == manana
        ]

        lineas = [
            f"Cierre del dia, {nombre_usuario}.",
            "",
        ]

        if hecho_hoy:
            lineas.append(f"Hecho hoy: {len(hecho_hoy)} tarea{'s' if len(hecho_hoy) > 1 else ''}")
            for t in hecho_hoy[:5]:
                lineas.append(f"   - {t['titulo']}")
        else:
            lineas.append("Nada marcado como hecho hoy. Manana es otro dia.")

        if pendientes_hoy:
            lineas.append("")
            lineas.append(f"Quedo pendiente: {len(pendientes_hoy)} tarea{'s' if len(pendientes_hoy) > 1 else ''}")
            for t in pendientes_hoy[:3]:
                lineas.append(f"   - {t['titulo']} -> movida a manana")

        if para_manana:
            lineas.append("")
            lineas.append(f"Para manana:")
            for t in para_manana[:3]:
                lineas.append(f"   - {t['titulo']}")

        lineas.append("")
        lineas.append("Algo mas antes de cerrar?")

        return "\n".join(lineas)

    def generar_weekly_planning(self, nombre_usuario: str = "Jefe") -> str:
        """Generate Monday weekly planning."""
        engine = MetasEngine(str(self.data_dir))
        sugerencias = engine.sugerir_metas_semanales()

        lineas = [
            f"Planning Semanal — {nombre_usuario}",
            "",
            "Basado en lo que veo en tu negocio, sugiero estas metas:",
            "",
        ]

        for i, s in enumerate(sugerencias[:3], 1):
            lineas.append(f"{i}. {s['titulo']}")
            lineas.append(f"   Razon: {s['razon']}")
            lineas.append(f"   Departamento: {s['departamento']}")
            lineas.append("")

        if not sugerencias:
            lineas.append("No tengo suficientes datos para sugerir metas.")
            lineas.append("Que quieres lograr esta semana?")

        lineas.append("Dime cuales aceptas o proponme las tuyas.")

        return "\n".join(lineas)

    def generar_weekly_retro(self, nombre_usuario: str = "Jefe") -> str:
        """Generate Sunday weekly retro."""
        hoy = datetime.now()
        inicio_semana = (hoy - timedelta(days=hoy.weekday())).strftime("%Y-%m-%d")

        metas_data = _load_json(self.data_dir, "metas.json")
        tasks_data = _load_json(self.data_dir, "tasks.json")
        pipeline_data = _load_json(self.data_dir, "pipeline.json")
        projects_data = _load_json(self.data_dir, "projects.json")

        metas = metas_data.get("metas", [])
        metas_texto = []
        for meta in metas:
            pct = (meta["progreso"] / meta["target"] * 100) if meta["target"] > 0 else 0
            if meta["estado"] == "cumplida":
                metas_texto.append(f"   Cumplida: {meta['titulo']} -> {meta['progreso']:.0f}/{meta['target']:.0f}")
            elif meta["estado"] == "activa":
                metas_texto.append(f"   Activa: {meta['titulo']} -> {pct:.0f}%")
            elif meta["estado"] == "fallida":
                metas_texto.append(f"   Fallida: {meta['titulo']} -> {pct:.0f}%")

        tasks = tasks_data.get("tasks", [])
        completadas = [t for t in tasks if t.get("estado") == "completada"]
        vencidas = [
            t for t in tasks
            if t.get("estado") in ["pendiente", "en_progreso", "bloqueada"]
            and t.get("fecha_vencimiento", "") < hoy.strftime("%Y-%m-%d")
        ]

        entries = pipeline_data.get("entries", [])
        nuevos_leads = len([e for e in entries if e.get("fecha_registro", "") >= inicio_semana])
        cotizaciones = len([e for e in entries if e.get("estado") == "cotizado"])
        contratados = len([e for e in entries if e.get("estado") == "contratado"])
        monto_contratado = sum(e.get("monto", 0) for e in entries if e.get("estado") == "contratado")

        projects = projects_data.get("projects", [])
        atrasados = 0
        for p in projects:
            if p.get("estado") in ["planificado", "en_progreso", "pausado"]:
                fecha_entrega = p.get("fecha_entrega")
                if fecha_entrega and fecha_entrega < hoy.strftime("%Y-%m-%d"):
                    atrasados += 1

        lineas = [
            f"Retro Semanal — Semana del {inicio_semana}",
            "",
            "Metas:",
        ]
        if metas_texto:
            lineas.extend(metas_texto)
        else:
            lineas.append("   No hay metas registradas esta semana.")

        lineas.extend([
            "",
            "Numeros:",
            f"   Nuevos leads: {nuevos_leads}",
            f"   Cotizaciones: {cotizaciones}",
            f"   Contratos: {contratados} ({self.moneda} {monto_contratado:,.0f})",
            f"   Tareas completadas: {len(completadas)}",
            f"   Tareas vencidas: {len(vencidas)}",
            f"   Proyectos atrasados: {atrasados}",
            "",
            "Patrones detectados:",
            "   Revisar despues de acumular mas datos.",
            "",
            "Sugerencias para la semana que entra:",
            "   1. Revisar tareas vencidas y reasignar las viables.",
            "   2. Identificar proyectos con riesgo de atraso antes del miercoles.",
            "",
            "Ajustamos algo?",
        ])

        return "\n".join(lineas)


if __name__ == "__main__":
    mb = Briefings()
    print("=== MORNING BRIEFING ===")
    print(mb.generar_morning_briefing("Pablo"))
    print("\n=== MIDDAY PULSE ===")
    print(mb.generar_midday_pulse("Pablo"))
    print("\n=== EVENING WRAP ===")
    print(mb.generar_evening_wrap("Pablo"))
    print("\n=== WEEKLY PLANNING ===")
    print(mb.generar_weekly_planning("Pablo"))
    print("\n=== WEEKLY RETRO ===")
    print(mb.generar_weekly_retro("Pablo"))
