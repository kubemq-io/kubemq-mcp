# KubeMQ MCP Examples — Rust

Copy-paste-ready examples for all 15 KubeMQ MCP tools using the [rmcp](https://crates.io/crates/rmcp) crate with the `transport-streamable-http-client-reqwest` feature.

## Prerequisites

- [Rust 1.75+](https://rustup.rs/) (stable)
- KubeMQ server running with MCP enabled (default: `http://localhost:9090/mcp`)

## Setup

```bash
cargo build
```

## Run

Each tool example is a separate binary target:

```bash
cargo run --bin queue_send
cargo run --bin queue_receive
cargo run --bin events_publish
```

## Environment Variable

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL |

## Tool Examples

| # | File | Tool | Description |
|---|------|------|-------------|
| 1 | `queue_send.rs` | queue_send | Send a message to a queue |
| 2 | `queue_receive.rs` | queue_receive | Receive messages from a queue |
| 3 | `queue_peek.rs` | queue_peek | Peek at messages without consuming |
| 4 | `events_publish.rs` | events_publish | Publish an ephemeral event |
| 5 | `events_store_publish.rs` | events_store_publish | Publish a persistent event |
| 6 | `events_store_read.rs` | events_store_read | Read stored events by sequence |
| 7 | `events_store_read_latest.rs` | events_store_read_latest | Read most recent stored events |
| 8 | `command_send.rs` | command_send | Send a command (requires subscriber) |
| 9 | `query_send.rs` | query_send | Send a query (requires subscriber) |
| 10 | `channel_list.rs` | channel_list | List all channels |
| 11 | `channel_info.rs` | channel_info | Get channel metadata |
| 12 | `agent_list.rs` | agent_list | List registered agents |
| 13 | `agent_info.rs` | agent_info | Get agent details |
| 14 | `agent_send.rs` | agent_send | Send a message to an agent |
| 15 | `agent_query.rs` | agent_query | Query an agent |

## Notes

- `command_send` and `query_send` require an active subscriber on the target channel.
- Agent tools (`agent_*`) require registered agents on the KubeMQ server.
- The `rmcp` crate API was verified against v1.3.0. If the API has changed, consult the [rmcp documentation](https://docs.rs/rmcp).
