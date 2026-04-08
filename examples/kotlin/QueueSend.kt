// KubeMQ MCP Example: queue_send
//
// Demonstrates the queue_send tool using the MCP Kotlin SDK.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 2,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_send",
//     "arguments": {
//       "channel": "example-queue",
//       "body": "Hello from Kotlin MCP",
//       "metadata": "example-metadata",
//       "tags": {"env": "dev", "source": "mcp-example"}
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 2,
//   "result": {
//     "content": [{"type": "text", "text": "Message sent successfully to queue 'example-queue'"}],
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

    val result = client.callTool("queue_send", mapOf(
        "channel" to "example-queue",
        "body" to "Hello from Kotlin MCP",
        "metadata" to "example-metadata",
        "tags" to mapOf("env" to "dev", "source" to "mcp-example")
    ))

    println("Tool: queue_send")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output:
// Tool: queue_send
// Result: Message sent successfully to queue 'example-queue'
