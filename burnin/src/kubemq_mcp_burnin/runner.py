from __future__ import annotations

import logging
import time

from kubemq_mcp_burnin.agents.manager import AgentManager
from kubemq_mcp_burnin.config import BurninConfig
from kubemq_mcp_burnin.metrics.tracker import TestTracker
from kubemq_mcp_burnin.suites.base import BaseSuite
from kubemq_mcp_burnin.suites.mcp_bridge import MCPBridgeSuite
from kubemq_mcp_burnin.suites.mcp_core import MCPCoreSuite
from kubemq_mcp_burnin.suites.mcp_protocol import MCPProtocolSuite
from kubemq_mcp_burnin.suites.mcp_soak import MCPSoakSuite

logger = logging.getLogger(__name__)


class BurninRunner:
    """Orchestrates suite execution based on run mode."""

    def __init__(self, config: BurninConfig) -> None:
        self.config = config
        self.tracker = TestTracker()

    async def run(self) -> int:
        start_time = time.time()
        mode = self.config.mode
        logger.info("Starting KubeMQ MCP burn-in — mode=%s, server=%s",
                     mode, self.config.server.address)

        agent_manager = AgentManager(self.config)

        needs_agents = mode in ("functional", "soak")
        if needs_agents:
            try:
                await agent_manager.create_all()
                await agent_manager.start_all()
                await agent_manager.register_all()
                logger.info("All mock agents started and registered")
            except Exception as exc:
                logger.error("Failed to set up agents: %s", exc)
                await agent_manager.cleanup()
                return 1

        try:
            suites = self._select_suites(mode, agent_manager)
            for suite in suites:
                await suite.run()
        finally:
            if needs_agents:
                await agent_manager.cleanup()

        elapsed = time.time() - start_time
        self._print_report(mode, elapsed)

        return 0 if self.tracker.failed == 0 else 1

    def _select_suites(self, mode: str, agent_manager: AgentManager) -> list[BaseSuite]:
        suites: list[BaseSuite] = []

        if mode == "smoke":
            suites.append(
                MCPProtocolSuite(self.config, agent_manager, self.tracker, smoke_only=True)
            )
        elif mode == "functional":
            if self.config.suites.mcp_core:
                suites.append(MCPCoreSuite(self.config, agent_manager, self.tracker))
            if self.config.suites.mcp_bridge:
                suites.append(MCPBridgeSuite(self.config, agent_manager, self.tracker))
            if self.config.suites.mcp_protocol:
                suites.append(MCPProtocolSuite(self.config, agent_manager, self.tracker))
        elif mode == "soak":
            if self.config.suites.mcp_core:
                suites.append(MCPCoreSuite(self.config, agent_manager, self.tracker))
            if self.config.suites.mcp_bridge:
                suites.append(MCPBridgeSuite(self.config, agent_manager, self.tracker))
            if self.config.suites.mcp_protocol:
                suites.append(MCPProtocolSuite(self.config, agent_manager, self.tracker))
            if self.config.suites.mcp_soak:
                suites.append(MCPSoakSuite(self.config, agent_manager, self.tracker))
        else:
            raise ValueError(f"Unknown mode: {mode!r}. Must be smoke, functional, or soak.")

        return suites

    def _print_report(self, mode: str, elapsed: float) -> None:
        mins = int(elapsed) // 60
        secs = int(elapsed) % 60

        print()
        print("=== KubeMQ MCP Burn-in Report ===")
        print(f"Mode: {mode} | Duration: {mins}m {secs}s")
        print(f"Server: {self.config.server.address}")
        print()

        suite_counts: dict[str, tuple[int, int]] = {}
        for r in self.tracker.results:
            p, f = suite_counts.get(r.suite, (0, 0))
            if r.status == "passed":
                suite_counts[r.suite] = (p + 1, f)
            else:
                suite_counts[r.suite] = (p, f + 1)

        for suite_name, (passed, failed) in suite_counts.items():
            total = passed + failed
            pad = " " * max(0, 16 - len(suite_name))
            print(f"Suite: {suite_name}{pad}| {passed}/{total} PASSED | {failed} FAILED")

        print()
        total_p = self.tracker.passed
        total_f = self.tracker.failed
        total_t = self.tracker.total
        err_pct = (total_f / total_t * 100) if total_t > 0 else 0.0
        print(f"Totals: {total_p}/{total_t} PASSED | {total_f} FAILED | Error Rate: {err_pct:.1f}%")

        durations = [r.duration_ms for r in self.tracker.results if r.status == "passed"]
        if durations:
            durations.sort()
            p50 = durations[len(durations) // 2]
            p95 = durations[int(len(durations) * 0.95)]
            p99 = durations[int(len(durations) * 0.99)]
            print(f"Latency: p50={p50:.0f}ms p95={p95:.0f}ms p99={p99:.0f}ms")
        print()
