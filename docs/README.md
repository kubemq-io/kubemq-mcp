# KubeMQ MCP — Documentation

Complete documentation for the KubeMQ MCP (Model Context Protocol) endpoint.

## Contents

### Architecture

| Document | Description |
|----------|-------------|
| [Architecture](architecture.md) | MCP protocol stack, JSON-RPC 2.0 envelope, session lifecycle, tool categories |

### Getting Started

| Document | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | Quick start: run KubeMQ, verify endpoint, first tool call in 5 minutes |

### Configuration

| Document | Description |
|----------|-------------|
| [Configuration](configuration.md) | Environment variables, server config, MCP client settings |

### Messaging Patterns

| Document | Description |
|----------|-------------|
| [Queues](patterns/queues.md) | `queue_send`, `queue_receive`, `queue_peek` — point-to-point messaging |
| [Events](patterns/events.md) | `events_publish`, `events_store_publish`, `events_store_read`, `events_store_read_latest` — pub/sub |
| [Commands](patterns/commands.md) | `command_send` — synchronous RPC with timeout |
| [Queries](patterns/queries.md) | `query_send` — synchronous RPC with data response |
| [Agents](patterns/agents.md) | `agent_list`, `agent_info`, `agent_send`, `agent_query` — MCP-to-A2A bridge |

### Guides

| Document | Description |
|----------|-------------|
| [Session Management](guides/session-management.md) | Initialize handshake, session IDs, lifecycle |
| [Error Handling](guides/error-handling.md) | JSON-RPC errors vs tool execution errors |
| [Channel Resolution](guides/channel-resolution.md) | Channel naming, reserved prefixes, types |
| [Authentication](guides/authentication.md) | JWT/token auth, production recommendations |

### Reference

| Document | Description |
|----------|-------------|
| [Endpoints](reference/endpoints.md) | `POST /mcp` endpoint, JSON-RPC methods, headers |
| [Tools Reference](reference/tools-reference.md) | All 15 tools with arguments, schemas, examples |
| [Error Codes](reference/error-codes.md) | JSON-RPC error codes, tool-level errors, HTTP status codes |

## Code Examples

See [`../examples/README.md`](../examples/README.md) for copy-paste-ready examples across all 9 supported languages.

## Prerequisites

- KubeMQ server (latest stable) running with MCP enabled
- Default MCP endpoint: `POST http://localhost:9090/mcp`

## Known Risks

- Rust, Ruby, Kotlin, and Swift MCP SDK APIs may evolve rapidly; example code should be verified against the latest SDK versions at implementation time.
- The `inputSchema` for each tool is authoritative from the KubeMQ server's `tools/list` response; documentation tables serve as a cross-check.
