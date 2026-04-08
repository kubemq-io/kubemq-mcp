"""KubeMQ MCP Example: channel_info

Demonstrates the channel_info tool using the official MCP Python SDK.
Returns metadata for a specific channel.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 12,
  "method": "tools/call",
  "params": {
    "name": "channel_info",
    "arguments": {
      "channel": "example-queue",
      "type": "queues"
    }
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 12,
  "result": {
    "content": [{"type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true,\"incoming\":5,\"outgoing\":3}"}],
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

            result = await session.call_tool("channel_info", {
                "channel": "example-queue",
                "type": "queues",
            })

            print(f"Tool: channel_info")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: channel_info
# IsError: False
# Result: {"name":"example-queue","type":"queues","is_active":true,"incoming":5,"outgoing":3}
