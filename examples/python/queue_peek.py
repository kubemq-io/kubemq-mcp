"""KubeMQ MCP Example: queue_peek

Demonstrates the queue_peek tool using the official MCP Python SDK.
Unlike queue_receive, peek does not consume messages — they remain in the queue.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 4,
  "method": "tools/call",
  "params": {
    "name": "queue_peek",
    "arguments": {
      "channel": "example-queue",
      "max_messages": 5
    }
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 4,
  "result": {
    "content": [{"type": "text", "text": "[{\"body\":\"Hello from Python MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\"}}]"}],
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

            result = await session.call_tool("queue_peek", {
                "channel": "example-queue",
                "max_messages": 5,
            })

            print(f"Tool: queue_peek")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: queue_peek
# IsError: False
# Result: [{"body":"Hello from Python MCP","metadata":"example-metadata","tags":{"env":"dev"}}]
