# KubeMQ MCP Example: channel_list
#
# Demonstrates the channel_list tool using the official MCP Ruby SDK.
# Lists all channels; pass "type" or "pattern" to filter.
#
# JSON-RPC Request (no filter):
# {
#   "jsonrpc": "2.0",
#   "id": 11,
#   "method": "tools/call",
#   "params": {
#     "name": "channel_list",
#     "arguments": {}
#   }
# }
#
# JSON-RPC Response:
# {
#   "jsonrpc": "2.0",
#   "id": 11,
#   "result": {
#     "content": [{"type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true},{\"name\":\"example-events\",\"type\":\"events\",\"is_active\":true}]"}],
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

result = client.call_tool("channel_list", {})

puts "Tool: channel_list"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: channel_list
# Result: [{"name":"example-queue","type":"queues","is_active":true},...]
