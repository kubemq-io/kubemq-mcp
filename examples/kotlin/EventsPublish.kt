// KubeMQ MCP Example: events_publish
//
// Demonstrates the events_publish tool using the MCP Kotlin SDK.
// Publishes an ephemeral event — lost if no subscriber is active.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "method": "tools/call",
//   "params": {
//     "name": "events_publish",
//     "arguments": {
//       "channel": "example-events",
//       "body": "Event data"
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "result": {
//     "content": [{"type": "text", "text": "Event published successfully to channel 'example-events'"}],
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

    val result = client.callTool("events_publish", mapOf(
        "channel" to "example-events",
        "body" to "Event data"
    ))

    println("Tool: events_publish")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output:
// Tool: events_publish
// Result: Event published successfully to channel 'example-events'
