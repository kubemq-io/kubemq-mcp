// KubeMQ MCP Example: command_send
//
// Demonstrates the command_send tool using the MCP Kotlin SDK.
// Requires an active command subscriber on the target channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "method": "tools/call",
//   "params": {
//     "name": "command_send",
//     "arguments": {
//       "channel": "example-commands",
//       "body": "do-work",
//       "timeout_seconds": 10
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "result": {
//     "content": [{"type": "text", "text": "Command executed successfully on channel 'example-commands'"}],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — no subscriber):
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "result": {
//     "content": [{"type": "text", "text": "Command timed out: no subscriber on channel 'example-commands' within 10s"}],
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

    val result = client.callTool("command_send", mapOf(
        "channel" to "example-commands",
        "body" to "do-work",
        "timeout_seconds" to 10
    ))

    println("Tool: command_send")
    println("Result: $result")

    client.close()
    httpClient.close()
}

// Expected output (with subscriber):
// Tool: command_send
// Result: Command executed successfully on channel 'example-commands'
//
// Expected output (without subscriber):
// Tool: command_send
// Result: Command timed out: no subscriber on channel 'example-commands' within 10s
