# Error Handling

KubeMQ MCP has two distinct error layers. Understanding the difference is critical for robust agent integrations.

## Two Error Layers

### Layer 1: JSON-RPC Protocol Errors

Protocol-level errors indicate that the request itself was malformed or targeted a non-existent method. These appear in the `error` field of the response (there is no `result` field).

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

### Layer 2: Tool Execution Errors

Tool-level errors indicate that the request was valid JSON-RPC but the tool operation failed. These appear in `result.isError` — the response has a `result` field with `isError: true`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{ "type": "text", "text": "Agent 'nonexistent' not found" }],
    "isError": true
  }
}
```

## JSON-RPC Error Codes

| Code | Name | Trigger |
|------|------|---------|
| `-32700` | Parse Error | Malformed JSON body, or wrong `Content-Type` (e.g., `text/plain` instead of `application/json`) |
| `-32600` | Invalid Request | Empty `method` field, or `jsonrpc` version is not `"2.0"` |
| `-32601` | Method Not Found | Unknown method name (e.g., `tools/unknown`) |
| `-32602` | Invalid Params | `params` is not an object, or required arguments are missing |

## Tool Execution Error Cases

| Error | Affected Tools | Details |
|-------|---------------|---------|
| Reserved channel rejection | `queue_send`, `events_publish`, `events_store_publish`, `command_send`, `query_send` | Channel starts with `_AGENTS_.*` prefix |
| Non-existent agent | `agent_info`, `agent_send`, `agent_query` | Agent ID not registered |
| Timeout exceeded | `command_send`, `query_send`, `agent_send`, `agent_query` | No response within timeout period |
| No subscriber available | `command_send`, `query_send` | No active subscriber on the target channel |

## Error Handling Best Practices

1. **Check for `error` first** — If the response has an `error` field, the request failed at the protocol level. Do not look for `result`.
2. **Then check `result.isError`** — If `isError` is `true`, the tool operation failed. Read the error message from `result.content[].text`.
3. **Log the full response** — For debugging, always log the complete JSON-RPC response.

## Code Example (Pseudocode)

```
response = call_tool("queue_send", { channel: "test", body: "hello" })

if response.error:
    # Protocol error — bad request, method not found, etc.
    log("Protocol error:", response.error.code, response.error.message)
    return

if response.result.isError:
    # Tool error — channel reserved, timeout, etc.
    log("Tool error:", response.result.content[0].text)
    return

# Success
log("Result:", response.result.content[0].text)
```
