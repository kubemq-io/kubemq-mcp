from __future__ import annotations

import json
import random
from typing import Any

from aiohttp import web

from kubemq_mcp_burnin.agents.base import BaseMockAgent


class ErrorAgent(BaseMockAgent):
    agent_type = "error"

    def __init__(self, *args: Any, error_rate: float = 1.0, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.error_rate = error_rate
        self._error_status_codes = [400, 500, 502, 503, 504]
        self._error_index = 0

    async def _handle_request(
        self, request: web.Request
    ) -> web.Response | web.StreamResponse:
        try:
            body = await request.json()
        except json.JSONDecodeError:
            return web.json_response(
                {
                    "jsonrpc": "2.0",
                    "error": {"code": -32700, "message": "Parse error"},
                    "id": None,
                },
                status=200,
            )

        headers = dict(request.headers)
        self.request_log.append({"body": body, "headers": headers})

        if random.random() < self.error_rate:
            status = self._error_status_codes[
                self._error_index % len(self._error_status_codes)
            ]
            self._error_index += 1
            return web.json_response(
                {"error": f"Simulated error with status {status}"},
                status=status,
            )

        method = body.get("method", "") if isinstance(body, dict) else ""
        request_id = body.get("id") if isinstance(body, dict) else None

        if method == "message/stream":
            return await self.handle_message_stream(body, headers, request)
        elif method == "stream_cancel":
            result = await self.handle_stream_cancel(body)
            return web.json_response(
                {"jsonrpc": "2.0", "id": request_id, "result": result}
            )
        else:
            result = await self.handle_message_send(body, headers)
            return web.json_response(
                {"jsonrpc": "2.0", "id": request_id, "result": result}
            )
