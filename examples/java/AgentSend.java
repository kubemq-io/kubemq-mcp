/**
 * KubeMQ MCP Example: agent_send
 *
 * Demonstrates the agent_send tool using the official MCP Java SDK.
 * Sends a message to a registered agent (blocking by default).
 *
 * JSON-RPC Request:
 * {
 *   "jsonrpc": "2.0",
 *   "id": 15,
 *   "method": "tools/call",
 *   "params": {
 *     "name": "agent_send",
 *     "arguments": { "agent_id": "example-agent", "message": "hello from MCP" }
 *   }
 * }
 *
 * JSON-RPC Response (success):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 15,
 *   "result": {
 *     "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"message/send\",\"params\":{\"message\":\"hello from MCP\"}}}"}],
 *     "isError": false
 *   }
 * }
 *
 * JSON-RPC Response (error — non-existent agent):
 * {
 *   "jsonrpc": "2.0",
 *   "id": 15,
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

public class AgentSend {
    public static void main(String[] args) {
        String url = System.getenv().getOrDefault("KUBEMQ_MCP_URL", "http://localhost:9090");
        var transport = HttpClientStreamableHttpTransport.builder(url).endpoint("/mcp").build();
        var client = McpClient.sync(transport).build();
        client.initialize();

        var result = client.callTool(new CallToolRequest(
            "agent_send",
            Map.of(
                "agent_id", "example-agent",
                "message", "hello from MCP"
            )
        ));
        System.out.println(result);

        client.closeGracefully();
    }
}

// Expected output (agent registered):
// CallToolResult[content=[TextContent[text={"echo":{"method":"message/send",...}}]], isError=false]
//
// Expected output (agent not found):
// CallToolResult[content=[TextContent[text=Agent 'example-agent' not found]], isError=true]
