// KubeMQ MCP Example: queue_send
//
// Demonstrates the queue_send tool using the MCP Swift SDK.
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
//       "body": "Hello from Swift MCP",
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
//     "content": [{"type": "text", "text": "Message sent successfully to queue 'example-queue'"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct QueueSend {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("queue_send", arguments: [
            "channel": "example-queue",
            "body": "Hello from Swift MCP",
            "metadata": "example-metadata",
            "tags": ["env": "dev", "source": "mcp-example"],
        ])

        print("Tool: queue_send")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: queue_send
// Result: Message sent successfully to queue 'example-queue'
