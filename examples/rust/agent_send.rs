// KubeMQ MCP Example: agent_send
//
// Demonstrates the agent_send tool using the rmcp crate.
// Sends a message to a registered agent (blocking mode by default).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 15,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_send",
//     "arguments": { "agent_id": "example-agent", "message": "hello from MCP" }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 15,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"echo\":{\"method\":\"message/send\",\"params\":{\"message\":\"hello\"}}}" }],
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

    let result = client.call_tool("agent_send", json!({
        "agent_id": "example-agent",
        "message": "hello from MCP"
    })).await?;

    println!("Tool: agent_send");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output:
// Tool: agent_send
// Result: {"echo":{"method":"message/send","params":{"message":"hello from MCP"}},"received_headers":{}}
