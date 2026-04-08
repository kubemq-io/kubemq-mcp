/**
 * KubeMQ MCP Example: channel_info
 *
 * Demonstrates the channel_info tool using the official MCP TypeScript SDK.
 * Returns metadata for a specific channel.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 12,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "channel_info",
 *     "arguments": { "channel": "example-queue", "type": "queues" }
 *   }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 12,
 *   "result": {
 *     "content": [{"type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true,\"incoming\":5,\"outgoing\":3}"}],
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
    name: "channel_info",
    arguments: {
      channel: "example-queue",
      type: "queues",
    },
  });
  console.log(JSON.stringify(result, null, 2));

  await client.close();
}

main().catch(console.error);

// Expected output:
// {
//   "content": [{"type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",...}"}],
//   "isError": false
// }
