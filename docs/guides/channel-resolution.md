# Channel Resolution

## Channel Naming

- Channels are arbitrary strings (e.g., `my-app.orders`, `notifications`, `user-events`).
- Channels are created implicitly on first use — no explicit creation step is required.
- **Convention:** Use dot-separated hierarchical names for organization (e.g., `orders.us-west`, `events.user.signup`).

## Reserved Prefixes

| Prefix | Purpose | Restriction |
|--------|---------|-------------|
| `_AGENTS_.*` | Agent bridge internal communication | Cannot be used with direct messaging tools |

Attempting to send or publish to channels matching the `_AGENTS_.*` prefix via `queue_send`, `events_publish`, `events_store_publish`, `command_send`, or `query_send` returns `isError: true`.

Use the agent bridge tools (`agent_send`, `agent_query`) to communicate with agents.

## Channel Types

Each channel belongs to one of 5 types:

| Type | Description | Associated Tools |
|------|-------------|-----------------|
| `queues` | Point-to-point queue channels | `queue_send`, `queue_receive`, `queue_peek` |
| `events` | Ephemeral pub/sub channels | `events_publish` |
| `events_store` | Persistent pub/sub channels | `events_store_publish`, `events_store_read`, `events_store_read_latest` |
| `commands` | RPC command channels | `command_send` |
| `queries` | RPC query channels | `query_send` |

## Listing and Filtering

### List All Channels

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

### Filter by Type

```json
{
  "jsonrpc": "2.0",
  "id": 11,
  "method": "tools/call",
  "params": {
    "name": "channel_list",
    "arguments": {
      "type": "queues"
    }
  }
}
```

### Filter by Pattern

```json
{
  "jsonrpc": "2.0",
  "id": 11,
  "method": "tools/call",
  "params": {
    "name": "channel_list",
    "arguments": {
      "pattern": "example-"
    }
  }
}
```

### Get Channel Details

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

The response includes channel metadata such as name, type, active status, and message statistics.
