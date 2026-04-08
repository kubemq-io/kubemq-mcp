// KubeMQ MCP Example: queue_send
//
// Demonstrates the queue_send tool using the mcp-go SDK.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 2,
//   "method": "tools/call",
//   "params": {
//     "name": "queue_send",
//     "arguments": {
//       "channel": "example-queue",
//       "body": "Hello from Go MCP",
//       "metadata": "example-metadata",
//       "tags": {"env": "dev", "source": "mcp-example"}
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 2,
//   "result": {
//     "content": [{ "type": "text", "text": "Message sent successfully to queue 'example-queue'" }],
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
			Name: "queue_send",
			Arguments: map[string]any{
				"channel":  "example-queue",
				"body":     "Hello from Go MCP",
				"metadata": "example-metadata",
				"tags":     map[string]any{"env": "dev", "source": "mcp-example"},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: queue_send")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: queue_send
// Result: Message sent successfully to queue 'example-queue'
