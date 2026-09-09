"""网关服务端：低层 Server + 自定义 list_tools/call_tool 处理器。"""

from __future__ import annotations

from typing import Any

from mcp.server.lowlevel import Server
from mcp.types import CallToolResult, Tool

from .aggregator import Aggregator


def build_server(aggregator: Aggregator) -> Server:
    """构建低层 MCP Server，透传上游工具原始 schema。"""
    server = Server("mcp-gateway")

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        return aggregator.list_tools()

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> CallToolResult:
        return await aggregator.call_tool(name, arguments)

    return server
