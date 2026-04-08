# Queue Pattern

Point-to-point message queuing via MCP tools. Messages are stored in named queue channels and consumed by receivers.

## Tools

| Tool | Description |
|------|-------------|
| `queue_send` | Send a message to a queue channel |
| `queue_receive` | Receive and consume messages from a queue channel |
| `queue_peek` | Peek at messages without consuming them |

## queue_send

Sends a message to a queue channel. The channel is created automatically if it does not exist.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target queue channel. Must not start with reserved prefix `_AGENTS_.` |
| `body` | string | YES | — | Message body content |
| `metadata` | string | no | `""` | Optional message metadata string |
| `tags` | object | no | `{}` | Key-value tags for message classification |
| `delay_seconds` | integer | no | `0` | Delay before the message becomes visible. `0` = immediately available |
| `expiration_seconds` | integer | no | `0` | Time-to-live in seconds. `0` = no expiration |
| `max_receive_count` | integer | no | `0` | Max receives before moving to dead letter queue. `0` = unlimited |
| `dead_letter_queue` | string | no | `""` | Channel name for the dead letter queue |

### JSON-RPC Example

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

## queue_receive

Receives and consumes messages from a queue channel. Messages are removed from the queue after receipt.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Source queue channel |
| `max_messages` | integer | no | `1` | Maximum number of messages to receive |

### JSON-RPC Example

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

## queue_peek

Peeks at messages in a queue without consuming them. Messages remain in the queue and can be received later.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Source queue channel |
| `max_messages` | integer | no | `1` | Maximum number of messages to peek |

### JSON-RPC Example

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

## Consume vs Peek

| Operation | `queue_receive` | `queue_peek` |
|-----------|----------------|-------------|
| Removes messages from queue | Yes | No |
| Use case | Processing work items | Monitoring, debugging |
| Idempotent | No | Yes |

## Advanced Patterns

### Delayed Messages

Set `delay_seconds` to make a message invisible for a specified duration after sending:

```json
{ "channel": "tasks", "body": "process-later", "delay_seconds": 60 }
```

### Message Expiration

Set `expiration_seconds` to automatically remove a message after a duration:

```json
{ "channel": "tasks", "body": "time-sensitive", "expiration_seconds": 300 }
```

### Dead Letter Queues

Combine `max_receive_count` and `dead_letter_queue` to redirect messages that fail processing:

```json
{
  "channel": "tasks",
  "body": "may-fail",
  "max_receive_count": 3,
  "dead_letter_queue": "tasks-dlq"
}
```

After 3 receive attempts, the message is moved to the `tasks-dlq` channel.

### Metadata and Tags

Use `metadata` for unstructured context and `tags` for structured key-value classification:

```json
{
  "channel": "orders",
  "body": "{\"order_id\": 123}",
  "metadata": "priority-high",
  "tags": { "region": "us-west", "tier": "premium" }
}
```
