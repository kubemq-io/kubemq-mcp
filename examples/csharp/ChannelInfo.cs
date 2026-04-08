// KubeMQ MCP Example: channel_info
//
// Demonstrates the channel_info tool using the official MCP C# SDK.
// Returns metadata for a specific channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_info",
//     "arguments": {
//       "channel": "example-queue",
//       "type": "queues"
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true,\"incoming\":5,\"outgoing\":3}" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class ChannelInfo
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("channel_info", new Dictionary<string, object>
        {
            ["channel"] = "example-queue",
            ["type"] = "queues",
        });

        Console.WriteLine($"Tool: channel_info");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: channel_info
// Result: {"name":"example-queue","type":"queues","is_active":true,"incoming":5,"outgoing":3}
