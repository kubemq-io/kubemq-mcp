/**
 * KubeMQ MCP Example: queue_send
 *
 * Demonstrates the queue_send tool using the official MCP Java SDK.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 2,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "queue_send",
 *     "arguments": {
 *       "channel": "example-queue",
 *       "body": "Hello from Java MCP",
 *       "metadata": "example-metadata",
 *       "tags": {"env": "dev", "source": "mcp-example"}
 *     }
 *   }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 2,
 *   "result": {
 *     "content": [{"type": "text", "text": "Message sent successfully to queue 'example-queue'"}],
 *     "isError": false
 *   }
 * }
 */

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class QueueSend {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "queue_send",
            Map.of(
                "channel", "example-queue",
                "body", "Hello from Java MCP",
                "metadata", "example-metadata",
                "tags", Map.of("env", "dev", "source", "mcp-example")
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output:
// CallToolResult[content=[TextContent[text=Message sent successfully to queue 'example-queue']], isError=false]
