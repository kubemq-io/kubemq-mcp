// KubeMQ MCP Example: events_store_publish
//
// Demonstrates the events_store_publish tool using the MCP Kotlin SDK.
// Publishes a persistent event that is stored and replayable.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_publish",
//     "arguments": {
//       "channel": "example-events-store",
//       "body": "Stored event"
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "result": {
//     "content": [{"type": "text", "text": "Event published successfully to events store channel 'example-events-store'"}],
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

    val result = client.callTool("events_store_publish", mapOf(
        "channel" to "example-events-store",
        "body" to "Stored event"
    ))

    println("Tool: events_store_publish")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output:
// Tool: events_store_publish
// Result: Event published successfully to events store channel 'example-events-store'
