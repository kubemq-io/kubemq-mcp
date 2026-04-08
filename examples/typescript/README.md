# KubeMQ MCP Examples — TypeScript

Copy-paste-ready examples for all 15 KubeMQ MCP tools using the official [MCP TypeScript SDK](https://www.npmjs.com/package/@modelcontextprotocol/sdk).

## Prerequisites

- Node.js 18+
- TypeScript 5+
- KubeMQ server running with MCP enabled (default: `http://localhost:9090`)

## Setup

```bash
npm install
```

## Run

```bash
npx tsx queue_send.ts
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL |

## Examples

| Tool | File | Notes |
|------|------|-------|
| queue_send | `queue_send.ts` | Send a message to a queue |
| queue_receive | `queue_receive.ts` | Consume messages from a queue |
| queue_peek | `queue_peek.ts` | Peek at messages without consuming |
| events_publish | `events_publish.ts` | Publish an ephemeral event |
| events_store_publish | `events_store_publish.ts` | Publish a persistent event |
| events_store_read | `events_store_read.ts` | Read stored events by sequence |
| events_store_read_latest | `events_store_read_latest.ts` | Read most recent stored events |
| command_send | `command_send.ts` | Send a command (requires subscriber) |
| query_send | `query_send.ts` | Send a query (requires subscriber) |
| channel_list | `channel_list.ts` | List all channels |
| channel_info | `channel_info.ts` | Get channel metadata |
| agent_list | `agent_list.ts` | List registered agents |
| agent_info | `agent_info.ts` | Get agent details |
| agent_send | `agent_send.ts` | Send a message to an agent |
| agent_query | `agent_query.ts` | Query an agent |

> **Note:** `command_send` and `query_send` require an active subscriber on the target channel.
> Agent tools (`agent_*`) require registered agents on the KubeMQ server.
