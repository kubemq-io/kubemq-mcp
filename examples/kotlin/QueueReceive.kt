// KubeMQ MCP Example: queue_receive
//
// Demonstrates the queue_receive tool using the MCP Kotlin SDK.
// Messages are consumed (removed from queue).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 3,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_receive",
//     "arguments": {
//       "channel": "example-queue",
//       "max_messages": 5
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 3,
//   "result": {
//     "content": [{"type": "text", "text": "[{\"body\":\"Hello from Kotlin MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\",\"source\":\"mcp-example\"}}]"}],
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

    val result = client.callTool("queue_receive", mapOf(
        "channel" to "example-queue",
        "max_messages" to 5
    ))

    println("Tool: queue_receive")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output:
// Tool: queue_receive
// Result: [{"body":"Hello from Kotlin MCP","metadata":"example-metadata","tags":{"env":"dev","source":"mcp-example"}}]
