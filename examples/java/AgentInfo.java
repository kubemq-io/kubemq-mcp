/**
 * KubeMQ MCP Example: agent_info
 *
 * Demonstrates the agent_info tool using the official MCP Java SDK.
 * Returns detailed information about a specific registered agent.
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 14,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "agent_info",
 *     "arguments": { "agent_id": "example-agent" }
 *   }
 * }
 *
 * JSON-RPC Response (success):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 14,
 *   "result": {
 *     "content": [{"type": "text", "text": "{\"agent_id\":\"example-agent\",\"name\":\"Example Agent\",...}"}],
 *     "isError": false
 *   }
 * }
 *
 * JSON-RPC Response (error — non-existent agent):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 14,
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

public class AgentInfo {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "agent_info",
            Map.of("agent_id", "example-agent")
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output (agent registered):
// CallToolResult[content=[TextContent[text={"agent_id":"example-agent","name":"Example Agent",...}]], isError=false]
//
// Expected output (agent not found):
// CallToolResult[content=[TextContent[text=Agent 'example-agent' not found]], isError=true]
