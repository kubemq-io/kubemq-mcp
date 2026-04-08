# Endpoint Reference

## POST /mcp

All MCP operations go through this single endpoint.

- **URL:** `http://localhost:9090/mcp`
- **Content-Type:** `application/json`
- **Protocol:** JSON-RPC 2.0

## JSON-RPC Methods

| Method | Type | Description |
|--------|------|-------------|
| `initialize` | Request | Start session, negotiate capabilities |
| `notifications/initialized` | Notification | Confirm initialization complete (no `id` field, no response body) |
| `ping` | Request | Health check |
| `tools/list` | Request | Discover available tools with their `inputSchema` |
| `tools/call` | Request | Invoke a tool by name |

## Headers

| Header | Direction | Description |
|--------|-----------|-------------|
| `Content-Type` | Request | Must be `application/json` |
| `MCP-Session-Id` | Both | Session identifier (returned by server in `initialize` response; must be sent by client on all subsequent requests) |
| `MCP-Protocol-Version` | Response | Protocol version `2025-11-25` |

## Request Shape

Standard JSON-RPC 2.0 request with `id`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "<method_name>",
  "params": { ... }
}
```

- `jsonrpc` — Must be `"2.0"`.
- `id` — Integer request identifier. Responses echo this value.
- `method` — One of the JSON-RPC methods listed above.
- `params` — Method-specific parameters (object).

## Notification Shape

Notifications have no `id` field and the server does not return a response body:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

## HTTP Status Codes

| Status | Meaning |
|--------|---------|
| `200` | Success — includes both successful results and JSON-RPC error responses |
| `202` | Accepted — returned for notifications (no response body) |
