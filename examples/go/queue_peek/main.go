// KubeMQ MCP Example: queue_peek
//
// Demonstrates the queue_peek tool using the mcp-go SDK.
// Messages remain in the queue after peek (non-destructive read).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 4,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_peek",
//     "arguments": { "channel": "example-queue", "max_messages": 5 }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 4,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"body\":\"Hello from Go MCP\"}]" }],
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
			Name: "queue_peek",
			Arguments: map[string]any{
				"channel":      "example-queue",
				"max_messages": 5,
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: queue_peek")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: queue_peek
// Result: [{"body":"Hello from Go MCP","metadata":"example-metadata","tags":{"env":"dev"}}]
