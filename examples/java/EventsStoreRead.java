/**
 * KubeMQ MCP Example: events_store_read
 *
 * Demonstrates the events_store_read tool using the official MCP Java SDK.
 * Reads stored events starting from a sequence number.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 7,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "events_store_read",
 *     "arguments": {
 *       "channel": "example-events-store",
 *       "from_sequence": 1,
 *       "max_messages": 10
 *     }
 *   }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 7,
 *   "result": {
 *     "content": [{"type": "text", "text": "[{\"body\":\"Stored event data\",\"sequence\":1,...}]"}],
 *     "isError": false
 *   }
 * }
 */

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class EventsStoreRead {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "events_store_read",
            Map.of(
                "channel", "example-events-store",
                "from_sequence", 1,
                "max_messages", 10
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output:
// CallToolResult[content=[TextContent[text=[{"body":"Stored event data","sequence":1,...}]]], isError=false]
