from __future__ import annotations

import json
from typing import Any

from kubemq_mcp_burnin.agents.manager import AgentManager
from kubemq_mcp_burnin.config import BurninConfig
from kubemq_mcp_burnin.metrics.tracker import TestTracker
from kubemq_mcp_burnin.suites.base import BaseSuite


class MCPProtocolSuite(BaseSuite):
    suite_name = "mcp_protocol"

    def __init__(
        self,
        config: BurninConfig,
        agent_manager: AgentManager,
        tracker: TestTracker,
        smoke_only: bool = False,
    ) -> None:
        super().__init__(config, agent_manager, tracker)
        self._smoke_only = smoke_only

    def get_tests(self) -> list[tuple[str, str, Any]]:
        all_tests = [
            ("P01", "Initialize handshake", self.test_p01),
            ("P02", "Ping", self.test_p02),
            ("P03", "Tools list (all tools)", self.test_p03),
            ("P04", "Tools list (with bridge)", self.test_p04),
            ("P05", "Unknown method", self.test_p05),
            ("P06", "Invalid params", self.test_p06),
            ("P07", "MCP-Protocol-Version header", self.test_p07),
            ("P08", "MCP-Session-Id header echo", self.test_p08),
            ("P09", "SSE keepalive stream (SKIP)", self.test_p09),
            ("P10", "Wrong Content-Type", self.test_p10),
            ("P11", "Empty method", self.test_p11),
            ("P12", "Invalid JSON-RPC version", self.test_p12),
            ("P13", "Notifications (no response)", self.test_p13),
        ]
        if self._smoke_only:
            return all_tests[:3]
        return all_tests

    async def test_p01(self) -> int:
        result = await self.mcp.initialize()
        assert "result" in result, f"Initialize failed: {result}"
        r = result["result"]
        assert r.get("protocolVersion") == "2025-11-25", (
            f"Expected protocolVersion '2025-11-25', got {r.get('protocolVersion')}"
        )
        assert "capabilities" in r, "Missing capabilities"
        assert "serverInfo" in r, "Missing serverInfo"
        assert r["serverInfo"].get("name") == "kubemq", (
            f"Expected serverInfo.name='kubemq', got {r['serverInfo'].get('name')}"
        )
        assert "_meta" in r and "sessionId" in r["_meta"], "Missing _meta.sessionId"
        return 5

    async def test_p02(self) -> int:
        await self.mcp.initialize()
        result = await self.mcp.ping()
        assert "result" in result, f"Ping failed: {result}"
        return 1

    async def test_p03(self) -> int:
        await self.mcp.initialize()
        result = await self.mcp.tools_list()
        assert "result" in result, f"tools/list failed: {result}"
        tools = result["result"].get("tools", [])
        assert len(tools) == 15, (
            f"Expected 15 tools (11 core + 4 bridge), got {len(tools)}"
        )
        for tool in tools:
            assert "name" in tool, f"Tool missing name: {tool}"
            assert "description" in tool, f"Tool missing description: {tool}"
            assert "inputSchema" in tool, f"Tool missing inputSchema: {tool}"
        return 3

    async def test_p04(self) -> int:
        await self.mcp.initialize()
        result = await self.mcp.tools_list()
        assert "result" in result
        tools = result["result"].get("tools", [])
        tool_names = {t["name"] for t in tools}
        bridge_tools = {"agent_list", "agent_info", "agent_send", "agent_query"}
        missing = bridge_tools - tool_names
        assert not missing, f"Missing bridge tools: {missing}"
        core_tools = {
            "queue_send",
            "queue_receive",
            "queue_peek",
            "events_publish",
            "events_store_publish",
            "events_store_read",
            "events_store_read_latest",
            "command_send",
            "query_send",
            "channel_list",
            "channel_info",
        }
        missing_core = core_tools - tool_names
        assert not missing_core, f"Missing core tools: {missing_core}"
        return 2

    async def test_p05(self) -> int:
        await self.mcp.initialize()
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 999,
                "method": "nonexistent/method",
            }
        )
        resp = await self.mcp.send_raw(payload.encode())
        data = resp.json()
        assert "error" in data, "Expected error for unknown method"
        assert data["error"]["code"] == -32601, (
            f"Expected code -32601 (MethodNotFound), got {data['error']['code']}"
        )
        return 2

    async def test_p06(self) -> int:
        await self.mcp.initialize()
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 998,
                "method": "tools/call",
                "params": "invalid-not-an-object",
            }
        )
        resp = await self.mcp.send_raw(payload.encode())
        data = resp.json()
        assert "error" in data, "Expected error for invalid params"
        assert data["error"]["code"] == -32602, (
            f"Expected code -32602 (InvalidParams), got {data['error']['code']}"
        )
        return 2

    async def test_p07(self) -> int:
        await self.mcp.initialize()
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 997,
                "method": "ping",
            }
        )
        resp = await self.mcp.send_raw(payload.encode())
        proto_version = resp.headers.get("MCP-Protocol-Version")
        assert proto_version == "2025-11-25", (
            f"Expected MCP-Protocol-Version: 2025-11-25, got {proto_version}"
        )
        return 1

    async def test_p08(self) -> int:
        await self.mcp.initialize()
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 996,
                "method": "ping",
            }
        )
        resp = await self.mcp.send_raw(
            payload.encode(),
            headers={"MCP-Session-Id": "test-session-p08"},
        )
        echoed = resp.headers.get("MCP-Session-Id")
        assert echoed == "test-session-p08", (
            f"Expected MCP-Session-Id echo 'test-session-p08', got {echoed}"
        )
        return 1

    async def test_p09(self) -> int:
        # SKIP — KubeMQ MCP endpoint uses stateless HTTP POST (Streamable HTTP transport),
        # not persistent SSE connections. SSE keepalive is not applicable.
        await self.mcp.initialize()
        return 1

    async def test_p10(self) -> int:
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 994,
                "method": "ping",
            }
        )
        resp = await self.mcp.send_raw(payload.encode(), content_type="text/plain")
        data = resp.json()
        assert "error" in data, "Expected error for wrong Content-Type"
        assert data["error"]["code"] == -32700, (
            f"Expected code -32700 (ParseError), got {data['error']['code']}"
        )
        return 2

    async def test_p11(self) -> int:
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 993,
                "method": "",
            }
        )
        resp = await self.mcp.send_raw(payload.encode())
        data = resp.json()
        assert "error" in data, "Expected error for empty method"
        assert data["error"]["code"] == -32600, (
            f"Expected code -32600 (InvalidRequest), got {data['error']['code']}"
        )
        return 2

    async def test_p12(self) -> int:
        payload = json.dumps(
            {
                "jsonrpc": "1.0",
                "id": 992,
                "method": "ping",
            }
        )
        resp = await self.mcp.send_raw(payload.encode())
        data = resp.json()
        assert "error" in data, "Expected error for invalid JSON-RPC version"
        assert data["error"]["code"] == -32600, (
            f"Expected code -32600 (InvalidRequest), got {data['error']['code']}"
        )
        return 2

    async def test_p13(self) -> int:
        await self.mcp.initialize()
        payload = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "notifications/initialized",
            }
        )
        resp = await self.mcp.send_raw(payload.encode())
        assert (
            resp.status_code == 200 or resp.status_code == 202 or len(resp.content) == 0
        ), (
            f"Notification should return empty or 202, got {resp.status_code} with body: {resp.text[:200]}"
        )
        return 1
