// KubeMQ MCP Example: events_store_read
//
// Demonstrates the events_store_read tool using the MCP Kotlin SDK.
// Reads stored events starting from a sequence number.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 7,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_read",
//     "arguments": {
//       "channel": "example-events-store",
//       "from_sequence": 1,
//       "max_messages": 10
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 7,
//   "result": {
//     "content": [{"type": "text", "text": "[{\"body\":\"Stored event\",\"metadata\":\"\",\"sequence\":1,\"timestamp\":\"2026-04-06T12:00:00Z\"}]"}],
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

    val result = client.callTool("events_store_read", mapOf(
        "channel" to "example-events-store",
        "from_sequence" to 1,
        "max_messages" to 10
    ))

    println("Tool: events_store_read")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output:
// Tool: events_store_read
// Result: [{"body":"Stored event","metadata":"","sequence":1,"timestamp":"..."}]
