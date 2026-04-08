// KubeMQ MCP Example: agent_send
//
// Demonstrates the agent_send tool using the mcp-go SDK.
// Sends a message to a registered agent (blocking mode by default).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 15,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_send",
//     "arguments": { "agent_id": "example-agent", "message": "hello" }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 15,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"echo\":{\"method\":\"message/send\",\"params\":{\"message\":\"hello\"}}}" }],
//     "isError": false
//   }
// }
package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/mark3labs/mcp-go/client"
	"github.com/mark3labs/mcp-go/mcp"
)

func main() {
	url := os.Getenv("KUBEMQ_MCP_URL")
	if url == "" {
		url = "http://localhost:9090"
	}

	c, err := client.NewStreamableHttpClient(url + "/mcp")
	if err != nil {
		log.Fatal(err)
	}
	defer c.Close()

	ctx := context.Background()
	if err := c.Start(ctx); err != nil {
		log.Fatal(err)
	}

	result, err := c.CallTool(ctx, mcp.CallToolRequest{
		Params: mcp.CallToolParams{
			Name: "agent_send",
			Arguments: map[string]any{
				"agent_id": "example-agent",
				"message":  "hello",
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: agent_send")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: agent_send
// Result: {"echo":{"method":"message/send","params":{"message":"hello"}},"received_headers":{}}
