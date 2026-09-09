"""传输入口：本地 stdio 与远程 streamable-http。"""

from __future__ import annotations

import contextlib
import logging

import anyio
import uvicorn
from mcp.server.stdio import stdio_server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from starlette.applications import Starlette
from starlette.routing import Route

from .aggregator import Aggregator
from .server import build_server

logger = logging.getLogger("gateway.transports")


async def _stdio_main(aggregator: Aggregator) -> None:
    """在单一事件循环内：连接上游 → 以 stdio 提供服务 → 关闭上游。"""
    await aggregator.start()
    try:
        server = build_server(aggregator)
        async with stdio_server() as (read, write):
            await server.run(read, write, server.create_initialization_options())
    finally:
        await aggregator.close()


def run_stdio(aggregator: Aggregator) -> None:
    """本地 stdio 模式：供 Claude Desktop / Claude Code / Cursor / mcp_pipe 使用。"""
    anyio.run(_stdio_main, aggregator)


class _ASGIEndpoint:
    """把 StreamableHTTPSessionManager 适配为 Starlette ASGI 端点。"""

    def __init__(self, session_manager: StreamableHTTPSessionManager):
        self._manager = session_manager

    async def __call__(self, scope, receive, send) -> None:
        await self._manager.handle_request(scope, receive, send)


def run_http(aggregator: Aggregator, host: str = "127.0.0.1", port: int = 8080) -> None:
    """远程 streamable-http 模式：供多设备 / 云端接入。"""
    server = build_server(aggregator)
    session_manager = StreamableHTTPSessionManager(app=server)
    endpoint = _ASGIEndpoint(session_manager)

    @contextlib.asynccontextmanager
    async def lifespan(app):
        await aggregator.start()
        try:
            async with session_manager.run():
                yield
        finally:
            await aggregator.close()

    app = Starlette(
        routes=[Route("/mcp", endpoint=endpoint)],
        lifespan=lifespan,
    )

    logger.info("网关 HTTP 服务启动: http://%s:%d/mcp", host, port)
    uvicorn.run(app, host=host, port=port, log_level="info")
