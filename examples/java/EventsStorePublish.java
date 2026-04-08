/**
 * KubeMQ MCP Example: events_store_publish
 *
 * Demonstrates the events_store_publish tool using the official MCP Java SDK.
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

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class EventsStorePublish {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "events_store_publish",
            Map.of(
                "channel", "example-events-store",
                "body", "Stored event data",
                "metadata", "store-meta",
                "tags", Map.of("source", "mcp-example")
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output:
// CallToolResult[content=[TextContent[text=Event published successfully to events store channel 'example-events-store']], isError=false]
