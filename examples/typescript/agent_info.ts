/**
 * KubeMQ MCP Example: agent_info
 *
 * Demonstrates the agent_info tool using the official MCP TypeScript SDK.
 * Returns detailed information about a specific registered agent.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 14,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "agent_info",
 *     "arguments": { "agent_id": "example-agent" }
 *   }
 * }
 *
 * JSON-RPC Response (success):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 14,
 *   "result": {
 *     "content": [{"type": "text", "text": "{\"agent_id\":\"example-agent\",\"name\":\"Example Agent\",...}"}],
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
    name: "agent_info",
    arguments: {
      agent_id: "example-agent",
    },
  });
  console.log(JSON.stringify(result, null, 2));

  await client.close();
}

main().catch(console.error);

// Expected output (agent registered):
// {
//   "content": [{"type": "text", "text": "{\"agent_id\":\"example-agent\",\"name\":\"Example Agent\",...}"}],
//   "isError": false
// }
