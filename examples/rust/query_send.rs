// KubeMQ MCP Example: query_send
//
// Demonstrates the query_send tool using the rmcp crate.
// Sends a synchronous query — requires an active subscriber on the target channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "method": "tools/call",
//   "params": {
//     "name": "query_send",
//     "arguments": {
//       "channel": "example-queries",
//       "body": "get-data",
//       "timeout_seconds": 10,
//       "metadata": "qry-meta",
//       "tags": {"action": "lookup"}
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"data\":\"query response payload from subscriber\"}" }],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — no subscriber / timeout):
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "result": {
//     "content": [{ "type": "text", "text": "Query timed out: no subscriber on channel 'example-queries' within 10s" }],
//     "isError": true
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

    let result = client.call_tool("query_send", json!({
        "channel": "example-queries",
        "body": "get-data",
        "timeout_seconds": 10,
        "metadata": "qry-meta",
        "tags": {"action": "lookup"}
    })).await?;

    println!("Tool: query_send");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output (with active subscriber):
// Tool: query_send
// Result: {"data":"query response payload from subscriber"}
//
// Expected output (no subscriber):
// Tool: query_send
// Result: Query timed out: no subscriber on channel 'example-queries' within 10s
