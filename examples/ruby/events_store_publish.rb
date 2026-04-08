# KubeMQ MCP Example: events_store_publish
#
# Demonstrates the events_store_publish tool using the official MCP Ruby SDK.
# Publishes a persistent event that is stored and replayable.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 6,
#   "method": "tools/call",
#   "params": {
#     "name": "events_store_publish",
#     "arguments": {
#       "channel": "example-events-store",
#       "body": "Stored event"
#     }
#   }
# }
#
# JSON-RPC Response:
# {
#   "jsonrpc": "2.0",
#   "id": 6,
#   "result": {
#     "content": [{"type": "text", "text": "Event published successfully to events store channel 'example-events-store'"}],
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

result = client.call_tool("events_store_publish", {
  "channel" => "example-events-store",
  "body" => "Stored event",
})

puts "Tool: events_store_publish"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: events_store_publish
# Result: Event published successfully to events store channel 'example-events-store'
