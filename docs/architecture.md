# MCP Architecture

## Overview

KubeMQ's MCP endpoint exposes messaging and agent operations via JSON-RPC 2.0. All operations flow through a single HTTP endpoint using the Streamable HTTP transport defined by the Model Context Protocol.

- **Single endpoint:** `POST /mcp`
- **Protocol:** MCP (Model Context Protocol) version `2025-11-25`
- **Wire format:** JSON-RPC 2.0

## Glossary

| Term | Definition |
|------|-----------|
| **MCP** | Model Context Protocol — an open standard for connecting AI agents to external tools and data sources via a unified JSON-RPC 2.0 interface. |
| **JSON-RPC 2.0** | A stateless, lightweight remote procedure call protocol encoded in JSON. A **request** includes `jsonrpc` and `method`, and an **`id`** so the client can correlate the response—**notifications** omit `id` and do not receive a JSON-RPC result (e.g. `notifications/initialized`). The **`params`** field is **optional**; some methods (e.g. `ping`) take no parameters. |
| **Streamable HTTP** | The MCP transport mode used by KubeMQ. Each request is a standalone HTTP POST; no persistent SSE connections are required. |
| **isError** | A boolean field in the tool call result indicating whether the tool execution itself failed (as distinct from a JSON-RPC protocol error). |
| **inputSchema** | A JSON Schema object returned by `tools/list` that describes the accepted arguments for each tool. |
| **Session ID** | An opaque string returned by the server during `initialize`, used in the `MCP-Session-Id` header on all subsequent requests. |

## Protocol Stack

```
AI Agent / LLM
    │
MCP Client (official SDK)
    │
JSON-RPC 2.0 over HTTP POST
    │
KubeMQ Server (/mcp endpoint)
    │
KubeMQ Messaging Engine
```

Every MCP SDK (Python, TypeScript, Java, C#, Go, Rust, Ruby, Kotlin, Swift) wraps this transport layer, managing session IDs, request IDs, and JSON-RPC serialization automatically.

## Session Lifecycle

1. **Initialize** — Client sends `initialize` with `protocolVersion`, `capabilities`, and `clientInfo`.
2. **Server response** — Server returns `protocolVersion`, `capabilities`, `serverInfo`, and `_meta.sessionId`.
3. **Notification** — Client sends `notifications/initialized` (a notification — no `id` field, no response expected).
4. **Tool calls** — Subsequent requests include the `MCP-Session-Id` header and use `tools/call` to invoke tools.
5. **Session end** — Session persists until client disconnects or server-side timeout.

```
Client                          Server
  │                               │
  ├── initialize ────────────────►│
  │◄──── result + sessionId ──────┤
  │                               │
  ├── notifications/initialized ─►│
  │◄──── 202 (accepted) ─────────┤
  │                               │
  ├── tools/call (+ Session-Id) ─►│
  │◄──── result ──────────────────┤
  │                               │
```

## Tool Categories

KubeMQ exposes 15 MCP tools across 5 categories:

| Category | Tools | Count |
|----------|-------|------:|
| **Queue** | `queue_send`, `queue_receive`, `queue_peek` | 3 |
| **Events** | `events_publish`, `events_store_publish`, `events_store_read`, `events_store_read_latest` | 4 |
| **Command/Query** | `command_send`, `query_send` | 2 |
| **Channel Management** | `channel_list`, `channel_info` | 2 |
| **Agent Bridge** | `agent_list`, `agent_info`, `agent_send`, `agent_query` | 4 |
| **Total** | | **15** |

## JSON-RPC 2.0 Envelope

**Requests vs notifications:** Only **requests** carry an `id`; **notifications** omit `id` and are not answered with a JSON-RPC `result` or `error` object (the transport may still return HTTP 202, as for `notifications/initialized`). **`params` is optional** when the method defines no arguments.

### Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "queue_send",
    "arguments": { "channel": "my-queue", "body": "hello" }
  }
}
```

### Response (success)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "Message sent successfully to queue 'my-queue'" }],
    "isError": false
  }
}
```

### Response (tool error)

When a tool call fails at the application level, the response still uses the `result` field but sets `isError: true`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "Channel '_AGENTS_reserved' uses a reserved prefix" }],
    "isError": true
  }
}
```

### Response (protocol error)

JSON-RPC protocol errors use the `error` field instead of `result`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found"
  }
}
```

## Tool Discovery

The `tools/list` method returns all 15 tools with their `name`, `description`, and `inputSchema`:

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/list"
}
```

The response includes a JSON Schema `inputSchema` for each tool, describing accepted argument names, types, required/optional status, and defaults.

## Reserved Channels

The `_AGENTS_.*` prefix is reserved for agent bridge internal communication. Attempting to send or publish to channels matching this prefix via direct messaging tools (`queue_send`, `events_publish`, etc.) returns `isError: true`.

Use the agent bridge tools (`agent_send`, `agent_query`) to communicate with agents.
