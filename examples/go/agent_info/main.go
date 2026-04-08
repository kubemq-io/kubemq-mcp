// KubeMQ MCP Example: agent_info
//
// Demonstrates the agent_info tool using the mcp-go SDK.
// Returns details for a specific agent.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_info",
//     "arguments": { "agent_id": "example-agent" }
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 14,
//   "result": {
//     "content": [{ "type": "text", "text": "{\"agent_id\":\"example-agent\",\"name\":\"Example Agent\"}" }],
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
			Name: "agent_info",
			Arguments: map[string]any{
				"agent_id": "example-agent",
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: agent_info")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: agent_info
// Result: {"agent_id":"example-agent","name":"Example Agent","description":"example agent","version":"1.0.0"}
