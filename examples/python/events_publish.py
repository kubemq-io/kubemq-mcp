"""KubeMQ MCP Example: events_publish

Demonstrates the events_publish tool using the official MCP Python SDK.
Publishes an ephemeral event — lost if no subscriber is active.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 5,
  "method": "tools/call",
  "params": {
    "name": "events_publish",
    "arguments": {
      "channel": "example-events",
      "body": "Event data",
      "metadata": "event-meta",
      "tags": {"source": "mcp-example"}
    }
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 5,
  "result": {
    "content": [{"type": "text", "text": "Event published successfully to channel 'example-events'"}],
    "isError": false
  }
}
"""

import asyncio
import os

from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

KUBEMQ_MCP_URL = os.environ.get("KUBEMQ_MCP_URL", "http://localhost:9090")


async def main():
    async with streamablehttp_client(f"{KUBEMQ_MCP_URL}/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            result = await session.call_tool("events_publish", {
                "channel": "example-events",
                "body": "Event data",
                "metadata": "event-meta",
                "tags": {"source": "mcp-example"},
            })

            print(f"Tool: events_publish")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: events_publish
# IsError: False
# Result: Event published successfully to channel 'example-events'
