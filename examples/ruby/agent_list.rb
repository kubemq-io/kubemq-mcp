# KubeMQ MCP Example: agent_list
#
# Demonstrates the agent_list tool using the official MCP Ruby SDK.
# Lists all registered agents, or filtered by skill_tags.
#
# JSON-RPC Request (no filter):
# {
#   "jsonrpc": "2.0",
#   "id": 13,
#   "method": "tools/call",
#   "params": {
#     "name": "agent_list",
#     "arguments": {}
#   }
# }
#
# JSON-RPC Response:
# {
#   "jsonrpc": "2.0",
#   "id": 13,
#   "result": {
#     "content": [{"type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\",\"skills\":[{\"id\":\"echo\",\"name\":\"Echo\",\"tags\":[\"test\",\"echo\"]}]}]"}],
#     "isError": false
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

result = client.call_tool("agent_list", {})

puts "Tool: agent_list"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: agent_list
# Result: [{"agent_id":"echo-01","name":"Echo Agent 01","skills":[...]}]
