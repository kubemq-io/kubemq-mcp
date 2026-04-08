"""KubeMQ MCP Example: events_store_read

Demonstrates the events_store_read tool using the official MCP Python SDK.
Reads stored events starting from a sequence number.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 7,
  "method": "tools/call",
  "params": {
    "name": "events_store_read",
    "arguments": {
      "channel": "example-events-store",
      "from_sequence": 1,
      "max_messages": 10
    }
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 7,
  "result": {
    "content": [{"type": "text", "text": "[{\"body\":\"Stored event data\",\"metadata\":\"store-meta\",\"sequence\":1,\"timestamp\":\"2026-04-06T12:00:00Z\"}]"}],
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

            result = await session.call_tool("events_store_read", {
                "channel": "example-events-store",
                "from_sequence": 1,
                "max_messages": 10,
            })

            print(f"Tool: events_store_read")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: events_store_read
# IsError: False
# Result: [{"body":"Stored event data","metadata":"store-meta","sequence":1,"timestamp":"..."}]
