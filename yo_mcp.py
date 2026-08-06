"""
小智 MCP 电脑控制服务器
自动加载 tools/ 目录下的所有工具模块
"""

from mcp.server.fastmcp import FastMCP
import os
import importlib

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
                print(f"✅ 已加载工具: {filename}")
        except ImportError as e:
            print(f"❌ 加载失败: {filename} - {e}")

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("小智 MCP 电脑控制服务器")
    print("=" * 50)
    print("已注册工具：")
    print("  - open_app_tool: 打开应用程序（200+ 热门软件）")
    print("  - list_installed_apps_tool: 扫描已安装软件")
    print("  - command_execution_tool: 执行终端命令")
    print("  - media_control_tool: 媒体播放控制")
    print("=" * 50 + "\n")
    mcp.run(transport="stdio")
