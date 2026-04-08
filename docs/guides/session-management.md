# Session Management

## The MCP Handshake

Every MCP interaction starts with a 3-step handshake:

### Step 1: Initialize

Send an `initialize` request with `protocolVersion`, `capabilities`, and `clientInfo`:

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

### Step 2: Receive Session ID

The server responds with `protocolVersion`, `capabilities`, `serverInfo`, and a session ID in `_meta`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": { "tools": {} },
    "serverInfo": { "name": "kubemq", "version": "..." },
    "_meta": { "sessionId": "abc123-def456" }
  }
}
```

Extract the session ID from `result._meta.sessionId`.

### Step 3: Send Initialized Notification

Send a `notifications/initialized` notification. This is a notification — it has no `id` field and the server does not return a response body:

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/initialized"
}
```

The server responds with HTTP 202 (Accepted) and an empty body.

## Session ID

- Returned in `result._meta.sessionId` during the initialize response.
- Must be sent as the `MCP-Session-Id` header on all subsequent requests.
- The server echoes the session ID back in the response headers.

## Session Lifecycle

- Sessions are server-managed.
- Multiple tool calls share the same session.
- Sessions persist until the client disconnects or a server-side inactivity timeout occurs.
- Each session maintains its own request context.

## Code Pattern (Pseudocode)

```
response = POST /mcp {
  jsonrpc: "2.0", id: 1,
  method: "initialize",
  params: { protocolVersion: "2025-11-25", capabilities: {}, clientInfo: { name: "agent", version: "1.0" } }
}

sessionId = response.result._meta.sessionId

POST /mcp {
  headers: { MCP-Session-Id: sessionId },
  body: { jsonrpc: "2.0", method: "notifications/initialized" }
}

result = POST /mcp {
  headers: { MCP-Session-Id: sessionId },
  body: { jsonrpc: "2.0", id: 2, method: "tools/call", params: { name: "queue_send", arguments: { ... } } }
}
```

## Header Requirements

| Header | Direction | Required | Description |
|--------|-----------|----------|-------------|
| `Content-Type` | Request | Always | Must be `application/json` |
| `MCP-Session-Id` | Request | After init | Session identifier from `initialize` response |
| `MCP-Session-Id` | Response | Always | Echoed back by server |
| `MCP-Protocol-Version` | Response | Always | Protocol version `2025-11-25` |
