"""通用 MCP 聚合网关 CLI 入口。

用法:
    python -m gateway --transport stdio
    python -m gateway --transport http --host 127.0.0.1 --port 8080
    python -m gateway --config servers.yaml --transport stdio
"""

from __future__ import annotations

import argparse
import logging
import sys

from . import transports
from .aggregator import Aggregator
from .config import load_config


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(description="通用 MCP 聚合网关")
    parser.add_argument("--config", default="servers.yaml", help="上游配置文件路径")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="对外传输: stdio(本地) 或 http(远程 streamable-http)",
    )
    parser.add_argument("--host", default="127.0.0.1", help="http 模式监听地址")
    parser.add_argument("--port", type=int, default=8080, help="http 模式监听端口")
    args = parser.parse_args(argv)

    configs = load_config(args.config)
    logging.getLogger("gateway").info("已加载 %d 个上游", len(configs))

    aggregator = Aggregator(configs)

    if args.transport == "stdio":
        transports.run_stdio(aggregator)
    else:
        transports.run_http(aggregator, host=args.host, port=args.port)

    return 0


if __name__ == "__main__":
    sys.exit(main())
