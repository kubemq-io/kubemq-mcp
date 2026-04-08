/**
 * KubeMQ MCP Example: channel_info
 *
 * Demonstrates the channel_info tool using the official MCP Java SDK.
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

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class ChannelInfo {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "channel_info",
            Map.of(
                "channel", "example-queue",
                "type", "queues"
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output:
// CallToolResult[content=[TextContent[text={"name":"example-queue","type":"queues","is_active":true,...}]], isError=false]
