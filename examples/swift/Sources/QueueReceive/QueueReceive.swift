// KubeMQ MCP Example: queue_receive
//
// Demonstrates the queue_receive tool using the MCP Swift SDK.
// Messages are consumed (removed from queue).
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
//     "content": [{"type": "text", "text": "[{\"body\":\"Hello from Swift MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\",\"source\":\"mcp-example\"}}]"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct QueueReceive {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("queue_receive", arguments: [
            "channel": "example-queue",
            "max_messages": 5,
        ])

        print("Tool: queue_receive")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: queue_receive
// Result: [{"body":"Hello from Swift MCP","metadata":"example-metadata","tags":{"env":"dev","source":"mcp-example"}}]
