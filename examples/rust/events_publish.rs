// KubeMQ MCP Example: events_publish
//
// Demonstrates the events_publish tool using the rmcp crate.
// Publishes an ephemeral event (fire-and-forget).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "method": "tools/call",
//   "params": {
//     "name": "events_publish",
//     "arguments": {
//       "channel": "example-events",
//       "body": "Event data",
//       "metadata": "event-meta",
//       "tags": {"source": "mcp-example"}
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "result": {
//     "content": [{ "type": "text", "text": "Event published successfully to channel 'example-events'" }],
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

    let result = client.call_tool("events_publish", json!({
        "channel": "example-events",
        "body": "Event data",
        "metadata": "event-meta",
        "tags": {"source": "mcp-example"}
    })).await?;

    println!("Tool: events_publish");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: events_publish
// Result: Event published successfully to channel 'example-events'
