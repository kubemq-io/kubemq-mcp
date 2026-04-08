// KubeMQ MCP Example: query_send
//
// Demonstrates the query_send tool using the MCP Swift SDK.
// Requires an active query subscriber on the target channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "method": "tools/call",
//   "params": {
//     "name": "query_send",
//     "arguments": {
//       "channel": "example-queries",
//       "body": "get-data",
//       "timeout_seconds": 10
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "result": {
//     "content": [{"type": "text", "text": "{\"data\":\"query response payload from subscriber\"}"}],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — no subscriber):
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "result": {
//     "content": [{"type": "text", "text": "Query timed out: no subscriber on channel 'example-queries' within 10s"}],
//     "isError": true
//   }
// }

import Foundation
import MCP

@main
struct QuerySend {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("query_send", arguments: [
            "channel": "example-queries",
            "body": "get-data",
            "timeout_seconds": 10,
        ])

        print("Tool: query_send")
        print("Result: \(result)")
    }
}

// Expected output (with subscriber):
// Tool: query_send
// Result: {"data":"query response payload from subscriber"}
//
// Expected output (without subscriber):
// Tool: query_send
// Result: Query timed out: no subscriber on channel 'example-queries' within 10s
