#!/usr/bin/env python3
"""
MCP client example — Partenon web promise placeholder.

Demonstrates how a hero profile or external tool would call the G-Brain MCP
server documented on `web/developers.html`. It uses the stdio transport to
launch `gbrain.server` and call the exposed tools.

This is a learning/example script, not production code.

Prerequisites:
  pip install mcp

Usage:
  python3 examples/mcp-client-example.py
"""

import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

REPO_ROOT = Path(__file__).resolve().parents[1]
GBRAIN_MODULE = REPO_ROOT / "gbrain"


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "gbrain.server"],
        env={"GBrain_DATABASE_URL": "sqlite:///data/gbrain_example.db"},
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("Available G-Brain tools:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            print("\nStoring a learning insight...")
            result = await session.call_tool(
                "gbrain_store_learning",
                {"profile": "scribe", "insight": "Example insight from MCP client stub"},
            )
            print(json.dumps(result, indent=2, default=str))

            print("\nSearching missions...")
            result = await session.call_tool("gbrain_search_missions", {"profile": "scribe"})
            print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
