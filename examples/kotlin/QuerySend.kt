// KubeMQ MCP Example: query_send
//
// Demonstrates the query_send tool using the MCP Kotlin SDK.
// Requires an active query subscriber on the target channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "method": "tools/call",
//   "params": {
//     "name": "query_send",
//     "arguments": {
//       "channel": "example-queries",
//       "body": "get-data",
//       "timeout_seconds": 10
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "result": {
//     "content": [{"type": "text", "text": "{\"data\":\"query response payload from subscriber\"}"}],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — no subscriber):
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "result": {
//     "content": [{"type": "text", "text": "Query timed out: no subscriber on channel 'example-queries' within 10s"}],
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

    val result = client.callTool("query_send", mapOf(
        "channel" to "example-queries",
        "body" to "get-data",
        "timeout_seconds" to 10
    ))

    println("Tool: query_send")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output (with subscriber):
// Tool: query_send
// Result: {"data":"query response payload from subscriber"}
//
// Expected output (without subscriber):
// Tool: query_send
// Result: Query timed out: no subscriber on channel 'example-queries' within 10s
