// KubeMQ MCP Example: agent_send
//
// Demonstrates the agent_send tool using the official MCP C# SDK.
// Sends a message to a registered agent (blocking mode by default).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 15,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_send",
//     "arguments": {
//       "agent_id": "example-agent",
//       "message": "hello"
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 15,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"echo\":{\"method\":\"message/send\",\"params\":{\"message\":\"hello\"}},\"received_headers\":{}}" }],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — non-existent agent):
// {
//   "jsonrpc": "2.0",
//   "id": 15,
//   "result": {
//     "content": [{ "type": "text", "text": "Agent 'example-agent' not found" }],
//     "isError": true
//   }
// }

using ModelContextProtocol.Client;

class AgentSend
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("agent_send", new Dictionary<string, object>
        {
            ["agent_id"] = "example-agent",
            ["message"] = "hello",
        });

        Console.WriteLine($"Tool: agent_send");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: agent_send
// Result: {"echo":{"method":"message/send","params":{"message":"hello"}},"received_headers":{}}
