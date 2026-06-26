"""
Partenon Diplomatico — Relations CRM Tool
Manages clients, suppliers, milestones, contracts and communications.
Uses local JSON or Google Workspace as data backend.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# Try to load Partenon config if available
def _load_config() -> Dict[str, Any]:
    """Load config from environment or fallback defaults."""
    return {
        "moneda": os.getenv("PARTENON_MONEDA", "MXN"),
        "timezone": os.getenv("PARTENON_TIMEZONE", "America/Mexico_City"),
    }


def _resolve_data_dir() -> Path:
    """Resolve data directory for local JSON storage."""
    env_dir = os.getenv("PARTENON_DATA_DIR")
    if env_dir:
        return Path(env_dir)

    # Fallback: six levels up from tools/relations/crm.py reaches project root
    project_root = Path(__file__).parent.parent.parent.parent.parent.parent
    return project_root / "data"


def _resolve_relations_file() -> Optional[Path]:
    """Resolve .relations file from workspace or project root."""
    env_file = os.getenv("PARTENON_RELATIONS_FILE")
    if env_file:
        return Path(env_file)

    cwd = Path.cwd()
    candidates = [
        cwd / ".relations",
        cwd / ".." / ".relations",
    ]
    project_root = Path(__file__).parent.parent.parent.parent.parent.parent
    candidates.append(project_root / ".relations")

    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()

    return None


class RelationsCRM:
    """Customer and supplier relationship manager for the Diplomatico profile."""

    CALIFICACIONES_VALIDAS = {"A", "B", "C", "D"}
    ESTADOS_ENTIDAD = {"activa", "pausada", "inactiva", "revisar", "archivada"}
    ESTADOS_HITO = {
        "propuesto",
        "confirmado",
        "en_curso",
        "completado",
        "cancelado",
        "reprogramado",
        "bloqueado",
        "cerrado",
    }
    TIPOS_ENTIDAD = {"cliente", "proveedor"}

    def __init__(self, relations_file: Optional[Path] = None):
        self.config = _load_config()
        self.data_dir = _resolve_data_dir()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.data_dir / "relations_cache.json"

        self.relations_file = relations_file or _resolve_relations_file()
        self._cache: Optional[Dict[str, Any]] = None
        self._next_ids: Dict[str, int] = {
            "cliente": 1,
            "proveedor": 1,
            "hito": 1,
            "contrato": 1,
            "comunicacion": 1,
            "recordatorio": 1,
        }

    def _load(self) -> Dict[str, Any]:
        """Load relations data from .relations file or local cache."""
        if self._cache is not None:
            return self._cache

        if self.relations_file and self.relations_file.exists():
            try:
                with open(self.relations_file, "r", encoding="utf-8") as f:
                    content = f.read()
                data = self._parse_relations(content)
                self._cache = data
                self._sync_cache(data)
                return data
            except Exception:
                pass

        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self._cache = data
                return data
            except Exception:
                pass

        self._cache = self._empty_data()
        return self._cache

    def _parse_relations(self, content: str) -> Dict[str, Any]:
        """Parse .relations file content. Supports JSON and simple YAML-like syntax."""
        content = content.strip()
        if not content:
            return self._empty_data()

        # Try JSON first
        if content.startswith("{"):
            try:
                return json.loads(content)
            except Exception:
                pass

        # Minimal YAML-like parser for the example template
        data = self._empty_data()
        current_section: Optional[str] = None
        current_item: Optional[Dict[str, Any]] = None
        indent_stack: List[tuple] = []

        for raw_line in content.splitlines():
            line = raw_line.rstrip()
            if not line.strip() or line.strip().startswith("#"):
                continue

            stripped = line.lstrip()
            indent = len(line) - len(stripped)

            # Section headers like "clientes:"
            if stripped.endswith(":") and ":" not in stripped[:-1]:
                key = stripped[:-1].strip()
                if key in data:
                    current_section = key
                    current_item = None
                    indent_stack = [(indent, key)]
                continue

            # List item like "- id: CLI-001"
            if stripped.startswith("- "):
                current_item = {}
                if current_section:
                    data[current_section].append(current_item)
                indent_stack = [(indent, current_section)]
                rest = stripped[2:]
                if ":" in rest:
                    k, v = rest.split(":", 1)
                    current_item[k.strip()] = self._coerce_value(v.strip())
                continue

            # Key-value pair
            if ":" in stripped and current_item is not None:
                k, v = stripped.split(":", 1)
                key = k.strip()
                value = v.strip()

                # Nested object handling for contacto_principal
                if value == "":
                    current_item[key] = {}
                    indent_stack.append((indent, key))
                    continue

                # Detect nested keys by indent
                if indent > indent_stack[-1][0] and isinstance(current_item.get(indent_stack[-1][1]), dict):
                    parent = current_item[indent_stack[-1][1]]
                    parent[key] = self._coerce_value(value)
                else:
                    current_item[key] = self._coerce_value(value)

        return data

    @staticmethod
    def _coerce_value(value: str) -> Any:
        """Coerce a string value to bool/int/float/None where possible."""
        lowered = value.lower()
        if lowered in {"true", "verdadero", "si", "sí"}:
            return True
        if lowered in {"false", "falso", "no"}:
            return False
        if lowered in {"null", "none", "nulo", "~"}:
            return None
        if value.startswith('"') and value.endswith('"'):
            return value[1:-1]
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        try:
            if "." in value:
                return float(value)
            return int(value)
        except ValueError:
            return value

    def _empty_data(self) -> Dict[str, Any]:
        return {
            "empresa": "",
            "archivo": ".relations",
            "actualizado": datetime.now().isoformat(),
            "clientes": [],
            "proveedores": [],
            "contratos": [],
            "comunicaciones": [],
            "recordatorios": [],
        }

    def _sync_cache(self, data: Dict[str, Any]) -> None:
        """Write a JSON cache copy for fast lookups."""
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _save(self) -> None:
        """Persist current state to cache. .relations remains the source of truth."""
        if self._cache is None:
            return
        self._cache["actualizado"] = datetime.now().isoformat()
        self._sync_cache(self._cache)

    def _generate_id(self, prefix: str, counter_key: str) -> str:
        """Generate sequential IDs like CLI-001, PROV-001, HIT-001."""
        number = self._next_ids.get(counter_key, 1)
        entity_id = f"{prefix}-{number:03d}"
        self._next_ids[counter_key] = number + 1
        return entity_id

    def _detect_existing_id(self, data: Dict[str, Any], prefix: str, key: str) -> None:
        """Update next ID counters based on existing records."""
        for section in ["clientes", "proveedores", "hitos", "contratos", "comunicaciones", "recordatorios"]:
            for item in data.get(section, []):
                entity_id = item.get("id", "")
                if entity_id.startswith(prefix + "-"):
                    try:
                        number = int(entity_id.split("-")[-1])
                        if number >= self._next_ids.get(key, 1):
                            self._next_ids[key] = number + 1
                    except ValueError:
                        pass

    def _find_entity(self, data: Dict[str, Any], query: str) -> Optional[Dict[str, Any]]:
        """Find an entity by ID or name across clients and suppliers."""
        query_lower = query.lower()
        for section in ["clientes", "proveedores"]:
            for entity in data.get(section, []):
                if entity.get("id", "").lower() == query_lower:
                    return entity
                if query_lower in entity.get("nombre", "").lower():
                    return entity
                contacto = entity.get("contacto_principal", {})
                if contacto and query_lower in contacto.get("email", "").lower():
                    return entity
        return None

    def _get_entity_type(self, entity: Dict[str, Any]) -> str:
        """Infer entity type from its structure or surrounding context."""
        if "proyectos" in entity:
            return "cliente"
        if "servicio" in entity or "contratos" in entity:
            return "proveedor"
        return "desconocido"

    def add_cliente(
        self,
        nombre: str,
        email: str = "",
        telefono: str = "",
        categoria: str = "",
        origen: str = "directo",
        notas: str = "",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Register a new client."""
        data = self._load()
        self._detect_existing_id(data, "CLI", "cliente")

        existing = self._find_entity(data, nombre)
        if existing:
            return {
                "success": False,
                "error": f"Entidad '{nombre}' ya existe ({existing['id']})",
                "entity": existing,
            }

        entity_id = self._generate_id("CLI", "cliente")
        cliente = {
            "id": entity_id,
            "nombre": nombre,
            "contacto_principal": {
                "nombre": kwargs.get("contacto_nombre", ""),
                "email": email,
                "telefono": telefono,
            },
            "categoria": categoria,
            "origen": origen,
            "estado": "activa",
            "calificacion": kwargs.get("calificacion", "B"),
            "calificacion_motivo": kwargs.get("calificacion_motivo", "Registro inicial."),
            "fecha_registro": datetime.now().isoformat(),
            "ultima_actividad": datetime.now().isoformat(),
            "notas": notas,
            "proyectos": [],
            "hitos": [],
        }
        cliente.update(kwargs)
        data["clientes"].append(cliente)
        self._save()

        return {
            "success": True,
            "entity": cliente,
            "message": f"Cliente registrado: {nombre} ({entity_id})",
        }

    def add_proveedor(
        self,
        nombre: str,
        email: str = "",
        telefono: str = "",
        categoria: str = "",
        servicio: str = "",
        origen: str = "directo",
        notas: str = "",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Register a new supplier."""
        data = self._load()
        self._detect_existing_id(data, "PROV", "proveedor")

        existing = self._find_entity(data, nombre)
        if existing:
            return {
                "success": False,
                "error": f"Entidad '{nombre}' ya existe ({existing['id']})",
                "entity": existing,
            }

        entity_id = self._generate_id("PROV", "proveedor")
        proveedor = {
            "id": entity_id,
            "nombre": nombre,
            "contacto_principal": {
                "nombre": kwargs.get("contacto_nombre", ""),
                "email": email,
                "telefono": telefono,
            },
            "categoria": categoria,
            "servicio": servicio,
            "origen": origen,
            "estado": "activa",
            "calificacion": kwargs.get("calificacion", "B"),
            "calificacion_motivo": kwargs.get("calificacion_motivo", "Registro inicial."),
            "fecha_registro": datetime.now().isoformat(),
            "ultima_actividad": datetime.now().isoformat(),
            "notas": notas,
            "contratos": [],
            "hitos": [],
        }
        proveedor.update(kwargs)
        data["proveedores"].append(proveedor)
        self._save()

        return {
            "success": True,
            "entity": proveedor,
            "message": f"Proveedor registrado: {nombre} ({entity_id})",
        }

    def get_entity(self, query: str) -> Optional[Dict[str, Any]]:
        """Find a client or supplier by ID, name or email."""
        data = self._load()
        return self._find_entity(data, query)

    def list_entities(self, tipo: Optional[str] = None, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """List entities filtered by type and/or status."""
        data = self._load()
        sections = []
        if tipo is None:
            sections = ["clientes", "proveedores"]
        elif tipo == "cliente":
            sections = ["clientes"]
        elif tipo == "proveedor":
            sections = ["proveedores"]
        else:
            raise ValueError(f"Tipo inválido: {tipo}. Use 'cliente' o 'proveedor'.")

        results = []
        for section in sections:
            for entity in data.get(section, []):
                if estado and entity.get("estado") != estado:
                    continue
                results.append(entity)
        return results

    def update_entity(self, entity_id: str, **updates: Any) -> Dict[str, Any]:
        """Update fields for a client or supplier."""
        data = self._load()

        for section in ["clientes", "proveedores"]:
            for entity in data.get(section, []):
                if entity.get("id", "").lower() == entity_id.lower():
                    for key, value in updates.items():
                        if key == "contacto_principal" and isinstance(value, dict):
                            entity["contacto_principal"].update(value)
                        else:
                            entity[key] = value
                    entity["ultima_actividad"] = datetime.now().isoformat()
                    self._save()
                    return {
                        "success": True,
                        "entity": entity,
                        "message": f"{entity_id} actualizado",
                    }

        return {
            "success": False,
            "error": f"Entidad {entity_id} no encontrada",
        }

    def add_hito(
        self,
        entity_id: str,
        descripcion: str,
        fecha: str,
        responsable: str = "Diplomatico",
        siguiente_paso: str = "",
    ) -> Dict[str, Any]:
        """Add a milestone to an entity."""
        data = self._load()
        self._detect_existing_id(data, "HIT", "hito")

        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entidad {entity_id} no encontrada",
            }

        hito_id = self._generate_id("HIT", "hito")
        entity_type = self._get_entity_type(entity)
        hito_id = f"HIT-{entity_id}-{hito_id.split('-')[-1]}"

        hito = {
            "id": hito_id,
            "descripcion": descripcion,
            "fecha": fecha,
            "estado": "propuesto",
            "confirmado_escrito": False,
            "responsable": responsable,
            "siguiente_paso": siguiente_paso,
        }
        entity.setdefault("hitos", []).append(hito)
        entity["ultima_actividad"] = datetime.now().isoformat()
        self._save()

        return {
            "success": True,
            "hito": hito,
            "message": f"Hito agregado a {entity_id}: {descripcion}",
        }

    def update_hito(
        self,
        hito_id: str,
        nuevo_estado: Optional[str] = None,
        nueva_fecha: Optional[str] = None,
        siguiente_paso: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update milestone state, date or next step."""
        if nuevo_estado and nuevo_estado not in self.ESTADOS_HITO:
            return {
                "success": False,
                "error": f"Estado inválido. Válidos: {', '.join(sorted(self.ESTADOS_HITO))}",
            }

        data = self._load()
        for section in ["clientes", "proveedores"]:
            for entity in data.get(section, []):
                for hito in entity.get("hitos", []):
                    if hito.get("id", "").lower() == hito_id.lower():
                        if nuevo_estado:
                            hito["estado"] = nuevo_estado
                        if nueva_fecha:
                            hito["fecha"] = nueva_fecha
                        if siguiente_paso is not None:
                            hito["siguiente_paso"] = siguiente_paso
                        entity["ultima_actividad"] = datetime.now().isoformat()
                        self._save()
                        return {
                            "success": True,
                            "hito": hito,
                            "message": f"Hito {hito_id} actualizado",
                        }

        return {
            "success": False,
            "error": f"Hito {hito_id} no encontrado",
        }

    def confirmar_hito(self, hito_id: str) -> Dict[str, Any]:
        """Mark a milestone as confirmed in writing."""
        result = self.update_hito(
            hito_id,
            nuevo_estado="confirmado",
        )
        if not result["success"]:
            return result

        result["hito"]["confirmado_escrito"] = True
        result["hito"]["fecha_confirmacion"] = datetime.now().isoformat()
        self._save()

        return {
            "success": True,
            "hito": result["hito"],
            "message": f"Hito {hito_id} confirmado por escrito",
        }

    def get_hitos(self, entity_id: str, estado: Optional[str] = None) -> List[Dict[str, Any]]:
        """List milestones for an entity, optionally filtered by state."""
        data = self._load()
        entity = self._find_entity(data, entity_id)
        if not entity:
            return []

        hitos = entity.get("hitos", [])
        if estado:
            hitos = [h for h in hitos if h.get("estado") == estado]
        return hitos

    def add_comunicacion(
        self,
        entity_id: str,
        canal: str,
        asunto: str,
        resumen: str,
        siguiente_paso: str = "",
        hito_relacionado: str = "",
    ) -> Dict[str, Any]:
        """Register a communication summary for an entity."""
        data = self._load()
        self._detect_existing_id(data, "COM", "comunicacion")

        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entidad {entity_id} no encontrada",
            }

        com_id = self._generate_id("COM", "comunicacion")
        comunicacion = {
            "id": com_id,
            "entidad_id": entity_id,
            "canal": canal,
            "fecha": datetime.now().isoformat(),
            "asunto": asunto,
            "resumen": resumen,
            "siguiente_paso": siguiente_paso,
            "hito_relacionado": hito_relacionado,
        }
        data.setdefault("comunicaciones", []).append(comunicacion)
        entity["ultima_actividad"] = datetime.now().isoformat()
        self._save()

        return {
            "success": True,
            "comunicacion": comunicacion,
            "message": f"Comunicación registrada para {entity_id}",
        }

    def add_contrato(
        self,
        entity_id: str,
        tipo: str,
        objeto: str,
        monto: float = 0,
        moneda: str = "",
        vigencia_inicio: str = "",
        vigencia_fin: str = "",
        documento_url: str = "",
    ) -> Dict[str, Any]:
        """Register a contract linked to an entity."""
        data = self._load()
        self._detect_existing_id(data, "CONT", "contrato")

        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entidad {entity_id} no encontrada",
            }

        cont_id = self._generate_id("CONT", "contrato")
        contrato = {
            "id": cont_id,
            "entidad_id": entity_id,
            "tipo": tipo,
            "objeto": objeto,
            "monto": monto,
            "moneda": moneda or self.config["moneda"],
            "vigencia_inicio": vigencia_inicio,
            "vigencia_fin": vigencia_fin,
            "estado": "vigente",
            "documento_url": documento_url,
        }
        data.setdefault("contratos", []).append(contrato)
        entity.setdefault("contratos", []).append(cont_id)
        entity["ultima_actividad"] = datetime.now().isoformat()
        self._save()

        return {
            "success": True,
            "contrato": contrato,
            "message": f"Contrato registrado para {entity_id}: {cont_id}",
        }

    def add_recordatorio(
        self,
        entity_id: str,
        mensaje: str,
        fecha: str,
        canal: str = "email",
        tipo: str = "seguimiento",
    ) -> Dict[str, Any]:
        """Schedule a follow-up reminder."""
        data = self._load()
        self._detect_existing_id(data, "REC", "recordatorio")

        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entidad {entity_id} no encontrada",
            }

        rec_id = self._generate_id("REC", "recordatorio")
        recordatorio = {
            "id": rec_id,
            "entidad_id": entity_id,
            "tipo": tipo,
            "fecha": fecha,
            "mensaje": mensaje,
            "canal": canal,
            "estado": "pendiente",
        }
        data.setdefault("recordatorios", []).append(recordatorio)
        self._save()

        return {
            "success": True,
            "recordatorio": recordatorio,
            "message": f"Recordatorio programado para {entity_id}",
        }

    def rate_relationship(self, entity_id: str, calificacion: str, motivo: str = "") -> Dict[str, Any]:
        """Rate a relationship as A, B, C or D."""
        calificacion_upper = calificacion.upper()
        if calificacion_upper not in self.CALIFICACIONES_VALIDAS:
            return {
                "success": False,
                "error": f"Calificación inválida. Válidas: {', '.join(sorted(self.CALIFICACIONES_VALIDAS))}",
            }

        return self.update_entity(
            entity_id,
            calificacion=calificacion_upper,
            calificacion_motivo=motivo or "Calificación actualizada.",
        )

    def get_relationship_summary(self, entity_id: str) -> Dict[str, Any]:
        """Get a complete summary for an entity."""
        data = self._load()
        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entidad {entity_id} no encontrada",
            }

        entity_id_actual = entity["id"]
        comunicaciones = [
            c for c in data.get("comunicaciones", [])
            if c.get("entidad_id", "").lower() == entity_id_actual.lower()
        ]
        contratos = [
            c for c in data.get("contratos", [])
            if c.get("entidad_id", "").lower() == entity_id_actual.lower()
        ]
        recordatorios = [
            r for r in data.get("recordatorios", [])
            if r.get("entidad_id", "").lower() == entity_id_actual.lower() and r.get("estado") == "pendiente"
        ]
        hitos_pendientes = [
            h for h in entity.get("hitos", [])
            if h.get("estado") not in {"completado", "cerrado", "cancelado"}
        ]

        return {
            "success": True,
            "entity": entity,
            "tipo": self._get_entity_type(entity),
            "hitos_pendientes": hitos_pendientes,
            "comunicaciones_recientes": sorted(
                comunicaciones,
                key=lambda x: x.get("fecha", ""),
                reverse=True,
            )[:5],
            "contratos": contratos,
            "recordatorios_pendientes": recordatorios,
        }

    def extract_entity_from_message(self, message: str) -> Optional[str]:
        """Try to extract an entity name from natural language."""
        patterns = [
            r"(?:cliente|proveedor|de|con|para)\s+([A-Z][a-z]+\s+(?:[A-Z][a-z]+\s*)+)",
            r"([A-Z][a-z]+\s+[A-Z][a-z]+)",
        ]

        data = self._load()
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                name = match.group(1).strip()
                entity = self._find_entity(data, name)
                if entity:
                    return entity["nombre"]

        return None


# Singleton
_crm_instance: Optional[RelationsCRM] = None


def get_relations_crm(relations_file: Optional[Path] = None) -> RelationsCRM:
    """Get or create singleton RelationsCRM instance."""
    global _crm_instance
    if _crm_instance is None:
        _crm_instance = RelationsCRM(relations_file=relations_file)
    return _crm_instance


if __name__ == "__main__":
    crm = get_relations_crm()
    print(crm.add_cliente("Acme Corp", email="hola@acme.test"))
    print(crm.add_proveedor("Papelera Central", categoria="papeleria"))
