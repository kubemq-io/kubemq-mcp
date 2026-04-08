"""KubeMQ MCP Example: queue_send

Demonstrates the queue_send tool using the official MCP Python SDK.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "queue_send",
    "arguments": {
      "channel": "example-queue",
      "body": "Hello from Python MCP",
      "metadata": "example-metadata",
      "tags": {"env": "dev", "source": "mcp-example"}
    }
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [{"type": "text", "text": "Message sent successfully to queue 'example-queue'"}],
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

            result = await session.call_tool("queue_send", {
                "channel": "example-queue",
                "body": "Hello from Python MCP",
                "metadata": "example-metadata",
                "tags": {"env": "dev", "source": "mcp-example"},
            })

            print(f"Tool: queue_send")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: queue_send
# IsError: False
# Result: Message sent successfully to queue 'example-queue'
