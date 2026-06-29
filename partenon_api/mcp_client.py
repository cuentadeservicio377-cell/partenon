"""Async client for the Partenon Memory MCP server (partenon-memory)."""

import asyncio
import json
import os
import sys
from contextlib import AsyncExitStack
from typing import Any, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

DEFAULT_GBRAIN_DATABASE_URL = "sqlite:///data/gbrain.db"


class AsyncMemoryClient:
    """stdio-based MCP client for `mcp_servers.memory.server`.

    Usage:
        async with AsyncMemoryClient() as client:
            page = await client.get_page("workspace/default/missions/m-1")
            await client.put_page("workspace/default/missions/m-1", json.dumps({...}), tags=["mission"])
    """

    def __init__(self, database_url: Optional[str] = None):
        self.database_url = (
            database_url
            or os.getenv("GBRAIN_DATABASE_URL")
            or os.getenv("GBrain_DATABASE_URL")
            or DEFAULT_GBRAIN_DATABASE_URL
        )
        self._session: Optional[ClientSession] = None
        self._exit_stack: Optional[AsyncExitStack] = None

    async def __aenter__(self) -> "AsyncMemoryClient":
        self._exit_stack = AsyncExitStack()
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "mcp_servers.memory.server"],
            env={**os.environ, "GBRAIN_DATABASE_URL": self.database_url},
        )
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(*stdio_transport)
        )
        await self._session.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._exit_stack is not None:
            await self._exit_stack.aclose()
        self._session = None
        self._exit_stack = None

    async def call_tool(self, tool_name: str, **arguments: Any) -> Any:
        if self._session is None:
            raise RuntimeError("AsyncMemoryClient is not connected. Use it as an async context manager.")
        result = await self._session.call_tool(tool_name, arguments=arguments)
        for content in result.content:
            if getattr(content, "type", None) == "text":
                text = getattr(content, "text", "")
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return text
        return None

    async def get_page(self, slug: str) -> dict:
        """Retrieve a page by slug."""
        return await self.call_tool("memory_get_page", slug=slug) or {}

    async def put_page(
        self,
        slug: str,
        content: str,
        tags: Optional[list] = None,
    ) -> str:
        """Save or update a page. Tags are passed as a list of strings."""
        tag_arg = ",".join(tags) if tags else None
        return await self.call_tool("memory_put_page", slug=slug, content=content, tags=tag_arg) or "ok"

    async def search(self, query: str, limit: int = 20) -> list:
        """Search pages by query text."""
        return await self.call_tool("memory_search", query=query, limit=limit) or []


class AsyncDomainClient:
    """stdio-based MCP client for arbitrary Partenon domain servers.

    Usage:
        async with AsyncDomainClient("mcp_servers.payments.server") as client:
            result = await client.call_tool("payments_create_invoice", customer_email="...", amount=100)
    """

    def __init__(self, module_path: str, env: Optional[dict] = None):
        self.module_path = module_path
        self.env = env or {}
        self._session: Optional[ClientSession] = None
        self._exit_stack: Optional[AsyncExitStack] = None

    async def __aenter__(self) -> "AsyncDomainClient":
        self._exit_stack = AsyncExitStack()
        server_params = StdioServerParameters(
            command=sys.executable,
            args=["-m", self.module_path],
            env={**os.environ, **self.env},
        )
        stdio_transport = await self._exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self._session = await self._exit_stack.enter_async_context(
            ClientSession(*stdio_transport)
        )
        await self._session.initialize()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._exit_stack is not None:
            await self._exit_stack.aclose()
        self._session = None
        self._exit_stack = None

    async def call_tool(self, tool_name: str, **arguments: Any) -> Any:
        if self._session is None:
            raise RuntimeError("AsyncDomainClient is not connected. Use it as an async context manager.")
        result = await self._session.call_tool(tool_name, arguments=arguments)
        for content in result.content:
            if getattr(content, "type", None) == "text":
                text = getattr(content, "text", "")
                try:
                    return json.loads(text)
                except json.JSONDecodeError:
                    return text
        return None


def sync_call(
    tool_name: str,
    *,
    server_module: Optional[str] = None,
    database_url: Optional[str] = None,
    **kwargs: Any,
) -> Any:
    """Synchronous helper for non-async callers.

    This spins up a fresh stdio client with `asyncio.run`. It is convenient for
    scripts and the workflow engine, but it cannot be called from inside a
    running event loop (e.g. inside an async FastAPI request handler). In those
    cases use `AsyncMemoryClient` or `AsyncDomainClient` directly.

    If `server_module` is provided, the call is routed to that domain MCP server.
    Otherwise the `partenon-memory` server is used.
    """

    async def _run() -> Any:
        if server_module:
            async with AsyncDomainClient(server_module) as client:
                return await client.call_tool(tool_name, **kwargs)
        async with AsyncMemoryClient(database_url=database_url) as client:
            return await client.call_tool(tool_name, **kwargs)

    try:
        return asyncio.run(_run())
    except RuntimeError as exc:
        if "already running" in str(exc).lower():
            raise RuntimeError(
                "sync_call cannot be used inside a running event loop. "
                "Use AsyncMemoryClient or AsyncDomainClient in async code instead."
            ) from exc
        raise
