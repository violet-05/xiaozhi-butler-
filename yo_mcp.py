"""
小智 MCP 电脑控制服务器
自动加载 tools/ 目录下的所有工具模块
"""

from mcp.server.fastmcp import FastMCP
import os
import importlib
import sys

# 创建 MCP 服务器
mcp = FastMCP("XiaoZhi_PC_Control")

# 自动导入并注册 tools 文件夹中的所有模块
tools_dir = os.path.join(os.path.dirname(__file__), 'tools')
for filename in os.listdir(tools_dir):
    if filename.endswith('.py') and filename != '__init__.py':
        module_name = f'tools.{filename[:-3]}'
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, 'register_tool'):
                module.register_tool(mcp)
                print(f"✅ 已加载工具: {filename}", file=sys.stderr)
        except ImportError as e:
            print(f"❌ 加载失败: {filename} - {e}", file=sys.stderr)

if __name__ == "__main__":
    # 注意：stdio 模式下 stdout 是 MCP 协议通道，任何提示信息都必须写 stderr
    print("\n" + "=" * 50, file=sys.stderr)
    print("小智 MCP 电脑控制服务器", file=sys.stderr)
    print("=" * 50, file=sys.stderr)
    print("已注册工具：", file=sys.stderr)
    print("  - open_app_tool: 打开应用程序（200+ 热门软件）", file=sys.stderr)
    print("  - list_installed_apps_tool: 扫描已安装软件", file=sys.stderr)
    print("  - command_execution_tool: 执行终端命令", file=sys.stderr)
    print("  - media_control_tool: 媒体播放控制", file=sys.stderr)
    print("=" * 50 + "\n", file=sys.stderr)
    mcp.run(transport="stdio")
