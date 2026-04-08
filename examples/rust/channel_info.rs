// KubeMQ MCP Example: channel_info
//
// Demonstrates the channel_info tool using the rmcp crate.
// Returns metadata for a specific channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_info",
//     "arguments": { "channel": "example-queue", "type": "queues" }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true,\"incoming\":5,\"outgoing\":3}" }],
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

    let result = client.call_tool("channel_info", json!({
        "channel": "example-queue",
        "type": "queues"
    })).await?;

    println!("Tool: channel_info");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: channel_info
// Result: {"name":"example-queue","type":"queues","is_active":true,"incoming":5,"outgoing":3}
