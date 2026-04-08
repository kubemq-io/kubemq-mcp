// KubeMQ MCP Example: events_store_read
//
// Demonstrates the events_store_read tool using the rmcp crate.
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
//     "content": [{ "type": "text", "text": "[{\"body\":\"Stored event data\",\"sequence\":1}]" }],
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

    let result = client.call_tool("events_store_read", json!({
        "channel": "example-events-store",
        "from_sequence": 1,
        "max_messages": 10
    })).await?;

    println!("Tool: events_store_read");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: events_store_read
// Result: [{"body":"Stored event data","metadata":"store-meta","sequence":1,"timestamp":"..."}]
