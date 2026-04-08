// KubeMQ MCP Example: agent_list
//
// Demonstrates the agent_list tool using the MCP Swift SDK.
// Lists all registered agents, or filtered by skill_tags.
//
// JSON-RPC Request (no filter):
// {
//   "jsonrpc": "2.0",
//   "id": 13,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_list",
//     "arguments": {}
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 13,
//   "result": {
//     "content": [{"type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\",\"skills\":[{\"id\":\"echo\",\"name\":\"Echo\",\"tags\":[\"test\",\"echo\"]}]}]"}],
//     "isError": false
//   }
// }

import Foundation
import MCP

@main
struct AgentList {
    static func main() async throws {
        let url = ProcessInfo.processInfo.environment["KUBEMQ_MCP_URL"] ?? "http://localhost:9090"

        let transport = HTTPClientTransport(endpoint: URL(string: "\(url)/mcp")!, streaming: true)
        let client = Client(name: "kubemq-mcp-swift-example", version: "1.0.0")
        try await client.connect(transport: transport)

        let result = try await client.callTool("agent_list", arguments: [:])

        print("Tool: agent_list")
        print("Result: \(result)")
    }
}

// Expected output:
// Tool: agent_list
// Result: [{"agent_id":"echo-01","name":"Echo Agent 01","skills":[...]}]
