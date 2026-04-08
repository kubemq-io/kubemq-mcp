/**
 * KubeMQ MCP Example: agent_list
 *
 * Demonstrates the agent_list tool using the official MCP Java SDK.
 * Lists all registered agents, or filtered by skill_tags.
 *
 * JSON-RPC Request (no filter):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 13,
 *   "method": "tools/call",
 *   "params": { "name": "agent_list", "arguments": {} }
 * }
 *
 * JSON-RPC Response:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 13,
 *   "result": {
 *     "content": [{"type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\",...}]"}],
 *     "isError": false
 *   }
 * }
 */

import io.modelcontextprotocol.sdk.McpClient;
import io.modelcontextprotocol.sdk.client.transport.HttpClientStreamableHttpTransport;
import io.modelcontextprotocol.spec.McpSchema.CallToolRequest;

import java.util.Map;

public class AgentList {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        // List all agents (no filter)
        var result = client.callTool(new CallToolRequest(
            "agent_list",
            Map.of()
        ));
        System.out.println(result);

        // To filter by skill tags: Map.of("skill_tags", List.of("echo"))

        client.closeGracefully();
    }
}

// Expected output:
// CallToolResult[content=[TextContent[text=[{"agent_id":"echo-01",...}]]], isError=false]
