// KubeMQ MCP Example: agent_query
//
// Demonstrates the agent_query tool using the MCP Swift SDK.
// Queries a registered agent using a specified method.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_query",
//     "arguments": {
//       "agent_id": "example-agent",
//       "method": "tasks/get"
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "result": {
//     "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}},\"received_headers\":{}}"}],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — non-existent agent):
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "result": {
//     "content": [{"type": "text", "text": "Agent 'example-agent' not found"}],
//     "isError": true
//   }
// }

import Foundation
import MCP

@main
struct AgentQuery {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("agent_query", arguments: [
            "agent_id": "example-agent",
            "method": "tasks/get",
        ])

        print("Tool: agent_query")
        print("Result: \(result)")
    }
}

// Expected output (agent registered):
// Tool: agent_query
// Result: {"echo":{"method":"tasks/get","params":{}},"received_headers":{}}
//
// Expected output (agent not found):
// Tool: agent_query
// Result: Agent 'example-agent' not found
