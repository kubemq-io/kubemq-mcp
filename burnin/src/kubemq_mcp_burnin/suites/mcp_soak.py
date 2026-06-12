from __future__ import annotations

import asyncio
import collections
import logging
import random
import time
import uuid
from typing import Any

from kubemq_mcp_burnin.clients.mcp_client import MCPClient
from kubemq_mcp_burnin.suites.base import BaseSuite

logger = logging.getLogger(__name__)


class MCPSoakSuite(BaseSuite):
    suite_name = "mcp_soak"

    def _channel(self, prefix: str) -> str:
        return f"soak-{prefix}-{uuid.uuid4().hex[:8]}"

    def get_tests(self) -> list[tuple[str, str, Any]]:
        return [
            ("S01", "Queue throughput", self.test_s01),
            ("S02", "Events-store throughput", self.test_s02),
            ("S03", "Mixed workload", self.test_s03),
            ("S04", "Session stability", self.test_s04),
            ("S05", "Concurrent sessions", self.test_s05),
        ]

    async def test_s01(self) -> int:
        """Sustained queue_send + queue_receive at target rate."""
        duration = self.config.duration_seconds()
        rate = self.config.soak.rate
        channels = [self._channel("s01") for _ in range(self.config.soak.channels_per_pattern)]
        errors = 0
        ops = 0
        start = time.time()

        while time.time() - start < duration:
            ch = channels[ops % len(channels)]
            try:
                send_result = await self.mcp.tools_call(
                    "queue_send", {"channel": ch, "body": f"s01-msg-{ops}"}
                )
                if send_result.get("result", {}).get("isError"):
                    errors += 1
                ops += 1

                recv_result = await self.mcp.tools_call(
                    "queue_receive", {"channel": ch, "max_messages": 1}
                )
                if recv_result.get("result", {}).get("isError"):
                    errors += 1
                ops += 1
            except Exception as exc:
                logger.debug("S01 soak operation failed: %s", exc)
                errors += 2
                ops += 2

            await asyncio.sleep(1.0 / rate)

        error_rate = (errors / ops * 100) if ops > 0 else 0.0
        assert error_rate < self.config.thresholds.max_error_rate_pct, (
            f"Queue throughput error rate {error_rate:.1f}% exceeds threshold "
            f"{self.config.thresholds.max_error_rate_pct}%"
        )
        return ops

    async def test_s02(self) -> int:
        """Sustained events publish + read at target rate."""
        duration = self.config.duration_seconds()
        rate = self.config.soak.rate
        channels = [self._channel("s02") for _ in range(self.config.soak.channels_per_pattern)]
        errors = 0
        ops = 0
        start = time.time()

        while time.time() - start < duration:
            ch = channels[ops % len(channels)]
            try:
                if ops % 3 == 0:
                    result = await self.mcp.tools_call(
                        "events_publish", {"channel": ch, "body": f"s02-ephemeral-{ops}"}
                    )
                elif ops % 3 == 1:
                    result = await self.mcp.tools_call(
                        "events_store_publish", {"channel": ch, "body": f"s02-stored-{ops}"}
                    )
                else:
                    result = await self.mcp.tools_call(
                        "events_store_read", {"channel": ch, "from_sequence": 1, "max_messages": 5}
                    )

                if result.get("result", {}).get("isError"):
                    errors += 1
                ops += 1
            except Exception as exc:
                logger.debug("S02 soak operation failed: %s", exc)
                errors += 1
                ops += 1

            await asyncio.sleep(1.0 / rate)

        error_rate = (errors / ops * 100) if ops > 0 else 0.0
        assert error_rate < self.config.thresholds.max_error_rate_pct, (
            f"Events throughput error rate {error_rate:.1f}% exceeds threshold"
        )
        return ops

    async def test_s03(self) -> int:
        """Random tool selection from weighted distribution."""
        duration = self.config.duration_seconds()
        rate = self.config.soak.rate
        errors = 0
        ops = 0
        latencies: collections.deque[float] = collections.deque(maxlen=50_000)
        start = time.time()

        tools_weights = [
            ("queue_send", 0.30),
            ("queue_receive", 0.30),
            ("events_publish", 0.15),
            ("events_store_publish", 0.10),
            ("command_send", 0.05),
            ("query_send", 0.05),
            ("channel_list", 0.05),
        ]
        tool_names = [t[0] for t in tools_weights]
        weights = [t[1] for t in tools_weights]

        ch_queue = self._channel("s03-q")
        ch_events = self._channel("s03-ev")
        ch_store = self._channel("s03-es")

        await self.mcp.tools_call("queue_send", {"channel": ch_queue, "body": "seed"})

        while time.time() - start < duration:
            tool = random.choices(tool_names, weights=weights, k=1)[0]
            op_start = time.time()
            try:
                if tool == "queue_send":
                    await self.mcp.tools_call("queue_send", {"channel": ch_queue, "body": f"s03-{ops}"})
                elif tool == "queue_receive":
                    await self.mcp.tools_call("queue_receive", {"channel": ch_queue, "max_messages": 1})
                elif tool == "events_publish":
                    await self.mcp.tools_call("events_publish", {"channel": ch_events, "body": f"s03-ev-{ops}"})
                elif tool == "events_store_publish":
                    await self.mcp.tools_call("events_store_publish", {"channel": ch_store, "body": f"s03-es-{ops}"})
                elif tool == "command_send":
                    await self.mcp.tools_call("command_send", {"channel": ch_queue, "body": "s03-cmd", "timeout_seconds": 2})
                elif tool == "query_send":
                    await self.mcp.tools_call("query_send", {"channel": ch_queue, "body": "s03-qry", "timeout_seconds": 2})
                elif tool == "channel_list":
                    await self.mcp.tools_call("channel_list", {})

                latencies.append((time.time() - op_start) * 1000)
                ops += 1
            except Exception as exc:
                logger.debug("S03 soak operation failed: %s", exc)
                errors += 1
                ops += 1

            await asyncio.sleep(1.0 / rate)

        error_rate = (errors / ops * 100) if ops > 0 else 0.0
        assert error_rate < self.config.thresholds.max_error_rate_pct, (
            f"Mixed workload error rate {error_rate:.1f}% exceeds threshold"
        )

        if latencies:
            sorted_lat = sorted(latencies)
            p99 = sorted_lat[int(len(sorted_lat) * 0.99)]
            assert p99 < self.config.thresholds.max_p99_latency_ms, (
                f"p99 latency {p99:.0f}ms exceeds threshold {self.config.thresholds.max_p99_latency_ms}ms"
            )
        return ops

    async def test_s04(self) -> int:
        """Repeated init/tool-call/close cycles with fresh client each time."""
        duration = self.config.duration_seconds()
        errors = 0
        cycles = 0
        start = time.time()

        ch = self._channel("s04")  # reuse one channel; the test churns sessions, not channels
        while time.time() - start < duration:
            client = MCPClient(self.config.server.address)
            try:
                await client.initialize()
                await client.tools_call("queue_send", {"channel": ch, "body": f"s04-cycle-{cycles}"})
                cycles += 1
            except Exception as exc:
                logger.debug("S04 session cycle failed: %s", exc)
                errors += 1
                cycles += 1
            finally:
                await client.close()

            await asyncio.sleep(0.1)

        error_rate = (errors / cycles * 100) if cycles > 0 else 0.0
        assert error_rate < self.config.thresholds.max_error_rate_pct, (
            f"Session stability error rate {error_rate:.1f}% exceeds threshold"
        )
        return cycles

    async def test_s05(self) -> int:
        """Multiple parallel MCP sessions."""
        duration = self.config.duration_seconds()
        num_workers = 10
        errors_per_worker: list[int] = [0] * num_workers
        ops_per_worker: list[int] = [0] * num_workers

        async def session_worker(worker_id: int) -> None:
            client = MCPClient(self.config.server.address)
            try:
                await client.initialize()
                worker_start = time.time()
                ch = f"soak-s05-worker-{worker_id}-{uuid.uuid4().hex[:6]}"  # one channel per worker, reused
                while time.time() - worker_start < duration:
                    try:
                        await client.tools_call("queue_send", {"channel": ch, "body": f"w{worker_id}-msg"})
                        ops_per_worker[worker_id] += 1
                    except Exception as exc:
                        logger.debug("S05 worker %d failed: %s", worker_id, exc)
                        errors_per_worker[worker_id] += 1
                        ops_per_worker[worker_id] += 1
                    await asyncio.sleep(0.05)
            finally:
                await client.close()

        await asyncio.gather(*[session_worker(i) for i in range(num_workers)])

        total_ops = sum(ops_per_worker)
        total_errors = sum(errors_per_worker)
        error_rate = (total_errors / total_ops * 100) if total_ops > 0 else 0.0

        assert error_rate < self.config.thresholds.max_error_rate_pct, (
            f"Concurrent sessions error rate {error_rate:.1f}% exceeds threshold"
        )
        return total_ops
