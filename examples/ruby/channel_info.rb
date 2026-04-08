# KubeMQ MCP Example: channel_info
#
# Demonstrates the channel_info tool using the official MCP Ruby SDK.
# Returns metadata for a specific channel.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 12,
#   "method": "tools/call",
#   "params": {
#     "name": "channel_info",
#     "arguments": {
#       "channel": "example-queue",
#       "type": "queues"
#     }
#   }
# }
#
# JSON-RPC Response:
# {
#   "jsonrpc": "2.0",
#   "id": 12,
#   "result": {
#     "content": [{"type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true,\"incoming\":5,\"outgoing\":3}"}],
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

result = client.call_tool("channel_info", {
  "channel" => "example-queue",
  "type" => "queues",
})

puts "Tool: channel_info"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: channel_info
# Result: {"name":"example-queue","type":"queues","is_active":true,"incoming":5,"outgoing":3}
