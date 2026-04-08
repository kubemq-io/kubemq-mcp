// KubeMQ MCP Example: channel_list
//
// Demonstrates the channel_list tool using the official MCP C# SDK.
// Lists all channels; pass "type" or "pattern" to filter.
//
// JSON-RPC Request (no filter):
// {
//   "jsonrpc": "2.0",
//   "id": 11,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_list",
//     "arguments": {}
//   }
// }
//
// JSON-RPC Request (filtered by type):
// {
//   "jsonrpc": "2.0",
//   "id": 11,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_list",
//     "arguments": { "type": "queues" }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 11,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true},{\"name\":\"example-events\",\"type\":\"events\",\"is_active\":true}]" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class ChannelList
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("channel_list", new Dictionary<string, object>());

        Console.WriteLine($"Tool: channel_list");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: channel_list
// Result: [{"name":"example-queue","type":"queues","is_active":true},{"name":"example-events","type":"events","is_active":true}]
