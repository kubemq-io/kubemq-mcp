"""KubeMQ MCP Example: agent_list

Demonstrates the agent_list tool using the official MCP Python SDK.
Lists all registered agents, or filtered by skill_tags.

JSON-RPC Request (no filter):
{
  "jsonrpc": "2.0",
  "id": 13,
  "method": "tools/call",
  "params": {
    "name": "agent_list",
    "arguments": {}
  }
}

JSON-RPC Response:
{
  "jsonrpc": "2.0",
  "id": 13,
  "result": {
    "content": [{"type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\",\"skills\":[{\"id\":\"echo\",\"name\":\"Echo\",\"tags\":[\"test\",\"echo\"]}]}]"}],
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

            # List all agents (no filter)
            result = await session.call_tool("agent_list", {})

            print(f"Tool: agent_list")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")

            # To filter by skill tags, use: {"skill_tags": ["echo"]}


if __name__ == "__main__":
    asyncio.run(main())

# Expected output:
# Tool: agent_list
# IsError: False
# Result: [{"agent_id":"echo-01","name":"Echo Agent 01","skills":[...]}]
