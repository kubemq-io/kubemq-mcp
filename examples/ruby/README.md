# KubeMQ MCP Examples — Ruby

Copy-paste-ready examples for all 15 KubeMQ MCP tools using the official [MCP Ruby SDK](https://rubygems.org/gems/mcp).

## Prerequisites

- Ruby 3.1+
- Bundler
- KubeMQ server running with MCP enabled (default: `http://localhost:9090`)

## Setup

```bash
bundle install
```

## Run

```bash
bundle exec ruby queue_send.rb
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL |

## Examples

| Tool | File | Notes |
|------|------|-------|
| queue_send | `queue_send.rb` | Send a message to a queue |
| queue_receive | `queue_receive.rb` | Consume messages from a queue |
| queue_peek | `queue_peek.rb` | Peek at messages without consuming |
| events_publish | `events_publish.rb` | Publish an ephemeral event |
| events_store_publish | `events_store_publish.rb` | Publish a persistent event |
| events_store_read | `events_store_read.rb` | Read stored events by sequence |
| events_store_read_latest | `events_store_read_latest.rb` | Read most recent stored events |
| command_send | `command_send.rb` | Send a command (requires subscriber) |
| query_send | `query_send.rb` | Send a query (requires subscriber) |
| channel_list | `channel_list.rb` | List all channels |
| channel_info | `channel_info.rb` | Get channel metadata |
| agent_list | `agent_list.rb` | List registered agents |
| agent_info | `agent_info.rb` | Get agent details |
| agent_send | `agent_send.rb` | Send a message to an agent |
| agent_query | `agent_query.rb` | Query an agent |

> **Note:** `command_send` and `query_send` require an active subscriber on the target channel.
> Agent tools (`agent_*`) require registered agents on the KubeMQ server.
>
> **SDK Note (I-2):** Ruby MCP SDK API verified against `mcp` gem v0.9.2. If the API has changed, update the transport class name and constructor parameters accordingly.
