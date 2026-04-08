"""KubeMQ MCP Example: queue_receive

Demonstrates the queue_receive tool using the official MCP Python SDK.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "queue_receive",
    "arguments": {
      "channel": "example-queue",
      "max_messages": 5
    }
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [{"type": "text", "text": "[{\"body\":\"Hello from Python MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\",\"source\":\"mcp-example\"}}]"}],
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

            result = await session.call_tool("queue_receive", {
                "channel": "example-queue",
                "max_messages": 5,
            })

            print(f"Tool: queue_receive")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: queue_receive
# IsError: False
# Result: [{"body":"Hello from Python MCP","metadata":"example-metadata","tags":{"env":"dev","source":"mcp-example"}}]
