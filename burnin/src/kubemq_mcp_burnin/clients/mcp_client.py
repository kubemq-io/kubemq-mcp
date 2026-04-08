from __future__ import annotations

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

_JSONRPC_VERSION = "2.0"


class MCPClient:
    """Raw httpx client for MCP JSON-RPC 2.0 endpoint."""

    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=httpx.Timeout(timeout, connect=10.0),
        )
        self._request_id = 0
        self._session_id: str | None = None
        self._initialized = False

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def _send_jsonrpc(
        self,
        method: str,
        params: dict[str, Any] | None = None,
        *,
        include_id: bool = True,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        payload: dict[str, Any] = {"jsonrpc": _JSONRPC_VERSION, "method": method}
        if include_id:
            payload["id"] = self._next_id()
        if params:
            payload["params"] = params

        hdrs = {"Content-Type": "application/json", **(headers or {})}
        if self._session_id:
            hdrs["MCP-Session-Id"] = self._session_id

        return await self._client.post("/mcp", json=payload, headers=hdrs)

    async def initialize(self) -> dict[str, Any]:
        """Perform MCP initialize handshake."""
        resp = await self._send_jsonrpc(
            "initialize",
            {
                "protocolVersion": "2025-11-25",
                "capabilities": {},
                "clientInfo": {"name": "kubemq-mcp-burnin", "version": "1.0.0"},
            },
        )
        resp.raise_for_status()
        result = resp.json()
        if "error" in result:
            raise RuntimeError(f"MCP initialize failed: {result['error']}")
        meta = result.get("result", {}).get("_meta")
        if isinstance(meta, dict):
            self._session_id = meta.get("sessionId")

        await self._send_jsonrpc("notifications/initialized", include_id=False)
        self._initialized = True
        return result

    async def ping(self) -> dict[str, Any]:
        """Send a ping health-check request."""
        resp = await self._send_jsonrpc("ping")
        resp.raise_for_status()
        return resp.json()

    async def tools_list(self) -> dict[str, Any]:
        """Retrieve the list of available MCP tools."""
        resp = await self._send_jsonrpc("tools/list")
        resp.raise_for_status()
        return resp.json()

    async def tools_call(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> dict[str, Any]:
        """Invoke an MCP tool by name with the given arguments."""
        resp = await self._send_jsonrpc(
            "tools/call",
            {
                "name": tool_name,
                "arguments": arguments,
            },
        )
        resp.raise_for_status()
        return resp.json()

    async def send_raw(
        self,
        body: bytes | str,
        content_type: str = "application/json",
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Send a raw HTTP request to the MCP endpoint."""
        hdrs = {"Content-Type": content_type, **(headers or {})}
        if self._session_id:
            hdrs.setdefault("MCP-Session-Id", self._session_id)
        return await self._client.post("/mcp", content=body, headers=hdrs)

    async def close(self) -> None:
        """Close the underlying httpx client."""
        await self._client.aclose()
