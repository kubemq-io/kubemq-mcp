// KubeMQ MCP Example: queue_peek
//
// Demonstrates the queue_peek tool using the MCP Swift SDK.
// Unlike queue_receive, peek does not consume messages — they remain in the queue.
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
//     "content": [{"type": "text", "text": "[{\"body\":\"Hello from Swift MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\"}}]"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct QueuePeek {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("queue_peek", arguments: [
            "channel": "example-queue",
            "max_messages": 5,
        ])

        print("Tool: queue_peek")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: queue_peek
// Result: [{"body":"Hello from Swift MCP","metadata":"example-metadata","tags":{"env":"dev"}}]
