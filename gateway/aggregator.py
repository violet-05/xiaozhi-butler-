"""聚合器：连接所有上游、合并工具、路由调用。"""

from __future__ import annotations

import logging

from mcp.types import CallToolResult, TextContent, Tool

from .config import ServerConfig
from .upstream import Upstream

logger = logging.getLogger("gateway.aggregator")

# 命名空间分隔符：聚合工具名 = f"{上游名}{SEPARATOR}{原始工具名}"
# 使用下划线以兼容 Anthropic 工具名规则 [a-zA-Z0-9_-]
SEPARATOR = "_"


class Aggregator:
    """管理所有上游，提供命名空间化的工具列表与调用路由。"""

    def __init__(self, configs: list[ServerConfig]):
        self.upstreams: list[Upstream] = [Upstream(c) for c in configs]
        # 聚合工具名 -> (上游, 原始工具名)
        self._index: dict[str, tuple[Upstream, str]] = {}

    async def start(self) -> None:
        """连接所有上游；单个失败仅告警，不阻塞整体启动。

        注意：顺序连接（而非并发），确保上游的 anyio cancel scope
        在「进入它的同一个 task」内建立，关闭时才不会报错。
        """
        for up in self.upstreams:
            try:
                await up.connect()
            except Exception as e:
                logger.warning("上游 %s 连接失败，已跳过: %s", up.name, e)
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        """重建 聚合工具名 -> (上游, 原始工具名) 的路由表。"""
        self._index.clear()
        for up in self.upstreams:
            if up._tools is None:
                continue
            for tool in up._tools:
                self._index[f"{up.name}{SEPARATOR}{tool.name}"] = (up, tool.name)

    def list_tools(self) -> list[Tool]:
        """合并所有已连接上游的工具，加命名空间前缀，保留原始 inputSchema。"""
        result: list[Tool] = []
        for up in self.upstreams:
            if up._tools is None:
                continue
            for tool in up._tools:
                ns_name = f"{up.name}{SEPARATOR}{tool.name}"
                desc = tool.description or ""
                new_desc = f"[来源: {up.name}] {desc}".strip()
                result.append(
                    Tool(
                        name=ns_name,
                        description=new_desc,
                        inputSchema=tool.inputSchema,
                        outputSchema=tool.outputSchema,
                        annotations=tool.annotations,
                    )
                )
        return result

    async def call_tool(self, name: str, arguments: dict | None) -> CallToolResult:
        """解析命名空间前缀并路由到对应上游。"""
        entry = self._index.get(name)
        if entry is None:
            return _error_result(f"工具不存在或上游未连接: {name}")

        upstream, raw_name = entry
        try:
            return await upstream.call_tool(raw_name, arguments)
        except Exception as e:
            logger.exception("调用工具 %s 失败", name)
            return _error_result(f"调用 {name} 失败: {e}")

    async def close(self) -> None:
        """关闭所有上游连接。

        逆序关闭：anyio 的 cancel scope 必须严格 LIFO 进出，先连接的要最后关闭，
        否则在关闭后续上游时会因 scope 顺序错乱而抛 CancelledError。
        """
        for up in reversed(self.upstreams):
            try:
                await up.close()
            except Exception as e:
                logger.warning("关闭上游 %s 失败: %s", up.name, e)


def _error_result(message: str) -> CallToolResult:
    """构造一个 isError=True 的友好错误结果。"""
    return CallToolResult(
        content=[TextContent(type="text", text=message)],
        isError=True,
    )
