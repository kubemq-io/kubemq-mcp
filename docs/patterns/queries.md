# Queries Pattern

Synchronous RPC with a data response. Like commands, but subscribers return a data payload.

## Tool

| Tool | Description |
|------|-------------|
| `query_send` | Send a query and receive a data response |

## query_send

Sends a query to a channel and blocks until a subscriber responds with data or the timeout expires.

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target query channel |
| `body` | string | YES | — | Query body content |
| `timeout_seconds` | integer | no | `10` | Timeout waiting for a subscriber response |
| `metadata` | string | no | `""` | Query metadata |
| `tags` | object | no | `{}` | Key-value tags |

### Behavior

- Requires an active query subscriber on the target channel.
- Blocks until the subscriber responds or `timeout_seconds` expires.
- Unlike `command_send`, the subscriber returns a data payload in the response.

### JSON-RPC Example

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

**Response (error — no subscriber / timeout):**

```json
{
  "jsonrpc": "2.0",
  "id": 10,
  "result": {
    "content": [{ "type": "text", "text": "Query timed out: no subscriber on channel 'example-queries' within 10s" }],
    "isError": true
  }
}
```

## Difference from Commands

| Aspect | `command_send` | `query_send` |
|--------|---------------|-------------|
| Subscriber returns data | No — acknowledge only | Yes — data payload |
| Use case | Trigger an action | Request information |
| Response content | Success/failure message | Subscriber response data |

## Error Cases

| Scenario | Result |
|----------|--------|
| No subscriber on channel | `isError: true` — timeout error |
| Subscriber rejects query | `isError: true` — error response from subscriber |
| Reserved channel (`_AGENTS_.*`) | `isError: true` — reserved prefix rejection |
| Missing required arguments | JSON-RPC error `-32602` (Invalid Params) |
