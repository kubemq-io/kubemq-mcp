# KubeMQ MCP Example: events_store_read_latest
#
# Demonstrates the events_store_read_latest tool using the official MCP Ruby SDK.
# Returns the N most recent events from the store.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 8,
#   "method": "tools/call",
#   "params": {
#     "name": "events_store_read_latest",
#     "arguments": {
#       "channel": "example-events-store",
#       "count": 3
#     }
#   }
# }
#
# JSON-RPC Response:
# {
#   "jsonrpc": "2.0",
#   "id": 8,
#   "result": {
#     "content": [{"type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3},{\"body\":\"Stored event 2\",\"sequence\":2},{\"body\":\"Stored event 1\",\"sequence\":1}]"}],
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

result = client.call_tool("events_store_read_latest", {
  "channel" => "example-events-store",
  "count" => 3,
})

puts "Tool: events_store_read_latest"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: events_store_read_latest
# Result: [{"body":"Stored event 3","sequence":3},{"body":"Stored event 2","sequence":2},{"body":"Stored event 1","sequence":1}]
