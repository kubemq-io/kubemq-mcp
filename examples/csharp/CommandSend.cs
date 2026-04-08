// KubeMQ MCP Example: command_send
//
// Demonstrates the command_send tool using the official MCP C# SDK.
// Sends a synchronous command — requires an active subscriber on the target channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "method": "tools/call",
//   "params": {
//     "name": "command_send",
//     "arguments": {
//       "channel": "example-commands",
//       "body": "do-work",
//       "timeout_seconds": 10,
//       "metadata": "cmd-meta",
//       "tags": {"action": "process"}
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "result": {
//     "content": [{ "type": "text", "text": "Command executed successfully on channel 'example-commands'" }],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — no subscriber / timeout):
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "result": {
//     "content": [{ "type": "text", "text": "Command timed out: no subscriber on channel 'example-commands' within 10s" }],
//     "isError": true
//   }
// }

using ModelContextProtocol.Client;

class CommandSend
{
    static async Task Main(string[] args)
    {
        var url = Environment.GetEnvironmentVariable("KUBEMQ_MCP_URL") ?? "http://localhost:9090";
        var transport = new HttpClientTransport(new HttpClientTransportOptions { Endpoint = new Uri($"{url}/mcp") });
        await using var client = await McpClientFactory.CreateAsync(transport);

        var result = await client.CallToolAsync("command_send", new Dictionary<string, object>
        {
            ["channel"] = "example-commands",
            ["body"] = "do-work",
            ["timeout_seconds"] = 10,
            ["metadata"] = "cmd-meta",
            ["tags"] = new Dictionary<string, string> { ["action"] = "process" },
        });

        Console.WriteLine($"Tool: command_send");
        Console.WriteLine($"Result: {result}");
    }
}

// Expected output (with active subscriber):
// Tool: command_send
// Result: Command executed successfully on channel 'example-commands'
//
// Expected output (no subscriber):
// Tool: command_send
// Result: Command timed out: no subscriber on channel 'example-commands' within 10s
