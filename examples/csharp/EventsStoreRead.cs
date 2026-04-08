// KubeMQ MCP Example: events_store_read
//
// Demonstrates the events_store_read tool using the official MCP C# SDK.
// Reads stored events starting from a sequence number.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 7,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_read",
//     "arguments": {
//       "channel": "example-events-store",
//       "from_sequence": 1,
//       "max_messages": 10
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 7,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"body\":\"Stored event data\",\"metadata\":\"store-meta\",\"sequence\":1,\"timestamp\":\"2026-04-06T12:00:00Z\"}]" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class EventsStoreRead
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("events_store_read", new Dictionary<string, object>
        {
            ["channel"] = "example-events-store",
            ["from_sequence"] = 1,
            ["max_messages"] = 10,
        });

        Console.WriteLine($"Tool: events_store_read");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: events_store_read
// Result: [{"body":"Stored event data","metadata":"store-meta","sequence":1,"timestamp":"..."}]
