/**
 * KubeMQ MCP Example: query_send
 *
 * Demonstrates the query_send tool using the official MCP Java SDK.
 * Requires an active query subscriber on the target channel.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 10,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "query_send",
 *     "arguments": {
 *       "channel": "example-queries",
 *       "body": "get-data",
 *       "timeout_seconds": 10,
 *       "metadata": "qry-meta",
 *       "tags": {"action": "lookup"}
 *     }
 *   }
 * }
 *
 * JSON-RPC Response (success):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 10,
 *   "result": {
 *     "content": [{"type": "text", "text": "{\"data\":\"query response payload from subscriber\"}"}],
 *     "isError": false
 *   }
 * }
 */

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class QuerySend {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "query_send",
            Map.of(
                "channel", "example-queries",
                "body", "get-data",
                "timeout_seconds", 10,
                "metadata", "qry-meta",
                "tags", Map.of("action", "lookup")
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output (with subscriber):
// CallToolResult[content=[TextContent[text={"data":"query response payload from subscriber"}]], isError=false]
