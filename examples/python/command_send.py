"""KubeMQ MCP Example: command_send

Demonstrates the command_send tool using the official MCP Python SDK.
Requires an active command subscriber on the target channel.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 9,
  "method": "tools/call",
  "params": {
    "name": "command_send",
    "arguments": {
      "channel": "example-commands",
      "body": "do-work",
      "timeout_seconds": 10,
      "metadata": "cmd-meta",
      "tags": {"action": "process"}
    }
  }
}

JSON-RPC Response (success):
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "content": [{"type": "text", "text": "Command executed successfully on channel 'example-commands'"}],
    "isError": false
  }
}

JSON-RPC Response (error — no subscriber):
{
  "jsonrpc": "2.0",
  "id": 9,
  "result": {
    "content": [{"type": "text", "text": "Command timed out: no subscriber on channel 'example-commands' within 10s"}],
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

            result = await session.call_tool("command_send", {
                "channel": "example-commands",
                "body": "do-work",
                "timeout_seconds": 10,
                "metadata": "cmd-meta",
                "tags": {"action": "process"},
            })

            print(f"Tool: command_send")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output (with subscriber):
# Tool: command_send
# IsError: False
# Result: Command executed successfully on channel 'example-commands'
#
# Expected output (without subscriber):
# Tool: command_send
# IsError: True
# Result: Command timed out: no subscriber on channel 'example-commands' within 10s
