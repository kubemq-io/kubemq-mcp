// KubeMQ MCP Example: events_publish
//
// Demonstrates the events_publish tool using the official MCP C# SDK.
// Publishes an ephemeral event (fire-and-forget).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "method": "tools/call",
//   "params": {
//     "name": "events_publish",
//     "arguments": {
//       "channel": "example-events",
//       "body": "Event data",
//       "metadata": "event-meta",
//       "tags": {"source": "mcp-example"}
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "result": {
//     "content": [{ "type": "text", "text": "Event published successfully to channel 'example-events'" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class EventsPublish
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("events_publish", new Dictionary<string, object>
        {
            ["channel"] = "example-events",
            ["body"] = "Event data",
            ["metadata"] = "event-meta",
            ["tags"] = new Dictionary<string, string> { ["source"] = "mcp-example" },
        });

        Console.WriteLine($"Tool: events_publish");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: events_publish
// Result: Event published successfully to channel 'example-events'
