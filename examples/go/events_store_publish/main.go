// KubeMQ MCP Example: events_store_publish
//
// Demonstrates the events_store_publish tool using the mcp-go SDK.
// Publishes a persistent event with sequence number.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "method": "tools/call",
//   "params": {
//     "name": "events_store_publish",
//     "arguments": {
//       "channel": "example-events-store",
//       "body": "Stored event data",
//       "metadata": "store-meta",
//       "tags": {"source": "mcp-example"}
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 6,
//   "result": {
//     "content": [{ "type": "text", "text": "Event published successfully to events store channel 'example-events-store'" }],
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
			Name: "events_store_publish",
			Arguments: map[string]any{
				"channel":  "example-events-store",
				"body":     "Stored event data",
				"metadata": "store-meta",
				"tags":     map[string]any{"source": "mcp-example"},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: events_store_publish")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: events_store_publish
// Result: Event published successfully to events store channel 'example-events-store'
