/**
 * KubeMQ MCP Example: agent_send
 *
 * Demonstrates the agent_send tool using the official MCP TypeScript SDK.
 * Sends a message to a registered agent (blocking by default).
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 15,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "agent_send",
 *     "arguments": { "agent_id": "example-agent", "message": "hello from MCP" }
 *   }
 * }
 *
 * JSON-RPC Response (success):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 15,
 *   "result": {
 *     "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"message/send\",\"params\":{\"message\":\"hello from MCP\"}}}"}],
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
    name: "agent_send",
    arguments: {
      agent_id: "example-agent",
      message: "hello from MCP",
    },
  });
  console.log(JSON.stringify(result, null, 2));

  await client.close();
}

main().catch(console.error);

// Expected output (agent registered):
// {
//   "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"message/send\",...}}"}],
//   "isError": false
// }
