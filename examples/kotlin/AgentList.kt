// KubeMQ MCP Example: agent_list
//
// Demonstrates the agent_list tool using the MCP Kotlin SDK.
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

    val result = client.callTool("agent_list", emptyMap())

    println("Tool: agent_list")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output:
// Tool: agent_list
// Result: [{"agent_id":"echo-01","name":"Echo Agent 01","skills":[...]}]
