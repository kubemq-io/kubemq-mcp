// KubeMQ MCP Example: agent_list
//
// Demonstrates the agent_list tool using the official MCP C# SDK.
// Lists all registered agents; pass "skill_tags" to filter.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 13,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_list",
//     "arguments": {}
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 13,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\",\"skills\":[{\"id\":\"echo\",\"name\":\"Echo\",\"tags\":[\"test\",\"echo\"]}]}]" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class AgentList
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("agent_list", new Dictionary<string, object>());

        Console.WriteLine($"Tool: agent_list");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: agent_list
// Result: [{"agent_id":"echo-01","name":"Echo Agent 01","skills":[{"id":"echo","name":"Echo","tags":["test","echo"]}]}]
