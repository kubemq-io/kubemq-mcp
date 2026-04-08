# KubeMQ MCP Examples — Go

Copy-paste-ready examples for all 15 KubeMQ MCP tools using the [mcp-go](https://github.com/mark3labs/mcp-go) module.

## Prerequisites

- [Go 1.21+](https://go.dev/dl/)
- KubeMQ server running with MCP enabled (default: `http://localhost:9090/mcp`)

## Setup

```bash
go mod download
```

## Run

Each tool example lives in its own subdirectory with a `main.go`:

```bash
go run ./queue_send/main.go
go run ./queue_receive/main.go
go run ./events_publish/main.go
```

## Environment Variable

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL |

## Tool Examples

| # | Directory | Tool | Description |
|---|-----------|------|-------------|
| 1 | `queue_send/` | queue_send | Send a message to a queue |
| 2 | `queue_receive/` | queue_receive | Receive messages from a queue |
| 3 | `queue_peek/` | queue_peek | Peek at messages without consuming |
| 4 | `events_publish/` | events_publish | Publish an ephemeral event |
| 5 | `events_store_publish/` | events_store_publish | Publish a persistent event |
| 6 | `events_store_read/` | events_store_read | Read stored events by sequence |
| 7 | `events_store_read_latest/` | events_store_read_latest | Read most recent stored events |
| 8 | `command_send/` | command_send | Send a command (requires subscriber) |
| 9 | `query_send/` | query_send | Send a query (requires subscriber) |
| 10 | `channel_list/` | channel_list | List all channels |
| 11 | `channel_info/` | channel_info | Get channel metadata |
| 12 | `agent_list/` | agent_list | List registered agents |
| 13 | `agent_info/` | agent_info | Get agent details |
| 14 | `agent_send/` | agent_send | Send a message to an agent |
| 15 | `agent_query/` | agent_query | Query an agent |

## Notes

- `command_send` and `query_send` require an active subscriber on the target channel.
- Agent tools (`agent_*`) require registered agents on the KubeMQ server.
