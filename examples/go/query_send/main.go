// KubeMQ MCP Example: query_send
//
// Demonstrates the query_send tool using the mcp-go SDK.
// Sends a synchronous query — requires an active subscriber on the target channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "method": "tools/call",
//   "params": {
//     "name": "query_send",
//     "arguments": {
//       "channel": "example-queries",
//       "body": "get-data",
//       "timeout_seconds": 10,
//       "metadata": "qry-meta",
//       "tags": {"action": "lookup"}
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 10,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"data\":\"query response payload from subscriber\"}" }],
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
			Name: "query_send",
			Arguments: map[string]any{
				"channel":         "example-queries",
				"body":            "get-data",
				"timeout_seconds": 10,
				"metadata":        "qry-meta",
				"tags":            map[string]any{"action": "lookup"},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: query_send")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output (with active subscriber):
// Tool: query_send
// Result: {"data":"query response payload from subscriber"}
//
// Expected output (no subscriber):
// Tool: query_send
// Result: Query timed out: no subscriber on channel 'example-queries' within 10s
