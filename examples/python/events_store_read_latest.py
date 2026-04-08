"""KubeMQ MCP Example: events_store_read_latest

Demonstrates the events_store_read_latest tool using the official MCP Python SDK.
Returns the N most recent events from the store.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 8,
  "method": "tools/call",
  "params": {
    "name": "events_store_read_latest",
    "arguments": {
      "channel": "example-events-store",
      "count": 3
    }
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 8,
  "result": {
    "content": [{"type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3},{\"body\":\"Stored event 2\",\"sequence\":2},{\"body\":\"Stored event 1\",\"sequence\":1}]"}],
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

            result = await session.call_tool("events_store_read_latest", {
                "channel": "example-events-store",
                "count": 3,
            })

            print(f"Tool: events_store_read_latest")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: events_store_read_latest
# IsError: False
# Result: [{"body":"Stored event 3","sequence":3},{"body":"Stored event 2","sequence":2},{"body":"Stored event 1","sequence":1}]
