// KubeMQ MCP Example: query_send
//
// Demonstrates the query_send tool using the official MCP C# SDK.
// Sends a synchronous query — requires an active subscriber on the target channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "method": "tools/call",
//   "params": {
//     "name": "query_send",
//     "arguments": {
//       "channel": "example-queries",
//       "body": "get-data",
//       "timeout_seconds": 10,
//       "metadata": "qry-meta",
//       "tags": {"action": "lookup"}
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"data\":\"query response payload from subscriber\"}" }],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — no subscriber / timeout):
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "result": {
//     "content": [{ "type": "text", "text": "Query timed out: no subscriber on channel 'example-queries' within 10s" }],
//     "isError": true
//   }
// }

using ModelContextProtocol.Client;

class QuerySend
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("query_send", new Dictionary<string, object>
        {
            ["channel"] = "example-queries",
            ["body"] = "get-data",
            ["timeout_seconds"] = 10,
            ["metadata"] = "qry-meta",
            ["tags"] = new Dictionary<string, string> { ["action"] = "lookup" },
        });

        Console.WriteLine($"Tool: query_send");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output (with active subscriber):
// Tool: query_send
// Result: {"data":"query response payload from subscriber"}
//
// Expected output (no subscriber):
// Tool: query_send
// Result: Query timed out: no subscriber on channel 'example-queries' within 10s
