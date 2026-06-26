"""
Partenon Estratega — Metas Engine
Defines, tracks, and reports business goals with automatic tracking
based on data from other departments.
"""

import json
from dataclasses import dataclass, asdict
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


@dataclass
class Meta:
    id: str
    titulo: str
    tipo: str  # semanal, mensual, trimestral, anual
    departamento: str
    target: float
    unidad: str
    deadline: str
    creada: str
    estado: str = "activa"  # activa, cumplida, fallida, cancelada
    progreso: float = 0.0
    auto_track: bool = True
    kpi_source: str = ""  # ej: "pipeline.contratado", "tasks.completadas"
    notas: str = ""


class MetasEngine:
    """Manages the full lifecycle of business goals."""

    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir) if data_dir else _resolve_data_dir()
        self.meta_file = self.data_dir / "metas.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.meta_file.exists():
            self._save_metas([])

    def _load_metas(self) -> List[Dict[str, Any]]:
        try:
            with open(self.meta_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("metas", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_metas(self, metas: List[Dict[str, Any]]):
        with open(self.meta_file, "w", encoding="utf-8") as f:
            json.dump({"metas": metas, "updated_at": datetime.now().isoformat()}, f, indent=2, ensure_ascii=False)

    def _generate_id(self) -> str:
        metas = self._load_metas()
        count = len(metas) + 1
        return f"META-{count:03d}"

    def create_meta(
        self,
        titulo: str,
        tipo: str = "semanal",
        departamento: str = "general",
        target: float = 1.0,
        unidad: str = "unidad",
        deadline: Optional[str] = None,
        auto_track: bool = True,
        kpi_source: str = "",
    ) -> Dict[str, Any]:
        """Create a new goal."""
        if deadline is None:
            if tipo == "semanal":
                deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
            elif tipo == "mensual":
                deadline = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
            else:
                deadline = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")

        meta = Meta(
            id=self._generate_id(),
            titulo=titulo,
            tipo=tipo,
            departamento=departamento,
            target=target,
            unidad=unidad,
            deadline=deadline,
            creada=datetime.now().strftime("%Y-%m-%d"),
            auto_track=auto_track,
            kpi_source=kpi_source,
        )

        metas = self._load_metas()
        metas.append(asdict(meta))
        self._save_metas(metas)
        return asdict(meta)

    def get_metas(
        self,
        estado: Optional[str] = None,
        tipo: Optional[str] = None,
        departamento: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get filtered goals."""
        metas = self._load_metas()
        if estado:
            metas = [m for m in metas if m["estado"] == estado]
        if tipo:
            metas = [m for m in metas if m["tipo"] == tipo]
        if departamento:
            metas = [m for m in metas if m["departamento"] == departamento]
        return metas

    def get_meta_by_id(self, meta_id: str) -> Optional[Dict[str, Any]]:
        """Find a goal by ID."""
        metas = self._load_metas()
        for meta in metas:
            if meta["id"] == meta_id:
                return meta
        return None

    def update_progreso(self, meta_id: str, progreso: float) -> Optional[Dict[str, Any]]:
        """Update goal progress."""
        metas = self._load_metas()
        for meta in metas:
            if meta["id"] == meta_id:
                meta["progreso"] = min(progreso, meta["target"])
                if meta["progreso"] >= meta["target"]:
                    meta["estado"] = "cumplida"
                self._save_metas(metas)
                return meta
        return None

    def auto_track_metas(self) -> List[Dict[str, Any]]:
        """Update progress automatically based on KPI sources."""
        metas = self._load_metas()
        actualizadas = []

        for meta in metas:
            if not meta.get("auto_track") or meta["estado"] != "activa":
                continue

            nuevo_progreso = self._calcular_kpi(meta["kpi_source"], meta)
            if nuevo_progreso is not None and nuevo_progreso != meta["progreso"]:
                meta["progreso"] = nuevo_progreso
                if meta["progreso"] >= meta["target"]:
                    meta["estado"] = "cumplida"
                actualizadas.append(meta)

        if actualizadas:
            self._save_metas(metas)

        return actualizadas

    def _calcular_kpi(self, kpi_source: str, meta: Dict[str, Any]) -> Optional[float]:
        """Calculate current KPI value by reading data from other tools."""
        if not kpi_source:
            return None

        try:
            if kpi_source.startswith("pipeline."):
                return self._kpi_pipeline(kpi_source, meta)
            elif kpi_source.startswith("tasks."):
                return self._kpi_tasks(kpi_source, meta)
            elif kpi_source.startswith("pagos."):
                return self._kpi_pagos(kpi_source, meta)
        except Exception:
            pass

        return None

    def _kpi_pipeline(self, kpi_source: str, meta: Dict[str, Any]) -> Optional[float]:
        """Read pipeline.json to calculate sales KPI."""
        pipeline_file = self.data_dir / "pipeline.json"
        if not pipeline_file.exists():
            return None

        with open(pipeline_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        entries = data.get("entries", [])
        estado = kpi_source.split(".")[1] if "." in kpi_source else "contratado"

        creada = datetime.strptime(meta["creada"], "%Y-%m-%d")
        deadline = datetime.strptime(meta["deadline"], "%Y-%m-%d")

        count = 0
        for entry in entries:
            if entry.get("estado") == estado:
                fecha = entry.get("fecha_actualizacion") or entry.get("fecha_registro")
                if fecha:
                    try:
                        fdt = datetime.strptime(fecha, "%Y-%m-%d")
                        if creada <= fdt <= deadline:
                            count += 1
                    except ValueError:
                        count += 1
                else:
                    count += 1

        return float(count)

    def _kpi_tasks(self, kpi_source: str, meta: Dict[str, Any]) -> Optional[float]:
        """Read tasks.json to calculate operations KPI."""
        tasks_file = self.data_dir / "tasks.json"
        if not tasks_file.exists():
            return None

        with open(tasks_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        tasks = data.get("tasks", [])
        creada = datetime.strptime(meta["creada"], "%Y-%m-%d")
        deadline = datetime.strptime(meta["deadline"], "%Y-%m-%d")

        count = 0
        for task in tasks:
            if task.get("estado") == "completada":
                fecha = task.get("fecha_completado") or task.get("fecha_vencimiento")
                if fecha:
                    try:
                        fdt = datetime.strptime(fecha, "%Y-%m-%d")
                        if creada <= fdt <= deadline:
                            count += 1
                    except ValueError:
                        pass

        return float(count)

    def _kpi_pagos(self, kpi_source: str, meta: Dict[str, Any]) -> Optional[float]:
        """Read quotes.json to calculate financial KPI."""
        quotes_file = self.data_dir / "quotes.json"
        if not quotes_file.exists():
            return 0.0

        with open(quotes_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        quotes = data.get("quotes", [])
        creada = datetime.strptime(meta["creada"], "%Y-%m-%d")
        deadline = datetime.strptime(meta["deadline"], "%Y-%m-%d")

        total = 0.0
        for quote in quotes:
            if quote.get("estado") in ["aprobada", "pagada"]:
                fecha = quote.get("fecha_aprobacion") or quote.get("fecha_creacion")
                monto = quote.get("total", 0)
                if fecha:
                    try:
                        fdt = datetime.strptime(fecha, "%Y-%m-%d")
                        if creada <= fdt <= deadline:
                            total += monto
                    except ValueError:
                        pass

        return total

    def get_resumen_metas(self, tipo: Optional[str] = None) -> Dict[str, Any]:
        """Generate executive summary of goals."""
        metas = self.get_metas(tipo=tipo)
        activas = [m for m in metas if m["estado"] == "activa"]
        cumplidas = [m for m in metas if m["estado"] == "cumplida"]
        fallidas = [m for m in metas if m["estado"] == "fallida"]

        hoy = datetime.now().date()
        urgentes = []
        for meta in activas:
            try:
                deadline = datetime.strptime(meta["deadline"], "%Y-%m-%d").date()
                dias_restantes = (deadline - hoy).days
                if dias_restantes <= 2:
                    urgentes.append({**meta, "dias_restantes": dias_restantes})
            except ValueError:
                pass

        return {
            "total": len(metas),
            "activas": len(activas),
            "cumplidas": len(cumplidas),
            "fallidas": len(fallidas),
            "urgentes": urgentes,
            "por_departamento": self._agrupar_por_departamento(metas),
            "promedio_progreso": self._calcular_promedio_progreso(activas) if activas else 0,
        }

    def _agrupar_por_departamento(
        self, metas: List[Dict[str, Any]]
    ) -> Dict[str, Dict[str, int]]:
        resultado: Dict[str, Dict[str, int]] = {}
        for meta in metas:
            dep = meta.get("departamento", "general")
            if dep not in resultado:
                resultado[dep] = {"total": 0, "activas": 0, "cumplidas": 0}
            resultado[dep]["total"] += 1
            if meta["estado"] == "activa":
                resultado[dep]["activas"] += 1
            elif meta["estado"] == "cumplida":
                resultado[dep]["cumplidas"] += 1
        return resultado

    def _calcular_promedio_progreso(self, metas: List[Dict[str, Any]]) -> float:
        if not metas:
            return 0.0
        total = sum(
            m["progreso"] / m["target"] * 100 if m["target"] > 0 else 0 for m in metas
        )
        return round(total / len(metas), 1)

    def cerrar_meta(
        self, meta_id: str, estado: str = "cumplida", notas: str = ""
    ) -> Optional[Dict[str, Any]]:
        """Close a goal manually."""
        metas = self._load_metas()
        for meta in metas:
            if meta["id"] == meta_id:
                meta["estado"] = estado
                meta["notas"] = notas
                self._save_metas(metas)
                return meta
        return None

    def sugerir_metas_semanales(self) -> List[Dict[str, Any]]:
        """Suggest goals based on current data."""
        sugerencias = []

        pipeline_file = self.data_dir / "pipeline.json"
        if pipeline_file.exists():
            with open(pipeline_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            entries = data.get("entries", [])
            prospectos = [e for e in entries if e.get("estado") in ["prospecto", "cotizado"]]
            if len(prospectos) >= 3:
                target = min(2, len(prospectos))
                sugerencias.append({
                    "titulo": f"Cerrar {target} contratos",
                    "tipo": "semanal",
                    "departamento": "ventas",
                    "target": target,
                    "unidad": "contratos",
                    "razon": f"Tienes {len(prospectos)} prospectos activos",
                    "kpi_source": "pipeline.contratado",
                })

        tasks_file = self.data_dir / "tasks.json"
        if tasks_file.exists():
            with open(tasks_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            tasks = data.get("tasks", [])
            pendientes = [t for t in tasks if t.get("estado") in ["pendiente", "en_progreso"]]
            if len(pendientes) >= 5:
                target = min(5, len(pendientes))
                sugerencias.append({
                    "titulo": f"Completar {target} tareas pendientes",
                    "tipo": "semanal",
                    "departamento": "operaciones",
                    "target": target,
                    "unidad": "tareas",
                    "razon": f"Tienes {len(pendientes)} tareas pendientes",
                    "kpi_source": "tasks.completadas",
                })

        return sugerencias


if __name__ == "__main__":
    engine = MetasEngine()
    meta = engine.create_meta(
        titulo="Cerrar 2 contratos",
        tipo="semanal",
        departamento="ventas",
        target=2,
        unidad="contratos",
        kpi_source="pipeline.contratado",
    )
    print(f"Meta creada: {meta['id']}")
    print(f"Resumen: {engine.get_resumen_metas()}")
