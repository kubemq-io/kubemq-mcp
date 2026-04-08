// KubeMQ MCP Example: events_publish
//
// Demonstrates the events_publish tool using the MCP Swift SDK.
// Publishes an ephemeral event — lost if no subscriber is active.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "method": "tools/call",
//   "params": {
//     "name": "events_publish",
//     "arguments": {
//       "channel": "example-events",
//       "body": "Event data"
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "result": {
//     "content": [{"type": "text", "text": "Event published successfully to channel 'example-events'"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct EventsPublish {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("events_publish", arguments: [
            "channel": "example-events",
            "body": "Event data",
        ])

        print("Tool: events_publish")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: events_publish
// Result: Event published successfully to channel 'example-events'
