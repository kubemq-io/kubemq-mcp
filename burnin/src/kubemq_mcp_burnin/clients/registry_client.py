from __future__ import annotations

from typing import Any

import httpx


class RegistryClient:
    """REST client for KubeMQ agent registry management."""

    def __init__(self, base_url: str) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=httpx.Timeout(10.0, connect=5.0),
        )

    async def register(self, card: dict[str, Any]) -> httpx.Response:
        """Register an agent with the KubeMQ registry."""
        return await self._client.post("/agents/register", json=card)

    async def deregister_post(self, agent_id: str) -> httpx.Response:
        """Deregister an agent via POST."""
        return await self._client.post(
            "/agents/deregister", json={"agent_id": agent_id}
        )

    async def deregister_delete(self, agent_id: str) -> httpx.Response:
        """Deregister an agent via DELETE."""
        return await self._client.delete(f"/agents/{agent_id}")

    async def heartbeat(self, agent_id: str) -> httpx.Response:
        """Send a heartbeat for the given agent."""
        return await self._client.post("/agents/heartbeat", json={"agent_id": agent_id})

    async def list_agents(self, **params: Any) -> httpx.Response:
        """List registered agents with optional query parameters."""
        return await self._client.get("/agents", params=params)

    async def get_agent(self, agent_id: str) -> httpx.Response:
        """Get details for a specific agent."""
        return await self._client.get(f"/agents/{agent_id}")

    async def close(self) -> None:
        """Close the underlying httpx client."""
        await self._client.aclose()
