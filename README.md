# KubeMQ MCP — Model Context Protocol Integration

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

KubeMQ MCP is a standalone repository providing comprehensive documentation, copy-paste-ready code examples in 9 languages, and a Python burn-in test suite for the KubeMQ MCP (Model Context Protocol) endpoint. It serves as the primary reference for AI agent developers integrating with KubeMQ via its JSON-RPC 2.0 MCP endpoint at `POST /mcp`.

## What This Project IS

- Complete documentation of the KubeMQ MCP JSON-RPC 2.0 endpoint (`POST /mcp`)
- Copy-paste-ready code examples for all 15 MCP tools in 9 languages
- A Python burn-in application adapted from kubemq-agents-fabric for soak testing
- A reference for AI agent developers integrating with KubeMQ via MCP

## What This Project IS NOT

- **Not** a new SDK or client library
- **Not** a wrapper around the MCP endpoint
- **Not** a runtime dependency for any other project
- **Not** a replacement for the official KubeMQ SDKs

## Target Audience

- **AI agent developers** using MCP-compatible tools
- **Developers** building LLM integrations that communicate with KubeMQ
- **DevOps teams** validating KubeMQ MCP deployments

## Supported Languages

| # | Language | MCP SDK Package |
|---|----------|----------------|
| 1 | Python | `mcp` (PyPI) |
| 2 | TypeScript/JS | `@modelcontextprotocol/sdk` (npm) |
| 3 | Java | `io.modelcontextprotocol:sdk` (Maven Central) |
| 4 | C# | `ModelContextProtocol` (NuGet) |
| 5 | Go | `github.com/mark3labs/mcp-go` (Go modules) |
| 6 | Rust | `rmcp` (crates.io) |
| 7 | Ruby | `mcp` (RubyGems) |
| 8 | Kotlin | `io.modelcontextprotocol:kotlin-sdk` (Maven Central) |
| 9 | Swift | `mcp-swift-sdk` (Swift Package Manager) |

## Quick Start

### 1. Start KubeMQ

```bash
docker run -d --name kubemq -p 9090:9090 -p 50000:50000 kubemq/kubemq
```

### 2. Verify MCP Endpoint

```bash
curl -X POST http://localhost:9090/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-11-25","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}'
```

Expected: JSON response with `protocolVersion`, `capabilities`, `serverInfo`, and `_meta.sessionId`.

### 3. Confirm Initialization

Send `notifications/initialized` with the session ID from step 2 (this is a notification -- no `id` field, no response body expected):

```bash
curl -X POST http://localhost:9090/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Session-Id: <sessionId from step 2>" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

Expected: HTTP 200 or 202 with empty body.

### 4. Your First Tool Call

Now call `queue_send`:

```bash
curl -X POST http://localhost:9090/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Session-Id: <sessionId from step 2>" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"queue_send","arguments":{"channel":"my-queue","body":"hello"}}}'
```

## MCP Tools

KubeMQ exposes 15 tools across 5 categories:

| Category | Tools | Count |
|----------|-------|------:|
| Queue | `queue_send`, `queue_receive`, `queue_peek` | 3 |
| Events | `events_publish`, `events_store_publish`, `events_store_read`, `events_store_read_latest` | 4 |
| Command/Query | `command_send`, `query_send` | 2 |
| Channel Management | `channel_list`, `channel_info` | 2 |
| Agent Bridge | `agent_list`, `agent_info`, `agent_send`, `agent_query` | 4 |

## Repository Structure

```
kubemq-mcp/
├── README.md              # This file
├── LICENSE                # Apache 2.0
├── .gitignore             # Multi-language gitignore
├── docs/                  # Documentation
│   ├── architecture.md    # MCP architecture and protocol
│   ├── getting-started.md # Quick start guide
│   ├── configuration.md   # Environment variables, server config
│   ├── patterns/          # Messaging patterns (queues, events, commands, queries, agents)
│   ├── guides/            # Session management, error handling, channels, auth
│   └── reference/         # Endpoint reference, tools reference, error codes
├── examples/              # Code examples in 9 languages
│   ├── python/
│   ├── typescript/
│   ├── java/
│   ├── csharp/
│   ├── go/
│   ├── rust/
│   ├── ruby/
│   ├── kotlin/
│   └── swift/
└── burnin/                # Python burn-in test suite
    └── src/
        └── kubemq_mcp_burnin/
```

## Documentation

| Document | Description |
|----------|-------------|
| [Architecture](docs/architecture.md) | MCP protocol stack, session lifecycle, tool categories |
| [Getting Started](docs/getting-started.md) | Quick start with curl examples |
| [Configuration](docs/configuration.md) | Environment variables, server config |
| **Patterns** | |
| [Queues](docs/patterns/queues.md) | `queue_send`, `queue_receive`, `queue_peek` |
| [Events](docs/patterns/events.md) | `events_publish`, `events_store_publish`, `events_store_read`, `events_store_read_latest` |
| [Commands](docs/patterns/commands.md) | `command_send` |
| [Queries](docs/patterns/queries.md) | `query_send` |
| [Agents](docs/patterns/agents.md) | `agent_list`, `agent_info`, `agent_send`, `agent_query` |
| **Guides** | |
| [Session Management](docs/guides/session-management.md) | MCP handshake, session IDs, lifecycle |
| [Error Handling](docs/guides/error-handling.md) | Two-layer error model (JSON-RPC + tool-level) |
| [Channel Resolution](docs/guides/channel-resolution.md) | Channel naming, reserved prefixes, types |
| [Authentication](docs/guides/authentication.md) | JWT tokens, auth configuration |
| **Reference** | |
| [Endpoints](docs/reference/endpoints.md) | `POST /mcp` endpoint details |
| [Tools Reference](docs/reference/tools-reference.md) | All 15 tools with inputSchema |
| [Error Codes](docs/reference/error-codes.md) | JSON-RPC and tool-level error codes |
| **Other** | |
| [Examples](examples/) | Copy-paste-ready examples for all 15 tools in 9 languages |
| [Burn-in](burnin/) | Python burn-in suite for soak testing |

## Prerequisites

- **KubeMQ server** (latest stable) with MCP enabled
- Default MCP endpoint: `POST http://localhost:9090/mcp`
- Default gRPC port: `50000` (used by command/query subscribers)

## License

Apache 2.0 — see [LICENSE](LICENSE) for details.
