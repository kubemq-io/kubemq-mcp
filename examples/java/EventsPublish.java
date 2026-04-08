/**
 * KubeMQ MCP Example: events_publish
 *
 * Demonstrates the events_publish tool using the official MCP Java SDK.
 * Publishes an ephemeral event — lost if no subscriber is active.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 5,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "events_publish",
 *     "arguments": {
 *       "channel": "example-events",
 *       "body": "Event data",
 *       "metadata": "event-meta",
 *       "tags": {"source": "mcp-example"}
 *     }
 *   }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 5,
 *   "result": {
 *     "content": [{"type": "text", "text": "Event published successfully to channel 'example-events'"}],
 *     "isError": false
 *   }
 * }
 */

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class EventsPublish {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "events_publish",
            Map.of(
                "channel", "example-events",
                "body", "Event data",
                "metadata", "event-meta",
                "tags", Map.of("source", "mcp-example")
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output:
// CallToolResult[content=[TextContent[text=Event published successfully to channel 'example-events']], isError=false]
