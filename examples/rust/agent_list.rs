// KubeMQ MCP Example: agent_list
//
// Demonstrates the agent_list tool using the rmcp crate.
// Lists all registered agents; pass "skill_tags" to filter.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 13,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_list",
//     "arguments": {}
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 13,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\"}]" }],
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

    let result = client.call_tool("agent_list", json!({})).await?;

    println!("Tool: agent_list");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: agent_list
// Result: [{"agent_id":"echo-01","name":"Echo Agent 01","skills":[{"id":"echo","name":"Echo","tags":["test","echo"]}]}]
