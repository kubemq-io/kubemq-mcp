// KubeMQ MCP Example: agent_query
//
// Demonstrates the agent_query tool using the official MCP C# SDK.
// Queries an agent using a specific method (e.g., tasks/get).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_query",
//     "arguments": {
//       "agent_id": "example-agent",
//       "method": "tasks/get"
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}},\"received_headers\":{}}" }],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — non-existent agent):
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "result": {
//     "content": [{ "type": "text", "text": "Agent 'example-agent' not found" }],
//     "isError": true
//   }
// }

using ModelContextProtocol.Client;

class AgentQuery
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("agent_query", new Dictionary<string, object>
        {
            ["agent_id"] = "example-agent",
            ["method"] = "tasks/get",
        });

        Console.WriteLine($"Tool: agent_query");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: agent_query
// Result: {"echo":{"method":"tasks/get","params":{}},"received_headers":{}}
