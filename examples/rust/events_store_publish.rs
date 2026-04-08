// KubeMQ MCP Example: events_store_publish
//
// Demonstrates the events_store_publish tool using the rmcp crate.
// Publishes a persistent event with sequence number.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_publish",
//     "arguments": {
//       "channel": "example-events-store",
//       "body": "Stored event data",
//       "metadata": "store-meta",
//       "tags": {"source": "mcp-example"}
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "result": {
//     "content": [{ "type": "text", "text": "Event published successfully to events store channel 'example-events-store'" }],
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

    let result = client.call_tool("events_store_publish", json!({
        "channel": "example-events-store",
        "body": "Stored event data",
        "metadata": "store-meta",
        "tags": {"source": "mcp-example"}
    })).await?;

    println!("Tool: events_store_publish");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: events_store_publish
// Result: Event published successfully to events store channel 'example-events-store'
