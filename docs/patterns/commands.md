# Commands Pattern

Synchronous RPC-style commands with timeout. The caller blocks until a subscriber responds or the timeout expires.

## Tool

| Tool | Description |
|------|-------------|
| `command_send` | Send a command and wait for acknowledgment |

## command_send

Sends a command to a channel and blocks until a subscriber responds or the timeout expires. Commands are acknowledged with success/failure — they do not return a data payload (use `query_send` for that).

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `channel` | string | YES | — | Target command channel |
| `body` | string | YES | — | Command body content |
| `timeout_seconds` | integer | no | `10` | Timeout waiting for a subscriber response |
| `metadata` | string | no | `""` | Command metadata |
| `tags` | object | no | `{}` | Key-value tags |

### Behavior

- Requires an active command subscriber on the target channel.
- Blocks until the subscriber responds or `timeout_seconds` expires.
- The response indicates success or failure but does not carry a data payload.

### JSON-RPC Example

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

**Response (error — no subscriber / timeout):**

```json
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "content": [{ "type": "text", "text": "Command timed out: no subscriber on channel 'example-commands' within 10s" }],
    "isError": true
  }
}
```

## Error Cases

| Scenario | Result |
|----------|--------|
| No subscriber on channel | `isError: true` — timeout error |
| Subscriber rejects command | `isError: true` — error response from subscriber |
| Reserved channel (`_AGENTS_.*`) | `isError: true` — reserved prefix rejection |
| Missing required arguments | JSON-RPC error `-32602` (Invalid Params) |
