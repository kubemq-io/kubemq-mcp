/**
 * KubeMQ MCP Example: command_send
 *
 * Demonstrates the command_send tool using the official MCP TypeScript SDK.
 * Requires an active command subscriber on the target channel.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 9,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "command_send",
 *     "arguments": {
 *       "channel": "example-commands",
 *       "body": "do-work",
 *       "timeout_seconds": 10,
 *       "metadata": "cmd-meta",
 *       "tags": {"action": "process"}
 *     }
 *   }
 * }
 *
 * JSON-RPC Response (success):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 9,
 *   "result": {
 *     "content": [{"type": "text", "text": "Command executed successfully on channel 'example-commands'"}],
 *     "isError": false
 *   }
 * }
 *
 * JSON-RPC Response (error — no subscriber):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 9,
 *   "result": {
 *     "content": [{"type": "text", "text": "Command timed out: no subscriber on channel 'example-commands' within 10s"}],
 *     "isError": true
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
    name: "command_send",
    arguments: {
      channel: "example-commands",
      body: "do-work",
      timeout_seconds: 10,
      metadata: "cmd-meta",
      tags: { action: "process" },
    },
  });
  console.log(JSON.stringify(result, null, 2));

  await client.close();
}

main().catch(console.error);

// Expected output (with subscriber):
// {
//   "content": [{"type": "text", "text": "Command executed successfully on channel 'example-commands'"}],
//   "isError": false
// }
