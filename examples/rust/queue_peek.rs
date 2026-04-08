// KubeMQ MCP Example: queue_peek
//
// Demonstrates the queue_peek tool using the rmcp crate.
// Messages remain in the queue after peek (non-destructive read).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 4,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_peek",
//     "arguments": { "channel": "example-queue", "max_messages": 5 }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 4,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"body\":\"Hello from Rust MCP\"}]" }],
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

    let result = client.call_tool("queue_peek", json!({
        "channel": "example-queue",
        "max_messages": 5
    })).await?;

    println!("Tool: queue_peek");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: queue_peek
// Result: [{"body":"Hello from Rust MCP","metadata":"example-metadata","tags":{"env":"dev"}}]
