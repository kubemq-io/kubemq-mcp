// KubeMQ MCP Example: channel_info
//
// Demonstrates the channel_info tool using the MCP Kotlin SDK.
// Returns metadata for a specific channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_info",
//     "arguments": {
//       "channel": "example-queue",
//       "type": "queues"
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "result": {
//     "content": [{"type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true,\"incoming\":5,\"outgoing\":3}"}],
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

    val result = client.callTool("channel_info", mapOf(
        "channel" to "example-queue",
        "type" to "queues"
    ))

    println("Tool: channel_info")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output:
// Tool: channel_info
// Result: {"name":"example-queue","type":"queues","is_active":true,"incoming":5,"outgoing":3}
