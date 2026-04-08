# KubeMQ MCP Example: agent_send
#
# Demonstrates the agent_send tool using the official MCP Ruby SDK.
# Sends a message to a registered agent (blocking by default).
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 15,
#   "method": "tools/call",
#   "params": {
#     "name": "agent_send",
#     "arguments": {
#       "agent_id": "example-agent",
#       "message": "hello from MCP"
#     }
#   }
# }
#
# JSON-RPC Response (success):
# {
#   "jsonrpc": "2.0",
#   "id": 15,
#   "result": {
#     "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"message/send\",\"params\":{\"message\":\"hello\"}},\"received_headers\":{}}"}],
#     "isError": false
#   }
# }
#
# JSON-RPC Response (error — non-existent agent):
# {
#   "jsonrpc": "2.0",
#   "id": 15,
#   "result": {
#     "content": [{"type": "text", "text": "Agent 'example-agent' not found"}],
#     "isError": true
#   }
# }

require "mcp"

url = ENV.fetch("KUBEMQ_MCP_URL", "http://localhost:9090")

client = MCP::Client.new(
  transport: MCP::Transport::StreamableHTTP.new("#{url}/mcp"),
  name: "kubemq-mcp-ruby-example",
  version: "1.0.0"
)
client.initialize_handshake

result = client.call_tool("agent_send", {
  "agent_id" => "example-agent",
  "message" => "hello from MCP",
})

puts "Tool: agent_send"
puts "Result: #{result}"

client.close

# Expected output (agent registered):
# Tool: agent_send
# Result: {"echo":{"method":"message/send","params":{"message":"hello from MCP"}},"received_headers":{}}
#
# Expected output (agent not found):
# Tool: agent_send
# Result: Agent 'example-agent' not found
