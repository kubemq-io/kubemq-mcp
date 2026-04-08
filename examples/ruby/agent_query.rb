# KubeMQ MCP Example: agent_query
#
# Demonstrates the agent_query tool using the official MCP Ruby SDK.
# Queries a registered agent using a specified method.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 16,
#   "method": "tools/call",
#   "params": {
#     "name": "agent_query",
#     "arguments": {
#       "agent_id": "example-agent",
#       "method": "tasks/get"
#     }
#   }
# }
#
# JSON-RPC Response (success):
# {
#   "jsonrpc": "2.0",
#   "id": 16,
#   "result": {
#     "content": [{"type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}},\"received_headers\":{}}"}],
#     "isError": false
#   }
# }
#
# JSON-RPC Response (error — non-existent agent):
# {
#   "jsonrpc": "2.0",
#   "id": 16,
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

result = client.call_tool("agent_query", {
  "agent_id" => "example-agent",
  "method" => "tasks/get",
})

puts "Tool: agent_query"
puts "Result: #{result}"

client.close

# Expected output (agent registered):
# Tool: agent_query
# Result: {"echo":{"method":"tasks/get","params":{}},"received_headers":{}}
#
# Expected output (agent not found):
# Tool: agent_query
# Result: Agent 'example-agent' not found
