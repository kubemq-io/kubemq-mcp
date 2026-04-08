// KubeMQ MCP Example: command_send
//
// Demonstrates the command_send tool using the MCP Swift SDK.
// Requires an active command subscriber on the target channel.
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
//       "timeout_seconds": 10
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "result": {
//     "content": [{"type": "text", "text": "Command executed successfully on channel 'example-commands'"}],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — no subscriber):
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "result": {
//     "content": [{"type": "text", "text": "Command timed out: no subscriber on channel 'example-commands' within 10s"}],
//     "isError": true
//   }
// }

import Foundation
import MCP

@main
struct CommandSend {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("command_send", arguments: [
            "channel": "example-commands",
            "body": "do-work",
            "timeout_seconds": 10,
        ])

        print("Tool: command_send")
        print("Result: \(result)")
    }
}

// Expected output (with subscriber):
// Tool: command_send
// Result: Command executed successfully on channel 'example-commands'
//
// Expected output (without subscriber):
// Tool: command_send
// Result: Command timed out: no subscriber on channel 'example-commands' within 10s
