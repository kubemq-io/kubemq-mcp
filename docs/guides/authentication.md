# Authentication

## Overview

KubeMQ supports optional JWT/token authentication for securing MCP endpoint access. Authentication is disabled by default for local development.

## Configuration

### Environment Variable

Set the `KUBEMQ_MCP_AUTH_TOKEN` environment variable with a valid JWT token:

```bash
export KUBEMQ_MCP_AUTH_TOKEN="eyJhbGciOiJIUzI1NiIs..."
```

### Authorization Header

Alternatively, pass the token directly in the `Authorization` header:

```bash
curl -X POST http://localhost:9090/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{...}}'
```

## Unauthenticated Mode

By default, KubeMQ does not require authentication for local development. The MCP endpoint accepts requests without any auth token.

This is suitable for:

- Local development and testing
- Internal network deployments with network-level security
- Proof-of-concept environments

## Production Recommendations

- **Always enable authentication** in production deployments.
- **Use short-lived tokens** to limit the impact of token compromise.
- **Rotate tokens regularly** as part of your security practices.
- **Use TLS** (`https://`) for all production MCP endpoint connections.
- **Restrict network access** to the MCP endpoint using firewall rules or network policies.
