// KubeMQ MCP Example: queue_send
//
// Demonstrates the queue_send tool using the official MCP C# SDK.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 2,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_send",
//     "arguments": {
//       "channel": "example-queue",
//       "body": "Hello from C# MCP",
//       "metadata": "example-metadata",
//       "tags": {"env": "dev", "source": "mcp-example"}
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 2,
//   "result": {
//     "content": [{ "type": "text", "text": "Message sent successfully to queue 'example-queue'" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class QueueSend
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("queue_send", new Dictionary<string, object>
        {
            ["channel"] = "example-queue",
            ["body"] = "Hello from C# MCP",
            ["metadata"] = "example-metadata",
            ["tags"] = new Dictionary<string, string> { ["env"] = "dev", ["source"] = "mcp-example" },
        });

        Console.WriteLine($"Tool: queue_send");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: queue_send
// Result: Message sent successfully to queue 'example-queue'
