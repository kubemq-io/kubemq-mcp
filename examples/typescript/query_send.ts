/**
 * KubeMQ MCP Example: query_send
 *
 * Demonstrates the query_send tool using the official MCP TypeScript SDK.
 * Requires an active query subscriber on the target channel.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 10,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "query_send",
 *     "arguments": {
 *       "channel": "example-queries",
 *       "body": "get-data",
 *       "timeout_seconds": 10,
 *       "metadata": "qry-meta",
 *       "tags": {"action": "lookup"}
 *     }
 *   }
 * }
 *
 * JSON-RPC Response (success):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 10,
 *   "result": {
 *     "content": [{"type": "text", "text": "{\"data\":\"query response payload from subscriber\"}"}],
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
    name: "query_send",
    arguments: {
      channel: "example-queries",
      body: "get-data",
      timeout_seconds: 10,
      metadata: "qry-meta",
      tags: { action: "lookup" },
    },
  });
  console.log(JSON.stringify(result, null, 2));

  await client.close();
}

main().catch(console.error);

// Expected output (with subscriber):
// {
//   "content": [{"type": "text", "text": "{\"data\":\"query response payload from subscriber\"}"}],
//   "isError": false
// }
