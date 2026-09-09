"""单个上游 MCP 服务器的连接封装。"""

from __future__ import annotations

import contextlib
import logging

from mcp import ClientSession, StdioServerParameters
from mcp.client.sse import sse_client
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import CallToolResult, Tool

from .config import ServerConfig

logger = logging.getLogger("gateway.upstream")


class Upstream:
    """一个上游 MCP 服务：负责连接、list_tools、call_tool、断开。

    连接建立后缓存工具列表；断开后再次调用会抛出异常，
    由 Aggregator 统一处理为友好错误。
    """

    def __init__(self, config: ServerConfig):
        self.config = config
        self.name = config.name
        self._stack: contextlib.AsyncExitStack | None = None
        self._session: ClientSession | None = None
        self._tools: list[Tool] | None = None

    @property
    def connected(self) -> bool:
        return self._session is not None

    async def connect(self) -> None:
        """建立连接并完成 MCP 初始化，然后缓存工具列表。"""
        await self.close()

        stack = contextlib.AsyncExitStack()
        try:
            cfg = self.config
            if cfg.transport == "stdio":
                params = StdioServerParameters(
                    command=cfg.command,
                    args=cfg.args,
                    cwd=cfg.cwd,
                    env=cfg.env or None,
                )
                read, write = await stack.enter_async_context(stdio_client(params))
            elif cfg.transport == "sse":
                read, write = await stack.enter_async_context(
                    sse_client(cfg.url, headers=cfg.headers or None)
                )
            else:  # streamable-http
                read, write, _get_session_id = await stack.enter_async_context(
                    streamablehttp_client(cfg.url, headers=cfg.headers or None)
                )

            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            result = await session.list_tools()

            self._session = session
            self._stack = stack
            self._tools = list(result.tools)
            logger.info("上游 %s 已连接，注册 %d 个工具", self.name, len(self._tools))
        except BaseException:
            # 连接失败时清理资源；吞掉 teardown 期间的异常（含 CancelledError），
            # 避免掩盖原始错误。
            await _safe_aclose(stack)
            raise

    async def list_tools(self) -> list[Tool]:
        """返回缓存的工具列表（连接时已拉取）。"""
        if not self.connected or self._tools is None:
            raise RuntimeError(f"上游 {self.name} 未连接")
        return list(self._tools)

    async def call_tool(self, name: str, arguments: dict | None) -> CallToolResult:
        """调用上游工具。"""
        if not self.connected or self._session is None:
            raise RuntimeError(f"上游 {self.name} 已断开")
        return await self._session.call_tool(name, arguments)

    async def close(self) -> None:
        """关闭连接，释放子进程 / 网络资源。"""
        if self._stack is not None:
            await _safe_aclose(self._stack)
        self._stack = None
        self._session = None
        self._tools = None


async def _safe_aclose(stack: contextlib.AsyncExitStack) -> None:
    """关闭资源栈，吞掉 teardown 期间的任何异常（含 CancelledError）。

    anyio 的 cancel scope（stdio_client / ClientSession 内部使用）在 Windows
    下关闭子进程时可能抛出 CancelledError，这里只记录、不影响整体关闭流程。
    """
    try:
        await stack.aclose()
    except BaseException as e:  # noqa: BLE001 - teardown 阶段需吞掉取消异常
        logger.debug("关闭上游资源时出错（已忽略）: %s", e)
