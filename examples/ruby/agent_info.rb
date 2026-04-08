# KubeMQ MCP Example: agent_info
#
# Demonstrates the agent_info tool using the official MCP Ruby SDK.
# Returns detailed information about a specific registered agent.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 14,
#   "method": "tools/call",
#   "params": {
#     "name": "agent_info",
#     "arguments": {
#       "agent_id": "example-agent"
#     }
#   }
# }
#
# JSON-RPC Response (success):
# {
#   "jsonrpc": "2.0",
#   "id": 14,
#   "result": {
#     "content": [{"type": "text", "text": "{\"agent_id\":\"example-agent\",\"name\":\"Example Agent\",\"description\":\"...\",\"version\":\"1.0.0\",\"url\":\"http://localhost:18080/\",\"skills\":[...]}"}],
#     "isError": false
#   }
# }
#
# JSON-RPC Response (error — non-existent agent):
# {
#   "jsonrpc": "2.0",
#   "id": 14,
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

result = client.call_tool("agent_info", {
  "agent_id" => "example-agent",
})

puts "Tool: agent_info"
puts "Result: #{result}"

client.close

# Expected output (agent registered):
# Tool: agent_info
# Result: {"agent_id":"example-agent","name":"Example Agent","description":"...","version":"1.0.0",...}
#
# Expected output (agent not found):
# Tool: agent_info
# Result: Agent 'example-agent' not found
