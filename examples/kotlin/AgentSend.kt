// KubeMQ MCP Example: agent_send
//
// Demonstrates the agent_send tool using the MCP Kotlin SDK.
// Sends a message to a registered agent (blocking by default).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 15,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_send",
//     "arguments": {
//       "agent_id": "example-agent",
//       "message": "hello"
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 15,
//   "result": {
//     "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"message/send\",\"params\":{\"message\":\"hello\"}},\"received_headers\":{}}"}],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — non-existent agent):
// {
//   "jsonrpc": "2.0",
//   "id": 15,
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

    val result = client.callTool("agent_send", mapOf(
        "agent_id" to "example-agent",
        "message" to "hello"
    ))

    println("Tool: agent_send")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output (agent registered):
// Tool: agent_send
// Result: {"echo":{"method":"message/send","params":{"message":"hello"}},"received_headers":{}}
//
// Expected output (agent not found):
// Tool: agent_send
// Result: Agent 'example-agent' not found
