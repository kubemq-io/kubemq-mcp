// KubeMQ MCP Example: command_send
//
// Demonstrates the command_send tool using the rmcp crate.
// Sends a synchronous command — requires an active subscriber on the target channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "method": "tools/call",
//   "params": {
//     "name": "command_send",
//     "arguments": {
//       "channel": "example-commands",
//       "body": "do-work",
//       "timeout_seconds": 10,
//       "metadata": "cmd-meta",
//       "tags": {"action": "process"}
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "result": {
//     "content": [{ "type": "text", "text": "Command executed successfully on channel 'example-commands'" }],
//     "isError": false
//   }
// }
//
// JSON-RPC Response (error — no subscriber / timeout):
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "result": {
//     "content": [{ "type": "text", "text": "Command timed out: no subscriber on channel 'example-commands' within 10s" }],
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

    let result = client.call_tool("command_send", json!({
        "channel": "example-commands",
        "body": "do-work",
        "timeout_seconds": 10,
        "metadata": "cmd-meta",
        "tags": {"action": "process"}
    })).await?;

    println!("Tool: command_send");
    println!("Result: {result:#?}");
    Ok(())
}

// Expected output (with active subscriber):
// Tool: command_send
// Result: Command executed successfully on channel 'example-commands'
//
// Expected output (no subscriber):
// Tool: command_send
// Result: Command timed out: no subscriber on channel 'example-commands' within 10s
