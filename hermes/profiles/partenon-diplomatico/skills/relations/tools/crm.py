"""
Partenon Diplomat — Relations CRM Tool
Manages clients, vendors, milestones, contracts, and communications.
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
        "currency": os.getenv("PARTENON_CURRENCY", "MXN"),
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
    """Customer and vendor relationship manager for the Diplomat profile."""

    VALID_RATINGS = {"A", "B", "C", "D"}
    ENTITY_STATES = {"active", "paused", "inactive", "review", "archived"}
    MILESTONE_STATES = {
        "proposed",
        "confirmed",
        "in_progress",
        "completed",
        "cancelled",
        "rescheduled",
        "blocked",
        "closed",
    }
    ENTITY_TYPES = {"client", "vendor"}

    def __init__(self, relations_file: Optional[Path] = None):
        self.config = _load_config()
        self.data_dir = _resolve_data_dir()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.data_dir / "relations_cache.json"

        self.relations_file = relations_file or _resolve_relations_file()
        self._cache: Optional[Dict[str, Any]] = None
        self._next_ids: Dict[str, int] = {
            "client": 1,
            "vendor": 1,
            "milestone": 1,
            "contract": 1,
            "communication": 1,
            "reminder": 1,
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

            # Section headers like "clients:"
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

                # Nested object handling for main_contact
                if value == "":
                    current_item[key] = {}
                    indent_stack.append((indent, key))
                    continue

                # Detect nested keys by indent
                if (
                    indent > indent_stack[-1][0]
                    and isinstance(current_item.get(indent_stack[-1][1]), dict)
                ):
                    parent = current_item[indent_stack[-1][1]]
                    parent[key] = self._coerce_value(value)
                else:
                    current_item[key] = self._coerce_value(value)

        return data

    @staticmethod
    def _coerce_value(value: str) -> Any:
        """Coerce a string value to bool/int/float/None where possible."""
        lowered = value.lower()
        if lowered in {"true", "yes"}:
            return True
        if lowered in {"false", "no"}:
            return False
        if lowered in {"null", "none", "~"}:
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
            "company": "",
            "file": ".relations",
            "updated": datetime.now().isoformat(),
            "clients": [],
            "vendors": [],
            "contracts": [],
            "communications": [],
            "reminders": [],
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
        self._cache["updated"] = datetime.now().isoformat()
        self._sync_cache(self._cache)

    def _generate_id(self, prefix: str, counter_key: str) -> str:
        """Generate sequential IDs like CLI-001, VEN-001, MIL-001."""
        number = self._next_ids.get(counter_key, 1)
        entity_id = f"{prefix}-{number:03d}"
        self._next_ids[counter_key] = number + 1
        return entity_id

    def _detect_existing_id(self, data: Dict[str, Any], prefix: str, key: str) -> None:
        """Update next ID counters based on existing records."""
        for section in ["clients", "vendors", "milestones", "contracts", "communications", "reminders"]:
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
        """Find an entity by ID or name across clients and vendors."""
        query_lower = query.lower()
        for section in ["clients", "vendors"]:
            for entity in data.get(section, []):
                if entity.get("id", "").lower() == query_lower:
                    return entity
                if query_lower in entity.get("name", "").lower():
                    return entity
                contact = entity.get("main_contact", {})
                if contact and query_lower in contact.get("email", "").lower():
                    return entity
        return None

    def _get_entity_type(self, entity: Dict[str, Any]) -> str:
        """Infer entity type from its structure or surrounding context."""
        if "projects" in entity:
            return "client"
        if "service" in entity or "contracts" in entity:
            return "vendor"
        return "unknown"

    def add_client(
        self,
        name: str,
        email: str = "",
        phone: str = "",
        category: str = "",
        origin: str = "direct",
        notes: str = "",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Register a new client."""
        data = self._load()
        self._detect_existing_id(data, "CLI", "client")

        existing = self._find_entity(data, name)
        if existing:
            return {
                "success": False,
                "error": f"Entity '{name}' already exists ({existing['id']})",
                "entity": existing,
            }

        entity_id = self._generate_id("CLI", "client")
        client = {
            "id": entity_id,
            "name": name,
            "main_contact": {
                "name": kwargs.get("contact_name", ""),
                "email": email,
                "phone": phone,
            },
            "category": category,
            "origin": origin,
            "status": "active",
            "rating": kwargs.get("rating", "B"),
            "rating_reason": kwargs.get("rating_reason", "Initial registration."),
            "registered_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "notes": notes,
            "projects": [],
            "milestones": [],
        }
        client.update(kwargs)
        data["clients"].append(client)
        self._save()

        return {
            "success": True,
            "entity": client,
            "message": f"Client registered: {name} ({entity_id})",
        }

    def add_vendor(
        self,
        name: str,
        email: str = "",
        phone: str = "",
        category: str = "",
        service: str = "",
        origin: str = "direct",
        notes: str = "",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Register a new vendor."""
        data = self._load()
        self._detect_existing_id(data, "VEN", "vendor")

        existing = self._find_entity(data, name)
        if existing:
            return {
                "success": False,
                "error": f"Entity '{name}' already exists ({existing['id']})",
                "entity": existing,
            }

        entity_id = self._generate_id("VEN", "vendor")
        vendor = {
            "id": entity_id,
            "name": name,
            "main_contact": {
                "name": kwargs.get("contact_name", ""),
                "email": email,
                "phone": phone,
            },
            "category": category,
            "service": service,
            "origin": origin,
            "status": "active",
            "rating": kwargs.get("rating", "B"),
            "rating_reason": kwargs.get("rating_reason", "Initial registration."),
            "registered_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "notes": notes,
            "contracts": [],
            "milestones": [],
        }
        vendor.update(kwargs)
        data["vendors"].append(vendor)
        self._save()

        return {
            "success": True,
            "entity": vendor,
            "message": f"Vendor registered: {name} ({entity_id})",
        }

    def get_entity(self, query: str) -> Optional[Dict[str, Any]]:
        """Find a client or vendor by ID, name or email."""
        data = self._load()
        return self._find_entity(data, query)

    def list_entities(
        self, entity_type: Optional[str] = None, status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List entities filtered by type and/or status."""
        data = self._load()
        sections = []
        if entity_type is None:
            sections = ["clients", "vendors"]
        elif entity_type == "client":
            sections = ["clients"]
        elif entity_type == "vendor":
            sections = ["vendors"]
        else:
            raise ValueError(f"Invalid type: {entity_type}. Use 'client' or 'vendor'.")

        results = []
        for section in sections:
            for entity in data.get(section, []):
                if status and entity.get("status") != status:
                    continue
                results.append(entity)
        return results

    def update_entity(self, entity_id: str, **updates: Any) -> Dict[str, Any]:
        """Update fields for a client or vendor."""
        data = self._load()

        for section in ["clients", "vendors"]:
            for entity in data.get(section, []):
                if entity.get("id", "").lower() == entity_id.lower():
                    for key, value in updates.items():
                        if key == "main_contact" and isinstance(value, dict):
                            entity["main_contact"].update(value)
                        else:
                            entity[key] = value
                    entity["last_activity"] = datetime.now().isoformat()
                    self._save()
                    return {
                        "success": True,
                        "entity": entity,
                        "message": f"{entity_id} updated",
                    }

        return {
            "success": False,
            "error": f"Entity {entity_id} not found",
        }

    def add_milestone(
        self,
        entity_id: str,
        description: str,
        date: str,
        responsible: str = "Diplomat",
        next_step: str = "",
    ) -> Dict[str, Any]:
        """Add a milestone to an entity."""
        data = self._load()
        self._detect_existing_id(data, "MIL", "milestone")

        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entity {entity_id} not found",
            }

        milestone_id = self._generate_id("MIL", "milestone")
        milestone_id = f"MIL-{entity_id}-{milestone_id.split('-')[-1]}"

        milestone = {
            "id": milestone_id,
            "description": description,
            "date": date,
            "status": "proposed",
            "confirmed_in_writing": False,
            "responsible": responsible,
            "next_step": next_step,
        }
        entity.setdefault("milestones", []).append(milestone)
        entity["last_activity"] = datetime.now().isoformat()
        self._save()

        return {
            "success": True,
            "milestone": milestone,
            "message": f"Milestone added to {entity_id}: {description}",
        }

    def update_milestone(
        self,
        milestone_id: str,
        new_status: Optional[str] = None,
        new_date: Optional[str] = None,
        next_step: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update milestone state, date or next step."""
        if new_status and new_status not in self.MILESTONE_STATES:
            return {
                "success": False,
                "error": f"Invalid status. Valid: {', '.join(sorted(self.MILESTONE_STATES))}",
            }

        data = self._load()
        for section in ["clients", "vendors"]:
            for entity in data.get(section, []):
                for milestone in entity.get("milestones", []):
                    if milestone.get("id", "").lower() == milestone_id.lower():
                        if new_status:
                            milestone["status"] = new_status
                        if new_date:
                            milestone["date"] = new_date
                        if next_step is not None:
                            milestone["next_step"] = next_step
                        entity["last_activity"] = datetime.now().isoformat()
                        self._save()
                        return {
                            "success": True,
                            "milestone": milestone,
                            "message": f"Milestone {milestone_id} updated",
                        }

        return {
            "success": False,
            "error": f"Milestone {milestone_id} not found",
        }

    def confirm_milestone(self, milestone_id: str) -> Dict[str, Any]:
        """Mark a milestone as confirmed in writing."""
        result = self.update_milestone(
            milestone_id,
            new_status="confirmed",
        )
        if not result["success"]:
            return result

        result["milestone"]["confirmed_in_writing"] = True
        result["milestone"]["confirmed_at"] = datetime.now().isoformat()
        self._save()

        return {
            "success": True,
            "milestone": result["milestone"],
            "message": f"Milestone {milestone_id} confirmed in writing",
        }

    def get_milestones(self, entity_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List milestones for an entity, optionally filtered by state."""
        data = self._load()
        entity = self._find_entity(data, entity_id)
        if not entity:
            return []

        milestones = entity.get("milestones", [])
        if status:
            milestones = [m for m in milestones if m.get("status") == status]
        return milestones

    def add_communication(
        self,
        entity_id: str,
        channel: str,
        subject: str,
        summary: str,
        next_step: str = "",
        related_milestone: str = "",
    ) -> Dict[str, Any]:
        """Register a communication summary for an entity."""
        data = self._load()
        self._detect_existing_id(data, "COM", "communication")

        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entity {entity_id} not found",
            }

        com_id = self._generate_id("COM", "communication")
        communication = {
            "id": com_id,
            "entity_id": entity_id,
            "channel": channel,
            "date": datetime.now().isoformat(),
            "subject": subject,
            "summary": summary,
            "next_step": next_step,
            "related_milestone": related_milestone,
        }
        data.setdefault("communications", []).append(communication)
        entity["last_activity"] = datetime.now().isoformat()
        self._save()

        return {
            "success": True,
            "communication": communication,
            "message": f"Communication registered for {entity_id}",
        }

    def add_contract(
        self,
        entity_id: str,
        contract_type: str,
        contract_object: str,
        amount: float = 0,
        currency: str = "",
        start_date: str = "",
        end_date: str = "",
        document_url: str = "",
    ) -> Dict[str, Any]:
        """Register a contract linked to an entity."""
        data = self._load()
        self._detect_existing_id(data, "CONT", "contract")

        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entity {entity_id} not found",
            }

        cont_id = self._generate_id("CONT", "contract")
        contract = {
            "id": cont_id,
            "entity_id": entity_id,
            "type": contract_type,
            "object": contract_object,
            "amount": amount,
            "currency": currency or self.config["currency"],
            "start_date": start_date,
            "end_date": end_date,
            "status": "active",
            "document_url": document_url,
        }
        data.setdefault("contracts", []).append(contract)
        entity.setdefault("contracts", []).append(cont_id)
        entity["last_activity"] = datetime.now().isoformat()
        self._save()

        return {
            "success": True,
            "contract": contract,
            "message": f"Contract registered for {entity_id}: {cont_id}",
        }

    def add_reminder(
        self,
        entity_id: str,
        message: str,
        date: str,
        channel: str = "email",
        reminder_type: str = "follow-up",
    ) -> Dict[str, Any]:
        """Schedule a follow-up reminder."""
        data = self._load()
        self._detect_existing_id(data, "REM", "reminder")

        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entity {entity_id} not found",
            }

        rec_id = self._generate_id("REM", "reminder")
        reminder = {
            "id": rec_id,
            "entity_id": entity_id,
            "type": reminder_type,
            "date": date,
            "message": message,
            "channel": channel,
            "status": "pending",
        }
        data.setdefault("reminders", []).append(reminder)
        self._save()

        return {
            "success": True,
            "reminder": reminder,
            "message": f"Reminder scheduled for {entity_id}",
        }

    def rate_relationship(self, entity_id: str, rating: str, reason: str = "") -> Dict[str, Any]:
        """Rate a relationship as A, B, C or D."""
        rating_upper = rating.upper()
        if rating_upper not in self.VALID_RATINGS:
            return {
                "success": False,
                "error": f"Invalid rating. Valid: {', '.join(sorted(self.VALID_RATINGS))}",
            }

        return self.update_entity(
            entity_id,
            rating=rating_upper,
            rating_reason=reason or "Rating updated.",
        )

    def get_relationship_summary(self, entity_id: str) -> Dict[str, Any]:
        """Get a complete summary for an entity."""
        data = self._load()
        entity = self._find_entity(data, entity_id)
        if not entity:
            return {
                "success": False,
                "error": f"Entity {entity_id} not found",
            }

        actual_entity_id = entity["id"]
        communications = [
            c for c in data.get("communications", [])
            if c.get("entity_id", "").lower() == actual_entity_id.lower()
        ]
        contracts = [
            c for c in data.get("contracts", [])
            if c.get("entity_id", "").lower() == actual_entity_id.lower()
        ]
        pending_reminders = [
            r for r in data.get("reminders", [])
            if r.get("entity_id", "").lower() == actual_entity_id.lower()
            and r.get("status") == "pending"
        ]
        pending_milestones = [
            m for m in entity.get("milestones", [])
            if m.get("status") not in {"completed", "closed", "cancelled"}
        ]

        return {
            "success": True,
            "entity": entity,
            "type": self._get_entity_type(entity),
            "pending_milestones": pending_milestones,
            "recent_communications": sorted(
                communications,
                key=lambda x: x.get("date", ""),
                reverse=True,
            )[:5],
            "contracts": contracts,
            "pending_reminders": pending_reminders,
        }

    def extract_entity_from_message(self, message: str) -> Optional[str]:
        """Try to extract an entity name from natural language."""
        patterns = [
            r"(?:client|vendor|from|with|for)\s+([A-Z][a-z]+\s+(?:[A-Z][a-z]+\s*)+)",
            r"([A-Z][a-z]+\s+[A-Z][a-z]+)",
        ]

        data = self._load()
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                name = match.group(1).strip()
                entity = self._find_entity(data, name)
                if entity:
                    return entity["name"]

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
    print(crm.add_client("Acme Corp", email="hello@acme.test"))
    print(crm.add_vendor("Paper Central", category="stationery"))
