// KubeMQ MCP Example: command_send
//
// Demonstrates the command_send tool using the mcp-go SDK.
// Sends a synchronous command — requires an active subscriber on the target channel.
//
// JSON-RPC Request:
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "method": "tools/call",
//   "params": {
//     "name": "command_send",
//     "arguments": {
//       "channel": "example-commands",
//       "body": "do-work",
//       "timeout_seconds": 10,
//       "metadata": "cmd-meta",
//       "tags": {"action": "process"}
//     }
//   }
// }
//
// JSON-RPC Response (success):
// {
//   "jsonrpc": "2.0",
//   "id": 9,
//   "result": {
//     "content": [{ "type": "text", "text": "Command executed successfully on channel 'example-commands'" }],
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
			Name: "command_send",
			Arguments: map[string]any{
				"channel":         "example-commands",
				"body":            "do-work",
				"timeout_seconds": 10,
				"metadata":        "cmd-meta",
				"tags":            map[string]any{"action": "process"},
			},
		},
	})
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println("Tool: command_send")
	fmt.Printf("Result: %+v\n", result)
}

// Expected output (with active subscriber):
// Tool: command_send
// Result: Command executed successfully on channel 'example-commands'
//
// Expected output (no subscriber):
// Tool: command_send
// Result: Command timed out: no subscriber on channel 'example-commands' within 10s
