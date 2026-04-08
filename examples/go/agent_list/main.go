// KubeMQ MCP Example: agent_list
//
// Demonstrates the agent_list tool using the mcp-go SDK.
// Lists all registered agents; pass "skill_tags" to filter.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 13,
//   "method": "tools/call",
//   "params": {
//     "name": "agent_list",
//     "arguments": {}
//   }
// }
//
// JSON-RPC Response:
// {
//   "jsonrpc": "2.0",
//   "id": 13,
//   "result": {
//     "content": [{ "type": "text", "text": "[{\"agent_id\":\"echo-01\",\"name\":\"Echo Agent 01\"}]" }],
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
			Name:      "agent_list",
			Arguments: map[string]any{},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: agent_list")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output:
// Tool: agent_list
// Result: [{"agent_id":"echo-01","name":"Echo Agent 01","skills":[{"id":"echo","name":"Echo","tags":["test","echo"]}]}]
