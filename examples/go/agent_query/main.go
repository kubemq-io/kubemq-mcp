// KubeMQ MCP Example: agent_query
//
// Demonstrates the agent_query tool using the mcp-go SDK.
// Queries an agent using a specific method (e.g., tasks/get).
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_query",
//     "arguments": { "agent_id": "example-agent", "method": "tasks/get" }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 16,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"echo\":{\"method\":\"tasks/get\",\"params\":{}}}" }],
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
			Name: "agent_query",
			Arguments: map[string]any{
				"agent_id": "example-agent",
				"method":   "tasks/get",
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: agent_query")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: agent_query
// Result: {"echo":{"method":"tasks/get","params":{}},"received_headers":{}}
