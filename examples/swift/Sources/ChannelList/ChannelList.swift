// KubeMQ MCP Example: channel_list
//
// Demonstrates the channel_list tool using the MCP Swift SDK.
// Lists all channels; pass "type" or "pattern" to filter.
//
// JSON-RPC Request (no filter):
// {
//   "jsonrpc": "2.0",
//   "id": 11,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_list",
//     "arguments": {}
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 11,
//   "result": {
//     "content": [{"type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true},{\"name\":\"example-events\",\"type\":\"events\",\"is_active\":true}]"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct ChannelList {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("channel_list", arguments: [:])

        print("Tool: channel_list")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: channel_list
// Result: [{"name":"example-queue","type":"queues","is_active":true},...]
