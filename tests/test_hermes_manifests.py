"""Hermes manifest validation tests.

Validates that every Partenon hero profile has a well-formed config.yaml and
distribution.yaml, that declared MCP servers can be imported, and that every
tool permission maps to a function in the corresponding MCP server.
"""

import ast
import importlib.util
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
HERMES_PROFILES_DIR = REPO_ROOT / "hermes" / "profiles"
MCP_SERVERS_DIR = REPO_ROOT / "mcp_servers"

REQUIRED_CONFIG_KEYS = [
    "profile",
    "model",
    "skills",
    "mcp_servers",
    "permissions",
    "workflows",
    "handoffs",
    "behavior",
]

# Map tool-name prefixes to the MCP server domain directory that implements them.
TOOL_PREFIX_TO_DOMAIN = {
    "finance_": "finance",
    "comms_": "comms",
    "payments_": "payments",
    "security_": "security",
    "relations_": "relations",
    "ops_": "ops",
    "gbrain_": "memory",
    "memory_": "memory",
    "workspace_": "google_workspace",
    "slack_": "notifications",
}

# Server names that may appear in permissions but are not tool names.
SERVER_PERMISSIONS = {
    "partenon-memory",
    "partenon-finance",
    "partenon-comms",
    "partenon-payments",
    "partenon-security",
    "partenon-relations",
    "partenon-ops",
    "partenon-google-workspace",
    "partenon-slack",
}


def _profile_dirs() -> list[Path]:
    return sorted(d for d in HERMES_PROFILES_DIR.iterdir() if d.is_dir())


def _server_functions(domain: str) -> set[str]:
    """Return the set of function names defined in mcp_servers/<domain>/server.py."""
    server_file = MCP_SERVERS_DIR / domain / "server.py"
    assert server_file.exists(), f"Missing server file: {server_file}"
    tree = ast.parse(server_file.read_text(encoding="utf-8"))
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}


@pytest.mark.parametrize("profile_dir", _profile_dirs(), ids=lambda d: d.name)
def test_config_yaml_exists_and_loads(profile_dir: Path) -> None:
    config_file = profile_dir / "config.yaml"
    assert config_file.exists(), f"Missing config file: {config_file}"
    data = yaml.safe_load(config_file.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "config.yaml must parse to a mapping"
    for key in REQUIRED_CONFIG_KEYS:
        assert key in data, f"Missing required key in config.yaml: {key}"


@pytest.mark.parametrize("profile_dir", _profile_dirs(), ids=lambda d: d.name)
def test_distribution_yaml_exists_and_loads(profile_dir: Path) -> None:
    dist_file = profile_dir / "distribution.yaml"
    assert dist_file.exists(), f"Missing distribution file: {dist_file}"
    data = yaml.safe_load(dist_file.read_text(encoding="utf-8"))
    assert isinstance(data, dict), "distribution.yaml must parse to a mapping"
    assert "name" in data, "distribution.yaml missing 'name'"
    assert "version" in data, "distribution.yaml missing 'version'"


@pytest.mark.parametrize("profile_dir", _profile_dirs(), ids=lambda d: d.name)
def test_mcp_servers_are_importable(profile_dir: Path) -> None:
    config = yaml.safe_load((profile_dir / "config.yaml").read_text(encoding="utf-8"))
    mcp_servers = config.get("mcp_servers", {})
    assert isinstance(mcp_servers, dict), "mcp_servers must be a mapping"
    for server_name, spec in mcp_servers.items():
        args = spec.get("args", [])
        # We expect args like ["-m", "mcp_servers.<domain>.server"].
        module_name = None
        for i, arg in enumerate(args):
            if arg == "-m" and i + 1 < len(args):
                module_name = args[i + 1]
                break
        assert module_name, f"MCP server {server_name} has no '-m <module>' args"
        module_path = REPO_ROOT / f"{module_name.replace('.', '/')}.py"
        assert module_path.exists(), f"MCP server module missing: {module_path}"
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)


@pytest.mark.parametrize("profile_dir", _profile_dirs(), ids=lambda d: d.name)
def test_permission_tools_exist(profile_dir: Path) -> None:
    config = yaml.safe_load((profile_dir / "config.yaml").read_text(encoding="utf-8"))
    permissions = config.get("permissions", [])
    assert isinstance(permissions, list), "permissions must be a list"

    domain_cache: dict[str, set[str]] = {}
    for perm in permissions:
        if perm in SERVER_PERMISSIONS or perm in {"file", "terminal"}:
            continue
        domain = None
        for prefix, dom in TOOL_PREFIX_TO_DOMAIN.items():
            if perm.startswith(prefix):
                domain = dom
                break
        if domain is None:
            pytest.fail(f"Permission '{perm}' does not match a known tool prefix")
        if domain not in domain_cache:
            domain_cache[domain] = _server_functions(domain)
        assert perm in domain_cache[domain], (
            f"Permission '{perm}' not found as a function in mcp_servers/{domain}/server.py"
        )
