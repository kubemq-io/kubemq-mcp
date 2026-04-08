/**
 * KubeMQ MCP Example: queue_peek
 *
 * Demonstrates the queue_peek tool using the official MCP TypeScript SDK.
 * Unlike queue_receive, peek does not consume messages.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 4,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "queue_peek",
 *     "arguments": { "channel": "example-queue", "max_messages": 5 }
 *   }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 4,
 *   "result": {
 *     "content": [{"type": "text", "text": "[{\"body\":\"Hello from TypeScript MCP\"}]"}],
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
    name: "queue_peek",
    arguments: {
      channel: "example-queue",
      max_messages: 5,
    },
  });
  console.log(JSON.stringify(result, null, 2));

  await client.close();
}

main().catch(console.error);

// Expected output:
// {
//   "content": [{"type": "text", "text": "[{\"body\":\"Hello from TypeScript MCP\",...}]"}],
//   "isError": false
// }
