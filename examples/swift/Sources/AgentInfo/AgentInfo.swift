// KubeMQ MCP Example: agent_info
//
// Demonstrates the agent_info tool using the MCP Swift SDK.
// Returns detailed information about a specific registered agent.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_info",
//     "arguments": {
//       "agent_id": "example-agent"
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "result": {
//     "content": [{"type": "text", "text": "{\"agent_id\":\"example-agent\",\"name\":\"Example Agent\",\"description\":\"...\",\"version\":\"1.0.0\",\"url\":\"http://localhost:18080/\",\"skills\":[...]}"}],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — non-existent agent):
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "result": {
//     "content": [{"type": "text", "text": "Agent 'example-agent' not found"}],
//     "isError": true
//   }
// }

import Foundation
import MCP

@main
struct AgentInfo {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("agent_info", arguments: [
            "agent_id": "example-agent",
        ])

        print("Tool: agent_info")
        print("Result: \(result)")
    }
}

// Expected output (agent registered):
// Tool: agent_info
// Result: {"agent_id":"example-agent","name":"Example Agent","description":"...","version":"1.0.0",...}
//
// Expected output (agent not found):
// Tool: agent_info
// Result: Agent 'example-agent' not found
