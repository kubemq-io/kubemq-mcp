# KubeMQ MCP Example: queue_peek
#
# Demonstrates the queue_peek tool using the official MCP Ruby SDK.
# Unlike queue_receive, peek does not consume messages — they remain in the queue.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 4,
#   "method": "tools/call",
#   "params": {
#     "name": "queue_peek",
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
#   "id": 4,
#   "result": {
#     "content": [{"type": "text", "text": "[{\"body\":\"Hello from Ruby MCP\",\"metadata\":\"example-metadata\",\"tags\":{\"env\":\"dev\"}}]"}],
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

result = client.call_tool("queue_peek", {
  "channel" => "example-queue",
  "max_messages" => 5,
})

puts "Tool: queue_peek"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: queue_peek
# Result: [{"body":"Hello from Ruby MCP","metadata":"example-metadata","tags":{"env":"dev"}}]
