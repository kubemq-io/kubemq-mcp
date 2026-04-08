# KubeMQ MCP Examples — Kotlin

Copy-paste-ready examples for all 15 KubeMQ MCP tools using the official [MCP Kotlin SDK](https://central.sonatype.com/artifact/io.modelcontextprotocol/kotlin-sdk).

## Prerequisites

- Kotlin 1.9+ / JVM 21+
- Gradle 8+
- KubeMQ server running with MCP enabled (default: `http://localhost:9090`)

## Setup

```bash
./gradlew build
```

## Run

```bash
./gradlew run -PmainClass=QueueSendKt
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL |

## Examples

| Tool | File | Run Command |
|------|------|-------------|
| queue_send | `QueueSend.kt` | `./gradlew run -PmainClass=QueueSendKt` |
| queue_receive | `QueueReceive.kt` | `./gradlew run -PmainClass=QueueReceiveKt` |
| queue_peek | `QueuePeek.kt` | `./gradlew run -PmainClass=QueuePeekKt` |
| events_publish | `EventsPublish.kt` | `./gradlew run -PmainClass=EventsPublishKt` |
| events_store_publish | `EventsStorePublish.kt` | `./gradlew run -PmainClass=EventsStorePublishKt` |
| events_store_read | `EventsStoreRead.kt` | `./gradlew run -PmainClass=EventsStoreReadKt` |
| events_store_read_latest | `EventsStoreReadLatest.kt` | `./gradlew run -PmainClass=EventsStoreReadLatestKt` |
| command_send | `CommandSend.kt` | `./gradlew run -PmainClass=CommandSendKt` |
| query_send | `QuerySend.kt` | `./gradlew run -PmainClass=QuerySendKt` |
| channel_list | `ChannelList.kt` | `./gradlew run -PmainClass=ChannelListKt` |
| channel_info | `ChannelInfo.kt` | `./gradlew run -PmainClass=ChannelInfoKt` |
| agent_list | `AgentList.kt` | `./gradlew run -PmainClass=AgentListKt` |
| agent_info | `AgentInfo.kt` | `./gradlew run -PmainClass=AgentInfoKt` |
| agent_send | `AgentSend.kt` | `./gradlew run -PmainClass=AgentSendKt` |
| agent_query | `AgentQuery.kt` | `./gradlew run -PmainClass=AgentQueryKt` |

> **Note:** `command_send` and `query_send` require an active subscriber on the target channel.
> Agent tools (`agent_*`) require registered agents on the KubeMQ server.
>
> **SDK Note (I-2):** Kotlin MCP SDK API verified against `kotlin-sdk` v0.9.0. Requires Ktor `HttpClient` with SSE plugin. If the API has changed, update the transport class name and constructor parameters accordingly.
