// KubeMQ MCP Example: queue_receive
//
// Demonstrates the queue_receive tool using the official MCP C# SDK.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 3,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_receive",
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
//   "id": 3,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"body\":\"Hello from C# MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\",\"source\":\"mcp-example\"}}]" }],
//     "isError": false
//   }
// }

using ModelContextProtocol.Client;

class QueueReceive
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("queue_receive", new Dictionary<string, object>
        {
            ["channel"] = "example-queue",
            ["max_messages"] = 5,
        });

        Console.WriteLine($"Tool: queue_receive");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output:
// Tool: queue_receive
// Result: [{"body":"Hello from C# MCP","metadata":"example-metadata","tags":{"env":"dev","source":"mcp-example"}}]
