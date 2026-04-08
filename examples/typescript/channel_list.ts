/**
 * KubeMQ MCP Example: channel_list
 *
 * Demonstrates the channel_list tool using the official MCP TypeScript SDK.
 * Lists all channels, or filtered by type/pattern.
 *
 * JSON-RPC Request (no filter):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 11,
 *   "method": "tools/call",
 *   "params": { "name": "channel_list", "arguments": {} }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 11,
 *   "result": {
 *     "content": [{"type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true}]"}],
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

  // List all channels (no filter)
  const result = await client.callTool({
    name: "channel_list",
    arguments: {},
  });
  console.log(JSON.stringify(result, null, 2));

  // To filter by type: { type: "queues" }
  // To filter by pattern: { pattern: "example-" }

  await client.close();
}

main().catch(console.error);

// Expected output:
// {
//   "content": [{"type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",...}]"}],
//   "isError": false
// }
