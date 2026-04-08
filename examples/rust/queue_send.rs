// KubeMQ MCP Example: queue_send
//
// Demonstrates the queue_send tool using the rmcp crate.
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
//       "body": "Hello from Rust MCP",
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
//     "content": [{ "type": "text", "text": "Message sent successfully to queue 'example-queue'" }],
//     "isError": false
//   }
// }

use rmcp::transport::streamable_http::StreamableHttpClientTransport;
use rmcp::service::RunService;
use serde_json::json;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let url = std::env::var("KUBEMQ_MCP_URL")
        .unwrap_or_else(|_| "http://localhost:9090".to_string());

    let transport = StreamableHttpClientTransport::from_uri(format!("{url}/mcp"))?;
    let client = ().serve(transport).await?;

    let result = client.call_tool("queue_send", json!({
        "channel": "example-queue",
        "body": "Hello from Rust MCP",
        "metadata": "example-metadata",
        "tags": {"env": "dev", "source": "mcp-example"}
    })).await?;

    println!("Tool: queue_send");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: queue_send
// Result: Message sent successfully to queue 'example-queue'
