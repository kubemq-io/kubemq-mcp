/**
 * KubeMQ MCP Example: agent_list
 *
 * Demonstrates the agent_list tool using the official MCP TypeScript SDK.
 * Lists all registered agents, or filtered by skill_tags.
 *
 * JSON-RPC Request (no filter):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 13,
 *   "method": "tools/call",
 *   "params": { "name": "agent_list", "arguments": {} }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 13,
 *   "result": {
 *     "content": [{"type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\"}]"}],
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

  // List all agents (no filter)
  const result = await client.callTool({
    name: "agent_list",
    arguments: {},
  });
  console.log(JSON.stringify(result, null, 2));

  // To filter by skill tags: { skill_tags: ["echo"] }

  await client.close();
}

main().catch(console.error);

// Expected output:
// {
//   "content": [{"type": "text", "text": "[{\"agent_id\":\"echo-01\",...}]"}],
//   "isError": false
// }
