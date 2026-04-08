// KubeMQ MCP Example: events_store_publish
//
// Demonstrates the events_store_publish tool using the official MCP C# SDK.
// Publishes a persistent event with sequence number.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_publish",
//     "arguments": {
//       "channel": "example-events-store",
//       "body": "Stored event data",
//       "metadata": "store-meta",
//       "tags": {"source": "mcp-example"}
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "result": {
//     "content": [{ "type": "text", "text": "Event published successfully to events store channel 'example-events-store'" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class EventsStorePublish
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("events_store_publish", new Dictionary<string, object>
        {
            ["channel"] = "example-events-store",
            ["body"] = "Stored event data",
            ["metadata"] = "store-meta",
            ["tags"] = new Dictionary<string, string> { ["source"] = "mcp-example" },
        });

        Console.WriteLine($"Tool: events_store_publish");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: events_store_publish
// Result: Event published successfully to events store channel 'example-events-store'
