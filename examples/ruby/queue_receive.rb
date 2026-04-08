# KubeMQ MCP Example: queue_receive
#
# Demonstrates the queue_receive tool using the official MCP Ruby SDK.
# Messages are consumed (removed from queue).
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 3,
#   "method": "tools/call",
#   "params": {
#     "name": "queue_receive",
#     "arguments": {
#       "channel": "example-queue",
#       "max_messages": 5
#     }
#   }
# }
#
# JSON-RPC Response:
# {
#   "jsonrpc": "2.0",
#   "id": 3,
#   "result": {
#     "content": [{"type": "text", "text": "[{\"body\":\"Hello from Ruby MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\",\"source\":\"mcp-example\"}}]"}],
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

result = client.call_tool("queue_receive", {
  "channel" => "example-queue",
  "max_messages" => 5,
})

puts "Tool: queue_receive"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: queue_receive
# Result: [{"body":"Hello from Ruby MCP","metadata":"example-metadata","tags":{"env":"dev","source":"mcp-example"}}]
