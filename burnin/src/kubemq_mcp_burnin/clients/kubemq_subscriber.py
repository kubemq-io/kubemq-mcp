from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable, Coroutine

logger = logging.getLogger(__name__)

_KUBEMQ_AVAILABLE = False
try:
    from kubemq import (
        AsyncCQClient,
        AsyncCancellationToken,
        CommandResponse,
        CommandsSubscription,
        QueryResponse,
        QueriesSubscription,
    )
    _KUBEMQ_AVAILABLE = True
except ImportError:
    logger.debug("kubemq package not available — command/query subscriber will be stubbed")

_MAX_RETRIES = 3


class KubeMQSubscriberManager:
    """Manages kubemq command/query subscribers for testing MCP command_send and query_send tools.

    When the kubemq gRPC SDK is not installed, subscriber methods log a warning and
    return without starting — M13/M14 tests will observe the timeout behavior instead.
    """

    def __init__(
        self, broker_address: str, client_id_prefix: str = "mcp-burnin"
    ) -> None:
        self._broker_address = broker_address
        self._client_id_prefix = client_id_prefix
        self._clients: list[Any] = []
        self._tokens: list[Any] = []
        self._tasks: list[asyncio.Task[None]] = []

    async def _start_subscriber(
        self,
        channel: str,
        sub_type: str,
        client_id_suffix: str,
        run_loop: Callable[[Any, Any], Coroutine[Any, Any, None]],
    ) -> None:
        if not _KUBEMQ_AVAILABLE:
            logger.warning(
                "kubemq SDK not installed — skipping %s subscriber on %s",
                sub_type, channel,
            )
            return

        client = AsyncCQClient(
            address=self._broker_address,
            client_id=f"{self._client_id_prefix}-{client_id_suffix}",
        )
        await client.connect()
        self._clients.append(client)

        token = AsyncCancellationToken()
        self._tokens.append(token)

        async def _run() -> None:
            retries = 0
            while retries < _MAX_RETRIES:
                try:
                    await run_loop(client, token)
                    break
                except asyncio.CancelledError:
                    raise
                except Exception as exc:
                    retries += 1
                    logger.error(
                        "%s subscriber error on %s (attempt %d/%d): %s",
                        sub_type, channel, retries, _MAX_RETRIES, exc,
                    )
                    if retries < _MAX_RETRIES:
                        await asyncio.sleep(1)

        self._tasks.append(asyncio.create_task(_run()))

    async def start_command_subscriber(self, channel: str) -> None:
        """Start a command subscriber that auto-responds with success."""
        sub = CommandsSubscription(
            channel=channel,
            on_receive_command_callback=lambda _: None,
        ) if _KUBEMQ_AVAILABLE else None

        async def _loop(client: Any, token: Any) -> None:
            async for cmd in client.subscribe_to_commands_fast(sub, token):
                resp = CommandResponse(command_received=cmd, is_executed=True)
                await client.send_response_fast(resp)

        await self._start_subscriber(channel, "command", "cmd-sub", _loop)

    async def start_query_subscriber(self, channel: str) -> None:
        """Start a query subscriber that auto-responds with a test payload."""
        sub = QueriesSubscription(
            channel=channel,
            on_receive_query_callback=lambda _: None,
        ) if _KUBEMQ_AVAILABLE else None

        async def _loop(client: Any, token: Any) -> None:
            async for query in client.subscribe_to_queries_fast(sub, token):
                resp = QueryResponse(
                    query_received=query,
                    is_executed=True,
                    body=b"burnin-query-response",
                )
                await client.send_response_fast(resp)

        await self._start_subscriber(channel, "query", "query-sub", _loop)

    async def stop_all(self) -> None:
        """Cancel all subscriber tasks and close clients."""
        for token in self._tokens:
            token.cancel()
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        for client in self._clients:
            await client.close()
        self._clients.clear()
        self._tokens.clear()
        self._tasks.clear()
