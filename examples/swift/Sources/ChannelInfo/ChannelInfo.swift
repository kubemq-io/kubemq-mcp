// KubeMQ MCP Example: channel_info
//
// Demonstrates the channel_info tool using the MCP Swift SDK.
// Returns metadata for a specific channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_info",
//     "arguments": {
//       "channel": "example-queue",
//       "type": "queues"
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "result": {
//     "content": [{"type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true,\"incoming\":5,\"outgoing\":3}"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct ChannelInfo {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("channel_info", arguments: [
            "channel": "example-queue",
            "type": "queues",
        ])

        print("Tool: channel_info")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: channel_info
// Result: {"name":"example-queue","type":"queues","is_active":true,"incoming":5,"outgoing":3}
