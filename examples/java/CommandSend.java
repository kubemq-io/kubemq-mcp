/**
 * KubeMQ MCP Example: command_send
 *
 * Demonstrates the command_send tool using the official MCP Java SDK.
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

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class CommandSend {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "command_send",
            Map.of(
                "channel", "example-commands",
                "body", "do-work",
                "timeout_seconds", 10,
                "metadata", "cmd-meta",
                "tags", Map.of("action", "process")
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output (with subscriber):
// CallToolResult[content=[TextContent[text=Command executed successfully on channel 'example-commands']], isError=false]
//
// Expected output (without subscriber):
// CallToolResult[content=[TextContent[text=Command timed out: no subscriber on channel 'example-commands' within 10s]], isError=true]
