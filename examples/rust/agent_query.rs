// KubeMQ MCP Example: agent_query
//
// Demonstrates the agent_query tool using the rmcp crate.
// Queries an agent using a specific method (e.g., tasks/get).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_query",
//     "arguments": { "agent_id": "example-agent", "method": "tasks/get" }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}}}" }],
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

    let result = client.call_tool("agent_query", json!({
        "agent_id": "example-agent",
        "method": "tasks/get"
    })).await?;

    println!("Tool: agent_query");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: agent_query
// Result: {"echo":{"method":"tasks/get","params":{}},"received_headers":{}}
