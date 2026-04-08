// KubeMQ MCP Example: events_store_publish
//
// Demonstrates the events_store_publish tool using the MCP Swift SDK.
// Publishes a persistent event that is stored and replayable.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_publish",
//     "arguments": {
//       "channel": "example-events-store",
//       "body": "Stored event"
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "result": {
//     "content": [{"type": "text", "text": "Event published successfully to events store channel 'example-events-store'"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct EventsStorePublish {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("events_store_publish", arguments: [
            "channel": "example-events-store",
            "body": "Stored event",
        ])

        print("Tool: events_store_publish")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: events_store_publish
// Result: Event published successfully to events store channel 'example-events-store'
