/**
 * KubeMQ MCP Example: events_store_publish
 *
 * Demonstrates the events_store_publish tool using the official MCP TypeScript SDK.
 * Publishes a persistent event that is stored and replayable.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 6,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "events_store_publish",
 *     "arguments": {
 *       "channel": "example-events-store",
 *       "body": "Stored event data",
 *       "metadata": "store-meta",
 *       "tags": {"source": "mcp-example"}
 *     }
 *   }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 6,
 *   "result": {
 *     "content": [{"type": "text", "text": "Event published successfully to events store channel 'example-events-store'"}],
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
    name: "events_store_publish",
    arguments: {
      channel: "example-events-store",
      body: "Stored event data",
      metadata: "store-meta",
      tags: { source: "mcp-example" },
    },
  });
  console.log(JSON.stringify(result, null, 2));

  await client.close();
}

main().catch(console.error);

// Expected output:
// {
//   "content": [{"type": "text", "text": "Event published successfully to events store channel 'example-events-store'"}],
//   "isError": false
// }
