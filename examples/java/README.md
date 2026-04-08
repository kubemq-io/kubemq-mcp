# KubeMQ MCP Examples — Java

Copy-paste-ready examples for all 15 KubeMQ MCP tools using the official [MCP Java SDK](https://central.sonatype.com/artifact/io.modelcontextprotocol/sdk).

## Prerequisites

- Java 21+
- Maven 3.8+
- KubeMQ server running with MCP enabled (default: `http://localhost:9090`)

## Setup

```bash
mvn dependency:resolve
```

## Run

```bash
mvn compile exec:java -Dexec.mainClass="QueueSend"
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL |

## Examples

| Tool | File | Notes |
|------|------|-------|
| queue_send | `QueueSend.java` | Send a message to a queue |
| queue_receive | `QueueReceive.java` | Consume messages from a queue |
| queue_peek | `QueuePeek.java` | Peek at messages without consuming |
| events_publish | `EventsPublish.java` | Publish an ephemeral event |
| events_store_publish | `EventsStorePublish.java` | Publish a persistent event |
| events_store_read | `EventsStoreRead.java` | Read stored events by sequence |
| events_store_read_latest | `EventsStoreReadLatest.java` | Read most recent stored events |
| command_send | `CommandSend.java` | Send a command (requires subscriber) |
| query_send | `QuerySend.java` | Send a query (requires subscriber) |
| channel_list | `ChannelList.java` | List all channels |
| channel_info | `ChannelInfo.java` | Get channel metadata |
| agent_list | `AgentList.java` | List registered agents |
| agent_info | `AgentInfo.java` | Get agent details |
| agent_send | `AgentSend.java` | Send a message to an agent |
| agent_query | `AgentQuery.java` | Query an agent |

> **Note:** `command_send` and `query_send` require an active subscriber on the target channel.
> Agent tools (`agent_*`) require registered agents on the KubeMQ server.
