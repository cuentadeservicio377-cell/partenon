"""Tests for partenon_api configuration helpers."""

import pytest

from partenon_api import config


class TestGetSecret:
    def test_prefers_partenon_api_secret(self, monkeypatch):
        monkeypatch.setenv("PARTENON_API_SECRET", "partenon-secret-32-chars-long")
        monkeypatch.setenv("DASHBOARD_AUTH_SECRET", "dashboard-secret-32-chars")
        assert config.get_secret() == "partenon-secret-32-chars-long"

    def test_falls_back_to_dashboard_auth_secret(self, monkeypatch):
        monkeypatch.delenv("PARTENON_API_SECRET", raising=False)
        monkeypatch.setenv("DASHBOARD_AUTH_SECRET", "dashboard-secret-32-chars")
        assert config.get_secret() == "dashboard-secret-32-chars"

    def test_raises_when_missing(self, monkeypatch):
        monkeypatch.delenv("PARTENON_API_SECRET", raising=False)
        monkeypatch.delenv("DASHBOARD_AUTH_SECRET", raising=False)
        with pytest.raises(RuntimeError):
            config.get_secret()


class TestGetGbrainDatabaseUrl:
    def test_defaults_to_sqlite(self, monkeypatch):
        monkeypatch.delenv("GBRAIN_DATABASE_URL", raising=False)
        monkeypatch.delenv("GBrain_DATABASE_URL", raising=False)
        assert config.get_gbrain_database_url() == config.DEFAULT_GBRAIN_DATABASE_URL

    def test_reads_gbrain_database_url(self, monkeypatch):
        monkeypatch.setenv("GBRAIN_DATABASE_URL", "postgresql://user:pass@host/db")
        assert config.get_gbrain_database_url() == "postgresql://user:pass@host/db"

    def test_reads_legacy_gbrain_database_url(self, monkeypatch):
        monkeypatch.setenv("GBrain_DATABASE_URL", "postgresql://legacy/db")
        assert config.get_gbrain_database_url() == "postgresql://legacy/db"


class TestNetworkDefaults:
    def test_get_api_host_default(self, monkeypatch):
        monkeypatch.delenv("PARTENON_API_HOST", raising=False)
        assert config.get_api_host() == config.DEFAULT_API_HOST

    def test_get_api_port_default(self, monkeypatch):
        monkeypatch.delenv("PARTENON_API_PORT", raising=False)
        assert config.get_api_port() == config.DEFAULT_API_PORT

    def test_get_dashboard_origin_default(self, monkeypatch):
        monkeypatch.delenv("DASHBOARD_ORIGIN", raising=False)
        assert config.get_dashboard_origin() == config.DEFAULT_DASHBOARD_ORIGIN


class TestGetDataDir:
    def test_uses_default_and_creates_path(self, monkeypatch, tmp_path):
        monkeypatch.setattr(config, "DATA_DIR", tmp_path / "data")
        monkeypatch.delenv("PARTENON_DATA_DIR", raising=False)
        result = config.get_data_dir()
        assert result == tmp_path / "data"
        assert result.exists()

    def test_respects_env_variable(self, monkeypatch, tmp_path):
        env_path = tmp_path / "custom_data"
        monkeypatch.setenv("PARTENON_DATA_DIR", str(env_path))
        result = config.get_data_dir()
        assert result == env_path
        assert result.exists()
