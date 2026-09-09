"""小智 mcp_pipe.py 兼容入口：以 stdio 模式启动聚合网关。

让小智也能用上聚合后的全部上游工具：

    python mcp_pipe.py gateway_stdio.py

mcp_pipe.py 会用 sys.executable 运行本脚本（stdio 模式），
把网关的 stdout/stdin 桥接到小智后台的 wss。
"""

import sys

from gateway.main import main

if __name__ == "__main__":
    sys.exit(main(["--transport", "stdio"]))
