"""
通用媒体控制工具
支持全局媒体键控制（播放/暂停/上下曲/音量）+ 网易云音乐深度控制
基于 pyautogui 实现，兼容所有音乐播放器
"""

import pyautogui
import subprocess
import platform
import time
import os

system = platform.system()


def register_tool(mcp):
    @mcp.tool()
    def media_control_tool(command: str) -> dict:
        """
        通用媒体控制工具。支持以下语音指令：

        播放控制（兼容所有播放器）：
            '播放' 或 '暂停' — 播放/暂停当前歌曲
            '下一首' 或 '切歌' — 切换到下一首
            '上一首' — 切换到上一首
            '停止' — 停止播放

        音量控制（系统全局）：
            '音量加' 或 '大声一点' — 增大音量
            '音量减' 或 '小声一点' — 减小音量
            '静音' — 静音/取消静音

        网易云音乐专用（需安装网易云）：
            '打开网易云' — 打开网易云音乐客户端
            '播放周杰伦的晴天' — 搜索并播放指定歌曲
            '搜索稻香' — 搜索歌曲
            '歌词' — 显示/隐藏桌面歌词
            '收藏' — 收藏当前歌曲

        参数：command: 用户的语音指令文本
        """
        try:
            cmd = command.strip()

            # === 播放控制（全局媒体键，兼容所有播放器） ===
            if cmd in ('播放', '暂停', '播放暂停', '继续播放', '继续'):
                _media_key('playpause')
                return {"success": True, "result": "已发送播放/暂停指令"}

            if cmd in ('下一首', '切歌', '下一个', '换一首', '下一首歌'):
                _media_key('nexttrack')
                return {"success": True, "result": "已切换到下一首"}

            if cmd in ('上一首', '上一个', '上一首歌'):
                _media_key('prevtrack')
                return {"success": True, "result": "已切换到上一首"}

            if cmd in ('停止', '停止播放'):
                _media_key('stop')
                return {"success": True, "result": "已停止播放"}

            # === 音量控制（系统全局） ===
            if cmd in ('音量加', '大声一点', '音量大一点', '大声些', '调高音量'):
                for _ in range(3):
                    _media_key('volumeup')
                return {"success": True, "result": "已增大音量"}

            if cmd in ('音量减', '小声一点', '音量小一点', '小声些', '调低音量'):
                for _ in range(3):
                    _media_key('volumedown')
                return {"success": True, "result": "已减小音量"}

            if cmd in ('静音', '关闭声音', '别出声'):
                _media_key('volumemute')
                return {"success": True, "result": "已切换静音"}

            # === 网易云音乐专用功能 ===
            if '打开' in cmd and ('网易云' in cmd or '音乐' in cmd):
                return _open_netease()

            if '歌词' in cmd:
                pyautogui.hotkey('ctrl', 'alt', 'd')
                return {"success": True, "result": "已切换桌面歌词显示"}

            if '收藏' in cmd:
                pyautogui.hotkey('ctrl', 'alt', 's')
                return {"success": True, "result": "已收藏当前歌曲"}

            # === 搜索并播放歌曲（网易云） ===
            song_name = None
            for prefix in ('播放', '搜索', '我想听', '来一首', '放一首', '来首', '放首'):
                if prefix in cmd:
                    song_name = cmd.replace(prefix, '').strip()
                    break

            if song_name:
                result = _search_and_play(song_name)
                return result

            # === 未识别的指令 ===
            return {"success": False, "result": f"未识别的指令：{cmd}。请说播放/暂停/下一首/上一首/音量加/音量减/播放歌曲名"}

        except Exception as e:
            return {"success": False, "result": f"执行失败：{str(e)}"}


def _media_key(key):
    """发送 Windows 媒体键"""
    pyautogui.press(key)


# 网易云音乐常见路径
NETEASE_PATHS = [
    r"C:\Program Files\NetEase\CloudMusic\cloudmusic.exe",
    r"D:\CloudMusic\cloudmusic.exe",
    r"F:\网易云\CloudMusic\cloudmusic.exe",
    r"E:\CloudMusic\cloudmusic.exe",
    r"G:\CloudMusic\cloudmusic.exe",
]


def _find_netease() -> str | None:
    """查找网易云音乐安装路径"""
    # 先检查进程是否已运行
    try:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq cloudmusic.exe'],
            capture_output=True, text=True, shell=True
        )
        if 'cloudmusic.exe' in result.stdout:
            return "running"
    except Exception:
        pass

    # 搜索安装路径
    for path in NETEASE_PATHS:
        if os.path.isfile(path):
            return path

    # 尝试 glob 搜索
    import glob
    for pattern in [r"C:\*\CloudMusic\cloudmusic.exe", r"D:\*\CloudMusic\cloudmusic.exe",
                    r"C:\Program Files\NetEase\*\cloudmusic.exe"]:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]

    return None


def _open_netease() -> dict:
    """打开网易云音乐"""
    path = _find_netease()
    if path == "running":
        return {"success": True, "result": "网易云音乐已在运行"}
    elif path:
        subprocess.Popen([path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return {"success": True, "result": "正在打开网易云音乐"}
    else:
        return {"success": False, "result": "未找到网易云音乐，请确认已安装"}


def _is_netease_running() -> bool:
    """检查网易云音乐是否在运行"""
    try:
        result = subprocess.run(
            ['tasklist', '/FI', 'IMAGENAME eq cloudmusic.exe'],
            capture_output=True, text=True, shell=True
        )
        return 'cloudmusic.exe' in result.stdout
    except Exception:
        return False


def _activate_netease_window():
    """激活网易云音乐窗口"""
    try:
        import ctypes

        EnumWindows = ctypes.windll.user32.EnumWindows
        GetWindowTextW = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLengthW = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible
        SetForegroundWindow = ctypes.windll.user32.SetForegroundWindow
        ShowWindow = ctypes.windll.user32.ShowWindow

        target_hwnd = [None]

        def enum_callback(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    GetWindowTextW(hwnd, buff, length + 1)
                    title = buff.value
                    if '网易云音乐' in title or 'cloudmusic' in title.lower():
                        target_hwnd[0] = hwnd
                        return False
            return True

        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        EnumWindows(WNDENUMPROC(enum_callback), 0)

        if target_hwnd[0]:
            ShowWindow(target_hwnd[0], 9)
            SetForegroundWindow(target_hwnd[0])
            return True
        return False
    except Exception:
        return False


def _clipboard_type(text: str):
    """通过剪贴板输入中文文本"""
    try:
        subprocess.run(
            ['powershell', '-command', f'Set-Clipboard -Value "{text}"'],
            capture_output=True, shell=True
        )
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
    except Exception:
        pyautogui.typewrite(text, interval=0.05)


def _search_and_play(song_name: str) -> dict:
    """搜索并播放歌曲（网易云音乐）"""
    try:
        # 确保网易云音乐在运行
        if not _is_netease_running():
            path = _find_netease()
            if path and path != "running":
                subprocess.Popen([path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(5)
            else:
                return {"success": False, "result": "未找到网易云音乐，请先安装"}

        # 激活网易云音乐窗口
        _activate_netease_window()
        time.sleep(0.5)

        # Ctrl+F 打开搜索框
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(0.3)

        # 清空搜索框并输入歌名
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)

        # 使用剪贴板输入中文
        _clipboard_type(song_name)
        time.sleep(0.3)

        # 回车搜索
        pyautogui.press('enter')
        time.sleep(1.5)

        # 点击第一首歌
        screen_w, screen_h = pyautogui.size()
        pyautogui.click(screen_w // 2, screen_h // 2)
        time.sleep(0.3)

        # 双击播放
        pyautogui.doubleClick(screen_w // 2, screen_h // 2)

        return {"success": True, "result": f"正在搜索并播放：{song_name}"}

    except Exception as e:
        return {"success": False, "result": f"搜索播放失败：{str(e)}"}
