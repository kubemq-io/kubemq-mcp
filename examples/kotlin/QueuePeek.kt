// KubeMQ MCP Example: queue_peek
//
// Demonstrates the queue_peek tool using the MCP Kotlin SDK.
// Unlike queue_receive, peek does not consume messages — they remain in the queue.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 4,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_peek",
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
//   "id": 4,
//   "result": {
//     "content": [{"type": "text", "text": "[{\"body\":\"Hello from Kotlin MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\"}}]"}],
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

    val result = client.callTool("queue_peek", mapOf(
        "channel" to "example-queue",
        "max_messages" to 5
    ))

    println("Tool: queue_peek")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output:
// Tool: queue_peek
// Result: [{"body":"Hello from Kotlin MCP","metadata":"example-metadata","tags":{"env":"dev"}}]
