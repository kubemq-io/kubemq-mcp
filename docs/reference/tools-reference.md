# Tools Reference

Complete reference for all 15 KubeMQ MCP tools.

> **Implementation note:** The complete `inputSchema` for all 15 tools is authoritative from the KubeMQ server's `tools/list` response. During implementation: (1) Run `tools/list` against a live KubeMQ server, (2) Extract each tool's `inputSchema`, (3) Use those schemas verbatim. The argument tables below serve as a cross-check.

## Tool Summary

| # | Tool | Category | Required Args | Optional Args |
|---|------|----------|--------------|---------------|
| 1 | `queue_send` | Queue | `channel`, `body` | `metadata`, `tags`, `delay_seconds`, `expiration_seconds`, `max_receive_count`, `dead_letter_queue` |
| 2 | `queue_receive` | Queue | `channel` | `max_messages` |
| 3 | `queue_peek` | Queue | `channel` | `max_messages` |
| 4 | `events_publish` | Events | `channel`, `body` | `metadata`, `tags` |
| 5 | `events_store_publish` | Events | `channel`, `body` | `metadata`, `tags` |
| 6 | `events_store_read` | Events | `channel` | `from_sequence`, `from_time`, `max_messages` |
| 7 | `events_store_read_latest` | Events | `channel` | `count` |
| 8 | `command_send` | Command/Query | `channel`, `body` | `timeout_seconds`, `metadata`, `tags` |
| 9 | `query_send` | Command/Query | `channel`, `body` | `timeout_seconds`, `metadata`, `tags` |
| 10 | `channel_list` | Channel | _(none)_ | `type`, `pattern` |
| 11 | `channel_info` | Channel | `channel`, `type` | _(none)_ |
| 12 | `agent_list` | Agent Bridge | _(none)_ | `skill_tags` |
| 13 | `agent_info` | Agent Bridge | `agent_id` | _(none)_ |
| 14 | `agent_send` | Agent Bridge | `agent_id`, `message` | `blocking`, `context_id`, `timeout_seconds` |
| 15 | `agent_query` | Agent Bridge | `agent_id`, `method` | `params` |

---

## 1. queue_send

Send a message to a queue channel.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target queue channel. Must not start with reserved prefix `_AGENTS_.` |
| `body` | string | YES | — | Message body content |
| `metadata` | string | no | `""` | Optional message metadata string |
| `tags` | object | no | `{}` | Key-value tags for message classification |
| `delay_seconds` | integer | no | `0` | Delay before message becomes visible. `0` = immediately available |
| `expiration_seconds` | integer | no | `0` | TTL in seconds. `0` = no expiration |
| `max_receive_count` | integer | no | `0` | Max receives before DLQ. `0` = unlimited |
| `dead_letter_queue` | string | no | `""` | DLQ channel name |

### inputSchema

```json
{
  "type": "object",
  "required": ["channel", "body"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Target queue channel name. Must not start with reserved prefix '_AGENTS_.'."
    },
    "body": {
      "type": "string",
      "description": "Message body content to send to the queue."
    },
    "metadata": {
      "type": "string",
      "description": "Optional message metadata string.",
      "default": ""
    },
    "tags": {
      "type": "object",
      "description": "Optional key-value tags for message classification.",
      "additionalProperties": { "type": "string" },
      "default": {}
    },
    "delay_seconds": {
      "type": "integer",
      "description": "Delay in seconds before the message becomes visible in the queue. 0 means immediately available.",
      "minimum": 0,
      "default": 0
    },
    "expiration_seconds": {
      "type": "integer",
      "description": "Time-to-live in seconds. The message is automatically removed after this duration. 0 means no expiration.",
      "minimum": 0,
      "default": 0
    },
    "max_receive_count": {
      "type": "integer",
      "description": "Maximum number of times the message can be received before being moved to the dead letter queue. 0 means unlimited.",
      "minimum": 0,
      "default": 0
    },
    "dead_letter_queue": {
      "type": "string",
      "description": "Channel name for the dead letter queue. Messages exceeding max_receive_count are moved here.",
      "default": ""
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "queue_send",
    "arguments": {
      "channel": "example-queue",
      "body": "Hello from MCP",
      "metadata": "example-metadata",
      "tags": { "env": "dev", "source": "mcp-example" }
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [{ "type": "text", "text": "Message sent successfully to queue 'example-queue'" }],
    "isError": false
  }
}
```

### Error Cases

- Reserved channel (`_AGENTS_.*`): `isError: true`
- Missing `channel` or `body`: `-32602` Invalid Params

---

## 2. queue_receive

Receive and consume messages from a queue channel.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Source queue channel |
| `max_messages` | integer | no | `1` | Max messages to receive |

### inputSchema

```json
{
  "type": "object",
  "required": ["channel"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Source queue channel name to receive messages from."
    },
    "max_messages": {
      "type": "integer",
      "description": "Maximum number of messages to receive in a single call.",
      "minimum": 1,
      "default": 1
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "queue_receive",
    "arguments": {
      "channel": "example-queue",
      "max_messages": 5
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [{ "type": "text", "text": "[{\"body\":\"Hello from MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\",\"source\":\"mcp-example\"}}]" }],
    "isError": false
  }
}
```

### Error Cases

- Reserved channel: `isError: true`
- Non-existent channel: empty result (no error)

---

## 3. queue_peek

Peek at messages without consuming them.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Source queue channel |
| `max_messages` | integer | no | `1` | Max messages to peek |

### inputSchema

```json
{
  "type": "object",
  "required": ["channel"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Source queue channel name to peek messages from."
    },
    "max_messages": {
      "type": "integer",
      "description": "Maximum number of messages to peek without consuming.",
      "minimum": 1,
      "default": 1
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "queue_peek",
    "arguments": {
      "channel": "example-queue",
      "max_messages": 5
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [{ "type": "text", "text": "[{\"body\":\"Hello from MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\"}}]" }],
    "isError": false
  }
}
```

### Error Cases

- Reserved channel: `isError: true`
- Non-existent channel: empty result (no error)

---

## 4. events_publish

Publish an ephemeral event (fire-and-forget).

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target events channel |
| `body` | string | YES | — | Event body |
| `metadata` | string | no | `""` | Event metadata |
| `tags` | object | no | `{}` | Key-value tags |

### inputSchema

```json
{
  "type": "object",
  "required": ["channel", "body"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Target events channel name."
    },
    "body": {
      "type": "string",
      "description": "Event body content."
    },
    "metadata": {
      "type": "string",
      "description": "Optional event metadata string.",
      "default": ""
    },
    "tags": {
      "type": "object",
      "description": "Optional key-value tags for event classification.",
      "additionalProperties": { "type": "string" },
      "default": {}
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "events_publish",
    "arguments": {
      "channel": "example-events",
      "body": "Event data",
      "metadata": "event-meta",
      "tags": { "source": "mcp-example" }
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "content": [{ "type": "text", "text": "Event published successfully to channel 'example-events'" }],
    "isError": false
  }
}
```

### Error Cases

- Reserved channel (`_AGENTS_*`): `isError: true`
- Missing required arguments (e.g. `channel`, `body`): `-32602` Invalid Params

---

## 5. events_store_publish

Publish a persistent event with sequence number.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target events-store channel |
| `body` | string | YES | — | Event body |
| `metadata` | string | no | `""` | Event metadata |
| `tags` | object | no | `{}` | Key-value tags |

### inputSchema

```json
{
  "type": "object",
  "required": ["channel", "body"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Target events-store channel name."
    },
    "body": {
      "type": "string",
      "description": "Event body content to store."
    },
    "metadata": {
      "type": "string",
      "description": "Optional event metadata string.",
      "default": ""
    },
    "tags": {
      "type": "object",
      "description": "Optional key-value tags for event classification.",
      "additionalProperties": { "type": "string" },
      "default": {}
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "events_store_publish",
    "arguments": {
      "channel": "example-events-store",
      "body": "Stored event data",
      "metadata": "store-meta",
      "tags": { "source": "mcp-example" }
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "content": [{ "type": "text", "text": "Event published successfully to events store channel 'example-events-store'" }],
    "isError": false
  }
}
```

### Error Cases

- Reserved channel (`_AGENTS_*`): `isError: true`
- Missing required arguments (e.g. `channel`, `body`): `-32602` Invalid Params

---

## 6. events_store_read

Read stored events from a sequence number or timestamp.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Source events-store channel |
| `from_sequence` | integer | no | — | Start from this sequence number |
| `from_time` | string | no | — | Start from ISO 8601 timestamp |
| `max_messages` | integer | no | `10` | Max messages to return |

> `from_sequence` and `from_time` are mutually exclusive.

### inputSchema

```json
{
  "type": "object",
  "required": ["channel"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Source events-store channel name to read from."
    },
    "from_sequence": {
      "type": "integer",
      "description": "Start reading from this sequence number. Mutually exclusive with from_time.",
      "minimum": 1
    },
    "from_time": {
      "type": "string",
      "description": "Start reading from this ISO 8601 timestamp. Mutually exclusive with from_sequence."
    },
    "max_messages": {
      "type": "integer",
      "description": "Maximum number of messages to return.",
      "minimum": 1,
      "default": 10
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "events_store_read",
    "arguments": {
      "channel": "example-events-store",
      "from_sequence": 1,
      "max_messages": 10
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "content": [{ "type": "text", "text": "[{\"body\":\"Stored event data\",\"metadata\":\"store-meta\",\"sequence\":1,\"timestamp\":\"2026-04-06T12:00:00Z\"}]" }],
    "isError": false
  }
}
```

### Error Cases

- Reserved channel (`_AGENTS_*`): `isError: true`
- Non-existent channel: empty result (no error)
- Missing required arguments (e.g. `channel`): `-32602` Invalid Params

---

## 7. events_store_read_latest

Read the N most recent stored events.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Source events-store channel |
| `count` | integer | no | `1` | Number of most recent events |

### inputSchema

```json
{
  "type": "object",
  "required": ["channel"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Source events-store channel name to read latest events from."
    },
    "count": {
      "type": "integer",
      "description": "Number of most recent events to return.",
      "minimum": 1,
      "default": 1
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 8,
  "method": "tools/call",
  "params": {
    "name": "events_store_read_latest",
    "arguments": {
      "channel": "example-events-store",
      "count": 3
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 8,
  "result": {
    "content": [{ "type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3},{\"body\":\"Stored event 2\",\"sequence\":2},{\"body\":\"Stored event 1\",\"sequence\":1}]" }],
    "isError": false
  }
}
```

### Error Cases

- Reserved channel (`_AGENTS_*`): `isError: true`
- Non-existent channel: empty result (no error)
- Missing required arguments (e.g. `channel`): `-32602` Invalid Params

---

## 8. command_send

Send a command and wait for acknowledgment.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target command channel |
| `body` | string | YES | — | Command body |
| `timeout_seconds` | integer | no | `10` | Timeout waiting for response |
| `metadata` | string | no | `""` | Command metadata |
| `tags` | object | no | `{}` | Key-value tags |

### inputSchema

```json
{
  "type": "object",
  "required": ["channel", "body"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Target command channel name."
    },
    "body": {
      "type": "string",
      "description": "Command body content."
    },
    "timeout_seconds": {
      "type": "integer",
      "description": "Timeout in seconds waiting for command response.",
      "minimum": 1,
      "default": 10
    },
    "metadata": {
      "type": "string",
      "description": "Optional command metadata string.",
      "default": ""
    },
    "tags": {
      "type": "object",
      "description": "Optional key-value tags for command classification.",
      "additionalProperties": { "type": "string" },
      "default": {}
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 9,
  "method": "tools/call",
  "params": {
    "name": "command_send",
    "arguments": {
      "channel": "example-commands",
      "body": "do-work",
      "timeout_seconds": 10,
      "metadata": "cmd-meta",
      "tags": { "action": "process" }
    }
  }
}
```

**Response (success):**

```json
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "content": [{ "type": "text", "text": "Command executed successfully on channel 'example-commands'" }],
    "isError": false
  }
}
```

### Error Cases

- Reserved channel (`_AGENTS_*`): `isError: true`
- No subscriber: `isError: true` (timeout)
- Subscriber rejects: `isError: true`
- Missing required arguments (e.g. `channel`, `body`): `-32602` Invalid Params

---

## 9. query_send

Send a query and receive a data response.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target query channel |
| `body` | string | YES | — | Query body |
| `timeout_seconds` | integer | no | `10` | Timeout waiting for response |
| `metadata` | string | no | `""` | Query metadata |
| `tags` | object | no | `{}` | Key-value tags |

### inputSchema

```json
{
  "type": "object",
  "required": ["channel", "body"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Target query channel name."
    },
    "body": {
      "type": "string",
      "description": "Query body content."
    },
    "timeout_seconds": {
      "type": "integer",
      "description": "Timeout in seconds waiting for query response.",
      "minimum": 1,
      "default": 10
    },
    "metadata": {
      "type": "string",
      "description": "Optional query metadata string.",
      "default": ""
    },
    "tags": {
      "type": "object",
      "description": "Optional key-value tags for query classification.",
      "additionalProperties": { "type": "string" },
      "default": {}
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "tools/call",
  "params": {
    "name": "query_send",
    "arguments": {
      "channel": "example-queries",
      "body": "get-data",
      "timeout_seconds": 10,
      "metadata": "qry-meta",
      "tags": { "action": "lookup" }
    }
  }
}
```

**Response (success):**

```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "result": {
    "content": [{ "type": "text", "text": "{\"data\":\"query response payload from subscriber\"}" }],
    "isError": false
  }
}
```

### Error Cases

- Reserved channel (`_AGENTS_*`): `isError: true`
- No subscriber: `isError: true` (timeout)
- Subscriber rejects: `isError: true`
- Missing required arguments (e.g. `channel`, `body`): `-32602` Invalid Params

---

## 10. channel_list

List channels, optionally filtered by type or name pattern.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `type` | string | no | — | Filter by channel type (`queues`, `events`, `events_store`, `commands`, `queries`) |
| `pattern` | string | no | — | Filter by channel name pattern/prefix |

### inputSchema

```json
{
  "type": "object",
  "required": [],
  "properties": {
    "type": {
      "type": "string",
      "description": "Filter by channel type (queues, events, events_store, commands, queries)."
    },
    "pattern": {
      "type": "string",
      "description": "Filter by channel name pattern or prefix."
    }
  }
}
```

### Example

**Request (no filter):**

```json
{
  "jsonrpc": "2.0",
  "id": 11,
  "method": "tools/call",
  "params": {
    "name": "channel_list",
    "arguments": {}
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 11,
  "result": {
    "content": [{ "type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true},{\"name\":\"example-events\",\"type\":\"events\",\"is_active\":true}]" }],
    "isError": false
  }
}
```

### Error Cases

- Invalid arguments: `-32602` Invalid Params
- Otherwise no tool-specific failures; an empty list is a normal successful result.

---

## 11. channel_info

Get metadata for a specific channel.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Channel name |
| `type` | string | YES | — | Channel type (`queues`, `events`, `events_store`, `commands`, `queries`) |

### inputSchema

```json
{
  "type": "object",
  "required": ["channel", "type"],
  "properties": {
    "channel": {
      "type": "string",
      "description": "Channel name to get information for."
    },
    "type": {
      "type": "string",
      "description": "Channel type (queues, events, events_store, commands, queries)."
    }
  }
}
```

### Example

**Request:**

```json
{
  "jsonrpc": "2.0",
  "id": 12,
  "method": "tools/call",
  "params": {
    "name": "channel_info",
    "arguments": {
      "channel": "example-queue",
      "type": "queues"
    }
  }
}
```

**Response (success):**

```json
{
  "jsonrpc": "2.0",
  "id": 12,
  "result": {
    "content": [{ "type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true,\"incoming\":5,\"outgoing\":3}" }],
    "isError": false
  }
}
```

### Error Cases

- Non-existent channel: `isError: true`

---

## 12. agent_list

List registered agents, optionally filtered by skill tags.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `skill_tags` | array[string] | no | — | Filter agents by skill tags |

### inputSchema

```json
{
  "type": "object",
  "required": [],
  "properties": {
    "skill_tags": {
      "type": "array",
      "description": "Filter agents by skill tags.",
      "items": { "type": "string" }
    }
  }
}
```

### Example

**Request:**

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

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 13,
  "result": {
    "content": [{ "type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\",\"skills\":[{\"id\":\"echo\",\"name\":\"Echo\",\"tags\":[\"test\",\"echo\"]}]}]" }],
    "isError": false
  }
}
```

### Error Cases

- Invalid arguments: `-32602` Invalid Params
- Otherwise no tool-specific failures; an empty list is a normal successful result.

---

## 13. agent_info

Get detailed metadata for a specific agent.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `agent_id` | string | YES | — | Agent identifier |

### inputSchema

```json
{
  "type": "object",
  "required": ["agent_id"],
  "properties": {
    "agent_id": {
      "type": "string",
      "description": "Agent identifier to get information for."
    }
  }
}
```

### Example

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

### Error Cases

- Non-existent agent: `isError: true`

---

## 14. agent_send

Send a message to an agent.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `agent_id` | string | YES | — | Target agent identifier |
| `message` | string | YES | — | Message to send |
| `blocking` | boolean | no | `true` | Wait for response if `true` |
| `context_id` | string | no | — | Conversation context ID |
| `timeout_seconds` | integer | no | — | Timeout (server adds +10s GatewayTimeoutBuffer) |

### inputSchema

```json
{
  "type": "object",
  "required": ["agent_id", "message"],
  "properties": {
    "agent_id": {
      "type": "string",
      "description": "Target agent identifier to send the message to."
    },
    "message": {
      "type": "string",
      "description": "Message content to send to the agent."
    },
    "blocking": {
      "type": "boolean",
      "description": "Wait for agent response if true, fire-and-forget if false.",
      "default": true
    },
    "context_id": {
      "type": "string",
      "description": "Conversation context ID for multi-turn interactions."
    },
    "timeout_seconds": {
      "type": "integer",
      "description": "Timeout in seconds waiting for agent response. Server adds +10s GatewayTimeoutBuffer.",
      "minimum": 1
    }
  }
}
```

### Example

**Request:**

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

**Response (success):**

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

### Error Cases

- Non-existent agent: `isError: true`
- Timeout exceeded: `isError: true`

---

## 15. agent_query

Query an agent with a specific method.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `agent_id` | string | YES | — | Target agent identifier |
| `method` | string | YES | — | Query method (`tasks/get`, `tasks/cancel`, or custom) |
| `params` | object | no | — | Method-specific parameters |

### inputSchema

```json
{
  "type": "object",
  "required": ["agent_id", "method"],
  "properties": {
    "agent_id": {
      "type": "string",
      "description": "Target agent identifier to query."
    },
    "method": {
      "type": "string",
      "description": "Query method to invoke (tasks/get, tasks/cancel, or custom)."
    },
    "params": {
      "type": "object",
      "description": "Method-specific parameters for the query."
    }
  }
}
```

### Example

**Request:**

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

### Error Cases

- Non-existent agent: `isError: true`
- Timeout exceeded: `isError: true`
