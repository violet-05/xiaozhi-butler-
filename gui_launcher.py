"""
小智 MCP 电脑控制 — 图形化启动器
一键配置、扫描软件、启动服务
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import sys
import json
from pathlib import Path

# 项目根目录
PROJECT_DIR = Path(__file__).parent
ENV_FILE = PROJECT_DIR / ".env"
CONFIG_FILE = PROJECT_DIR / "config.json"


class MCPLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("小智 MCP 电脑控制 — 启动器")
        self.root.geometry("800x650")
        self.root.minsize(700, 550)

        # 设置图标和样式
        self.root.configure(bg="#1e1e2e")
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configure_styles()

        # 进程引用
        self.process = None
        self.is_running = False

        # 加载配置
        self.config = self._load_config()

        # 构建界面
        self._build_ui()

        # 窗口关闭处理
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _configure_styles(self):
        """配置 UI 样式"""
        bg = "#1e1e2e"
        fg = "#cdd6f4"
        accent = "#89b4fa"
        surface = "#313244"
        green = "#a6e3a1"
        red = "#f38ba8"

        self.style.configure("Title.TLabel", font=("Microsoft YaHei UI", 16, "bold"),
                             foreground=accent, background=bg)
        self.style.configure("Subtitle.TLabel", font=("Microsoft YaHei UI", 9),
                             foreground="#a6adc8", background=bg)
        self.style.configure("Section.TLabelframe.Label", font=("Microsoft YaHei UI", 10, "bold"),
                             foreground=accent, background=bg)
        self.style.configure("Section.TLabelframe", background=surface, foreground=fg)
        self.style.configure("TLabel", foreground=fg, background=surface, font=("Microsoft YaHei UI", 9))
        self.style.configure("Bg.TLabel", background=bg)
        self.style.configure("TEntry", fieldbackground="#45475a", foreground=fg, insertcolor=fg)
        self.style.configure("TButton", font=("Microsoft YaHei UI", 9))

        self.style.configure("Green.TButton", foreground="#1e1e2e", background=green,
                             font=("Microsoft YaHei UI", 10, "bold"))
        self.style.map("Green.TButton", background=[("active", "#94e2d5")])

        self.style.configure("Red.TButton", foreground="#1e1e2e", background=red,
                             font=("Microsoft YaHei UI", 10, "bold"))
        self.style.map("Red.TButton", background=[("active", "#eba0ac")])

        self.style.configure("Blue.TButton", foreground="#1e1e2e", background=accent,
                             font=("Microsoft YaHei UI", 9))
        self.style.map("Blue.TButton", background=[("active", "#74c7ec")])

    def _build_ui(self):
        """构建主界面"""
        bg = "#1e1e2e"

        # ===== 标题区 =====
        title_frame = tk.Frame(self.root, bg=bg, pady=10)
        title_frame.pack(fill="x", padx=15)

        ttk.Label(title_frame, text="🤖 小智 MCP 电脑控制", style="Title.TLabel").pack(anchor="w")
        ttk.Label(title_frame, text="通过小智 AI 语音控制你的电脑 | 支持 200+ 热门软件",
                  style="Subtitle.TLabel").pack(anchor="w", pady=(2, 0))

        # ===== 配置区 =====
        config_frame = ttk.LabelFrame(self.root, text="⚙️ MCP 配置", style="Section.TLabelframe", padding=10)
        config_frame.pack(fill="x", padx=15, pady=(5, 5))

        # MCP 接入点
        row1 = tk.Frame(config_frame, bg="#313244")
        row1.pack(fill="x", pady=2)
        ttk.Label(row1, text="MCP 接入点：").pack(side="left")
        self.endpoint_var = tk.StringVar(value=self.config.get("endpoint", ""))
        endpoint_entry = ttk.Entry(row1, textvariable=self.endpoint_var, width=60)
        endpoint_entry.pack(side="left", padx=(5, 10), fill="x", expand=True)

        # 按钮行
        btn_row = tk.Frame(config_frame, bg="#313244")
        btn_row.pack(fill="x", pady=(5, 0))

        ttk.Button(btn_row, text="💾 保存配置", style="Blue.TButton",
                   command=self._save_config).pack(side="left", padx=(0, 5))
        ttk.Button(btn_row, text="🔍 扫描已安装软件", style="Blue.TButton",
                   command=self._scan_software).pack(side="left", padx=(0, 5))

        # ===== 功能开关区 =====
        features_frame = ttk.LabelFrame(self.root, text="🔧 功能模块", style="Section.TLabelframe", padding=10)
        features_frame.pack(fill="x", padx=15, pady=(0, 5))

        features_inner = tk.Frame(features_frame, bg="#313244")
        features_inner.pack(fill="x")

        self.var_app = tk.BooleanVar(value=True)
        self.var_cmd = tk.BooleanVar(value=True)
        self.var_media = tk.BooleanVar(value=True)

        tk.Checkbutton(features_inner, text="📦 应用启动 (200+ 软件)", variable=self.var_app,
                       bg="#313244", fg="#cdd6f4", selectcolor="#45475a",
                       activebackground="#313244", activeforeground="#cdd6f4",
                       font=("Microsoft YaHei UI", 9)).pack(side="left", padx=(0, 20))
        tk.Checkbutton(features_inner, text="💻 命令执行", variable=self.var_cmd,
                       bg="#313244", fg="#cdd6f4", selectcolor="#45475a",
                       activebackground="#313244", activeforeground="#cdd6f4",
                       font=("Microsoft YaHei UI", 9)).pack(side="left", padx=(0, 20))
        tk.Checkbutton(features_inner, text="🎵 媒体控制", variable=self.var_media,
                       bg="#313244", fg="#cdd6f4", selectcolor="#45475a",
                       activebackground="#313244", activeforeground="#cdd6f4",
                       font=("Microsoft YaHei UI", 9)).pack(side="left")

        # ===== 控制按钮区 =====
        ctrl_frame = tk.Frame(self.root, bg=bg, pady=5)
        ctrl_frame.pack(fill="x", padx=15)

        self.start_btn = ttk.Button(ctrl_frame, text="▶ 启动服务", style="Green.TButton",
                                    command=self._start_service)
        self.start_btn.pack(side="left", padx=(0, 10))

        self.stop_btn = ttk.Button(ctrl_frame, text="⏹ 停止服务", style="Red.TButton",
                                   command=self._stop_service, state="disabled")
        self.stop_btn.pack(side="left", padx=(0, 10))

        self.status_label = ttk.Label(ctrl_frame, text="● 未运行", style="Bg.TLabel",
                                      font=("Microsoft YaHei UI", 10))
        self.status_label.pack(side="left", padx=(10, 0))

        # ===== 日志区 =====
        log_frame = ttk.LabelFrame(self.root, text="📋 运行日志", style="Section.TLabelframe", padding=10)
        log_frame.pack(fill="both", expand=True, padx=15, pady=(5, 15))

        self.log_text = scrolledtext.ScrolledText(
            log_frame, height=12, bg="#181825", fg="#cdd6f4",
            font=("Consolas", 9), insertbackground="#cdd6f4",
            selectbackground="#45475a", relief="flat", borderwidth=0
        )
        self.log_text.pack(fill="both", expand=True)
        self.log_text.configure(state="disabled")

        # 初始日志
        self._log("欢迎使用小智 MCP 电脑控制！")
        self._log("请先配置 MCP 接入点地址，然后点击「启动服务」")
        self._log("─" * 50)

    def _load_config(self) -> dict:
        """加载配置"""
        config = {}

        # 从 .env 读取
        if ENV_FILE.exists():
            for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    if key.strip() == "MCP_ENDPOINT":
                        config["endpoint"] = value.strip()

        # 从 config.json 读取
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    config.update(json.load(f))
            except Exception:
                pass

        return config

    def _save_config(self):
        """保存配置"""
        endpoint = self.endpoint_var.get().strip()
        if not endpoint:
            messagebox.showwarning("提示", "请输入 MCP 接入点地址")
            return

        # 保存到 .env
        env_content = f"# 小智 MCP 接入点地址\nMCP_ENDPOINT={endpoint}\n"
        ENV_FILE.write_text(env_content, encoding="utf-8")

        # 保存到 config.json
        self.config["endpoint"] = endpoint
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)

        self._log(f"✅ 配置已保存")
        messagebox.showinfo("成功", "配置已保存！")

    def _scan_software(self):
        """扫描已安装软件"""
        self._log("🔍 正在扫描已安装软件...")

        def do_scan():
            try:
                # 动态导入并扫描
                sys.path.insert(0, str(PROJECT_DIR))
                from tools.open_app_tool import discovery
                found = discovery.scan_installed()

                self.root.after(0, lambda: self._show_scan_result(found))
            except Exception as e:
                self.root.after(0, lambda: self._log(f"❌ 扫描失败: {e}"))

        threading.Thread(target=do_scan, daemon=True).start()

    def _show_scan_result(self, found: list):
        """显示扫描结果"""
        self._log(f"✅ 共发现 {len(found)} 个已安装软件：")
        for app in found:
            self._log(f"  📦 {app['name']} → {app['path']}")

        # 弹窗显示
        result_text = f"共发现 {len(found)} 个已安装软件：\n\n"
        for app in found:
            result_text += f"✅ {app['name']}\n   {app['path']}\n\n"

        win = tk.Toplevel(self.root)
        win.title("扫描结果")
        win.geometry("600x500")
        win.configure(bg="#1e1e2e")

        text = scrolledtext.ScrolledText(win, bg="#181825", fg="#cdd6f4",
                                         font=("Consolas", 9), relief="flat")
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", result_text)
        text.configure(state="disabled")

    def _start_service(self):
        """启动 MCP 服务"""
        endpoint = self.endpoint_var.get().strip()
        if not endpoint:
            messagebox.showwarning("提示", "请先配置 MCP 接入点地址")
            return

        if "你的token" in endpoint or not endpoint.startswith("wss://"):
            messagebox.showwarning("提示", "请输入有效的 MCP 接入点地址（wss://...）")
            return

        self._log("🚀 正在启动 MCP 服务...")

        # 更新 .env
        env_content = f"# 小智 MCP 接入点地址\nMCP_ENDPOINT={endpoint}\n"
        ENV_FILE.write_text(env_content, encoding="utf-8")

        def run_service():
            try:
                # 启动 mcp_pipe.py
                self.process = subprocess.Popen(
                    [sys.executable, str(PROJECT_DIR / "mcp_pipe.py"), str(PROJECT_DIR / "yo_mcp.py")],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    encoding="utf-8",
                    errors="replace",
                    cwd=str(PROJECT_DIR),
                    env={**os.environ, "PYTHONIOENCODING": "utf-8"}
                )

                self.root.after(0, self._on_service_started)

                # 读取输出
                for line in self.process.stdout:
                    if line:
                        self.root.after(0, lambda l=line.strip(): self._log(f"  {l}"))

                # 进程结束
                self.root.after(0, self._on_service_stopped)

            except Exception as e:
                self.root.after(0, lambda: self._log(f"❌ 启动失败: {e}"))
                self.root.after(0, self._on_service_stopped)

        threading.Thread(target=run_service, daemon=True).start()

    def _on_service_started(self):
        """服务启动成功"""
        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.status_label.configure(text="● 运行中", foreground="#a6e3a1")
        self._log("✅ MCP 服务已启动！")
        self._log("现在可以对小智说话来控制电脑了")
        self._log("─" * 50)

    def _on_service_stopped(self):
        """服务停止"""
        self.is_running = False
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.status_label.configure(text="● 未运行", foreground="#f38ba8")
        self._log("⏹ MCP 服务已停止")

    def _stop_service(self):
        """停止服务"""
        if self.process:
            self._log("正在停止服务...")
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
            self.process = None
        self._on_service_stopped()

    def _log(self, message: str):
        """写入日志"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _on_close(self):
        """窗口关闭"""
        if self.is_running:
            if messagebox.askyesno("确认", "服务正在运行中，确定要退出吗？"):
                self._stop_service()
                self.root.destroy()
        else:
            self.root.destroy()


def main():
    root = tk.Tk()

    # 设置 DPI 感知（Windows）
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = MCPLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
