"""Partenon Relations MCP server (dry-run wrapper)."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("partenon-relations")


@mcp.tool()
def relations_register_client(name: str, email: str = "", dry_run: bool = True) -> dict:
    """Register a client or vendor."""
    if dry_run:
        return {"ok": True, "dry_run": True, "client_id": "CLI-001", "name": name}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_schedule_followup(client_id: str, days: int = 2, dry_run: bool = True) -> dict:
    """Schedule a follow-up with a contact."""
    if dry_run:
        return {"ok": True, "dry_run": True, "client_id": client_id, "due_in_days": days}
    return {"ok": False, "error": "live execution requires CRM credentials"}


@mcp.tool()
def relations_generate_proposal(client_id: str, amount: float, dry_run: bool = True) -> dict:
    """Generate a proposal for a client."""
    if dry_run:
        return {"ok": True, "dry_run": True, "client_id": client_id, "amount": amount}
    return {"ok": False, "error": "live execution requires CRM credentials"}


if __name__ == "__main__":
    mcp.run()
