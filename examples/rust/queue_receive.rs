// KubeMQ MCP Example: queue_receive
//
// Demonstrates the queue_receive tool using the rmcp crate.
// Consumes messages from a queue (destructive read).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 3,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_receive",
//     "arguments": { "channel": "example-queue", "max_messages": 5 }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 3,
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

    let result = client.call_tool("queue_receive", json!({
        "channel": "example-queue",
        "max_messages": 5
    })).await?;

    println!("Tool: queue_receive");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: queue_receive
// Result: [{"body":"Hello from Rust MCP","metadata":"example-metadata","tags":{"env":"dev","source":"mcp-example"}}]
