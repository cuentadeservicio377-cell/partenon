"""
Partenon configuration loader.

Minimal loader for company.yaml used by the onboarding engine.
"""

from pathlib import Path
from typing import Any, Dict, Optional


class ConfigLoader:
    """Loads and exposes company.yaml configuration."""

    def __init__(self, config_path: Optional[str] = None):
        if config_path:
            self.config_path = Path(config_path)
        else:
            self.config_path = self._find_company_config()
        self._data = self._load()

    def _find_company_config(self) -> Path:
        """Look for config/company.yaml starting from the current directory."""
        cwd = Path.cwd()
        candidates = [
            cwd / "config" / "company.yaml",
            cwd.parent / "config" / "company.yaml",
            Path.home() / ".hermes" / "partenon" / "config" / "company.yaml",
        ]
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return cwd / "config" / "company.yaml"

    def _load(self) -> Dict[str, Any]:
        """Load YAML or fallback to empty dict."""
        if not self.config_path.exists():
            return {}
        try:
            import yaml

            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}

    @property
    def name(self) -> str:
        company = self._data.get("company", {})
        return company.get("name", "My Company")

    @property
    def industry(self) -> str:
        company = self._data.get("company", {})
        return company.get("industry", "services")

    @property
    def currency(self) -> str:
        company = self._data.get("company", {})
        return company.get("currency", "USD")

    @property
    def language(self) -> str:
        company = self._data.get("company", {})
        return company.get("language", "en")

    @property
    def timezone(self) -> str:
        company = self._data.get("company", {})
        return company.get("timezone", "UTC")

    def integration_active(self, name: str) -> bool:
        integrations = self._data.get("integrations", {})
        integration = integrations.get(name, {})
        return bool(integration.get("active", False))

    def department_active(self, name: str) -> bool:
        profiles = self._data.get("profiles", {})
        profile = profiles.get(name, {})
        return bool(profile.get("active", False))


def get_config() -> ConfigLoader:
    return ConfigLoader()
