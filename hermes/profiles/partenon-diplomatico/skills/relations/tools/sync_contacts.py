"""
Partenon Diplomat — Contact Sync Tool
Syncs clients and vendors between `.relations` and external CRM providers
(HubSpot, Salesforce, or a generic custom CRM).
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))
from crm import RelationsCRM, get_relations_crm


DEFAULT_CRM_PROVIDER = os.getenv("CRM_PROVIDER", "hubspot")


def _crm_record_from_entity(entity: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a `.relations` entity into a CRM-neutral record."""
    contact = entity.get("main_contact", {}) or {}
    return {
        "external_id": entity.get("id"),
        "name": entity.get("name"),
        "type": "client" if entity.get("id", "").startswith("CLI-") else "vendor",
        "email": contact.get("email", ""),
        "phone": contact.get("phone", ""),
        "contact_name": contact.get("name", ""),
        "category": entity.get("category", ""),
        "status": entity.get("status", "active"),
        "rating": entity.get("rating", "B"),
        "rating_reason": entity.get("rating_reason", ""),
        "notes": entity.get("notes", ""),
        "last_activity": entity.get("last_activity", ""),
    }


def _entity_from_crm_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a CRM-neutral record into a `.relations`-style entity."""
    entity_type = record.get("type", "client").lower()
    now = datetime.now().isoformat()
    if entity_type == "client":
        return {
            "id": record.get("external_id") or f"CLI-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": record.get("name", ""),
            "main_contact": {
                "name": record.get("contact_name", ""),
                "email": record.get("email", ""),
                "phone": record.get("phone", ""),
            },
            "category": record.get("category", ""),
            "origin": "crm_sync",
            "status": record.get("status", "active"),
            "rating": record.get("rating", "B"),
            "rating_reason": record.get("rating_reason", "Imported from CRM."),
            "registered_at": now,
            "last_activity": record.get("last_activity") or now,
            "notes": record.get("notes", ""),
            "projects": [],
            "milestones": [],
        }
    return {
        "id": record.get("external_id") or f"VEN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "name": record.get("name", ""),
        "main_contact": {
            "name": record.get("contact_name", ""),
            "email": record.get("email", ""),
            "phone": record.get("phone", ""),
        },
        "category": record.get("category", ""),
        "service": record.get("service", ""),
        "origin": "crm_sync",
        "status": record.get("status", "active"),
        "rating": record.get("rating", "B"),
        "rating_reason": record.get("rating_reason", "Imported from CRM."),
        "registered_at": now,
        "last_activity": record.get("last_activity") or now,
        "notes": record.get("notes", ""),
        "contracts": [],
        "milestones": [],
    }


def _provider_config(provider: str) -> Dict[str, Any]:
    """Build a provider configuration from environment variables."""
    provider = (provider or DEFAULT_CRM_PROVIDER).lower()
    if provider == "hubspot":
        return {
            "provider": "hubspot",
            "api_key": os.getenv("HUBSPOT_ACCESS_TOKEN") or os.getenv("CRM_API_KEY"),
            "api_url": os.getenv("CRM_API_URL", "https://api.hubapi.com"),
        }
    if provider == "salesforce":
        return {
            "provider": "salesforce",
            "client_id": os.getenv("SALESFORCE_CLIENT_ID"),
            "client_secret": os.getenv("SALESFORCE_CLIENT_SECRET"),
            "username": os.getenv("SALESFORCE_USERNAME"),
            "password": os.getenv("SALESFORCE_PASSWORD"),
            "security_token": os.getenv("SALESFORCE_SECURITY_TOKEN"),
            "instance_url": os.getenv("SALESFORCE_INSTANCE_URL"),
        }
    return {
        "provider": provider,
        "api_key": os.getenv("CRM_API_KEY"),
        "api_url": os.getenv("CRM_API_URL", ""),
    }


def export_contacts(
    crm: Optional[RelationsCRM] = None,
    entity_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Export `.relations` entities as CRM-neutral records."""
    crm = crm or get_relations_crm()
    entities = crm.list_entities(entity_type=entity_type)
    return [_crm_record_from_entity(e) for e in entities]


def import_contacts(
    records: List[Dict[str, Any]],
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """Import CRM-neutral records into `.relations`."""
    crm = crm or get_relations_crm()
    added: List[Dict[str, Any]] = []
    updated: List[Dict[str, Any]] = []
    failed: List[Dict[str, Any]] = []

    for record in records:
        entity = _entity_from_crm_record(record)
        entity_id = entity.get("id", "")
        entity_name = entity.get("name", "")

        if not entity_name:
            failed.append({"record": record, "reason": "missing name"})
            continue

        existing = crm.get_entity(entity_name)
        if existing:
            result = crm.update_entity(existing.get("id", ""), **entity)
            if result.get("success"):
                updated.append(result.get("entity", entity))
            else:
                failed.append({"record": record, "reason": result.get("error", "update failed")})
        else:
            if entity_id.startswith("CLI-"):
                result = crm.add_client(
                    name=entity_name,
                    email=entity.get("main_contact", {}).get("email", ""),
                    phone=entity.get("main_contact", {}).get("phone", ""),
                    category=entity.get("category", ""),
                    origin="crm_sync",
                    notes=entity.get("notes", ""),
                    rating=entity.get("rating", "B"),
                    rating_reason=entity.get("rating_reason", "Imported from CRM."),
                )
            else:
                result = crm.add_vendor(
                    name=entity_name,
                    email=entity.get("main_contact", {}).get("email", ""),
                    phone=entity.get("main_contact", {}).get("phone", ""),
                    category=entity.get("category", ""),
                    service=entity.get("service", ""),
                    origin="crm_sync",
                    notes=entity.get("notes", ""),
                    rating=entity.get("rating", "B"),
                    rating_reason=entity.get("rating_reason", "Imported from CRM."),
                )
            if result.get("success"):
                added.append(result.get("entity", entity))
            else:
                failed.append({"record": record, "reason": result.get("error", "add failed")})

    return {
        "success": True,
        "added": added,
        "updated": updated,
        "failed": failed,
        "total": len(added) + len(updated) + len(failed),
    }


def sync_contacts(
    provider: Optional[str] = None,
    direction: str = "export",
    records: Optional[List[Dict[str, Any]]] = None,
    crm: Optional[RelationsCRM] = None,
) -> Dict[str, Any]:
    """
    Sync contacts between `.relations` and an external CRM.

    Args:
        provider: CRM provider name (hubspot, salesforce, custom).
        direction: 'export', 'import', or 'bidirectional'.
        records: Optional list of CRM records to import.
        crm: RelationsCRM instance.

    Returns:
        A structured sync report.
    """
    crm = crm or get_relations_crm()
    config = _provider_config(provider)

    if direction == "export":
        payload = export_contacts(crm=crm)
        return {
            "success": True,
            "provider": config["provider"],
            "direction": "export",
            "config": {k: ("***" if "key" in k or "token" in k or "secret" in k or "password" in k else v) for k, v in config.items()},
            "count": len(payload),
            "records": payload,
            "note": "This payload can be sent to the CRM MCP or API. No external network call was made.",
        }

    if direction == "import":
        if not records:
            return {
                "success": False,
                "error": "No records provided for import.",
            }
        return import_contacts(records, crm=crm)

    if direction == "bidirectional":
        exported = export_contacts(crm=crm)
        imported = import_contacts(records or [], crm=crm) if records else {"success": True, "added": [], "updated": [], "failed": [], "total": 0}
        return {
            "success": True,
            "provider": config["provider"],
            "direction": "bidirectional",
            "exported": {"count": len(exported), "records": exported},
            "imported": imported,
        }

    return {
        "success": False,
        "error": f"Invalid direction: {direction}. Use 'export', 'import', or 'bidirectional'.",
    }


if __name__ == "__main__":
    print(json.dumps(sync_contacts(direction="export"), indent=2, ensure_ascii=False))
