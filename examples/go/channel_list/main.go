// KubeMQ MCP Example: channel_list
//
// Demonstrates the channel_list tool using the mcp-go SDK.
// Lists all channels; pass "type" or "pattern" to filter.
//
// JSON-RPC Request (no filter):
// {
//   "jsonrpc": "2.0",
//   "id": 11,
//   "method": "tools/call",
//   "params": {
//     "name": "channel_list",
//     "arguments": {}
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 11,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"name\":\"example-queue\",\"type\":\"queues\",\"is_active\":true}]" }],
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
			Name:      "channel_list",
			Arguments: map[string]any{},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: channel_list")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: channel_list
// Result: [{"name":"example-queue","type":"queues","is_active":true},{"name":"example-events","type":"events","is_active":true}]
