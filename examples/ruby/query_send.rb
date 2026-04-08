# KubeMQ MCP Example: query_send
#
# Demonstrates the query_send tool using the official MCP Ruby SDK.
# Requires an active query subscriber on the target channel.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 10,
#   "method": "tools/call",
#   "params": {
#     "name": "query_send",
#     "arguments": {
#       "channel": "example-queries",
#       "body": "get-data",
#       "timeout_seconds": 10
#     }
#   }
# }
#
# JSON-RPC Response (success):
# {
#   "jsonrpc": "2.0",
#   "id": 10,
#   "result": {
#     "content": [{"type": "text", "text": "{\"data\":\"query response payload from subscriber\"}"}],
#     "isError": false
#   }
# }
#
# JSON-RPC Response (error — no subscriber):
# {
#   "jsonrpc": "2.0",
#   "id": 10,
#   "result": {
#     "content": [{"type": "text", "text": "Query timed out: no subscriber on channel 'example-queries' within 10s"}],
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

result = client.call_tool("query_send", {
  "channel" => "example-queries",
  "body" => "get-data",
  "timeout_seconds" => 10,
})

puts "Tool: query_send"
puts "Result: #{result}"

client.close

# Expected output (with subscriber):
# Tool: query_send
# Result: {"data":"query response payload from subscriber"}
#
# Expected output (without subscriber):
# Tool: query_send
# Result: Query timed out: no subscriber on channel 'example-queries' within 10s
