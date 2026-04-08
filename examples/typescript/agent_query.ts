/**
 * KubeMQ MCP Example: agent_query
 *
 * Demonstrates the agent_query tool using the official MCP TypeScript SDK.
 * Queries a registered agent using a specified method.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 16,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "agent_query",
 *     "arguments": { "agent_id": "example-agent", "method": "tasks/get" }
 *   }
 * }
 *
 * JSON-RPC Response (success):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 16,
 *   "result": {
 *     "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}}}"}],
 *     "isError": false
 *   }
 * }
 */

import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const KUBEMQ_MCP_URL = process.env.KUBEMQ_MCP_URL || "http://localhost:9090";

async function main() {
  const transport = new StreamableHTTPClientTransport(
    new URL(`${KUBEMQ_MCP_URL}/mcp`)
  );
  const client = new Client({ name: "kubemq-mcp-ts-example", version: "1.0.0" });
  await client.connect(transport);

  const result = await client.callTool({
    name: "agent_query",
    arguments: {
      agent_id: "example-agent",
      method: "tasks/get",
    },
  });
  console.log(JSON.stringify(result, null, 2));

  await client.close();
}

main().catch(console.error);

// Expected output (agent registered):
// {
//   "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}}}"}],
//   "isError": false
// }
