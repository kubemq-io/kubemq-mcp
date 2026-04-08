# KubeMQ MCP Example: command_send
#
# Demonstrates the command_send tool using the official MCP Ruby SDK.
# Requires an active command subscriber on the target channel.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 9,
#   "method": "tools/call",
#   "params": {
#     "name": "command_send",
#     "arguments": {
#       "channel": "example-commands",
#       "body": "do-work",
#       "timeout_seconds": 10
#     }
#   }
# }
#
# JSON-RPC Response (success):
# {
#   "jsonrpc": "2.0",
#   "id": 9,
#   "result": {
#     "content": [{"type": "text", "text": "Command executed successfully on channel 'example-commands'"}],
#     "isError": false
#   }
# }
#
# JSON-RPC Response (error — no subscriber):
# {
#   "jsonrpc": "2.0",
#   "id": 9,
#   "result": {
#     "content": [{"type": "text", "text": "Command timed out: no subscriber on channel 'example-commands' within 10s"}],
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

result = client.call_tool("command_send", {
  "channel" => "example-commands",
  "body" => "do-work",
  "timeout_seconds" => 10,
})

puts "Tool: command_send"
puts "Result: #{result}"

client.close

# Expected output (with subscriber):
# Tool: command_send
# Result: Command executed successfully on channel 'example-commands'
#
# Expected output (without subscriber):
# Tool: command_send
# Result: Command timed out: no subscriber on channel 'example-commands' within 10s
