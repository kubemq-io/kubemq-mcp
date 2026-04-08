// KubeMQ MCP Example: agent_query
//
// Demonstrates the agent_query tool using the MCP Kotlin SDK.
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

    val result = client.callTool("agent_query", mapOf(
        "agent_id" to "example-agent",
        "method" to "tasks/get"
    ))

    println("Tool: agent_query")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output (agent registered):
// Tool: agent_query
// Result: {"echo":{"method":"tasks/get","params":{}},"received_headers":{}}
//
// Expected output (agent not found):
// Tool: agent_query
// Result: Agent 'example-agent' not found
