"""KubeMQ MCP Example: agent_info

Demonstrates the agent_info tool using the official MCP Python SDK.
Returns detailed information about a specific registered agent.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 14,
  "method": "tools/call",
  "params": {
    "name": "agent_info",
    "arguments": {
      "agent_id": "example-agent"
    }
  }
}

JSON-RPC Response (success):
{
  "jsonrpc": "2.0",
  "id": 14,
  "result": {
    "content": [{"type": "text", "text": "{\"agent_id\":\"example-agent\",\"name\":\"Example Agent\",\"description\":\"...\",\"version\":\"1.0.0\",\"url\":\"http://localhost:18080/\",\"skills\":[...]}"}],
    "isError": false
  }
}

JSON-RPC Response (error — non-existent agent):
{
  "jsonrpc": "2.0",
  "id": 14,
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

            result = await session.call_tool("agent_info", {
                "agent_id": "example-agent",
            })

            print(f"Tool: agent_info")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output (agent registered):
# Tool: agent_info
# IsError: False
# Result: {"agent_id":"example-agent","name":"Example Agent","description":"...","version":"1.0.0",...}
#
# Expected output (agent not found):
# Tool: agent_info
# IsError: True
# Result: Agent 'example-agent' not found
