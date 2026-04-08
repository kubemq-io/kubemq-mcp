# KubeMQ MCP Example: events_publish
#
# Demonstrates the events_publish tool using the official MCP Ruby SDK.
# Publishes an ephemeral event — lost if no subscriber is active.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 5,
#   "method": "tools/call",
#   "params": {
#     "name": "events_publish",
#     "arguments": {
#       "channel": "example-events",
#       "body": "Event data"
#     }
#   }
# }
#
# JSON-RPC Response:
# {
#   "jsonrpc": "2.0",
#   "id": 5,
#   "result": {
#     "content": [{"type": "text", "text": "Event published successfully to channel 'example-events'"}],
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

result = client.call_tool("events_publish", {
  "channel" => "example-events",
  "body" => "Event data",
})

puts "Tool: events_publish"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: events_publish
# Result: Event published successfully to channel 'example-events'
