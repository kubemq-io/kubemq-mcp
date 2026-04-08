// KubeMQ MCP Example: events_store_read_latest
//
// Demonstrates the events_store_read_latest tool using the MCP Swift SDK.
// Returns the N most recent events from the store.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_read_latest",
//     "arguments": {
//       "channel": "example-events-store",
//       "count": 3
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "result": {
//     "content": [{"type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3},{\"body\":\"Stored event 2\",\"sequence\":2},{\"body\":\"Stored event 1\",\"sequence\":1}]"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct EventsStoreReadLatest {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("events_store_read_latest", arguments: [
            "channel": "example-events-store",
            "count": 3,
        ])

        print("Tool: events_store_read_latest")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: events_store_read_latest
// Result: [{"body":"Stored event 3","sequence":3},{"body":"Stored event 2","sequence":2},{"body":"Stored event 1","sequence":1}]
