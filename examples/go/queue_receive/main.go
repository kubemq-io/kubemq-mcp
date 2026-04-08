// KubeMQ MCP Example: queue_receive
//
// Demonstrates the queue_receive tool using the mcp-go SDK.
// Consumes messages from a queue (destructive read).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 3,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_receive",
//     "arguments": { "channel": "example-queue", "max_messages": 5 }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 3,
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
			Name: "queue_receive",
			Arguments: map[string]any{
				"channel":      "example-queue",
				"max_messages": 5,
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: queue_receive")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: queue_receive
// Result: [{"body":"Hello from Go MCP","metadata":"example-metadata","tags":{"env":"dev","source":"mcp-example"}}]
