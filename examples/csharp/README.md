# KubeMQ MCP Examples — C\#

Copy-paste-ready examples for all 15 KubeMQ MCP tools using the official [ModelContextProtocol](https://www.nuget.org/packages/ModelContextProtocol) NuGet package.

## Prerequisites

- [.NET 8+](https://dotnet.microsoft.com/download)
- KubeMQ server running with MCP enabled (default: `http://localhost:9090/mcp`)

## Setup

```bash
dotnet restore
```

## Run

Each file contains a class with an explicit `static async Task Main` method. Use `StartupObject` to select which example to run:

```bash
dotnet run /p:StartupObject=QueueSend
dotnet run /p:StartupObject=QueueReceive
dotnet run /p:StartupObject=EventsPublish
```

## Environment Variable

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL |

## Tool Examples

| # | File | Tool | Description |
|---|------|------|-------------|
| 1 | `QueueSend.cs` | queue_send | Send a message to a queue |
| 2 | `QueueReceive.cs` | queue_receive | Receive messages from a queue |
| 3 | `QueuePeek.cs` | queue_peek | Peek at messages without consuming |
| 4 | `EventsPublish.cs` | events_publish | Publish an ephemeral event |
| 5 | `EventsStorePublish.cs` | events_store_publish | Publish a persistent event |
| 6 | `EventsStoreRead.cs` | events_store_read | Read stored events by sequence |
| 7 | `EventsStoreReadLatest.cs` | events_store_read_latest | Read most recent stored events |
| 8 | `CommandSend.cs` | command_send | Send a command (requires subscriber) |
| 9 | `QuerySend.cs` | query_send | Send a query (requires subscriber) |
| 10 | `ChannelList.cs` | channel_list | List all channels |
| 11 | `ChannelInfo.cs` | channel_info | Get channel metadata |
| 12 | `AgentList.cs` | agent_list | List registered agents |
| 13 | `AgentInfo.cs` | agent_info | Get agent details |
| 14 | `AgentSend.cs` | agent_send | Send a message to an agent |
| 15 | `AgentQuery.cs` | agent_query | Query an agent |

## Notes

- `command_send` and `query_send` require an active subscriber on the target channel.
- Agent tools (`agent_*`) require registered agents on the KubeMQ server.
