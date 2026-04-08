// KubeMQ MCP Example: agent_info
//
// Demonstrates the agent_info tool using the official MCP C# SDK.
// Returns details for a specific agent.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_info",
//     "arguments": {
//       "agent_id": "example-agent"
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"agent_id\":\"example-agent\",\"name\":\"Example Agent\",\"description\":\"example agent\",\"version\":\"1.0.0\"}" }],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — non-existent agent):
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "result": {
//     "content": [{ "type": "text", "text": "Agent 'example-agent' not found" }],
//     "isError": true
//   }
// }

using ModelContextProtocol.Client;

class AgentInfo
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("agent_info", new Dictionary<string, object>
        {
            ["agent_id"] = "example-agent",
        });

        Console.WriteLine($"Tool: agent_info");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: agent_info
// Result: {"agent_id":"example-agent","name":"Example Agent","description":"example agent","version":"1.0.0"}
