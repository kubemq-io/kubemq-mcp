# KubeMQ MCP Examples — Swift

Copy-paste-ready examples for all 15 KubeMQ MCP tools using the official [MCP Swift SDK](https://github.com/modelcontextprotocol/swift-sdk).

## Prerequisites

- Swift 6.0+ (macOS 13+ or Linux)
- KubeMQ server running with MCP enabled (default: `http://localhost:9090`)

## Setup

```bash
swift build
```

## Run

```bash
swift run QueueSend
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL |

## Examples

| Tool | Target | Run Command |
|------|--------|-------------|
| queue_send | `QueueSend` | `swift run QueueSend` |
| queue_receive | `QueueReceive` | `swift run QueueReceive` |
| queue_peek | `QueuePeek` | `swift run QueuePeek` |
| events_publish | `EventsPublish` | `swift run EventsPublish` |
| events_store_publish | `EventsStorePublish` | `swift run EventsStorePublish` |
| events_store_read | `EventsStoreRead` | `swift run EventsStoreRead` |
| events_store_read_latest | `EventsStoreReadLatest` | `swift run EventsStoreReadLatest` |
| command_send | `CommandSend` | `swift run CommandSend` |
| query_send | `QuerySend` | `swift run QuerySend` |
| channel_list | `ChannelList` | `swift run ChannelList` |
| channel_info | `ChannelInfo` | `swift run ChannelInfo` |
| agent_list | `AgentList` | `swift run AgentList` |
| agent_info | `AgentInfo` | `swift run AgentInfo` |
| agent_send | `AgentSend` | `swift run AgentSend` |
| agent_query | `AgentQuery` | `swift run AgentQuery` |

> **Note:** `command_send` and `query_send` require an active subscriber on the target channel.
> Agent tools (`agent_*`) require registered agents on the KubeMQ server.
>
> **SDK Note (I-2):** Swift MCP SDK API verified against `swift-sdk` v0.12.0. **Swift 6.0+ required** (corrected from spec's 5.9+). If the API has changed, update the transport class name and constructor parameters accordingly.
