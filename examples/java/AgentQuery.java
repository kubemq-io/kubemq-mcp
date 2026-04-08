/**
 * KubeMQ MCP Example: agent_query
 *
 * Demonstrates the agent_query tool using the official MCP Java SDK.
 * Queries a registered agent using a specified method.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 16,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "agent_query",
 *     "arguments": { "agent_id": "example-agent", "method": "tasks/get" }
 *   }
 * }
 *
 * JSON-RPC Response (success):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 16,
 *   "result": {
 *     "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}}}"}],
 *     "isError": false
 *   }
 * }
 *
 * JSON-RPC Response (error — non-existent agent):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 16,
 *   "result": {
 *     "content": [{"type": "text", "text": "Agent 'example-agent' not found"}],
 *     "isError": true
 *   }
 * }
 */

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class AgentQuery {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "agent_query",
            Map.of(
                "agent_id", "example-agent",
                "method", "tasks/get"
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output (agent registered):
// CallToolResult[content=[TextContent[text={"echo":{"method":"tasks/get","params":{}}}]], isError=false]
//
// Expected output (agent not found):
// CallToolResult[content=[TextContent[text=Agent 'example-agent' not found]], isError=true]
