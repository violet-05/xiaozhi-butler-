# 🤖 小智 MCP 电脑控制

> 通过小智 AI 语音助手控制你的 Windows 电脑 — 支持 200+ 热门软件，开箱即用

[![GitHub Stars](https://img.shields.io/github/stars/user/xiaozhi-pc-control?style=social)]()
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

---

## ✨ 功能特性

- 🗣️ **语音控制电脑** — 对小智说话即可打开软件、执行命令、控制媒体播放
- 📦 **200+ 热门软件** — 内置市面主流软件路径，自动搜索已安装应用，无需手动配置
- 🔍 **智能路径发现** — 三层发现机制（注册表 + 路径扫描 + PATH 搜索），自动找到软件
- 🖥️ **图形化界面** — 一键启动，可视化配置，实时日志
- 🎵 **媒体播放控制** — 播放/暂停/切歌/音量控制，兼容所有播放器
- 💻 **命令执行** — 支持执行任意终端命令
- 🔄 **自动重连** — 网络断开后自动重连，无需手动重启

---

## 📋 支持的软件列表（200+）

<details>
<summary>📱 社交通讯（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| 微信 | "打开微信" |
| QQ | "打开QQ" |
| 钉钉 | "打开钉钉" |
| 企业微信 | "打开企业微信" |
| 飞书 | "打开飞书" |
| Telegram | "打开Telegram" |
| Discord | "打开Discord" |
</details>

<details>
<summary>🌐 浏览器（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| Chrome | "打开浏览器" / "打开Chrome" |
| Edge | "打开Edge" |
| Firefox | "打开火狐" |
| Brave | "打开Brave" |
| Opera | "打开Opera" |
| Arc | "打开Arc" |
</details>

<details>
<summary>📝 办公软件（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| Word | "打开Word" |
| Excel | "打开Excel" |
| PPT | "打开PPT" |
| WPS | "打开WPS" |
| Typora | "打开Typora" |
| Notion | "打开Notion" |
| OneNote | "打开OneNote" |
| 有道云笔记 | "打开有道云笔记" |
</details>

<details>
<summary>💻 开发工具（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| VS Code | "打开VS Code" / "打开Code" |
| Cursor | "打开Cursor" |
| IntelliJ IDEA | "打开IDEA" / "打开IntelliJ" |
| PyCharm | "打开PyCharm" |
| Android Studio | "打开Android Studio" |
| WebStorm | "打开WebStorm" |
| Sublime Text | "打开Sublime" |
| HBuilderX | "打开HBuilderX" |
| Git | "打开Git" |
| Python | "打开Python" |
| Node.js | "打开Node" |
| Java | "打开Java" |
| Arduino | "打开Arduino" |
| Keil | "打开Keil" |
| 微信开发者工具 | "打开微信开发者工具" |
</details>

<details>
<summary>🎵 影音娱乐（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| 网易云音乐 | "打开网易云" / "播放周杰伦的晴天" |
| QQ音乐 | "打开QQ音乐" |
| 酷狗音乐 | "打开酷狗" |
| 酷我音乐 | "打开酷我" |
| Spotify | "打开Spotify" |
| PotPlayer | "打开PotPlayer" |
| VLC | "打开VLC" |
| mpv | "打开mpv" |
| 暴风影音 | "打开暴风" |
</details>

<details>
<summary>🎬 视频平台（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| 哔哩哔哩 | "打开B站" / "打开哔哩哔哩" |
| 腾讯视频 | "打开腾讯视频" |
| 爱奇艺 | "打开爱奇艺" |
| 优酷 | "打开优酷" |
| 抖音 | "打开抖音" |
| 快手 | "打开快手" |
</details>

<details>
<summary>🎥 直播 & 剪辑（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| OBS | "打开OBS" |
| 虎牙直播 | "打开虎牙" |
| B站直播 | "打开直播姬" |
| 剪映 | "打开剪映" |
| Premiere | "打开PR" |
| After Effects | "打开AE" |
| 达芬奇 | "打开达芬奇" |
</details>

<details>
<summary>🎮 游戏平台 & 游戏（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| Steam | "打开Steam" |
| Epic | "打开Epic" |
| WeGame | "打开WeGame" |
| Ubisoft | "打开育碧" |
| EA | "打开EA" |
| 暴雪 | "打开暴雪" |
| Rockstar | "打开R星" |
| Steam++ | "打开Steam++" |
| UU加速器 | "打开UU加速器" |
| 迅游加速器 | "打开迅游" |
| 英雄联盟 | "打开英雄联盟" / "打开LOL" |
| 我的世界 | "打开我的世界" / "打开MC" |
| 原神 | "打开原神" |
| 崩坏星穹铁道 | "打开星穹铁道" |
| 植物大战僵尸 | "打开植物大战僵尸" |
| CS2 | "打开CS2" |
</details>

<details>
<summary>⬇️ 下载 & 网盘（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| IDM | "打开IDM" |
| 迅雷 | "打开迅雷" |
| Motrix | "打开Motrix" |
| aria2 | "打开aria2" |
| 百度网盘 | "打开百度网盘" |
| 阿里云盘 | "打开阿里云盘" |
| 夸克网盘 | "打开夸克" |
| OneDrive | "打开OneDrive" |
| 坚果云 | "打开坚果云" |
| 123云盘 | "打开123云盘" |
</details>

<details>
<summary>🔗 远程工具（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| 向日葵 | "打开向日葵" |
| ToDesk | "打开ToDesk" |
| TeamViewer | "打开TeamViewer" |
| AnyDesk | "打开AnyDesk" |
| RustDesk | "打开RustDesk" |
</details>

<details>
<summary>⚙️ 系统工具（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| 记事本 | "打开记事本" |
| 画图 | "打开画图" |
| 计算器 | "打开计算器" |
| 任务管理器 | "打开任务管理器" |
| 控制面板 | "打开控制面板" |
| 注册表 | "打开注册表" |
| CMD | "打开CMD" / "打开终端" |
| PowerShell | "打开PowerShell" |
| Windows Terminal | "打开Windows Terminal" |
| 远程桌面 | "打开远程桌面" |
| 截图工具 | "打开截图工具" |
| 资源监视器 | "打开资源监视器" |
| 磁盘清理 | "打开磁盘清理" |
</details>

<details>
<summary>🛡️ 安全 & 设计 & 其他（点击展开）</summary>

| 软件 | 语音指令 |
|------|---------|
| 火绒 | "打开火绒" |
| 360安全卫士 | "打开360" |
| 电脑管家 | "打开电脑管家" |
| Photoshop | "打开PS" |
| Illustrator | "打开AI" |
| Figma | "打开Figma" |
| SolidWorks | "打开SolidWorks" |
| AutoCAD | "打开CAD" |
| 立创EDA | "打开立创EDA" |
| 嘉立创 | "打开嘉立创" |
| 搜狗输入法 | "打开搜狗输入法" |
| 百度输入法 | "打开百度输入法" |
| 微信输入法 | "打开微信输入法" |
| 有道词典 | "打开有道词典" |
| DeepL | "打开DeepL" |
| Clash | "打开Clash" |
| V2Ray | "打开V2Ray" |
| VMware | "打开VMware" |
| VirtualBox | "打开VirtualBox" |
| Tabby | "打开Tabby" |
| MobaXterm | "打开MobaXterm" |
| Xshell | "打开Xshell" |
| Everything | "打开Everything" |
| Snipaste | "打开Snipaste" |
| 7-Zip | "打开7-Zip" |
| WinRAR | "打开WinRAR" |
| Bandizip | "打开Bandizip" |
| 雨滴桌面 | "打开雨滴桌面" |
| 壁纸引擎 | "打开壁纸引擎" |
| NVIDIA | "打开NVIDIA" |
| Logitech | "打开罗技" |
| CrystalDiskInfo | "打开DiskInfo" |
| CrystalDiskMark | "打开DiskMark" |
| R-Studio | "打开R-Studio" |
</details>

---

## 🚀 快速开始

### 1. 环境要求

- **操作系统**：Windows 10/11
- **Python**：3.10 或更高版本
- **小智设备**：已配置好并能正常对话

### 2. 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/your-username/xiaozhi-pc-control.git
cd xiaozhi-pc-control

# 2. 创建虚拟环境（推荐）
conda create -n xiaozhi-pc python=3.10
conda activate xiaozhi-pc

# 3. 安装依赖
pip install -r requirements.txt
```

### 3. 配置 MCP 接入点

1. 登录 [小智后台](https://xiaozhi.me)
2. 进入你的设备 → MCP 接入点
3. 复制接入点地址（格式：`wss://api.xiaozhi.me/mcp/?token=...`）

**方式一：图形化配置（推荐）**

```bash
python gui_launcher.py
```

在界面中粘贴 MCP 接入点地址，点击「保存配置」。

**方式二：手动配置**

编辑 `.env` 文件：

```env
MCP_ENDPOINT=wss://api.xiaozhi.me/mcp/?token=你的token
```

### 4. 启动服务

**方式一：图形化启动（推荐）**

```bash
python gui_launcher.py
```

点击「启动服务」按钮。

**方式二：命令行启动**

```bash
python mcp_pipe.py yo_mcp.py
```

### 5. 开始使用

对着小智说：

- "打开微信"
- "打开浏览器"
- "打开Steam"
- "播放下一首"
- "音量大一点"
- "执行 dir 命令"

---

## 🖥️ 图形化界面

运行 `python gui_launcher.py` 打开图形化启动器：

```
┌─────────────────────────────────────────────────┐
│  🤖 小智 MCP 电脑控制                            │
│  通过小智 AI 语音控制你的电脑 | 支持 200+ 热门软件 │
├─────────────────────────────────────────────────┤
│  ⚙️ MCP 配置                                    │
│  MCP 接入点：[wss://api.xiaozhi.me/mcp/?...]    │
│  [💾 保存配置]  [🔍 扫描已安装软件]              │
├─────────────────────────────────────────────────┤
│  🔧 功能模块                                     │
│  [✓] 📦 应用启动    [✓] 💻 命令执行    [✓] 🎵 媒体 │
├─────────────────────────────────────────────────┤
│  [▶ 启动服务]  [⏹ 停止服务]  ● 运行中           │
├─────────────────────────────────────────────────┤
│  📋 运行日志                                     │
│  ✅ MCP 服务已启动！                             │
│  现在可以对小智说话来控制电脑了                    │
└─────────────────────────────────────────────────┘
```

---

## 🎙️ 语音指令示例

### 打开应用

| 你说的话 | 小智执行 |
|---------|---------|
| "打开微信" | 启动微信客户端 |
| "打开浏览器" | 启动 Chrome |
| "打开浏览器 https://www.baidu.com" | Chrome 打开百度 |
| "打开VS Code" | 启动 VS Code |
| "打开Steam" | 启动 Steam |
| "打开网易云" | 启动网易云音乐 |

### 媒体控制

| 你说的话 | 小智执行 |
|---------|---------|
| "播放" / "暂停" | 播放/暂停当前歌曲 |
| "下一首" / "切歌" | 切换到下一首 |
| "上一首" | 切换到上一首 |
| "音量大一点" | 增大系统音量 |
| "音量小一点" | 减小系统音量 |
| "静音" | 切换静音 |
| "播放周杰伦的晴天" | 在网易云搜索并播放 |
| "歌词" | 显示/隐藏桌面歌词 |
| "收藏" | 收藏当前歌曲 |

### 执行命令

| 你说的话 | 小智执行 |
|---------|---------|
| "执行 dir 命令" | 列出当前目录文件 |
| "执行 ipconfig" | 查看网络配置 |
| "执行 tasklist" | 查看运行中的进程 |

---

## 📁 项目结构

```
xiaozhi-pc-control/
├── gui_launcher.py              # 🖥️ 图形化启动器（入口）
├── yo_mcp.py                    # 🔌 MCP 服务器主程序
├── mcp_pipe.py                  # 🔗 WebSocket 管道
├── tools/                       # 🔧 工具模块（自动加载）
│   ├── open_app_tool.py         # 📦 智能软件发现与启动（200+）
│   ├── command_execution_tool.py # 💻 终端命令执行
│   └── media_control_tool.py    # 🎵 媒体播放控制
├── .env                         # ⚙️ 配置文件
├── config.json                  # 📝 GUI 配置文件
├── requirements.txt             # 📋 Python 依赖
└── README.md                    # 📖 说明文档
```

---

## 🔍 软件发现机制

本项目采用**三层智能发现机制**，自动搜索用户电脑上已安装的软件：

### 第一层：Windows 注册表扫描
- 扫描 `HKLM` 和 `HKCU` 下的已安装软件列表
- 提取 `DisplayName`、`InstallLocation` 等信息
- 覆盖通过安装程序安装的软件

### 第二层：常见路径匹配
- 内置 200+ 热门软件的常见安装路径
- 支持通配符匹配（如 `C:\Program Files\JetBrains\*\bin\idea64.exe`）
- 覆盖 C/D/E/F/G 等多个磁盘分区

### 第三层：PATH 环境变量搜索
- 使用 `shutil.which()` 搜索 PATH 中的可执行文件
- 覆盖 git、python、node、java 等命令行工具

---

## ❓ 常见问题

### Q: 某个软件打不开怎么办？

**A:** 可能是软件安装在非标准路径。你可以：

1. 找到软件的 exe 文件路径
2. 对小智说"打开 [完整路径]"，如"打开 D:\MyApp\app.exe"
3. 或者在 `tools/open_app_tool.py` 的 `SOFTWARE_DB` 中添加你的路径

### Q: 如何添加新的软件支持？

**A:** 编辑 `tools/open_app_tool.py`，在 `SOFTWARE_DB` 字典中添加：

```python
"我的软件": {
    "aliases": ["我的软件", "myapp"],  # 支持的名称
    "exe_names": ["myapp.exe"],        # exe 文件名
    "search_paths": [                  # 常见安装路径
        r"C:\Program Files\MyApp\myapp.exe",
        r"D:\MyApp\myapp.exe",
    ],
    "registry_keywords": ["MyApp"],    # 注册表关键词
},
```

### Q: 支持 macOS 吗？

**A:** 当前仅支持 Windows。macOS 用户需要自行修改路径和系统调用。

### Q: MCP token 过期了怎么办？

**A:** 登录小智后台重新获取 token，然后更新 `.env` 文件或在 GUI 中重新配置。

### Q: 扫描软件很慢怎么办？

**A:** 扫描需要遍历注册表和搜索路径，首次扫描可能需要几秒钟。扫描结果会自动缓存。

### Q: 如何让小智打开浏览器并访问指定网站？

**A:** 对小智说"打开浏览器 https://www.baidu.com"，系统会自动将网址作为参数传递给浏览器。

---

## 🛠️ 开发说明

### 添加新工具

1. 在 `tools/` 目录下创建新的 Python 文件
2. 定义 `register_tool(mcp)` 函数
3. 使用 `@mcp.tool()` 装饰器注册工具
4. 重启服务即可自动加载

示例：

```python
# tools/my_tool.py
def register_tool(mcp):
    @mcp.tool()
    def my_tool(param: str) -> dict:
        """工具描述"""
        # 你的逻辑
        return {"success": True, "result": "执行结果"}
```

### 依赖说明

| 依赖 | 用途 |
|------|------|
| python-dotenv | 读取 .env 配置 |
| websockets | WebSocket 客户端 |
| mcp | MCP 协议实现 |
| pydantic | 数据验证 |
| pyautogui | 键鼠模拟（媒体控制） |

---

## 🔌 通用 MCP 聚合网关（Gateway）

除了只接小智，本项目还内置了一个**通用 MCP 聚合网关**，能把任意多个 MCP 服务聚合成一个入口，
同时用本地 `stdio` 和远程 `HTTP` 两种方式暴露给任意客户端（Claude Desktop / Claude Code / Cursor / 小智 / 云端设备）。

### 架构

```
   上游 MCP 服务（任意多个，可扩展）
  yo_mcp.py ── filesystem ── github ── ...
        └────────────┬────────────┘
                     │ 聚合器（命名空间 + 路由 + 断线隔离）
              ┌──────┴──────┐
          stdio(本地)    HTTP(远程 streamable-http)
  Claude/Cursor/小智      云端 / 多设备
```

聚合后的工具名 = `{上游名}_{原始工具名}`（例如 `pc-control_open_app_tool`），
且**完整保留上游工具的原始 inputSchema**。

### 配置上游（servers.yaml）

编辑项目根目录的 `servers.yaml`，`transport` 支持三种：

| transport | 说明 | 必需字段 |
|-----------|------|---------|
| `stdio` | 启动本地子进程（MCP 服务） | `args`（`command` 缺省用当前 Python） |
| `sse` | 连接远程 SSE MCP | `url` |
| `streamable-http` | 连接远程 Streamable HTTP MCP | `url` |

```yaml
servers:
  - name: pc-control            # 你现有的电脑控制
    transport: stdio
    args: ["yo_mcp.py"]
    cwd: "."
  # 第三方示例（去掉注释启用）
  # - name: filesystem
  #   transport: stdio
  #   command: npx
  #   args: ["-y", "@modelcontextprotocol/server-filesystem", "C:/Users/21711"]
  # - name: github
  #   transport: streamable-http
  #   url: "https://api.githubcopilot.com/mcp/"
  #   headers:
  #     Authorization: "Bearer <token>"
```

### 启动方式

```bash
# 方式一：本地 stdio（挂 Claude Desktop / Claude Code / Cursor）
python -m gateway --transport stdio

# 方式二：远程 HTTP（多设备 / 云端接入）
python -m gateway --transport http --host 0.0.0.0 --port 8080
# 接入点: http://<主机>:8080/mcp

# 方式三：小智桥接（让小智也用上聚合后的全部工具）
python mcp_pipe.py gateway_stdio.py
```

> 新增依赖：`pyyaml`、`uvicorn`（已加入 `requirements.txt`，`pip install -r requirements.txt` 即可）。
> 网关的日志走 stderr，stdout 始终保持干净的 MCP 协议通道，因此与 `mcp_pipe.py` 完全兼容。

---

## 🙏 致谢

- [虾哥 MCP 原项目](https://github.com/78/mcp-calculator) — 本项目基于此实现
- [小智 ESP32](https://github.com/78/xiaozhi-esp32) — 开源智能硬件项目
- [小智后端服务](https://github.com/xinnan-tech/xiaozhi-esp32-server) — 后端服务实现

---

## 📄 许可证

本项目基于 [MIT 许可证](LICENSE) 开源。

---

<p align="center">
  觉得有用的话，别忘了点个 ⭐ Star 支持一下！
</p>
