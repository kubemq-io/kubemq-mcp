// KubeMQ MCP Example: channel_list
//
// Demonstrates the channel_list tool using the rmcp crate.
// Lists all channels; pass "type" or "pattern" to filter.
//
// JSON-RPC Request (no filter):
// {
//   "jsonrpc": "2.0",
//   "id": 11,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_list",
//     "arguments": {}
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 11,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true}]" }],
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

    let result = client.call_tool("channel_list", json!({})).await?;

    println!("Tool: channel_list");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: channel_list
// Result: [{"name":"example-queue","type":"queues","is_active":true},{"name":"example-events","type":"events","is_active":true}]
