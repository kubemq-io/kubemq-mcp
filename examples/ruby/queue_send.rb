# KubeMQ MCP Example: queue_send
#
# Demonstrates the queue_send tool using the official MCP Ruby SDK.
#
# JSON-RPC Request:
# {
#   "jsonrpc": "2.0",
#   "id": 2,
#   "method": "tools/call",
#   "params": {
#     "name": "queue_send",
#     "arguments": {
#       "channel": "example-queue",
#       "body": "Hello from Ruby MCP",
#       "metadata": "example-metadata",
#       "tags": {"env": "dev", "source": "mcp-example"}
#     }
#   }
# }
#
# JSON-RPC Response:
# {
#   "jsonrpc": "2.0",
#   "id": 2,
#   "result": {
#     "content": [{"type": "text", "text": "Message sent successfully to queue 'example-queue'"}],
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

result = client.call_tool("queue_send", {
  "channel" => "example-queue",
  "body" => "Hello from Ruby MCP",
  "metadata" => "example-metadata",
  "tags" => { "env" => "dev", "source" => "mcp-example" },
})

puts "Tool: queue_send"
puts "Result: #{result}"

client.close

# Expected output:
# Tool: queue_send
# Result: Message sent successfully to queue 'example-queue'
