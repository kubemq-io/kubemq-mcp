// KubeMQ MCP Example: events_publish
//
// Demonstrates the events_publish tool using the mcp-go SDK.
// Publishes an ephemeral event (fire-and-forget).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "method": "tools/call",
//   "params": {
//     "name": "events_publish",
//     "arguments": {
//       "channel": "example-events",
//       "body": "Event data",
//       "metadata": "event-meta",
//       "tags": {"source": "mcp-example"}
//     }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 5,
//   "result": {
//     "content": [{ "type": "text", "text": "Event published successfully to channel 'example-events'" }],
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
			Name: "events_publish",
			Arguments: map[string]any{
				"channel":  "example-events",
				"body":     "Event data",
				"metadata": "event-meta",
				"tags":     map[string]any{"source": "mcp-example"},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: events_publish")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: events_publish
// Result: Event published successfully to channel 'example-events'
