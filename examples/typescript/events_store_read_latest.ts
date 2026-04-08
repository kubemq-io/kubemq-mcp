/**
 * KubeMQ MCP Example: events_store_read_latest
 *
 * Demonstrates the events_store_read_latest tool using the official MCP TypeScript SDK.
 * Returns the N most recent events from the store.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 8,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "events_store_read_latest",
 *     "arguments": { "channel": "example-events-store", "count": 3 }
 *   }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 8,
 *   "result": {
 *     "content": [{"type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3}]"}],
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
    name: "events_store_read_latest",
    arguments: {
      channel: "example-events-store",
      count: 3,
    },
  });
  console.log(JSON.stringify(result, null, 2));

  await client.close();
}

main().catch(console.error);

// Expected output:
// {
//   "content": [{"type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3},...]"}],
//   "isError": false
// }
