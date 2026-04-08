"""KubeMQ MCP Example: channel_list

Demonstrates the channel_list tool using the official MCP Python SDK.
Lists all channels, or filtered by type/pattern.

JSON-RPC Request (no filter):
{
  "jsonrpc": "2.0",
  "id": 11,
  "method": "tools/call",
  "params": {
    "name": "channel_list",
    "arguments": {}
  }
}

JSON-RPC Request (filtered by type):
{
  "jsonrpc": "2.0",
  "id": 11,
  "method": "tools/call",
  "params": {
    "name": "channel_list",
    "arguments": {"type": "queues"}
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 11,
  "result": {
    "content": [{"type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true},{\"name\":\"example-events\",\"type\":\"events\",\"is_active\":true}]"}],
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

            # List all channels (no filter)
            result = await session.call_tool("channel_list", {})

            print(f"Tool: channel_list")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")

            # To filter by type, use: {"type": "queues"}
            # To filter by pattern, use: {"pattern": "example-"}


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: channel_list
# IsError: False
# Result: [{"name":"example-queue","type":"queues","is_active":true},...]
