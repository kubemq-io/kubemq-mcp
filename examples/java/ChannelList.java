/**
 * KubeMQ MCP Example: channel_list
 *
 * Demonstrates the channel_list tool using the official MCP Java SDK.
 * Lists all channels, or filtered by type/pattern.
 *
 * JSON-RPC Request (no filter):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 11,
 *   "method": "tools/call",
 *   "params": { "name": "channel_list", "arguments": {} }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 11,
 *   "result": {
 *     "content": [{"type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true}]"}],
 *     "isError": false
 *   }
 * }
 */

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class ChannelList {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        // List all channels (no filter)
        var result = client.callTool(new CallToolRequest(
            "channel_list",
            Map.of()
        ));
        System.out.println(result);

        // To filter by type: Map.of("type", "queues")
        // To filter by pattern: Map.of("pattern", "example-")

        client.closeGracefully();
    }
}

// Expected output:
// CallToolResult[content=[TextContent[text=[{"name":"example-queue","type":"queues",...}]]], isError=false]
