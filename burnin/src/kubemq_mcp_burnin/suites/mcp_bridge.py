from __future__ import annotations

import json
from typing import Any

from kubemq_mcp_burnin.suites.base import BaseSuite


class MCPBridgeSuite(BaseSuite):
    suite_name = "mcp_bridge"

    def _echo_agent_id(self) -> str:
        agents = self.agent_manager.get_agents_by_type("echo")
        if not agents:
            raise RuntimeError("No echo agents registered")
        return agents[0].agent_id

    def get_tests(self) -> list[tuple[str, str, Any]]:
        return [
            ("B01", "agent_list (no filter)", self.test_b01),
            ("B02", "agent_list with skill_tags", self.test_b02),
            ("B03", "agent_info", self.test_b03),
            ("B04", "agent_info non-existent", self.test_b04),
            ("B05", "agent_send blocking=true", self.test_b05),
            ("B06", "agent_send blocking=false", self.test_b06),
            ("B07", "agent_send with context_id", self.test_b07),
            ("B08", "agent_send with timeout", self.test_b08),
            ("B09", "agent_send timeout exceeded", self.test_b09),
            ("B10", "agent_query tasks/get", self.test_b10),
            ("B11", "agent_query tasks/cancel", self.test_b11),
            ("B12", "agent_query custom method", self.test_b12),
            ("B13", "Bridge to non-existent agent", self.test_b13),
            ("B14", "Bridge timeout propagation", self.test_b14),
        ]

    async def test_b01(self) -> int:
        result = await self.mcp.tools_call("agent_list", {})
        assert "result" in result, f"agent_list failed: {result}"
        content = result["result"].get("content", [])
        assert len(content) > 0, "Expected content from agent_list"
        text = content[0].get("text", "")
        agents = json.loads(text) if text else []
        assert isinstance(agents, list), f"Expected list, got {type(agents)}"
        assert len(agents) > 0, "Expected at least one registered agent"
        return 3

    async def test_b02(self) -> int:
        result = await self.mcp.tools_call(
            "agent_list",
            {
                "skill_tags": ["test"],
            },
        )
        assert "result" in result, f"agent_list with skill_tags failed: {result}"
        content = result["result"].get("content", [])
        assert len(content) > 0
        return 1

    async def test_b03(self) -> int:
        agent_id = self._echo_agent_id()
        result = await self.mcp.tools_call(
            "agent_info",
            {
                "agent_id": agent_id,
            },
        )
        assert "result" in result, f"agent_info failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error, f"agent_info returned error: {result}"
        content = result["result"].get("content", [])
        assert len(content) > 0
        text = content[0].get("text", "")
        info = json.loads(text)
        assert info.get("agent_id") == agent_id
        return 3

    async def test_b04(self) -> int:
        result = await self.mcp.tools_call(
            "agent_info",
            {
                "agent_id": "nonexistent-b04",
            },
        )
        assert "result" in result
        is_error = result.get("result", {}).get("isError", False)
        assert is_error, "Expected isError=true for non-existent agent"
        return 1

    async def test_b05(self) -> int:
        result = await self.mcp.tools_call(
            "agent_send",
            {
                "agent_id": self._echo_agent_id(),
                "message": "hello from b05",
            },
        )
        assert "result" in result, f"agent_send failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error, f"agent_send returned error: {result}"
        content = result["result"].get("content", [])
        assert len(content) > 0, "Expected response content from echo agent"
        return 2

    async def test_b06(self) -> int:
        agent_id = self._echo_agent_id()
        result = await self.mcp.tools_call(
            "agent_send",
            {
                "agent_id": agent_id,
                "message": "b06-nonblocking",
                "blocking": False,
            },
        )
        assert "result" in result, f"agent_send blocking=false failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error, f"agent_send returned error: {result}"
        return 2

    async def test_b07(self) -> int:
        result = await self.mcp.tools_call(
            "agent_send",
            {
                "agent_id": self._echo_agent_id(),
                "message": "b07-context",
                "context_id": "ctx-b07",
            },
        )
        assert "result" in result, f"agent_send with context_id failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error
        return 1

    async def test_b08(self) -> int:
        result = await self.mcp.tools_call(
            "agent_send",
            {
                "agent_id": self._echo_agent_id(),
                "message": "b08-timeout",
                "timeout_seconds": 5,
            },
        )
        assert "result" in result, f"agent_send with timeout failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error
        return 1

    async def test_b09(self) -> int:
        slow_agents = self.agent_manager.get_agents_by_type("slow")
        if not slow_agents:
            raise RuntimeError("No slow agents available")
        result = await self.mcp.tools_call(
            "agent_send",
            {
                "agent_id": slow_agents[0].agent_id,
                "message": "b09-will-timeout",
                "timeout_seconds": 1,
            },
        )
        assert "result" in result
        is_error = result.get("result", {}).get("isError", False)
        assert is_error, "Expected timeout error for slow agent with short timeout"
        return 1

    async def test_b10(self) -> int:
        result = await self.mcp.tools_call(
            "agent_query",
            {
                "agent_id": self._echo_agent_id(),
                "method": "tasks/get",
            },
        )
        assert "result" in result, f"agent_query tasks/get failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error
        return 1

    async def test_b11(self) -> int:
        result = await self.mcp.tools_call(
            "agent_query",
            {
                "agent_id": self._echo_agent_id(),
                "method": "tasks/cancel",
            },
        )
        assert "result" in result, f"agent_query tasks/cancel failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error
        return 1

    async def test_b12(self) -> int:
        result = await self.mcp.tools_call(
            "agent_query",
            {
                "agent_id": self._echo_agent_id(),
                "method": "custom/action",
            },
        )
        assert "result" in result, f"agent_query custom method failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error
        return 1

    async def test_b13(self) -> int:
        result = await self.mcp.tools_call(
            "agent_send",
            {
                "agent_id": "invalid-agent-b13",
                "message": "b13-nonexistent",
            },
        )
        assert "result" in result
        is_error = result.get("result", {}).get("isError", False)
        assert is_error, "Expected isError=true for non-existent agent"
        return 1

    async def test_b14(self) -> int:
        result = await self.mcp.tools_call(
            "agent_send",
            {
                "agent_id": self._echo_agent_id(),
                "message": "b14-timeout-prop",
                "timeout_seconds": 5,
            },
        )
        assert "result" in result, (
            f"agent_send for timeout propagation failed: {result}"
        )
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error, (
            "Expected success (GatewayTimeoutBuffer adds 10s to user timeout)"
        )
        return 1
