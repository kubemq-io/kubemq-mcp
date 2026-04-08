# KubeMQ MCP Example: events_store_read
#
# Demonstrates the events_store_read tool using the official MCP Ruby SDK.
# Reads stored events starting from a sequence number.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 7,
#   "method": "tools/call",
#   "params": {
#     "name": "events_store_read",
#     "arguments": {
#       "channel": "example-events-store",
#       "from_sequence": 1,
#       "max_messages": 10
#     }
#   }
# }
#
# JSON-RPC Response:
# {
#   "jsonrpc": "2.0",
#   "id": 7,
#   "result": {
#     "content": [{"type": "text", "text": "[{\"body\":\"Stored event\",\"metadata\":\"\",\"sequence\":1,\"timestamp\":\"2026-04-06T12:00:00Z\"}]"}],
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

result = client.call_tool("events_store_read", {
  "channel" => "example-events-store",
  "from_sequence" => 1,
  "max_messages" => 10,
})

puts "Tool: events_store_read"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: events_store_read
# Result: [{"body":"Stored event","metadata":"","sequence":1,"timestamp":"..."}]
