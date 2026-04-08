/**
 * KubeMQ MCP Example: queue_receive
 *
 * Demonstrates the queue_receive tool using the official MCP Java SDK.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 3,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "queue_receive",
 *     "arguments": { "channel": "example-queue", "max_messages": 5 }
 *   }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 3,
 *   "result": {
 *     "content": [{"type": "text", "text": "[{\"body\":\"Hello from Java MCP\",...}]"}],
 *     "isError": false
 *   }
 * }
 */

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class QueueReceive {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "queue_receive",
            Map.of(
                "channel", "example-queue",
                "max_messages", 5
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output:
// CallToolResult[content=[TextContent[text=[{"body":"Hello from Java MCP",...}]]], isError=false]
