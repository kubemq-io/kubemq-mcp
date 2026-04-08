// KubeMQ MCP Example: queue_peek
//
// Demonstrates the queue_peek tool using the official MCP C# SDK.
// Messages remain in the queue after peek (non-destructive read).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 4,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_peek",
//     "arguments": {
//       "channel": "example-queue",
//       "max_messages": 5
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 4,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"body\":\"Hello from C# MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\"}}]" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class QueuePeek
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("queue_peek", new Dictionary<string, object>
        {
            ["channel"] = "example-queue",
            ["max_messages"] = 5,
        });

        Console.WriteLine($"Tool: queue_peek");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: queue_peek
// Result: [{"body":"Hello from C# MCP","metadata":"example-metadata","tags":{"env":"dev"}}]
