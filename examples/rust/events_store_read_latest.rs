// KubeMQ MCP Example: events_store_read_latest
//
// Demonstrates the events_store_read_latest tool using the rmcp crate.
// Returns the N most recent events from the store.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_read_latest",
//     "arguments": { "channel": "example-events-store", "count": 3 }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3}]" }],
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

    let result = client.call_tool("events_store_read_latest", json!({
        "channel": "example-events-store",
        "count": 3
    })).await?;

    println!("Tool: events_store_read_latest");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: events_store_read_latest
// Result: [{"body":"Stored event 3","sequence":3},{"body":"Stored event 2","sequence":2},{"body":"Stored event 1","sequence":1}]
