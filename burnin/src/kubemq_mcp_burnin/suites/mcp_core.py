from __future__ import annotations

import asyncio
import time
import uuid
from typing import Any

from kubemq_mcp_burnin.suites.base import BaseSuite


class MCPCoreSuite(BaseSuite):
    suite_name = "mcp_core"

    def _channel(self, suffix: str) -> str:
        return f"burnin-mcp-{suffix}-{uuid.uuid4().hex[:8]}"

    def get_tests(self) -> list[tuple[str, str, Any]]:
        return [
            ("M01", "queue_send", self.test_m01),
            ("M02", "queue_receive", self.test_m02),
            ("M03", "queue_peek", self.test_m03),
            ("M04", "queue_send with metadata/tags", self.test_m04),
            ("M05", "queue_send with delay", self.test_m05),
            ("M06", "queue_send with expiration", self.test_m06),
            ("M07", "queue_send with DLQ", self.test_m07),
            ("M08", "events_publish", self.test_m08),
            ("M09", "events_store_publish", self.test_m09),
            ("M10", "events_store_read (from_sequence)", self.test_m10),
            ("M11", "events_store_read (from_time)", self.test_m11),
            ("M12", "events_store_read_latest", self.test_m12),
            ("M13", "command_send", self.test_m13),
            ("M14", "query_send", self.test_m14),
            ("M15", "channel_list (all)", self.test_m15),
            ("M16", "channel_list (filtered by type)", self.test_m16),
            ("M17", "channel_list (filtered by pattern)", self.test_m17),
            ("M18", "channel_info", self.test_m18),
            ("M19", "Reserved channel rejection", self.test_m19),
        ]

    async def test_m01(self) -> int:
        ch = self._channel("q01")
        result = await self.mcp.tools_call(
            "queue_send",
            {
                "channel": ch,
                "body": "hello from m01",
            },
        )
        assert "error" not in result, f"queue_send JSON-RPC error: {result}"
        assert "result" in result, f"queue_send missing result: {result}"
        assert not result["result"].get("isError"), f"queue_send tool error: {result}"
        return 1

    async def test_m02(self) -> int:
        ch = self._channel("q02")
        await self.mcp.tools_call("queue_send", {"channel": ch, "body": "m02-body"})
        await asyncio.sleep(0.5)
        result = await self.mcp.tools_call(
            "queue_receive",
            {
                "channel": ch,
                "max_messages": 1,
            },
        )
        assert "result" in result, f"queue_receive failed: {result}"
        content = result["result"].get("content", [])
        assert len(content) > 0, "Expected at least one content item"
        text = content[0].get("text", "")
        assert "m02-body" in text, (
            f"Expected body 'm02-body' in received message, got: {text}"
        )
        return 3

    async def test_m03(self) -> int:
        ch = self._channel("q03")
        await self.mcp.tools_call("queue_send", {"channel": ch, "body": "m03-peek"})
        await asyncio.sleep(0.5)
        peek_result = await self.mcp.tools_call(
            "queue_peek",
            {
                "channel": ch,
                "max_messages": 1,
            },
        )
        assert "result" in peek_result
        recv_result = await self.mcp.tools_call(
            "queue_receive",
            {
                "channel": ch,
                "max_messages": 1,
            },
        )
        assert "result" in recv_result, "Message should still be in queue after peek"
        content = recv_result["result"].get("content", [])
        assert len(content) > 0, "Expected message still available after peek"
        return 3

    async def test_m04(self) -> int:
        ch = self._channel("q04")
        result = await self.mcp.tools_call(
            "queue_send",
            {
                "channel": ch,
                "body": "m04-body",
                "metadata": "m04-metadata",
                "tags": {"env": "test", "suite": "mcp_core"},
            },
        )
        assert "result" in result
        await asyncio.sleep(0.5)
        recv = await self.mcp.tools_call(
            "queue_receive", {"channel": ch, "max_messages": 1}
        )
        assert "result" in recv
        content = recv["result"].get("content", [])
        assert len(content) > 0
        text = content[0].get("text", "")
        assert "m04-body" in text, f"Body not preserved: {text}"
        return 3

    async def test_m05(self) -> int:
        ch = self._channel("q05")
        await self.mcp.tools_call(
            "queue_send",
            {
                "channel": ch,
                "body": "m05-delayed",
                "delay_seconds": 2,
            },
        )
        immediate = await self.mcp.tools_call(
            "queue_receive",
            {
                "channel": ch,
                "max_messages": 1,
            },
        )
        imm_content = immediate.get("result", {}).get("content", [])
        imm_text = imm_content[0].get("text", "") if imm_content else ""
        has_message_immediately = "m05-delayed" in imm_text

        await asyncio.sleep(3)
        delayed = await self.mcp.tools_call(
            "queue_receive",
            {
                "channel": ch,
                "max_messages": 1,
            },
        )
        del_content = delayed.get("result", {}).get("content", [])
        del_text = del_content[0].get("text", "") if del_content else ""
        has_message_after_delay = "m05-delayed" in del_text

        assert has_message_after_delay, (
            f"Delayed message should be available after waiting: {del_text}"
        )
        return 2

    async def test_m06(self) -> int:
        ch = self._channel("q06")
        await self.mcp.tools_call(
            "queue_send",
            {
                "channel": ch,
                "body": "m06-expiring",
                "expiration_seconds": 1,
            },
        )
        await asyncio.sleep(2)
        result = await self.mcp.tools_call(
            "queue_receive",
            {
                "channel": ch,
                "max_messages": 1,
            },
        )
        content = result.get("result", {}).get("content", [])
        text = content[0].get("text", "") if content else ""
        assert "m06-expiring" not in text or not content, (
            "Expired message should not be receivable"
        )
        return 1

    async def test_m07(self) -> int:
        ch = self._channel("q07")
        dlq_ch = self._channel("q07-dlq")
        await self.mcp.tools_call(
            "queue_send",
            {
                "channel": ch,
                "body": "m07-dlq",
                "max_receive_count": 1,
                "dead_letter_queue": dlq_ch,
            },
        )
        await asyncio.sleep(0.5)
        await self.mcp.tools_call("queue_receive", {"channel": ch, "max_messages": 1})
        await asyncio.sleep(1)
        dlq_result = await self.mcp.tools_call(
            "queue_receive",
            {
                "channel": dlq_ch,
                "max_messages": 1,
            },
        )
        assert "result" in dlq_result, "Expected DLQ result"
        return 2

    async def test_m08(self) -> int:
        ch = self._channel("ev08")
        result = await self.mcp.tools_call(
            "events_publish",
            {
                "channel": ch,
                "body": "m08-event",
            },
        )
        assert "result" in result, f"events_publish failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error, f"events_publish returned error: {result}"
        return 1

    async def test_m09(self) -> int:
        ch = self._channel("es09")
        result = await self.mcp.tools_call(
            "events_store_publish",
            {
                "channel": ch,
                "body": "m09-stored-event",
            },
        )
        assert "result" in result, f"events_store_publish failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error, f"events_store_publish returned error: {result}"
        return 1

    async def test_m10(self) -> int:
        ch = self._channel("es10")
        for i in range(3):
            await self.mcp.tools_call(
                "events_store_publish",
                {
                    "channel": ch,
                    "body": f"m10-msg-{i}",
                },
            )
        await asyncio.sleep(1)
        result = await self.mcp.tools_call(
            "events_store_read",
            {
                "channel": ch,
                "from_sequence": 1,
                "max_messages": 10,
            },
        )
        assert "result" in result, f"events_store_read failed: {result}"
        content = result["result"].get("content", [])
        assert len(content) > 0, "Expected at least one stored event"
        return 2

    async def test_m11(self) -> int:
        ch = self._channel("es11")
        ts_before = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        await self.mcp.tools_call(
            "events_store_publish",
            {
                "channel": ch,
                "body": "m11-timed",
            },
        )
        await asyncio.sleep(1)
        result = await self.mcp.tools_call(
            "events_store_read",
            {
                "channel": ch,
                "from_time": ts_before,
                "max_messages": 10,
            },
        )
        assert "result" in result, f"events_store_read (from_time) failed: {result}"
        return 1

    async def test_m12(self) -> int:
        ch = self._channel("es12")
        for i in range(5):
            await self.mcp.tools_call(
                "events_store_publish",
                {
                    "channel": ch,
                    "body": f"m12-latest-{i}",
                },
            )
        await asyncio.sleep(1)
        result = await self.mcp.tools_call(
            "events_store_read_latest",
            {
                "channel": ch,
                "count": 3,
            },
        )
        assert "result" in result, f"events_store_read_latest failed: {result}"
        return 1

    async def test_m13(self) -> int:
        ch = self._channel("cmd13")
        from kubemq_mcp_burnin.clients.kubemq_subscriber import (
            KubeMQSubscriberManager,
        )

        sub_mgr = KubeMQSubscriberManager(self.config.server.broker_address)
        try:
            await sub_mgr.start_command_subscriber(ch)
            await asyncio.sleep(1)
            result = await self.mcp.tools_call(
                "command_send",
                {
                    "channel": ch,
                    "body": "m13-command",
                    "timeout_seconds": 10,
                },
            )
            assert "result" in result, f"command_send failed: {result}"
            is_error = result.get("result", {}).get("isError", False)
            assert not is_error, f"command_send returned error: {result}"
        finally:
            await sub_mgr.stop_all()
        return 2

    async def test_m14(self) -> int:
        ch = self._channel("qry14")
        from kubemq_mcp_burnin.clients.kubemq_subscriber import (
            KubeMQSubscriberManager,
        )

        sub_mgr = KubeMQSubscriberManager(self.config.server.broker_address)
        try:
            await sub_mgr.start_query_subscriber(ch)
            await asyncio.sleep(1)
            result = await self.mcp.tools_call(
                "query_send",
                {
                    "channel": ch,
                    "body": "m14-query",
                    "timeout_seconds": 10,
                },
            )
            assert "result" in result, f"query_send failed: {result}"
            is_error = result.get("result", {}).get("isError", False)
            assert not is_error, f"query_send returned error: {result}"
        finally:
            await sub_mgr.stop_all()
        return 2

    async def test_m15(self) -> int:
        result = await self.mcp.tools_call("channel_list", {})
        assert "result" in result, f"channel_list failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error, f"channel_list returned error: {result}"
        return 1

    async def test_m16(self) -> int:
        result = await self.mcp.tools_call("channel_list", {"type": "queues"})
        assert "result" in result, f"channel_list (type=queues) failed: {result}"
        is_error = result.get("result", {}).get("isError", False)
        assert not is_error, f"channel_list returned error: {result}"
        return 1

    async def test_m17(self) -> int:
        result = await self.mcp.tools_call("channel_list", {"pattern": "burnin-"})
        assert "result" in result, f"channel_list (pattern) failed: {result}"
        return 1

    async def test_m18(self) -> int:
        ch = self._channel("info18")
        await self.mcp.tools_call("queue_send", {"channel": ch, "body": "m18-info"})
        await asyncio.sleep(0.5)
        result = await self.mcp.tools_call(
            "channel_info",
            {
                "channel": ch,
                "type": "queues",
            },
        )
        assert "result" in result, f"channel_info failed: {result}"
        return 1

    async def test_m19(self) -> int:
        result = await self.mcp.tools_call(
            "queue_send",
            {
                "channel": "_AGENTS_.test",
                "body": "m19-reserved",
            },
        )
        assert "result" in result
        is_error = result.get("result", {}).get("isError", False)
        assert is_error, "Expected error for reserved channel prefix _AGENTS_."
        return 1
