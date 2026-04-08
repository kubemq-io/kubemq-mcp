# Error Codes Reference

## JSON-RPC Standard Error Codes

| Code | Name | Trigger |
|------|------|---------|
| `-32700` | Parse Error | Malformed JSON body, or wrong `Content-Type` (e.g., `text/plain` instead of `application/json`) |
| `-32600` | Invalid Request | Empty `method` field, or `jsonrpc` version is not `"2.0"` |
| `-32601` | Method Not Found | Unknown method name (e.g., `tools/unknown`) |
| `-32602` | Invalid Params | `params` is not an object, or missing required arguments for a tool |

## Error Response Format

JSON-RPC protocol errors use the `error` field (no `result` field):

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

### Parse Error (-32700)

```json
{
  "jsonrpc": "2.0",
  "id": null,
  "error": {
    "code": -32700,
    "message": "Parse error"
  }
}
```

### Invalid Request (-32600)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32600,
    "message": "Invalid Request"
  }
}
```

### Method Not Found (-32601)

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

### Invalid Params (-32602)

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params"
  }
}
```

## Tool-Level Errors

Tool-level errors are **not** JSON-RPC errors. They return a normal `result` with `isError: true`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "Error description here" }],
    "isError": true
  }
}
```

### Common Tool-Level Errors

| Error | Affected Tools | Example Message |
|-------|---------------|-----------------|
| Reserved channel rejection | `queue_send`, `events_publish`, `events_store_publish`, `command_send`, `query_send` | `"Channel '_AGENTS_reserved' uses a reserved prefix"` |
| Non-existent agent | `agent_info`, `agent_send`, `agent_query` | `"Agent 'nonexistent' not found"` |
| Timeout exceeded | `command_send`, `query_send`, `agent_send`, `agent_query` | `"Command timed out: no subscriber on channel 'ch' within 10s"` |
| No subscriber available | `command_send`, `query_send` | `"Command timed out: no subscriber on channel 'ch' within 10s"` |
| Non-existent channel | `channel_info` | `"Channel 'nonexistent' of type 'queues' not found"` |

## HTTP Status Codes

| Status | Meaning | When |
|--------|---------|------|
| `200` | Success | All JSON-RPC responses (including error responses) |
| `202` | Accepted | Notifications (e.g., `notifications/initialized`) — no response body |

> **Note:** HTTP 200 is returned even for JSON-RPC error responses. The error is encoded in the JSON body, not the HTTP status code.
