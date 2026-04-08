# KubeMQ MCP Examples

Copy-paste-ready code examples for all 15 MCP tools in 9 languages. Each example is fully self-contained — it performs the MCP handshake, calls one tool, prints the result, and cleans up.

## Tool × Language Matrix

| Tool | Python | TypeScript | Java | C# | Go | Rust | Ruby | Kotlin | Swift |
|------|--------|-----------|------|-----|-----|------|------|--------|-------|
| queue_send | [queue_send.py](python/queue_send.py) | [queue_send.ts](typescript/queue_send.ts) | [QueueSend.java](java/QueueSend.java) | [QueueSend.cs](csharp/QueueSend.cs) | [main.go](go/queue_send/main.go) | [queue_send.rs](rust/queue_send.rs) | [queue_send.rb](ruby/queue_send.rb) | [QueueSend.kt](kotlin/QueueSend.kt) | [QueueSend.swift](swift/Sources/QueueSend/QueueSend.swift) |
| queue_receive | [queue_receive.py](python/queue_receive.py) | [queue_receive.ts](typescript/queue_receive.ts) | [QueueReceive.java](java/QueueReceive.java) | [QueueReceive.cs](csharp/QueueReceive.cs) | [main.go](go/queue_receive/main.go) | [queue_receive.rs](rust/queue_receive.rs) | [queue_receive.rb](ruby/queue_receive.rb) | [QueueReceive.kt](kotlin/QueueReceive.kt) | [QueueReceive.swift](swift/Sources/QueueReceive/QueueReceive.swift) |
| queue_peek | [queue_peek.py](python/queue_peek.py) | [queue_peek.ts](typescript/queue_peek.ts) | [QueuePeek.java](java/QueuePeek.java) | [QueuePeek.cs](csharp/QueuePeek.cs) | [main.go](go/queue_peek/main.go) | [queue_peek.rs](rust/queue_peek.rs) | [queue_peek.rb](ruby/queue_peek.rb) | [QueuePeek.kt](kotlin/QueuePeek.kt) | [QueuePeek.swift](swift/Sources/QueuePeek/QueuePeek.swift) |
| events_publish | [events_publish.py](python/events_publish.py) | [events_publish.ts](typescript/events_publish.ts) | [EventsPublish.java](java/EventsPublish.java) | [EventsPublish.cs](csharp/EventsPublish.cs) | [main.go](go/events_publish/main.go) | [events_publish.rs](rust/events_publish.rs) | [events_publish.rb](ruby/events_publish.rb) | [EventsPublish.kt](kotlin/EventsPublish.kt) | [EventsPublish.swift](swift/Sources/EventsPublish/EventsPublish.swift) |
| events_store_publish | [events_store_publish.py](python/events_store_publish.py) | [events_store_publish.ts](typescript/events_store_publish.ts) | [EventsStorePublish.java](java/EventsStorePublish.java) | [EventsStorePublish.cs](csharp/EventsStorePublish.cs) | [main.go](go/events_store_publish/main.go) | [events_store_publish.rs](rust/events_store_publish.rs) | [events_store_publish.rb](ruby/events_store_publish.rb) | [EventsStorePublish.kt](kotlin/EventsStorePublish.kt) | [EventsStorePublish.swift](swift/Sources/EventsStorePublish/EventsStorePublish.swift) |
| events_store_read | [events_store_read.py](python/events_store_read.py) | [events_store_read.ts](typescript/events_store_read.ts) | [EventsStoreRead.java](java/EventsStoreRead.java) | [EventsStoreRead.cs](csharp/EventsStoreRead.cs) | [main.go](go/events_store_read/main.go) | [events_store_read.rs](rust/events_store_read.rs) | [events_store_read.rb](ruby/events_store_read.rb) | [EventsStoreRead.kt](kotlin/EventsStoreRead.kt) | [EventsStoreRead.swift](swift/Sources/EventsStoreRead/EventsStoreRead.swift) |
| events_store_read_latest | [events_store_read_latest.py](python/events_store_read_latest.py) | [events_store_read_latest.ts](typescript/events_store_read_latest.ts) | [EventsStoreReadLatest.java](java/EventsStoreReadLatest.java) | [EventsStoreReadLatest.cs](csharp/EventsStoreReadLatest.cs) | [main.go](go/events_store_read_latest/main.go) | [events_store_read_latest.rs](rust/events_store_read_latest.rs) | [events_store_read_latest.rb](ruby/events_store_read_latest.rb) | [EventsStoreReadLatest.kt](kotlin/EventsStoreReadLatest.kt) | [EventsStoreReadLatest.swift](swift/Sources/EventsStoreReadLatest/EventsStoreReadLatest.swift) |
| command_send | [command_send.py](python/command_send.py) | [command_send.ts](typescript/command_send.ts) | [CommandSend.java](java/CommandSend.java) | [CommandSend.cs](csharp/CommandSend.cs) | [main.go](go/command_send/main.go) | [command_send.rs](rust/command_send.rs) | [command_send.rb](ruby/command_send.rb) | [CommandSend.kt](kotlin/CommandSend.kt) | [CommandSend.swift](swift/Sources/CommandSend/CommandSend.swift) |
| query_send | [query_send.py](python/query_send.py) | [query_send.ts](typescript/query_send.ts) | [QuerySend.java](java/QuerySend.java) | [QuerySend.cs](csharp/QuerySend.cs) | [main.go](go/query_send/main.go) | [query_send.rs](rust/query_send.rs) | [query_send.rb](ruby/query_send.rb) | [QuerySend.kt](kotlin/QuerySend.kt) | [QuerySend.swift](swift/Sources/QuerySend/QuerySend.swift) |
| channel_list | [channel_list.py](python/channel_list.py) | [channel_list.ts](typescript/channel_list.ts) | [ChannelList.java](java/ChannelList.java) | [ChannelList.cs](csharp/ChannelList.cs) | [main.go](go/channel_list/main.go) | [channel_list.rs](rust/channel_list.rs) | [channel_list.rb](ruby/channel_list.rb) | [ChannelList.kt](kotlin/ChannelList.kt) | [ChannelList.swift](swift/Sources/ChannelList/ChannelList.swift) |
| channel_info | [channel_info.py](python/channel_info.py) | [channel_info.ts](typescript/channel_info.ts) | [ChannelInfo.java](java/ChannelInfo.java) | [ChannelInfo.cs](csharp/ChannelInfo.cs) | [main.go](go/channel_info/main.go) | [channel_info.rs](rust/channel_info.rs) | [channel_info.rb](ruby/channel_info.rb) | [ChannelInfo.kt](kotlin/ChannelInfo.kt) | [ChannelInfo.swift](swift/Sources/ChannelInfo/ChannelInfo.swift) |
| agent_list | [agent_list.py](python/agent_list.py) | [agent_list.ts](typescript/agent_list.ts) | [AgentList.java](java/AgentList.java) | [AgentList.cs](csharp/AgentList.cs) | [main.go](go/agent_list/main.go) | [agent_list.rs](rust/agent_list.rs) | [agent_list.rb](ruby/agent_list.rb) | [AgentList.kt](kotlin/AgentList.kt) | [AgentList.swift](swift/Sources/AgentList/AgentList.swift) |
| agent_info | [agent_info.py](python/agent_info.py) | [agent_info.ts](typescript/agent_info.ts) | [AgentInfo.java](java/AgentInfo.java) | [AgentInfo.cs](csharp/AgentInfo.cs) | [main.go](go/agent_info/main.go) | [agent_info.rs](rust/agent_info.rs) | [agent_info.rb](ruby/agent_info.rb) | [AgentInfo.kt](kotlin/AgentInfo.kt) | [AgentInfo.swift](swift/Sources/AgentInfo/AgentInfo.swift) |
| agent_send | [agent_send.py](python/agent_send.py) | [agent_send.ts](typescript/agent_send.ts) | [AgentSend.java](java/AgentSend.java) | [AgentSend.cs](csharp/AgentSend.cs) | [main.go](go/agent_send/main.go) | [agent_send.rs](rust/agent_send.rs) | [agent_send.rb](ruby/agent_send.rb) | [AgentSend.kt](kotlin/AgentSend.kt) | [AgentSend.swift](swift/Sources/AgentSend/AgentSend.swift) |
| agent_query | [agent_query.py](python/agent_query.py) | [agent_query.ts](typescript/agent_query.ts) | [AgentQuery.java](java/AgentQuery.java) | [AgentQuery.cs](csharp/AgentQuery.cs) | [main.go](go/agent_query/main.go) | [agent_query.rs](rust/agent_query.rs) | [agent_query.rb](ruby/agent_query.rb) | [AgentQuery.kt](kotlin/AgentQuery.kt) | [AgentQuery.swift](swift/Sources/AgentQuery/AgentQuery.swift) |

## Quick Start by Language

| Language | Prerequisites | Setup | Run Example |
|----------|--------------|-------|-------------|
| [Python](python/) | Python 3.10+, uv | `cd python && uv venv && uv pip install -e .` | `uv run python queue_send.py` |
| [TypeScript](typescript/) | Node.js 18+, TypeScript 5+ | `cd typescript && npm install` | `npx tsx queue_send.ts` |
| [Java](java/) | Java 21+, Maven | `cd java && mvn dependency:resolve` | `mvn compile exec:java -Dexec.mainClass="QueueSend"` |
| [C#](csharp/) | .NET 8+ | `cd csharp && dotnet restore` | `dotnet run /p:StartupObject=QueueSend` |
| [Go](go/) | Go 1.21+ | `cd go && go mod download` | `go run ./queue_send/main.go` |
| [Rust](rust/) | Rust 1.75+ | `cd rust && cargo build` | `cargo run --bin queue_send` |
| [Ruby](ruby/) | Ruby 3.1+, Bundler | `cd ruby && bundle install` | `bundle exec ruby queue_send.rb` |
| [Kotlin](kotlin/) | Kotlin 1.9+, JVM 21+ | `cd kotlin && ./gradlew build` | `./gradlew run -PmainClass=QueueSendKt` |
| [Swift](swift/) | Swift 6.0+, macOS 13+ | `cd swift && swift build` | `swift run QueueSend` |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL (examples append `/mcp`) |

## Tool Descriptions

| Tool | Category | Description |
|------|----------|-------------|
| `queue_send` | Queue | Send a message to a queue channel |
| `queue_receive` | Queue | Receive (consume) messages from a queue channel |
| `queue_peek` | Queue | Peek at messages without consuming them |
| `events_publish` | Events | Publish an ephemeral event (fire-and-forget) |
| `events_store_publish` | Events | Publish a persistent event to an events store channel |
| `events_store_read` | Events | Read stored events from a sequence number or timestamp |
| `events_store_read_latest` | Events | Read the N most recent stored events |
| `command_send` | Command/Query | Send a synchronous command (requires active subscriber) |
| `query_send` | Command/Query | Send a synchronous query with data response (requires active subscriber) |
| `channel_list` | Channel | List channels, optionally filtered by type or pattern |
| `channel_info` | Channel | Get metadata for a specific channel |
| `agent_list` | Agent Bridge | List registered agents, optionally filtered by skill tags |
| `agent_info` | Agent Bridge | Get detailed information about a specific agent |
| `agent_send` | Agent Bridge | Send a message to an agent (blocking or non-blocking) |
| `agent_query` | Agent Bridge | Query an agent with a specific method (tasks/get, tasks/cancel, custom) |

## Notes

- **command_send** and **query_send** require an active subscriber on the target channel. Without one, the call will timeout.
- **agent_\*** tools require agents registered with the KubeMQ server.
- All examples use the official MCP SDK for each language — not raw HTTP.
- Each example includes JSON-RPC request/response documentation as comments and expected output at the end.
