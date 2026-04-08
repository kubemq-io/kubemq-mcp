# Configuration

## Server Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| MCP endpoint | `http://localhost:9090/mcp` | The single HTTP endpoint for all MCP operations |
| gRPC port | `50000` | Used by command/query subscribers (not MCP directly) |

## Environment Variables

All examples across all 9 languages use the same environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL (examples append `/mcp` to construct the full endpoint) |
| `KUBEMQ_MCP_TIMEOUT` | `30` | Default HTTP request timeout in seconds |
| `KUBEMQ_MCP_AUTH_TOKEN` | _(none)_ | JWT auth token for authenticated deployments (optional) |

> **Note:** `KUBEMQ_MCP_TIMEOUT` is a client-side HTTP request timeout controlling how long the HTTP client waits for any response from the server. Individual tool timeouts (e.g., `timeout_seconds` on `command_send` or `agent_send`) are separate and controlled by the tool's own arguments.

## MCP Client Configuration

When using an MCP SDK, the client is configured during initialization:

| Setting | Value | Description |
|---------|-------|-------------|
| Protocol version | `2025-11-25` | MCP protocol version sent in the `initialize` handshake |
| Client info | `{ name, version }` | Identifies the client to the server |
| Capabilities | `{}` | Empty object — capabilities are server-driven |

### Initialize Request

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": {},
    "clientInfo": {
      "name": "my-agent",
      "version": "1.0.0"
    }
  }
}
```

The server responds with its own `protocolVersion`, `capabilities`, `serverInfo`, and a `sessionId` in `_meta`. See [Session Management](guides/session-management.md) for the complete handshake flow.
