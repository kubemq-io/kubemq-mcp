# Getting Started

Get up and running with KubeMQ MCP in 5 minutes.

## Prerequisites

- **KubeMQ server** (latest stable) with MCP enabled
- One of the 9 supported language runtimes (Python 3.10+, Node.js 18+, Java 21+, .NET 8+, Go 1.21+, Rust 1.75+, Ruby 3.1+, Kotlin 1.9+, Swift 6.0+)

## Step 1: Start KubeMQ

```bash
docker run -d --name kubemq -p 9090:9090 -p 50000:50000 kubemq/kubemq
```

MCP is enabled by default on the `/mcp` endpoint. No special environment variable is required.

## Step 2: Verify MCP Endpoint

```bash
curl -X POST http://localhost:9090/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-11-25",
      "capabilities": {},
      "clientInfo": { "name": "test", "version": "1.0.0" }
    }
  }'
```

**Expected response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-11-25",
    "capabilities": { "tools": {} },
    "serverInfo": { "name": "kubemq", "version": "..." },
    "_meta": { "sessionId": "<session-id>" }
  }
}
```

Save the `sessionId` value from `result._meta.sessionId` — you will need it for subsequent requests.

## Step 3: Send the Initialized Notification

```bash
curl -X POST http://localhost:9090/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Session-Id: <session-id>" \
  -d '{
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
  }'
```

This is a notification (no `id` field). The server responds with HTTP 202 and an empty body.

## Step 4: Your First Tool Call

Send a message to a queue:

```bash
curl -X POST http://localhost:9090/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Session-Id: <session-id>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "queue_send",
      "arguments": {
        "channel": "my-queue",
        "body": "Hello from MCP"
      }
    }
  }'
```

**Expected response:**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [{ "type": "text", "text": "Message sent successfully to queue 'my-queue'" }],
    "isError": false
  }
}
```

## Next Steps

- Browse examples in your preferred language: [`../examples/`](../examples/)
- Read the full tools reference: [Tools Reference](reference/tools-reference.md)
- Learn about session management: [Session Management](guides/session-management.md)
- Understand error handling: [Error Handling](guides/error-handling.md)
