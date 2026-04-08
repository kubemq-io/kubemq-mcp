"""KubeMQ MCP Example: query_send

Demonstrates the query_send tool using the official MCP Python SDK.
Requires an active query subscriber on the target channel.

JSON-RPC Request:
{
  "jsonrpc": "2.0",
  "id": 10,
  "method": "tools/call",
  "params": {
    "name": "query_send",
    "arguments": {
      "channel": "example-queries",
      "body": "get-data",
      "timeout_seconds": 10,
      "metadata": "qry-meta",
      "tags": {"action": "lookup"}
    }
  }
}

JSON-RPC Response (success):
{
  "jsonrpc": "2.0",
  "id": 10,
  "result": {
    "content": [{"type": "text", "text": "{\"data\":\"query response payload from subscriber\"}"}],
    "isError": false
  }
}

JSON-RPC Response (error — no subscriber):
{
  "jsonrpc": "2.0",
  "id": 10,
  "result": {
    "content": [{"type": "text", "text": "Query timed out: no subscriber on channel 'example-queries' within 10s"}],
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

            result = await session.call_tool("query_send", {
                "channel": "example-queries",
                "body": "get-data",
                "timeout_seconds": 10,
                "metadata": "qry-meta",
                "tags": {"action": "lookup"},
            })

            print(f"Tool: query_send")
            print(f"IsError: {result.isError}")
            for content in result.content:
                print(f"Result: {content.text}")


if __name__ == "__main__":
    asyncio.run(main())

# Expected output (with subscriber):
# Tool: query_send
# IsError: False
# Result: {"data":"query response payload from subscriber"}
#
# Expected output (without subscriber):
# Tool: query_send
# IsError: True
# Result: Query timed out: no subscriber on channel 'example-queries' within 10s
