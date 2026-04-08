/**
 * KubeMQ MCP Example: events_store_read_latest
 *
 * Demonstrates the events_store_read_latest tool using the official MCP Java SDK.
 * Returns the N most recent events from the store.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 8,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "events_store_read_latest",
 *     "arguments": { "channel": "example-events-store", "count": 3 }
 *   }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 8,
 *   "result": {
 *     "content": [{"type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3},...]"}],
 *     "isError": false
 *   }
 * }
 */

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class EventsStoreReadLatest {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "events_store_read_latest",
            Map.of(
                "channel", "example-events-store",
                "count", 3
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output:
// CallToolResult[content=[TextContent[text=[{"body":"Stored event 3","sequence":3},...]]], isError=false]
