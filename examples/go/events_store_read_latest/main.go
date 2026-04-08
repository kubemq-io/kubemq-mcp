// KubeMQ MCP Example: events_store_read_latest
//
// Demonstrates the events_store_read_latest tool using the mcp-go SDK.
// Returns the N most recent events from the store.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_read_latest",
//     "arguments": { "channel": "example-events-store", "count": 3 }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 8,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"body\":\"Stored event 3\",\"sequence\":3}]" }],
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
			Name: "events_store_read_latest",
			Arguments: map[string]any{
				"channel": "example-events-store",
				"count":   3,
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: events_store_read_latest")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: events_store_read_latest
// Result: [{"body":"Stored event 3","sequence":3},{"body":"Stored event 2","sequence":2},{"body":"Stored event 1","sequence":1}]
