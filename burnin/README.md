# KubeMQ MCP Burn-in Suite

Validates all 15 MCP tools under sustained load against a live KubeMQ server. Adapted from `kubemq-agents-fabric` burn-in patterns.

## Prerequisites

- KubeMQ server running on `http://localhost:9090` with MCP enabled
- Python 3.10+
- `uv` package manager

## Run Modes

| Mode | Suites | Duration | Purpose |
|------|--------|----------|---------|
| **smoke** | mcp_protocol (P01-P03 only) | ~10s | Quick health check |
| **functional** | mcp_core + mcp_bridge + mcp_protocol | ~2-5 min | Full functional validation (46 tests) |
| **soak** | All suites including mcp_soak | Configurable (default 15m) | Sustained load testing (51 tests) |

## Setup

```bash
cd burnin
uv venv
uv pip install -e .
```

## Running

```bash
# Smoke test — quick MCP health check
uv run python -m kubemq_mcp_burnin --mode smoke

# Functional test — full validation of all tools
uv run python -m kubemq_mcp_burnin --mode functional

# Soak test — sustained load (default 15 minutes)
uv run python -m kubemq_mcp_burnin --mode soak --duration 15m
```

## Configuration

Configuration is loaded from `burnin-config.yaml` with environment variable overrides.

### Environment Variable Overrides

| Variable | Config Path | Description |
|----------|------------|-------------|
| `KUBEMQ_MCP_URL` | `server.address` | KubeMQ server URL |
| `BURNIN_MODE` | `mode` | Run mode (smoke/functional/soak) |
| `BURNIN_DURATION` | `duration` | Soak duration (e.g., 15m, 1h) |
| `BURNIN_LOG_LEVEL` | `output.log_level` | Log verbosity (debug/info/warn/error) |

### Config File Reference

See `burnin-config.yaml` for all available settings including agent fixtures, soak thresholds, and output configuration.

## Test Suites

### mcp_core (M01-M19) — 19 tests

Tests all 15 MCP tools across 19 test cases: queue_send/receive/peek, events_publish, events_store_publish/read/read_latest, command_send, query_send, channel_list/info, and reserved channel rejection.

### mcp_bridge (B01-B14) — 14 tests

Tests all 4 agent bridge tools: agent_list, agent_info, agent_send, agent_query. Requires mock agents registered with KubeMQ.

### mcp_protocol (P01-P13) — 13 tests

Tests MCP protocol compliance: initialize handshake, ping, tools/list, error codes (-32700, -32600, -32601, -32602), headers, and notifications.

### mcp_soak (S01-S05) — 5 tests

Continuous load tests: queue throughput, events-store throughput, mixed workload, session stability, and concurrent sessions.

## Report Format

```
=== KubeMQ MCP Burn-in Report ===
Mode: functional | Duration: 3m 42s
Server: http://localhost:9090

Suite: mcp_core     | 19/19 PASSED | 0 FAILED
Suite: mcp_protocol | 13/13 PASSED | 0 FAILED
Suite: mcp_bridge   | 14/14 PASSED | 0 FAILED

Totals: 46/46 PASSED | 0 FAILED | Error Rate: 0.0%
Latency: p50=12ms p95=45ms p99=120ms
```
