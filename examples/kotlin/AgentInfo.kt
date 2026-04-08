// KubeMQ MCP Example: agent_info
//
// Demonstrates the agent_info tool using the MCP Kotlin SDK.
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

import io.modelcontextprotocol.kotlin.sdk.Implementation
import io.modelcontextprotocol.kotlin.sdk.client.Client
import io.modelcontextprotocol.kotlin.sdk.client.StreamableHttpClientTransport
import io.ktor.client.*
import io.ktor.client.plugins.sse.*
import kotlinx.coroutines.runBlocking

fun main() = runBlocking {
    val url = System.getenv("KUBEMQ_MCP_URL") ?: "http://localhost:9090"

    val httpClient = HttpClient { install(SSE) }
    val transport = StreamableHttpClientTransport(client = httpClient, url = "$url/mcp")
    val client = Client(clientInfo = Implementation(name = "kubemq-mcp-kotlin-example", version = "1.0.0"))
    client.connect(transport)

    val result = client.callTool("agent_info", mapOf(
        "agent_id" to "example-agent"
    ))

    println("Tool: agent_info")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output (agent registered):
// Tool: agent_info
// Result: {"agent_id":"example-agent","name":"Example Agent","description":"...","version":"1.0.0",...}
//
// Expected output (agent not found):
// Tool: agent_info
// Result: Agent 'example-agent' not found
