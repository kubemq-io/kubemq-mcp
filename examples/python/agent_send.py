"""KubeMQ MCP Example: agent_send

Demonstrates the agent_send tool using the official MCP Python SDK.
Sends a message to a registered agent (blocking by default).

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 15,
  "method": "tools/call",
  "params": {
    "name": "agent_send",
    "arguments": {
      "agent_id": "example-agent",
      "message": "hello from MCP"
    }
  }
}

JSON-RPC Response (success):
{
  "jsonrpc": "2.0",
  "id": 15,
  "result": {
    "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"message/send\",\"params\":{\"message\":\"hello from MCP\"}},\"received_headers\":{}}"}],
    "isError": false
  }
}

JSON-RPC Response (error — non-existent agent):
{
  "jsonrpc": "2.0",
  "id": 15,
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

            result = await session.call_tool("agent_send", {
                "agent_id": "example-agent",
                "message": "hello from MCP",
            })

            print(f"Tool: agent_send")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output (agent registered):
# Tool: agent_send
# IsError: False
# Result: {"echo":{"method":"message/send","params":{"message":"hello from MCP"}},"received_headers":{}}
#
# Expected output (agent not found):
# Tool: agent_send
# IsError: True
# Result: Agent 'example-agent' not found
