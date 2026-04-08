# KubeMQ MCP Examples — Python

Copy-paste-ready examples for all 15 KubeMQ MCP tools using the official [MCP Python SDK](https://pypi.org/project/mcp/).

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- KubeMQ server running with MCP enabled (default: `http://localhost:9090`)

## Setup

```bash
uv venv
uv pip install -e .
```

## Run

```bash
uv run python queue_send.py
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KUBEMQ_MCP_URL` | `http://localhost:9090` | KubeMQ server base URL |

## Examples

| Tool | File | Notes |
|------|------|-------|
| queue_send | `queue_send.py` | Send a message to a queue |
| queue_receive | `queue_receive.py` | Consume messages from a queue |
| queue_peek | `queue_peek.py` | Peek at messages without consuming |
| events_publish | `events_publish.py` | Publish an ephemeral event |
| events_store_publish | `events_store_publish.py` | Publish a persistent event |
| events_store_read | `events_store_read.py` | Read stored events by sequence |
| events_store_read_latest | `events_store_read_latest.py` | Read most recent stored events |
| command_send | `command_send.py` | Send a command (requires subscriber) |
| query_send | `query_send.py` | Send a query (requires subscriber) |
| channel_list | `channel_list.py` | List all channels |
| channel_info | `channel_info.py` | Get channel metadata |
| agent_list | `agent_list.py` | List registered agents |
| agent_info | `agent_info.py` | Get agent details |
| agent_send | `agent_send.py` | Send a message to an agent |
| agent_query | `agent_query.py` | Query an agent |

> **Note:** `command_send` and `query_send` require an active subscriber on the target channel.
> Agent tools (`agent_*`) require registered agents on the KubeMQ server.
