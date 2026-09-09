"""网关配置：解析 servers.yaml，定义上游 MCP 服务器配置。"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

VALID_TRANSPORTS = ("stdio", "sse", "streamable-http")


@dataclass
class ServerConfig:
    """单个上游 MCP 服务器的配置。

    transport 为 stdio 时使用 command/args/cwd/env（本地子进程）；
    为 sse / streamable-http 时使用 url/headers（远程服务）。
    """

    name: str
    transport: str
    command: str | None = None
    args: list[str] = field(default_factory=list)
    cwd: str | None = None
    env: dict[str, str] = field(default_factory=dict)
    url: str | None = None
    headers: dict[str, str] = field(default_factory=dict)

    def validate(self) -> None:
        """校验配置字段，非法时抛出 ValueError。"""
        if not self.name or not self.name.strip():
            raise ValueError("server.name 不能为空")
        if self.transport not in VALID_TRANSPORTS:
            raise ValueError(
                f"上游 '{self.name}' 的 transport 非法: {self.transport!r}，"
                f"可选: {', '.join(VALID_TRANSPORTS)}"
            )
        if self.transport == "stdio":
            if not self.command:
                raise ValueError(f"stdio 上游 '{self.name}' 缺少 command")
        else:
            if not self.url:
                raise ValueError(f"{self.transport} 上游 '{self.name}' 缺少 url")


def load_config(path: str | Path = "servers.yaml") -> list[ServerConfig]:
    """从 YAML 文件加载上游服务器配置，并做基本校验。

    - 相对路径的 cwd 会解析为相对配置文件所在目录的绝对路径。
    - stdio 上游未指定 command 时，默认使用当前解释器（sys.executable）。
    """
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    servers_raw = raw.get("servers")
    if not servers_raw:
        raise ValueError("配置文件中缺少 'servers' 列表")
    if not isinstance(servers_raw, list):
        raise ValueError("配置文件的 'servers' 必须是一个列表")

    configs: list[ServerConfig] = []
    seen_names: set[str] = set()
    for item in servers_raw:
        if not isinstance(item, dict):
            raise ValueError(f"servers 中的每一项必须是对象，收到: {item!r}")

        transport = str(item.get("transport", "stdio")).strip()
        command = item.get("command")
        if transport == "stdio" and not command:
            command = sys.executable

        cwd = item.get("cwd")
        if cwd and not Path(cwd).is_absolute():
            cwd = str((config_path.parent / cwd).resolve())

        cfg = ServerConfig(
            name=str(item.get("name", "")).strip(),
            transport=transport,
            command=command,
            args=[str(a) for a in (item.get("args") or [])],
            cwd=cwd,
            env=dict(item.get("env") or {}),
            url=item.get("url"),
            headers=dict(item.get("headers") or {}),
        )
        cfg.validate()
        if cfg.name in seen_names:
            raise ValueError(f"上游名称重复: {cfg.name}")
        seen_names.add(cfg.name)
        configs.append(cfg)

    return configs
