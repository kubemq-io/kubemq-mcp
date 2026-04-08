# Agent Bridge Pattern

MCP-to-A2A bridge enabling AI agent communication through KubeMQ. These tools allow MCP clients to discover, inspect, and communicate with registered agents.

## Tools

| Tool | Description |
|------|-------------|
| `agent_list` | List registered agents, optionally filtered by skill tags |
| `agent_info` | Get detailed metadata for a specific agent |
| `agent_send` | Send a message to an agent (blocking or non-blocking) |
| `agent_query` | Query an agent with a specific method |

## agent_list

Lists all agents registered with KubeMQ, optionally filtered by skill tags.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `skill_tags` | array[string] | no | — | Filter agents by skill tags |

### JSON-RPC Example

**Request (no filter):**

```json
{
  "jsonrpc": "2.0",
  "id": 13,
  "method": "tools/call",
  "params": {
    "name": "agent_list",
    "arguments": {}
  }
}
```

**Request (filtered by skill_tags):**

```json
{
  "jsonrpc": "2.0",
  "id": 13,
  "method": "tools/call",
  "params": {
    "name": "agent_list",
    "arguments": {
      "skill_tags": ["test"]
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 13,
  "result": {
    "content": [{ "type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\",\"skills\":[{\"id\":\"echo\",\"name\":\"Echo\",\"tags\":[\"test\",\"echo\"]}]},{\"agent_id\":\"slow-01\",\"name\":\"Slow Agent 01\",\"skills\":[{\"id\":\"slow\",\"name\":\"Slow\",\"tags\":[\"test\",\"slow\"]}]}]" }],
    "isError": false
  }
}
```

## agent_info

Returns detailed metadata for a specific agent.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `agent_id` | string | YES | — | Agent identifier |

### JSON-RPC Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 14,
  "method": "tools/call",
  "params": {
    "name": "agent_info",
    "arguments": {
      "agent_id": "echo-01"
    }
  }
}
```

**Response (success):**

```json
{
  "jsonrpc": "2.0",
  "id": 14,
  "result": {
    "content": [{ "type": "text", "text": "{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\",\"description\":\"echo agent for burn-in testing\",\"version\":\"1.0.0\",\"url\":\"http://localhost:18080/\",\"skills\":[{\"id\":\"echo\",\"name\":\"Echo\",\"tags\":[\"test\",\"echo\"]}]}" }],
    "isError": false
  }
}
```

**Response (error — non-existent agent):**

```json
{
  "jsonrpc": "2.0",
  "id": 14,
  "result": {
    "content": [{ "type": "text", "text": "Agent 'nonexistent-agent' not found" }],
    "isError": true
  }
}
```

## agent_send

Sends a message to an agent. In blocking mode (default), waits for the agent's response. In non-blocking mode, the message is sent fire-and-forget.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `agent_id` | string | YES | — | Target agent identifier |
| `message` | string | YES | — | Message to send to the agent |
| `blocking` | boolean | no | `true` | Wait for response if `true` |
| `context_id` | string | no | — | Conversation context ID for multi-turn interactions |
| `timeout_seconds` | integer | no | — | Timeout waiting for agent response (server adds +10s GatewayTimeoutBuffer) |

### GatewayTimeoutBuffer

When `timeout_seconds` is specified, the server automatically adds a 10-second buffer (GatewayTimeoutBuffer) to the user-specified timeout. For example, if you set `timeout_seconds: 5`, the server-side timeout is 15 seconds.

### JSON-RPC Example

**Request (blocking, default):**

```json
{
  "jsonrpc": "2.0",
  "id": 15,
  "method": "tools/call",
  "params": {
    "name": "agent_send",
    "arguments": {
      "agent_id": "echo-01",
      "message": "hello from MCP"
    }
  }
}
```

**Request (non-blocking with context_id and timeout):**

```json
{
  "jsonrpc": "2.0",
  "id": 15,
  "method": "tools/call",
  "params": {
    "name": "agent_send",
    "arguments": {
      "agent_id": "echo-01",
      "message": "async task",
      "blocking": false,
      "context_id": "ctx-abc123",
      "timeout_seconds": 5
    }
  }
}
```

**Response (success — blocking echo agent):**

```json
{
  "jsonrpc": "2.0",
  "id": 15,
  "result": {
    "content": [{ "type": "text", "text": "{\"echo\":{\"method\":\"message/send\",\"params\":{\"message\":\"hello from MCP\"}},\"received_headers\":{}}" }],
    "isError": false
  }
}
```

## agent_query

Queries an agent with a specific method. Supports standard methods (`tasks/get`, `tasks/cancel`) and custom methods.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `agent_id` | string | YES | — | Target agent identifier |
| `method` | string | YES | — | Query method (`tasks/get`, `tasks/cancel`, or custom) |
| `params` | object | no | — | Method-specific parameters |

### JSON-RPC Example

**Request (tasks/get):**

```json
{
  "jsonrpc": "2.0",
  "id": 16,
  "method": "tools/call",
  "params": {
    "name": "agent_query",
    "arguments": {
      "agent_id": "echo-01",
      "method": "tasks/get"
    }
  }
}
```

**Request (custom method with params):**

```json
{
  "jsonrpc": "2.0",
  "id": 16,
  "method": "tools/call",
  "params": {
    "name": "agent_query",
    "arguments": {
      "agent_id": "echo-01",
      "method": "custom/action",
      "params": { "key": "value" }
    }
  }
}
```

**Response (success):**

```json
{
  "jsonrpc": "2.0",
  "id": 16,
  "result": {
    "content": [{ "type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}},\"received_headers\":{}}" }],
    "isError": false
  }
}
```

## Error Cases

| Scenario | Tool | Result |
|----------|------|--------|
| Non-existent agent | `agent_info`, `agent_send`, `agent_query` | `isError: true` — agent not found |
| Timeout exceeded | `agent_send`, `agent_query` | `isError: true` — timeout error |
| Agent processing error | `agent_send`, `agent_query` | `isError: true` — agent error message |
| Missing required arguments | All agent tools | JSON-RPC error `-32602` (Invalid Params) |
