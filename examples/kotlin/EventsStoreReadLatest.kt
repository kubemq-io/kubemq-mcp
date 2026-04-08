// KubeMQ MCP Example: events_store_read_latest
//
// Demonstrates the events_store_read_latest tool using the MCP Kotlin SDK.
// Returns the N most recent events from the store.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_read_latest",
//     "arguments": {
//       "channel": "example-events-store",
//       "count": 3
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "result": {
//     "content": [{"type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3},{\"body\":\"Stored event 2\",\"sequence\":2},{\"body\":\"Stored event 1\",\"sequence\":1}]"}],
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

    val result = client.callTool("events_store_read_latest", mapOf(
        "channel" to "example-events-store",
        "count" to 3
    ))

    println("Tool: events_store_read_latest")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output:
// Tool: events_store_read_latest
// Result: [{"body":"Stored event 3","sequence":3},{"body":"Stored event 2","sequence":2},{"body":"Stored event 1","sequence":1}]
