"""KubeMQ MCP Example: events_store_publish

Demonstrates the events_store_publish tool using the official MCP Python SDK.
Publishes a persistent event that is stored and replayable.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 6,
  "method": "tools/call",
  "params": {
    "name": "events_store_publish",
    "arguments": {
      "channel": "example-events-store",
      "body": "Stored event data",
      "metadata": "store-meta",
      "tags": {"source": "mcp-example"}
    }
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 6,
  "result": {
    "content": [{"type": "text", "text": "Event published successfully to events store channel 'example-events-store'"}],
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

            result = await session.call_tool("events_store_publish", {
                "channel": "example-events-store",
                "body": "Stored event data",
                "metadata": "store-meta",
                "tags": {"source": "mcp-example"},
            })

            print(f"Tool: events_store_publish")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: events_store_publish
# IsError: False
# Result: Event published successfully to events store channel 'example-events-store'
