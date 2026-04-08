# Events Pattern

Pub/sub messaging with both ephemeral and persistent event models.

## Tools

| Tool | Description | Persistence |
|------|-------------|-------------|
| `events_publish` | Publish an ephemeral event | No — lost if no subscriber active |
| `events_store_publish` | Publish a persistent event | Yes — stored with sequence number |
| `events_store_read` | Read stored events from a sequence or timestamp | Yes — replay from store |
| `events_store_read_latest` | Read the N most recent stored events | Yes — tail from store |

## events_publish

Publishes a fire-and-forget ephemeral event. The event is delivered to active subscribers but not persisted. If no subscriber is listening, the event is lost.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target events channel |
| `body` | string | YES | — | Event body content |
| `metadata` | string | no | `""` | Event metadata |
| `tags` | object | no | `{}` | Key-value tags |

### JSON-RPC Example

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

## events_store_publish

Publishes a persistent event with an assigned sequence number. The event is stored and can be replayed later.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target events-store channel |
| `body` | string | YES | — | Event body content |
| `metadata` | string | no | `""` | Event metadata |
| `tags` | object | no | `{}` | Key-value tags |

### JSON-RPC Example

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

## events_store_read

Reads stored events starting from a sequence number or an ISO 8601 timestamp.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Source events-store channel |
| `from_sequence` | integer | no | — | Start reading from this sequence number |
| `from_time` | string | no | — | Start reading from ISO 8601 timestamp (`YYYY-MM-DDTHH:MM:SSZ`) |
| `max_messages` | integer | no | `10` | Maximum messages to return |

> **Note:** `from_sequence` and `from_time` are mutually exclusive. Provide exactly one. If neither is provided, server behavior is implementation-defined.

### JSON-RPC Example (from_sequence)

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

### JSON-RPC Example (from_time)

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
      "from_time": "2026-04-06T00:00:00Z",
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

## events_store_read_latest

Returns the N most recent events from the store channel.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Source events-store channel |
| `count` | integer | no | `1` | Number of most recent events to return |

### JSON-RPC Example

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

## When to Use Which

| Scenario | Tool | Reason |
|----------|------|--------|
| Real-time notifications, no replay needed | `events_publish` | Fire-and-forget, lowest overhead |
| Audit logs, event sourcing | `events_store_publish` | Persistent, replayable |
| Replay from a specific point | `events_store_read` | Sequence or time-based cursor |
| Get most recent N events | `events_store_read_latest` | Tail the store |
