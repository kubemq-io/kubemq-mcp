// KubeMQ MCP Example: channel_info
//
// Demonstrates the channel_info tool using the mcp-go SDK.
// Returns metadata for a specific channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_info",
//     "arguments": { "channel": "example-queue", "type": "queues" }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 12,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true,\"incoming\":5,\"outgoing\":3}" }],
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
			Name: "channel_info",
			Arguments: map[string]any{
				"channel": "example-queue",
				"type":    "queues",
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: channel_info")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: channel_info
// Result: {"name":"example-queue","type":"queues","is_active":true,"incoming":5,"outgoing":3}
