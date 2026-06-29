"""Tests for the MCP stdio clients."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from partenon_api.mcp_client import AsyncDomainClient, AsyncMemoryClient, sync_call


class FakeContent:
    def __init__(self, text, content_type="text"):
        self.type = content_type
        self.text = text


class FakeToolResult:
    def __init__(self, content):
        self.content = content


def _make_client(session):
    client = AsyncMemoryClient(database_url="sqlite:///test.db")
    client._session = session
    return client


@pytest.mark.asyncio
async def test_call_tool_parses_json():
    session = AsyncMock()
    session.call_tool = AsyncMock(
        return_value=FakeToolResult([FakeContent(json.dumps({"ok": True}))])
    )
    client = _make_client(session)

    result = await client.call_tool("memory_search", query="test")
    assert result == {"ok": True}


@pytest.mark.asyncio
async def test_call_tool_returns_plain_text():
    session = AsyncMock()
    session.call_tool = AsyncMock(return_value=FakeToolResult([FakeContent("plain")]))
    client = _make_client(session)

    result = await client.call_tool("memory_get_page", slug="x")
    assert result == "plain"


@pytest.mark.asyncio
async def test_call_tool_returns_none_for_empty_content():
    session = AsyncMock()
    session.call_tool = AsyncMock(return_value=FakeToolResult([]))
    client = _make_client(session)

    result = await client.call_tool("memory_search", query="test")
    assert result is None


@pytest.mark.asyncio
async def test_call_tool_raises_when_not_connected():
    client = AsyncMemoryClient(database_url="sqlite:///test.db")
    with pytest.raises(RuntimeError):
        await client.call_tool("memory_search", query="test")


@pytest.mark.asyncio
async def test_get_page():
    session = AsyncMock()
    session.call_tool = AsyncMock(return_value=FakeToolResult([FakeContent('{"page": 1}')]))
    client = _make_client(session)

    result = await client.get_page("slug")
    assert result == {"page": 1}
    session.call_tool.assert_awaited_once_with(
        "memory_get_page", arguments={"slug": "slug"}
    )


@pytest.mark.asyncio
async def test_put_page_joins_tags():
    session = AsyncMock()
    session.call_tool = AsyncMock(return_value=FakeToolResult([FakeContent('"ok"')]))
    client = _make_client(session)

    await client.put_page("slug", "content", tags=["a", "b"])
    session.call_tool.assert_awaited_once_with(
        "memory_put_page",
        arguments={"slug": "slug", "content": "content", "tags": "a,b"},
    )


@pytest.mark.asyncio
async def test_search():
    session = AsyncMock()
    session.call_tool = AsyncMock(
        return_value=FakeToolResult([FakeContent(json.dumps([{"slug": "s"}]))])
    )
    client = _make_client(session)

    result = await client.search("query", limit=10)
    assert result == [{"slug": "s"}]
    session.call_tool.assert_awaited_once_with(
        "memory_search", arguments={"query": "query", "limit": 10}
    )


@pytest.mark.asyncio
async def test_async_domain_client_call_tool():
    session = AsyncMock()
    session.call_tool = AsyncMock(
        return_value=FakeToolResult([FakeContent(json.dumps({"invoice_id": "inv-1"}))])
    )
    client = AsyncDomainClient("mcp_servers.payments.server")
    client._session = session

    result = await client.call_tool("payments_create_invoice", customer_email="a@b.com", amount=100)
    assert result["invoice_id"] == "inv-1"


@pytest.mark.asyncio
async def test_async_domain_client_call_tool_raises_when_not_connected():
    client = AsyncDomainClient("mcp_servers.payments.server")
    with pytest.raises(RuntimeError):
        await client.call_tool("payments_create_invoice", customer_email="a@b.com")


def test_sync_call_routes_to_domain_server():
    with patch("partenon_api.mcp_client.AsyncDomainClient") as mock_domain:
        instance = MagicMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.call_tool = AsyncMock(return_value={"ok": True})
        mock_domain.return_value = instance

        result = sync_call(
            "payments_create_invoice",
            server_module="mcp_servers.payments.server",
            customer_email="a@b.com",
            amount=100,
        )
        assert result == {"ok": True}
        mock_domain.assert_called_once_with("mcp_servers.payments.server")


def test_sync_call_uses_memory_server_by_default():
    with patch("partenon_api.mcp_client.AsyncMemoryClient") as mock_memory:
        instance = MagicMock()
        instance.__aenter__ = AsyncMock(return_value=instance)
        instance.__aexit__ = AsyncMock(return_value=False)
        instance.call_tool = AsyncMock(return_value={"saved": True})
        mock_memory.return_value = instance

        result = sync_call("memory_put_page", slug="s", content="c")
        assert result == {"saved": True}
        mock_memory.assert_called_once_with(database_url=None)
