// KubeMQ MCP Example: events_store_read
//
// Demonstrates the events_store_read tool using the MCP Swift SDK.
// Reads stored events starting from a sequence number.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 7,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_read",
//     "arguments": {
//       "channel": "example-events-store",
//       "from_sequence": 1,
//       "max_messages": 10
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 7,
//   "result": {
//     "content": [{"type": "text", "text": "[{\"body\":\"Stored event\",\"metadata\":\"\",\"sequence\":1,\"timestamp\":\"2026-04-06T12:00:00Z\"}]"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct EventsStoreRead {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("events_store_read", arguments: [
            "channel": "example-events-store",
            "from_sequence": 1,
            "max_messages": 10,
        ])

        print("Tool: events_store_read")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: events_store_read
// Result: [{"body":"Stored event","metadata":"","sequence":1,"timestamp":"..."}]
