"""KubeMQ MCP Example: agent_query

Demonstrates the agent_query tool using the official MCP Python SDK.
Queries a registered agent using a specified method.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 16,
  "method": "tools/call",
  "params": {
    "name": "agent_query",
    "arguments": {
      "agent_id": "example-agent",
      "method": "tasks/get"
    }
  }
}

JSON-RPC Response (success):
{
  "jsonrpc": "2.0",
  "id": 16,
  "result": {
    "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}},\"received_headers\":{}}"}],
    "isError": false
  }
}

JSON-RPC Response (error — non-existent agent):
{
  "jsonrpc": "2.0",
  "id": 16,
  "result": {
    "content": [{"type": "text", "text": "Agent 'example-agent' not found"}],
    "isError": true
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

            result = await session.call_tool("agent_query", {
                "agent_id": "example-agent",
                "method": "tasks/get",
            })

            print(f"Tool: agent_query")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output (agent registered):
# Tool: agent_query
# IsError: False
# Result: {"echo":{"method":"tasks/get","params":{}},"received_headers":{}}
#
# Expected output (agent not found):
# Tool: agent_query
# IsError: True
# Result: Agent 'example-agent' not found
