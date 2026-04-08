// KubeMQ MCP Example: events_store_read
//
// Demonstrates the events_store_read tool using the mcp-go SDK.
// Reads stored events starting from a sequence number.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 7,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_read",
//     "arguments": {
//       "channel": "example-events-store",
//       "from_sequence": 1,
//       "max_messages": 10
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 7,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"body\":\"Stored event data\",\"sequence\":1}]" }],
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
			Name: "events_store_read",
			Arguments: map[string]any{
				"channel":       "example-events-store",
				"from_sequence": 1,
				"max_messages":  10,
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: events_store_read")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: events_store_read
// Result: [{"body":"Stored event data","metadata":"store-meta","sequence":1,"timestamp":"..."}]
