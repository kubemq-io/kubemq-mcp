// KubeMQ MCP Example: agent_info
//
// Demonstrates the agent_info tool using the rmcp crate.
// Returns details for a specific agent.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_info",
//     "arguments": { "agent_id": "example-agent" }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"agent_id\":\"example-agent\",\"name\":\"Example Agent\"}" }],
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

    let result = client.call_tool("agent_info", json!({
        "agent_id": "example-agent"
    })).await?;

    println!("Tool: agent_info");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: agent_info
// Result: {"agent_id":"example-agent","name":"Example Agent","description":"example agent","version":"1.0.0"}
