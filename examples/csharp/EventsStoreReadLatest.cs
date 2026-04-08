// KubeMQ MCP Example: events_store_read_latest
//
// Demonstrates the events_store_read_latest tool using the official MCP C# SDK.
// Returns the N most recent events from the store.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_read_latest",
//     "arguments": {
//       "channel": "example-events-store",
//       "count": 3
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3},{\"body\":\"Stored event 2\",\"sequence\":2},{\"body\":\"Stored event 1\",\"sequence\":1}]" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class EventsStoreReadLatest
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("events_store_read_latest", new Dictionary<string, object>
        {
            ["channel"] = "example-events-store",
            ["count"] = 3,
        });

        Console.WriteLine($"Tool: events_store_read_latest");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: events_store_read_latest
// Result: [{"body":"Stored event 3","sequence":3},{"body":"Stored event 2","sequence":2},{"body":"Stored event 1","sequence":1}]
