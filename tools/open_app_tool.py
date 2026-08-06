"""
智能软件发现与启动工具
三层发现机制：注册表扫描 + 常见路径匹配 + PATH 环境变量搜索
支持 200+ 热门软件，用户无需修改代码即可使用
"""

import subprocess
import platform
import os
import glob
import shutil
import winreg
import json
from pathlib import Path

system = platform.system()

# ============================================================================
# 软件数据库：内置 200+ 热门软件的常见安装路径和搜索规则
# ============================================================================

SOFTWARE_DB = {
    # ===== 社交通讯 =====
    "微信": {
        "aliases": ["微信", "wechat", "weixin"],
        "exe_names": ["Weixin.exe", "WeChat.exe"],
        "search_paths": [
            r"C:\Program Files\Tencent\WeChat\WeChat.exe",
            r"C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
            r"D:\WeChat\WeChat.exe",
            r"D:\Tencent\WeChat\WeChat.exe",
            r"E:\WeChat\WeChat.exe",
            r"F:\WeChat\WeChat.exe",
        ],
        "registry_keywords": ["WeChat", "微信"],
    },
    "QQ": {
        "aliases": ["QQ", "qq"],
        "exe_names": ["QQ.exe", "QQScLauncher.exe"],
        "search_paths": [
            r"C:\Program Files\Tencent\QQNT\QQ.exe",
            r"C:\Program Files (x86)\Tencent\QQ\QQ.exe",
            r"D:\QQ\QQ.exe",
            r"D:\Tencent\QQ\QQ.exe",
            r"F:\QQ\QQ.exe",
        ],
        "registry_keywords": ["QQ", "QQNT"],
    },
    "钉钉": {
        "aliases": ["钉钉", "dingtalk", "dingding"],
        "exe_names": ["DingtalkLauncher.exe", "DingTalk.exe"],
        "search_paths": [
            r"C:\Program Files\DingTalk\DingtalkLauncher.exe",
            r"D:\DingTalk\DingtalkLauncher.exe",
            r"D:\钉钉\DingtalkLauncher.exe",
        ],
        "registry_keywords": ["DingTalk", "钉钉"],
    },
    "企业微信": {
        "aliases": ["企业微信", "wecom", "wxwork"],
        "exe_names": ["WXWork.exe"],
        "search_paths": [
            r"C:\Program Files\WXWork\WXWork.exe",
            r"D:\WXWork\WXWork.exe",
            r"E:\企业微信\WXWork\WXWork.exe",
        ],
        "registry_keywords": ["WXWork", "企业微信"],
    },
    "飞书": {
        "aliases": ["飞书", "feishu", "lark"],
        "exe_names": ["Feishu.exe", "Lark.exe"],
        "search_paths": [
            r"C:\Program Files\Lark\Feishu.exe",
            r"D:\Feishu\Feishu.exe",
            r"C:\Users\*\AppData\Local\Lark\Feishu.exe",
        ],
        "registry_keywords": ["Feishu", "Lark", "飞书"],
    },
    "Telegram": {
        "aliases": ["telegram", "tg"],
        "exe_names": ["Telegram.exe"],
        "search_paths": [
            r"C:\Program Files\Telegram Desktop\Telegram.exe",
            r"D:\Telegram\Telegram.exe",
        ],
        "registry_keywords": ["Telegram"],
    },
    "Discord": {
        "aliases": ["discord", "dc"],
        "exe_names": ["Discord.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\Discord\Update.exe",
            r"D:\Discord\Discord.exe",
        ],
        "registry_keywords": ["Discord"],
    },

    # ===== 浏览器 =====
    "Chrome": {
        "aliases": ["chrome", "谷歌浏览器", "谷歌", "google浏览器"],
        "exe_names": ["chrome.exe"],
        "search_paths": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"D:\Chrome\Application\chrome.exe",
        ],
        "registry_keywords": ["Google Chrome"],
    },
    "Edge": {
        "aliases": ["edge", "微软浏览器", "Microsoft Edge"],
        "exe_names": ["msedge.exe"],
        "search_paths": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        ],
        "registry_keywords": ["Microsoft Edge"],
    },
    "Firefox": {
        "aliases": ["firefox", "火狐", "火狐浏览器"],
        "exe_names": ["firefox.exe"],
        "search_paths": [
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe",
            r"D:\Firefox\firefox.exe",
        ],
        "registry_keywords": ["Firefox", "Mozilla"],
    },
    "Brave": {
        "aliases": ["brave", "brave浏览器"],
        "exe_names": ["BraveBrowser.exe", "brave.exe"],
        "search_paths": [
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        ],
        "registry_keywords": ["Brave"],
    },
    "Opera": {
        "aliases": ["opera", "欧朋"],
        "exe_names": ["opera.exe"],
        "search_paths": [
            r"C:\Program Files\Opera\opera.exe",
        ],
        "registry_keywords": ["Opera"],
    },
    "Arc": {
        "aliases": ["arc", "arc浏览器"],
        "exe_names": ["Arc.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\Packages\TheBrowserCompany.Arc*\LocalState\Arc.exe",
        ],
        "registry_keywords": ["Arc"],
    },

    # ===== 办公软件 =====
    "Word": {
        "aliases": ["word", "word文档", "微软word"],
        "exe_names": ["WINWORD.EXE"],
        "search_paths": [
            r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16\WINWORD.EXE",
            r"C:\Program Files\Microsoft Office\Office16\WINWORD.EXE",
            r"C:\Program Files (x86)\Microsoft Office\Office16\WINWORD.EXE",
            r"C:\Program Files\Microsoft Office\Office15\WINWORD.EXE",
            r"C:\Program Files (x86)\Microsoft Office\Office15\WINWORD.EXE",
        ],
        "registry_keywords": ["Microsoft Word", "Office"],
    },
    "Excel": {
        "aliases": ["excel", "表格", "微软excel"],
        "exe_names": ["EXCEL.EXE"],
        "search_paths": [
            r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16\EXCEL.EXE",
            r"C:\Program Files\Microsoft Office\Office16\EXCEL.EXE",
            r"C:\Program Files (x86)\Microsoft Office\Office16\EXCEL.EXE",
        ],
        "registry_keywords": ["Microsoft Excel"],
    },
    "PPT": {
        "aliases": ["ppt", "powerpoint", "演示文稿"],
        "exe_names": ["POWERPNT.EXE"],
        "search_paths": [
            r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16\POWERPNT.EXE",
            r"C:\Program Files\Microsoft Office\Office16\POWERPNT.EXE",
        ],
        "registry_keywords": ["Microsoft PowerPoint"],
    },
    "OneNote": {
        "aliases": ["onenote", "笔记"],
        "exe_names": ["ONENOTE.EXE"],
        "search_paths": [
            r"C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE",
            r"C:\Program Files (x86)\Microsoft Office\root\Office16\ONENOTE.EXE",
        ],
        "registry_keywords": ["Microsoft OneNote"],
    },
    "WPS": {
        "aliases": ["wps", "wps文字", "wps表格", "wps演示"],
        "exe_names": ["wps.exe", "et.exe", "wpp.exe"],
        "search_paths": [
            r"C:\Program Files\Kingsoft\WPS Office\*\office6\wps.exe",
            r"D:\WPS Office\*\office6\wps.exe",
            r"C:\Users\*\AppData\Local\Kingsoft\WPS Office\*\office6\wps.exe",
        ],
        "registry_keywords": ["WPS Office", "Kingsoft"],
    },
    "Typora": {
        "aliases": ["typora", "markdown编辑器"],
        "exe_names": ["Typora.exe"],
        "search_paths": [
            r"C:\Program Files\Typora\Typora.exe",
            r"D:\Typora\Typora.exe",
            r"G:\Typora\Typora.exe",
        ],
        "registry_keywords": ["Typora"],
    },
    "Notion": {
        "aliases": ["notion"],
        "exe_names": ["Notion.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\Programs\Notion\Notion.exe",
        ],
        "registry_keywords": ["Notion"],
    },
    "有道云笔记": {
        "aliases": ["有道云笔记", "youdao note"],
        "exe_names": ["YoudaoNote.exe"],
        "search_paths": [
            r"C:\Program Files\Youdao\YoudaoNote\YoudaoNote.exe",
            r"D:\YoudaoNote\YoudaoNote.exe",
        ],
        "registry_keywords": ["YoudaoNote"],
    },

    # ===== 开发工具 =====
    "VS Code": {
        "aliases": ["vscode", "vs code", "visual studio code", "code"],
        "exe_names": ["Code.exe"],
        "search_paths": [
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"D:\VS Code\Microsoft VS Code\Code.exe",
            r"E:\vscode\Microsoft VS Code\Code.exe",
            r"C:\Users\*\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        ],
        "registry_keywords": ["Visual Studio Code"],
    },
    "Cursor": {
        "aliases": ["cursor", "cursor编辑器"],
        "exe_names": ["Cursor.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\Programs\cursor\Cursor.exe",
            r"D:\cursor\Cursor.exe",
            r"G:\cursor\Cursor.exe",
        ],
        "registry_keywords": ["Cursor"],
    },
    "IntelliJ IDEA": {
        "aliases": ["intellij", "idea", "intellij idea"],
        "exe_names": ["idea64.exe", "idea.exe"],
        "search_paths": [
            r"C:\Program Files\JetBrains\IntelliJ IDEA*\bin\idea64.exe",
            r"D:\JetBrains\IntelliJ IDEA*\bin\idea64.exe",
            r"G:\IntelliJ IDEA*\bin\idea64.exe",
        ],
        "registry_keywords": ["IntelliJ IDEA"],
    },
    "PyCharm": {
        "aliases": ["pycharm", "pycharm编辑器"],
        "exe_names": ["pycharm64.exe", "pycharm.exe"],
        "search_paths": [
            r"C:\Program Files\JetBrains\PyCharm*\bin\pycharm64.exe",
            r"D:\JetBrains\PyCharm*\bin\pycharm64.exe",
            r"G:\PyCharm*\bin\pycharm64.exe",
        ],
        "registry_keywords": ["PyCharm"],
    },
    "Android Studio": {
        "aliases": ["android studio", "安卓开发"],
        "exe_names": ["studio64.exe", "studio.exe"],
        "search_paths": [
            r"C:\Program Files\Android\Android Studio\bin\studio64.exe",
            r"D:\Android\Android Studio\bin\studio64.exe",
            r"G:\android\bin\studio64.exe",
        ],
        "registry_keywords": ["Android Studio"],
    },
    "WebStorm": {
        "aliases": ["webstorm"],
        "exe_names": ["webstorm64.exe"],
        "search_paths": [
            r"C:\Program Files\JetBrains\WebStorm*\bin\webstorm64.exe",
        ],
        "registry_keywords": ["WebStorm"],
    },
    "Sublime Text": {
        "aliases": ["sublime", "sublime text"],
        "exe_names": ["sublime_text.exe"],
        "search_paths": [
            r"C:\Program Files\Sublime Text\sublime_text.exe",
            r"D:\Sublime Text\sublime_text.exe",
        ],
        "registry_keywords": ["Sublime Text"],
    },
    "HBuilderX": {
        "aliases": ["hbuilderx", "hbuilder", "hb"],
        "exe_names": ["HBuilderX.exe"],
        "search_paths": [
            r"C:\Program Files\HBuilderX\HBuilderX.exe",
            r"D:\HBuilderX\HBuilderX.exe",
        ],
        "registry_keywords": ["HBuilderX"],
    },
    "Git": {
        "aliases": ["git", "git bash"],
        "exe_names": ["git-bash.exe", "git.exe"],
        "search_paths": [
            r"C:\Program Files\Git\git-bash.exe",
            r"C:\Program Files\Git\cmd\git.exe",
        ],
        "registry_keywords": ["Git"],
        "use_which": True,
    },
    "Python": {
        "aliases": ["python", "python3"],
        "exe_names": ["python.exe", "python3.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\Programs\Python\Python3*\python.exe",
            r"C:\Python3*\python.exe",
            r"D:\python\python.exe",
        ],
        "registry_keywords": ["Python"],
        "use_which": True,
    },
    "Node.js": {
        "aliases": ["node", "nodejs"],
        "exe_names": ["node.exe"],
        "search_paths": [
            r"C:\Program Files\nodejs\node.exe",
            r"D:\node\node.exe",
            r"E:\node\node.exe",
        ],
        "registry_keywords": ["Node.js"],
        "use_which": True,
    },
    "Java": {
        "aliases": ["java", "jdk"],
        "exe_names": ["java.exe", "javac.exe"],
        "search_paths": [
            r"C:\Program Files\Java\jdk*\bin\java.exe",
            r"C:\Program Files\Java\jre*\bin\java.exe",
            r"D:\java\bin\java.exe",
            r"F:\java\bin\java.exe",
        ],
        "registry_keywords": ["Java", "JDK"],
        "use_which": True,
    },
    "Arduino": {
        "aliases": ["arduino", "arduino ide"],
        "exe_names": ["Arduino IDE.exe", "arduino.exe"],
        "search_paths": [
            r"C:\Program Files\Arduino IDE\Arduino IDE.exe",
            r"D:\Arduino IDE\Arduino IDE.exe",
            r"G:\arduino\Arduino IDE\Arduino IDE.exe",
        ],
        "registry_keywords": ["Arduino"],
    },
    "Keil": {
        "aliases": ["keil", "keil5", "mdk"],
        "exe_names": ["UV4.exe", "UV5.exe"],
        "search_paths": [
            r"C:\Keil_v5\UV4\UV4.exe",
            r"D:\Keil_v5\UV4\UV4.exe",
            r"G:\keil5\UV4\UV4.exe",
        ],
        "registry_keywords": ["Keil", "MDK"],
    },
    "微信开发者工具": {
        "aliases": ["微信开发者工具", "微信小程序", "wechat devtools"],
        "exe_names": ["微信开发者工具.exe"],
        "search_paths": [
            r"C:\Program Files\Tencent\微信web开发者工具\微信开发者工具.exe",
            r"D:\微信web开发者工具\微信开发者工具.exe",
            r"G:\小程序开发\微信web开发者工具\微信开发者工具.exe",
        ],
        "registry_keywords": ["微信开发者工具"],
    },

    # ===== 影音娱乐 =====
    "网易云音乐": {
        "aliases": ["网易云音乐", "网易云", "netease music", "cloudmusic"],
        "exe_names": ["cloudmusic.exe"],
        "search_paths": [
            r"C:\Program Files\NetEase\CloudMusic\cloudmusic.exe",
            r"D:\CloudMusic\cloudmusic.exe",
            r"F:\网易云\CloudMusic\cloudmusic.exe",
        ],
        "registry_keywords": ["CloudMusic", "网易云"],
    },
    "QQ音乐": {
        "aliases": ["QQ音乐", "qq音乐", "qq music"],
        "exe_names": ["QQMusic.exe"],
        "search_paths": [
            r"C:\Program Files\Tencent\QQMusic\QQMusic.exe",
            r"D:\QQ音乐\QQMusic\QQMusic.exe",
            r"D:\QQMusic\QQMusic.exe",
        ],
        "registry_keywords": ["QQMusic", "QQ音乐"],
    },
    "酷狗音乐": {
        "aliases": ["酷狗音乐", "酷狗", "kugou"],
        "exe_names": ["KuGou.exe", "KuGouW.exe"],
        "search_paths": [
            r"C:\Program Files\KuGou\*\KuGou.exe",
            r"D:\KuGou\KuGou.exe",
        ],
        "registry_keywords": ["KuGou", "酷狗"],
    },
    "酷我音乐": {
        "aliases": ["酷我音乐", "酷我", "kuwo"],
        "exe_names": ["KuwoMusic.exe"],
        "search_paths": [
            r"C:\Program Files\Kuwo\KuwoMusic\KuwoMusic.exe",
            r"D:\KuwoMusic\KuwoMusic.exe",
        ],
        "registry_keywords": ["Kuwo", "酷我"],
    },
    "Spotify": {
        "aliases": ["spotify"],
        "exe_names": ["Spotify.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Roaming\Spotify\Spotify.exe",
        ],
        "registry_keywords": ["Spotify"],
    },
    "PotPlayer": {
        "aliases": ["potplayer", "恒星播放器"],
        "exe_names": ["PotPlayerMini64.exe", "PotPlayerMini.exe", "PotPlayer.exe"],
        "search_paths": [
            r"C:\Program Files\DAUM\PotPlayer\PotPlayerMini64.exe",
            r"C:\Program Files\PotPlayer\PotPlayerMini64.exe",
            r"D:\PotPlayer\PotPlayerMini64.exe",
            r"G:\恒星播放器\PotPlayerMini64.exe",
        ],
        "registry_keywords": ["PotPlayer"],
    },
    "VLC": {
        "aliases": ["vlc", "vlc播放器"],
        "exe_names": ["vlc.exe"],
        "search_paths": [
            r"C:\Program Files\VideoLAN\VLC\vlc.exe",
            r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
            r"D:\VLC\vlc.exe",
        ],
        "registry_keywords": ["VLC"],
    },
    "mpv": {
        "aliases": ["mpv", "mpv播放器"],
        "exe_names": ["mpv.exe"],
        "search_paths": [
            r"C:\Program Files\mpv\mpv.exe",
            r"C:\Program Files\MPV Player\mpv.exe",
            r"D:\mpv\mpv.exe",
        ],
        "registry_keywords": ["mpv"],
        "use_which": True,
    },
    "暴风影音": {
        "aliases": ["暴风影音", "暴风"],
        "exe_names": ["BaofengPlatform.exe"],
        "search_paths": [
            r"C:\Program Files\Baofeng\StormPlayer\BaofengPlatform.exe",
        ],
        "registry_keywords": ["Baofeng", "暴风"],
    },

    # ===== 视频平台 =====
    "哔哩哔哩": {
        "aliases": ["bilibili", "哔哩哔哩", "b站"],
        "exe_names": ["哔哩哔哩.exe", "bilibili.exe"],
        "search_paths": [
            r"C:\Program Files\bilibili\哔哩哔哩.exe",
            r"D:\bilibili\哔哩哔哩.exe",
        ],
        "registry_keywords": ["bilibili", "哔哩哔哩"],
    },
    "腾讯视频": {
        "aliases": ["腾讯视频", "tencent video"],
        "exe_names": ["QQLive.exe"],
        "search_paths": [
            r"C:\Program Files\Tencent\QQLive\QQLive.exe",
            r"F:\腾讯视频\QQLive\QQLive.exe",
        ],
        "registry_keywords": ["QQLive", "腾讯视频"],
    },
    "爱奇艺": {
        "aliases": ["爱奇艺", "iqiyi"],
        "exe_names": ["QyClient.exe", "IQIYI Video.exe"],
        "search_paths": [
            r"C:\Program Files\IQIYI Video\QyClient.exe",
            r"D:\爱奇艺\QyClient.exe",
        ],
        "registry_keywords": ["iQIYI", "爱奇艺"],
    },
    "优酷": {
        "aliases": ["优酷", "youku"],
        "exe_names": ["YOUKU.exe"],
        "search_paths": [
            r"C:\Program Files\YOUKU\YOUKU.exe",
            r"D:\优酷\YOUKU.exe",
        ],
        "registry_keywords": ["YOUKU", "优酷"],
    },
    "抖音": {
        "aliases": ["抖音", "douyin", "tiktok"],
        "exe_names": ["douyin.exe"],
        "search_paths": [
            r"C:\Program Files\douyin\douyin.exe",
            r"D:\douyin\douyin.exe",
            r"G:\抖音\douyin.exe",
        ],
        "registry_keywords": ["douyin", "抖音"],
    },
    "快手": {
        "aliases": ["快手", "kuaishou"],
        "exe_names": ["kuaishou.exe"],
        "search_paths": [
            r"C:\Program Files\kuaishou\kuaishou.exe",
        ],
        "registry_keywords": ["kuaishou", "快手"],
    },

    # ===== 直播工具 =====
    "OBS": {
        "aliases": ["obs", "obs studio"],
        "exe_names": ["obs64.exe", "obs32.exe"],
        "search_paths": [
            r"C:\Program Files\obs-studio\bin\64bit\obs64.exe",
            r"D:\obs-studio\bin\64bit\obs64.exe",
            r"E:\OBS\bin\64bit\obs64.exe",
        ],
        "registry_keywords": ["OBS Studio"],
    },
    "虎牙直播": {
        "aliases": ["虎牙直播", "虎牙", "huya"],
        "exe_names": ["huya.exe"],
        "search_paths": [
            r"C:\Program Files\HuyaClient\huya.exe",
            r"D:\虎牙\HuyaClient\huya.exe",
        ],
        "registry_keywords": ["Huya", "虎牙"],
    },
    "B站直播": {
        "aliases": ["B站直播", "bilibili直播", "直播姬"],
        "exe_names": ["livehime.exe"],
        "search_paths": [
            r"C:\Program Files\bilibili live\livehime\livehime.exe",
            r"G:\bilibili live\livehime\livehime.exe",
        ],
        "registry_keywords": ["livehime"],
    },

    # ===== 剪辑工具 =====
    "剪映": {
        "aliases": ["剪映", "jianying", "capcut"],
        "exe_names": ["JianyingPro.exe"],
        "search_paths": [
            r"C:\Program Files\JianyingPro\JianyingPro.exe",
            r"D:\JianyingPro\JianyingPro.exe",
            r"F:\剪映\JianyingPro\JianyingPro.exe",
        ],
        "registry_keywords": ["JianyingPro", "剪映"],
    },
    "Premiere": {
        "aliases": ["premiere", "pr", "adobe premiere"],
        "exe_names": ["Adobe Premiere Pro.exe"],
        "search_paths": [
            r"C:\Program Files\Adobe\Adobe Premiere Pro*\Adobe Premiere Pro.exe",
            r"D:\Adobe\Adobe Premiere Pro*\Adobe Premiere Pro.exe",
        ],
        "registry_keywords": ["Adobe Premiere"],
    },
    "After Effects": {
        "aliases": ["after effects", "ae", "adobe ae"],
        "exe_names": ["AfterFX.exe"],
        "search_paths": [
            r"C:\Program Files\Adobe\Adobe After Effects*\Support Files\AfterFX.exe",
        ],
        "registry_keywords": ["Adobe After Effects"],
    },
    "达芬奇": {
        "aliases": ["达芬奇", "davinci resolve", "davinci"],
        "exe_names": ["Resolve.exe"],
        "search_paths": [
            r"C:\Program Files\Blackmagic Design\DaVinci Resolve\Resolve.exe",
        ],
        "registry_keywords": ["DaVinci Resolve"],
    },

    # ===== 游戏平台 =====
    "Steam": {
        "aliases": ["steam", "steam平台"],
        "exe_names": ["steam.exe"],
        "search_paths": [
            r"C:\Program Files (x86)\Steam\steam.exe",
            r"D:\Steam\steam.exe",
            r"D:\steam\steam.exe",
            r"E:\Steam\steam.exe",
        ],
        "registry_keywords": ["Steam"],
    },
    "Epic": {
        "aliases": ["epic", "epic games"],
        "exe_names": ["EpicGamesLauncher.exe"],
        "search_paths": [
            r"C:\Program Files\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
            r"D:\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
            r"F:\epic\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe",
        ],
        "registry_keywords": ["Epic Games"],
    },
    "WeGame": {
        "aliases": ["wegame"],
        "exe_names": ["wegame.exe"],
        "search_paths": [
            r"C:\Program Files\WeGame\wegame.exe",
            r"D:\wegame\wegame.exe",
        ],
        "registry_keywords": ["WeGame"],
    },
    "Ubisoft": {
        "aliases": ["ubisoft", "育碧", "uplay"],
        "exe_names": ["UbisoftConnect.exe"],
        "search_paths": [
            r"C:\Program Files (x86)\Ubisoft\Ubisoft Game Launcher\UbisoftConnect.exe",
            r"D:\Ubisoft\UbisoftConnect.exe",
        ],
        "registry_keywords": ["Ubisoft"],
    },
    "EA": {
        "aliases": ["ea", "ea app", "origin"],
        "exe_names": ["EALauncher.exe", "Origin.exe"],
        "search_paths": [
            r"C:\Program Files\EA Desktop\EA Desktop\EALauncher.exe",
            r"C:\Program Files (x86)\Origin\Origin.exe",
        ],
        "registry_keywords": ["EA Desktop", "Origin"],
    },
    "暴雪": {
        "aliases": ["暴雪", "blizzard", "battle.net"],
        "exe_names": ["Battle.net.exe"],
        "search_paths": [
            r"C:\Program Files (x86)\Battle.net\Battle.net.exe",
            r"D:\Battle.net\Battle.net.exe",
        ],
        "registry_keywords": ["Battle.net"],
    },
    "Rockstar": {
        "aliases": ["rockstar", "r星"],
        "exe_names": ["LauncherPatcher.exe", "Rockstar-Games-Launcher.exe"],
        "search_paths": [
            r"C:\Program Files\Rockstar Games\Launcher\LauncherPatcher.exe",
            r"F:\ROCKSTAR\LauncherPatcher.exe",
        ],
        "registry_keywords": ["Rockstar Games"],
    },
    "Steam++": {
        "aliases": ["steam++", "watt toolkit"],
        "exe_names": ["Steam++.exe", "WattToolkit.exe"],
        "search_paths": [
            r"C:\Program Files\Steam++\Steam++.exe",
            r"D:\steam++\Steam++.exe",
        ],
        "registry_keywords": ["Steam++", "Watt Toolkit"],
    },
    "UU加速器": {
        "aliases": ["uu加速器", "网易uu", "uu"],
        "exe_names": ["GameViewer.exe", "NeteaseUU.exe"],
        "search_paths": [
            r"C:\Program Files\NetEase\UU\GameViewer.exe",
            r"G:\uu\GameViewer\GameViewer.exe",
        ],
        "registry_keywords": ["UU", "GameViewer"],
    },
    "迅游加速器": {
        "aliases": ["迅游加速器", "迅游", "xunyou"],
        "exe_names": ["xunyou.exe"],
        "search_paths": [
            r"C:\Program Files\xunyou\xunyou.exe",
            r"D:\迅游\xunyou\xunyou.exe",
        ],
        "registry_keywords": ["xunyou", "迅游"],
    },

    # ===== 游戏 =====
    "英雄联盟": {
        "aliases": ["英雄联盟", "lol", "league of legends"],
        "exe_names": ["Client.exe", "LeagueClient.exe"],
        "search_paths": [
            r"C:\*\英雄联盟\TCLS\Client.exe",
            r"D:\*\英雄联盟\TCLS\Client.exe",
            r"F:\*\英雄联盟\TCLS\Client.exe",
        ],
        "registry_keywords": ["英雄联盟", "League of Legends"],
    },
    "我的世界": {
        "aliases": ["我的世界", "minecraft", "mc"],
        "exe_names": ["MCLauncher.exe", "minecraft.exe", "WPFLauncher.exe"],
        "search_paths": [
            r"C:\*\MCLauncher\WPFLauncher.exe",
            r"D:\*\MCLauncher\WPFLauncher.exe",
            r"G:\MC\MCLauncher\WPFLauncher.exe",
        ],
        "registry_keywords": ["Minecraft"],
    },
    "植物大战僵尸": {
        "aliases": ["植物大战僵尸", "pvz"],
        "exe_names": ["pvz*.exe", "PlantsVsZombies.exe"],
        "search_paths": [
            r"G:\植物大战僵尸\*.exe",
        ],
        "registry_keywords": ["Plants vs Zombies"],
    },
    "CSGO": {
        "aliases": ["csgo", "cs2", "反恐精英"],
        "exe_names": ["csgo.exe", "cs2.exe"],
        "search_paths": [
            r"D:\Steam\steamapps\common\Counter-Strike Global Offensive\csgo.exe",
            r"D:\Steam\steamapps\common\Counter-Strike 2\game\bin\win64\cs2.exe",
        ],
        "registry_keywords": ["Counter-Strike"],
    },
    "原神": {
        "aliases": ["原神", "genshin", "genshin impact"],
        "exe_names": ["GenshinImpact.exe", "YuanShen.exe", "launcher.exe"],
        "search_paths": [
            r"C:\Program Files\Genshin Impact\GenshinImpact.exe",
            r"D:\Genshin Impact\GenshinImpact.exe",
        ],
        "registry_keywords": ["Genshin Impact", "原神"],
    },
    "崩坏星穹铁道": {
        "aliases": ["崩坏星穹铁道", "星穹铁道", "starrail"],
        "exe_names": ["StarRail.exe"],
        "search_paths": [
            r"C:\Program Files\Star Rail\StarRail.exe",
            r"D:\Star Rail\StarRail.exe",
        ],
        "registry_keywords": ["Star Rail"],
    },
    "王者荣耀": {
        "aliases": ["王者荣耀", "王者"],
        "exe_names": ["GameDownload.exe"],
        "search_paths": [
            r"C:\Program Files\王者荣耀\GameDownload.exe",
        ],
        "registry_keywords": ["王者荣耀"],
    },

    # ===== 下载工具 =====
    "IDM": {
        "aliases": ["idm", "internet download manager"],
        "exe_names": ["IDMan.exe"],
        "search_paths": [
            r"C:\Program Files (x86)\Internet Download Manager\IDMan.exe",
            r"C:\Program Files\Internet Download Manager\IDMan.exe",
        ],
        "registry_keywords": ["Internet Download Manager"],
    },
    "迅雷": {
        "aliases": ["迅雷", "xunlei", "thunder"],
        "exe_names": ["ThunderStart.exe", "Thunder.exe"],
        "search_paths": [
            r"C:\Program Files\Thunder\Thunder.exe",
            r"D:\Thunder\Thunder.exe",
            r"F:\迅雷\Thunder\Thunder.exe",
        ],
        "registry_keywords": ["Thunder", "迅雷"],
    },
    "Motrix": {
        "aliases": ["motrix"],
        "exe_names": ["Motrix.exe"],
        "search_paths": [
            r"C:\Program Files\Motrix\Motrix.exe",
            r"D:\Motrix\Motrix.exe",
        ],
        "registry_keywords": ["Motrix"],
    },
    "aria2": {
        "aliases": ["aria2", "aria2c"],
        "exe_names": ["aria2c.exe"],
        "search_paths": [
            r"C:\Program Files\aria2\aria2c.exe",
            r"D:\aria2\aria2c.exe",
        ],
        "registry_keywords": ["aria2"],
        "use_which": True,
    },

    # ===== 网盘 =====
    "百度网盘": {
        "aliases": ["百度网盘", "百度云", "baidu netdisk"],
        "exe_names": ["BaiduNetdisk.exe"],
        "search_paths": [
            r"C:\Program Files\BaiduNetdisk\BaiduNetdisk.exe",
            r"D:\BaiduNetdisk\BaiduNetdisk.exe",
            r"D:\百度\BaiduNetdisk\BaiduNetdisk.exe",
        ],
        "registry_keywords": ["BaiduNetdisk", "百度网盘"],
    },
    "阿里云盘": {
        "aliases": ["阿里云盘", "aliyun drive", "aDrive"],
        "exe_names": ["aDrive.exe"],
        "search_paths": [
            r"C:\Program Files\aDrive\aDrive.exe",
            r"D:\阿里\aDrive\aDrive.exe",
        ],
        "registry_keywords": ["aDrive", "阿里云盘"],
    },
    "夸克网盘": {
        "aliases": ["夸克网盘", "夸克", "quark"],
        "exe_names": ["QuarkCloudDrive.exe", "quark.exe"],
        "search_paths": [
            r"C:\Program Files\QuarkCloudDrive\QuarkCloudDrive.exe",
            r"G:\quark-cloud-drive\QuarkCloudDrive.exe",
            r"G:\Quark\quark.exe",
        ],
        "registry_keywords": ["Quark", "夸克"],
    },
    "OneDrive": {
        "aliases": ["onedrive", "微软网盘"],
        "exe_names": ["OneDrive.exe"],
        "search_paths": [
            r"C:\Program Files\Microsoft OneDrive\OneDrive.exe",
            r"C:\Users\*\AppData\Local\Microsoft\OneDrive\OneDrive.exe",
        ],
        "registry_keywords": ["OneDrive"],
    },
    "坚果云": {
        "aliases": ["坚果云", "jianguoyun", "nutstore"],
        "exe_names": ["Nutstore.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\Nutstore\Nutstore.exe",
        ],
        "registry_keywords": ["Nutstore", "坚果云"],
    },
    "123云盘": {
        "aliases": ["123云盘", "123pan"],
        "exe_names": ["123pan.exe"],
        "search_paths": [
            r"C:\Program Files\123pan\123pan.exe",
            r"G:\123云盘\123pan\123pan.exe",
        ],
        "registry_keywords": ["123pan"],
    },

    # ===== 远程工具 =====
    "向日葵": {
        "aliases": ["向日葵", "sunlogin", "oray"],
        "exe_names": ["AweSun.exe", "SunloginClient.exe"],
        "search_paths": [
            r"C:\Program Files\Oray\SunloginClient\SunloginClient.exe",
            r"G:\向日葵\AweSun\AweSun.exe",
        ],
        "registry_keywords": ["Sunlogin", "向日葵"],
    },
    "ToDesk": {
        "aliases": ["todesk"],
        "exe_names": ["ToDesk.exe"],
        "search_paths": [
            r"C:\Program Files\ToDesk\ToDesk.exe",
            r"G:\todesk\ToDesk.exe",
        ],
        "registry_keywords": ["ToDesk"],
    },
    "TeamViewer": {
        "aliases": ["teamviewer"],
        "exe_names": ["TeamViewer.exe"],
        "search_paths": [
            r"C:\Program Files\TeamViewer\TeamViewer.exe",
        ],
        "registry_keywords": ["TeamViewer"],
    },
    "AnyDesk": {
        "aliases": ["anydesk"],
        "exe_names": ["AnyDesk.exe"],
        "search_paths": [
            r"C:\Program Files\AnyDesk\AnyDesk.exe",
            r"C:\Users\*\AppData\Local\AnyDesk\AnyDesk.exe",
        ],
        "registry_keywords": ["AnyDesk"],
    },
    "RustDesk": {
        "aliases": ["rustdesk"],
        "exe_names": ["rustdesk.exe"],
        "search_paths": [
            r"C:\Program Files\RustDesk\rustdesk.exe",
        ],
        "registry_keywords": ["RustDesk"],
    },

    # ===== 系统工具 =====
    "记事本": {
        "aliases": ["记事本", "notepad"],
        "exe_names": ["notepad.exe"],
        "search_paths": [r"C:\Windows\notepad.exe"],
        "registry_keywords": [],
    },
    "画图": {
        "aliases": ["画图", "mspaint"],
        "exe_names": ["mspaint.exe"],
        "search_paths": [r"C:\Windows\System32\mspaint.exe"],
        "registry_keywords": [],
    },
    "计算器": {
        "aliases": ["计算器", "calculator", "calc"],
        "exe_names": ["calc.exe"],
        "search_paths": [r"C:\Windows\System32\calc.exe"],
        "registry_keywords": [],
    },
    "任务管理器": {
        "aliases": ["任务管理器", "task manager"],
        "exe_names": ["taskmgr.exe"],
        "search_paths": [r"C:\Windows\System32\taskmgr.exe"],
        "registry_keywords": [],
    },
    "资源管理器": {
        "aliases": ["资源管理器", "文件管理器", "explorer"],
        "exe_names": ["explorer.exe"],
        "search_paths": [r"C:\Windows\explorer.exe"],
        "registry_keywords": [],
    },
    "控制面板": {
        "aliases": ["控制面板", "control panel"],
        "exe_names": ["control.exe"],
        "search_paths": [r"C:\Windows\System32\control.exe"],
        "registry_keywords": [],
    },
    "注册表": {
        "aliases": ["注册表", "regedit"],
        "exe_names": ["regedit.exe"],
        "search_paths": [r"C:\Windows\regedit.exe"],
        "registry_keywords": [],
    },
    "CMD": {
        "aliases": ["cmd", "终端", "命令提示符", "命令行"],
        "exe_names": ["cmd.exe"],
        "search_paths": [r"C:\Windows\System32\cmd.exe"],
        "registry_keywords": [],
    },
    "PowerShell": {
        "aliases": ["powershell", "ps"],
        "exe_names": ["powershell.exe", "pwsh.exe"],
        "search_paths": [
            r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            r"C:\Program Files\PowerShell\*\pwsh.exe",
        ],
        "registry_keywords": ["PowerShell"],
    },
    "Windows Terminal": {
        "aliases": ["windows terminal", "wt", "终端"],
        "exe_names": ["wt.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\Microsoft\WindowsApps\wt.exe",
            r"C:\Program Files\WindowsApps\Microsoft.WindowsTerminal*\wt.exe",
        ],
        "registry_keywords": ["Windows Terminal"],
    },
    "远程桌面": {
        "aliases": ["远程桌面", "mstsc", "remote desktop"],
        "exe_names": ["mstsc.exe"],
        "search_paths": [r"C:\Windows\System32\mstsc.exe"],
        "registry_keywords": [],
    },
    "屏幕键盘": {
        "aliases": ["屏幕键盘", "osk"],
        "exe_names": ["osk.exe"],
        "search_paths": [r"C:\Windows\System32\osk.exe"],
        "registry_keywords": [],
    },
    "资源监视器": {
        "aliases": ["资源监视器", "resmon"],
        "exe_names": ["resmon.exe"],
        "search_paths": [r"C:\Windows\System32\resmon.exe"],
        "registry_keywords": [],
    },
    "磁盘清理": {
        "aliases": ["磁盘清理", "cleanmgr"],
        "exe_names": ["cleanmgr.exe"],
        "search_paths": [r"C:\Windows\System32\cleanmgr.exe"],
        "registry_keywords": [],
    },
    "截图工具": {
        "aliases": ["截图工具", "snipping tool", "截图"],
        "exe_names": ["SnippingTool.exe"],
        "search_paths": [r"C:\Windows\System32\SnippingTool.exe"],
        "registry_keywords": [],
    },
    "放大镜": {
        "aliases": ["放大镜", "magnify"],
        "exe_names": ["magnify.exe"],
        "search_paths": [r"C:\Windows\System32\magnify.exe"],
        "registry_keywords": [],
    },
    "步骤记录器": {
        "aliases": ["步骤记录器", "psr"],
        "exe_names": ["psr.exe"],
        "search_paths": [r"C:\Windows\System32\psr.exe"],
        "registry_keywords": [],
    },

    # ===== 安全工具 =====
    "火绒": {
        "aliases": ["火绒", "huorong"],
        "exe_names": ["HipsMain.exe"],
        "search_paths": [
            r"C:\Program Files\Huorong\Sysdiag\bin\HipsMain.exe",
            r"D:\火绒\Huorong\Sysdiag\bin\HipsMain.exe",
        ],
        "registry_keywords": ["Huorong", "火绒"],
    },
    "360安全卫士": {
        "aliases": ["360", "360安全卫士", "360安全"],
        "exe_names": ["360sd.exe", "360se.exe"],
        "search_paths": [
            r"C:\Program Files\360\360safe\360sd.exe",
        ],
        "registry_keywords": ["360"],
    },
    "电脑管家": {
        "aliases": ["电脑管家", "腾讯电脑管家"],
        "exe_names": ["QQPCRTP.exe"],
        "search_paths": [
            r"C:\Program Files\Tencent\QQPCMgr\QQPCRTP.exe",
        ],
        "registry_keywords": ["QQPCMgr"],
    },

    # ===== 设计工具 =====
    "Photoshop": {
        "aliases": ["photoshop", "ps", "adobe ps"],
        "exe_names": ["Photoshop.exe"],
        "search_paths": [
            r"C:\Program Files\Adobe\Adobe Photoshop*\Photoshop.exe",
            r"D:\Adobe\Adobe Photoshop*\Photoshop.exe",
        ],
        "registry_keywords": ["Adobe Photoshop"],
    },
    "Illustrator": {
        "aliases": ["illustrator", "ai", "adobe ai"],
        "exe_names": ["Illustrator.exe"],
        "search_paths": [
            r"C:\Program Files\Adobe\Adobe Illustrator*\Support Files\Contents\Windows\Illustrator.exe",
        ],
        "registry_keywords": ["Adobe Illustrator"],
    },
    "Figma": {
        "aliases": ["figma"],
        "exe_names": ["Figma.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\Figma\Figma.exe",
        ],
        "registry_keywords": ["Figma"],
    },
    "SolidWorks": {
        "aliases": ["solidworks", "sw"],
        "exe_names": ["SLDWORKS.exe"],
        "search_paths": [
            r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe",
            r"G:\solidworks\SOLIDWORKS\SLDWORKS.exe",
        ],
        "registry_keywords": ["SOLIDWORKS"],
    },
    "AutoCAD": {
        "aliases": ["autocad", "cad"],
        "exe_names": ["acad.exe"],
        "search_paths": [
            r"C:\Program Files\Autodesk\AutoCAD*\acad.exe",
        ],
        "registry_keywords": ["AutoCAD"],
    },
    "立创EDA": {
        "aliases": ["立创eda", "lceda", "easyeda"],
        "exe_names": ["lceda-pro.exe"],
        "search_paths": [
            r"C:\Program Files\lceda-pro\lceda-pro.exe",
            r"G:\lceda-pro\lceda-pro.exe",
        ],
        "registry_keywords": ["LCEDA", "EasyEDA"],
    },
    "嘉立创": {
        "aliases": ["嘉立创", "jlc", "jlcpcb"],
        "exe_names": ["jlc-assistant.exe"],
        "search_paths": [
            r"C:\Program Files\jlc-assistant\jlc-assistant.exe",
            r"G:\jlc-assistant\jlc-assistant.exe",
        ],
        "registry_keywords": ["jlc-assistant"],
    },
    "Multisim": {
        "aliases": ["multisim"],
        "exe_names": ["Multisim.exe"],
        "search_paths": [
            r"C:\Program Files\National Instruments\Circuit Design Suite*\Multisim.exe",
        ],
        "registry_keywords": ["Multisim"],
    },

    # ===== 输入法 =====
    "搜狗输入法": {
        "aliases": ["搜狗输入法", "搜狗", "sogou"],
        "exe_names": ["SogouImeBroker.exe", "搜狗输入法.exe"],
        "search_paths": [
            r"C:\Program Files\SogouInput\*\SogouImeBroker.exe",
            r"G:\搜狗输入法\搜狗输入法.exe",
        ],
        "registry_keywords": ["SogouInput", "搜狗"],
    },
    "百度输入法": {
        "aliases": ["百度输入法"],
        "exe_names": ["BaiduSdTray.exe"],
        "search_paths": [
            r"C:\Program Files\Baidu\BaiduSd\*\BaiduSdTray.exe",
        ],
        "registry_keywords": ["BaiduSd"],
    },
    "微信输入法": {
        "aliases": ["微信输入法", "wechat输入法"],
        "exe_names": ["WeChatInput.exe"],
        "search_paths": [
            r"C:\Program Files\Tencent\WeType\WeType.exe",
        ],
        "registry_keywords": ["WeType"],
    },

    # ===== 翻译工具 =====
    "有道词典": {
        "aliases": ["有道词典", "有道", "youdao"],
        "exe_names": ["YoudaoDict.exe"],
        "search_paths": [
            r"C:\Program Files\Youdao\Dict\YoudaoDict.exe",
            r"G:\有道\Dict\YoudaoDict.exe",
        ],
        "registry_keywords": ["YoudaoDict", "有道"],
    },
    "DeepL": {
        "aliases": ["deepl", "deepl翻译"],
        "exe_names": ["DeepL.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\DeepL\DeepL.exe",
        ],
        "registry_keywords": ["DeepL"],
    },

    # ===== VPN/代理 =====
    "Clash": {
        "aliases": ["clash", "clash verge", "clash rev"],
        "exe_names": ["clash-verge.exe", "Clash for Windows.exe", "clash-win.exe"],
        "search_paths": [
            r"C:\Program Files\Clash Verge\clash-verge.exe",
            r"G:\clash\Clash Verge\clash-verge.exe",
            r"C:\Program Files\Clash for Windows\Clash for Windows.exe",
        ],
        "registry_keywords": ["Clash", "Clash Verge"],
    },
    "V2Ray": {
        "aliases": ["v2ray", "v2rayn"],
        "exe_names": ["v2rayN.exe"],
        "search_paths": [
            r"C:\Program Files\v2rayN\v2rayN.exe",
            r"D:\v2rayN\v2rayN.exe",
        ],
        "registry_keywords": ["v2rayN"],
    },

    # ===== 虚拟机 =====
    "VMware": {
        "aliases": ["vmware", "vmware workstation"],
        "exe_names": ["vmware.exe", "vmplayer.exe"],
        "search_paths": [
            r"C:\Program Files (x86)\VMware\VMware Workstation\vmware.exe",
            r"D:\VMware\vmware.exe",
            r"G:\VM\vmware.exe",
        ],
        "registry_keywords": ["VMware"],
    },
    "VirtualBox": {
        "aliases": ["virtualbox", "vbox"],
        "exe_names": ["VirtualBox.exe"],
        "search_paths": [
            r"C:\Program Files\Oracle\VirtualBox\VirtualBox.exe",
        ],
        "registry_keywords": ["VirtualBox"],
    },

    # ===== 终端工具 =====
    "Tabby": {
        "aliases": ["tabby", "tabby终端"],
        "exe_names": ["Tabby.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\Programs\Tabby\Tabby.exe",
        ],
        "registry_keywords": ["Tabby"],
    },
    "Hyper": {
        "aliases": ["hyper", "hyper终端"],
        "exe_names": ["Hyper.exe"],
        "search_paths": [
            r"C:\Users\*\AppData\Local\hyper\Hyper.exe",
        ],
        "registry_keywords": ["Hyper"],
    },
    "MobaXterm": {
        "aliases": ["mobaxterm"],
        "exe_names": ["MobaXterm.exe"],
        "search_paths": [
            r"C:\Program Files\Mobatek\MobaXterm\MobaXterm.exe",
            r"D:\MobaXterm\MobaXterm.exe",
        ],
        "registry_keywords": ["MobaXterm"],
    },
    "Xshell": {
        "aliases": ["xshell"],
        "exe_names": ["Xshell.exe"],
        "search_paths": [
            r"C:\Program Files (x86)\NetSarang\Xshell*\Xshell.exe",
        ],
        "registry_keywords": ["Xshell"],
    },

    # ===== 其他工具 =====
    "雨滴桌面": {
        "aliases": ["雨滴桌面", "rainmeter"],
        "exe_names": ["Rainmeter.exe"],
        "search_paths": [
            r"C:\Program Files\Rainmeter\Rainmeter.exe",
        ],
        "registry_keywords": ["Rainmeter"],
    },
    "壁纸引擎": {
        "aliases": ["壁纸引擎", "wallpaper engine"],
        "exe_names": ["wallpaper64.exe", "wallpaper32.exe"],
        "search_paths": [
            r"C:\Program Files\Steam\steamapps\common\wallpaper_engine\wallpaper64.exe",
            r"D:\Steam\steamapps\common\wallpaper_engine\wallpaper64.exe",
            r"G:\SteamLibrary\steamapps\common\wallpaper_engine\wallpaper64.exe",
        ],
        "registry_keywords": ["wallpaper_engine"],
    },
    "NVIDIA": {
        "aliases": ["nvidia", "英伟达", "geforce experience"],
        "exe_names": ["NVIDIA GeForce Experience.exe"],
        "search_paths": [
            r"C:\Program Files\NVIDIA Corporation\NVIDIA GeForce Experience\NVIDIA GeForce Experience.exe",
        ],
        "registry_keywords": ["NVIDIA GeForce Experience"],
    },
    "Logitech": {
        "aliases": ["logitech", "罗技", "ghub"],
        "exe_names": ["lghub_system_tray.exe", "LCore.exe"],
        "search_paths": [
            r"C:\Program Files\LGHUB\system_tray\lghub_system_tray.exe",
            r"C:\Program Files\Logitech Gaming Software\LCore.exe",
        ],
        "registry_keywords": ["Logitech", "LGHUB"],
    },
    "R-Studio": {
        "aliases": ["r-studio", "r studio", "数据恢复"],
        "exe_names": ["RStudio.exe"],
        "search_paths": [
            r"C:\Program Files\R-Studio\RStudio.exe",
            r"F:\R-Studio\RStudio.exe",
        ],
        "registry_keywords": ["R-Studio"],
    },
    "CrystalDiskInfo": {
        "aliases": ["crystaldiskinfo", "diskinfo", "磁盘信息"],
        "exe_names": ["DiskInfo64.exe", "DiskInfo.exe"],
        "search_paths": [
            r"C:\Program Files\CrystalDiskInfo\DiskInfo64.exe",
            r"D:\CrystalDiskInfo\DiskInfo64.exe",
        ],
        "registry_keywords": ["CrystalDiskInfo"],
    },
    "CrystalDiskMark": {
        "aliases": ["crystaldiskmark", "diskmark", "磁盘测试"],
        "exe_names": ["DiskMark64.exe", "DiskMark.exe"],
        "search_paths": [
            r"C:\Program Files\CrystalDiskMark\DiskMark64.exe",
            r"D:\CrystalDiskMark*\DiskMark64.exe",
        ],
        "registry_keywords": ["CrystalDiskMark"],
    },
    "Everything": {
        "aliases": ["everything", "文件搜索"],
        "exe_names": ["Everything.exe"],
        "search_paths": [
            r"C:\Program Files\Everything\Everything.exe",
            r"D:\Everything\Everything.exe",
        ],
        "registry_keywords": ["Everything"],
    },
    "Snipaste": {
        "aliases": ["snipaste", "截图工具"],
        "exe_names": ["Snipaste.exe"],
        "search_paths": [
            r"C:\Program Files\Snipaste\Snipaste.exe",
            r"D:\Snipaste\Snipaste.exe",
        ],
        "registry_keywords": ["Snipaste"],
    },
    "Bandizip": {
        "aliases": ["bandizip", "压缩"],
        "exe_names": ["Bandizip.exe"],
        "search_paths": [
            r"C:\Program Files\Bandizip\Bandizip.exe",
            r"D:\Bandizip\Bandizip.exe",
        ],
        "registry_keywords": ["Bandizip"],
    },
    "7-Zip": {
        "aliases": ["7zip", "7-zip", "7z"],
        "exe_names": ["7zFM.exe", "7z.exe"],
        "search_paths": [
            r"C:\Program Files\7-Zip\7zFM.exe",
            r"C:\Program Files (x86)\7-Zip\7zFM.exe",
        ],
        "registry_keywords": ["7-Zip"],
    },
    "WinRAR": {
        "aliases": ["winrar", "rar"],
        "exe_names": ["WinRAR.exe"],
        "search_paths": [
            r"C:\Program Files\WinRAR\WinRAR.exe",
            r"C:\Program Files (x86)\WinRAR\WinRAR.exe",
        ],
        "registry_keywords": ["WinRAR"],
    },
}


# ============================================================================
# 软件发现引擎
# ============================================================================

class SoftwareDiscovery:
    """智能软件发现引擎：注册表 + 路径扫描 + PATH 搜索"""

    def __init__(self):
        self._cache = {}  # 缓存已发现的软件路径
        self._registry_cache = None

    def find_software(self, name: str) -> str | None:
        """
        根据用户输入的名称查找软件的实际路径
        返回 exe 路径，找不到返回 None
        """
        name = name.strip().lower()

        # 检查缓存
        if name in self._cache:
            return self._cache[name]

        # 在软件数据库中查找匹配
        for soft_name, info in SOFTWARE_DB.items():
            if name in [a.lower() for a in info["aliases"]]:
                path = self._resolve_path(info)
                if path:
                    self._cache[name] = path
                    return path

        # 数据库中没有，尝试作为直接路径或 exe 名称处理
        return name  # 让 subprocess 自己处理

    def _resolve_path(self, info: dict) -> str | None:
        """三层解析：注册表 → 常见路径 → PATH"""

        # 第一层：注册表扫描
        for keyword in info.get("registry_keywords", []):
            path = self._search_registry(keyword, info.get("exe_names", []))
            if path:
                return path

        # 第二层：常见路径匹配
        for pattern in info.get("search_paths", []):
            # 处理通配符路径
            if "*" in pattern:
                matches = glob.glob(pattern)
                if matches:
                    return matches[0]
            else:
                if os.path.isfile(pattern):
                    return pattern

        # 第三层：PATH 环境变量搜索
        if info.get("use_which"):
            for exe in info.get("exe_names", []):
                path = shutil.which(exe)
                if path:
                    return path

        return None

    def _search_registry(self, keyword: str, exe_names: list) -> str | None:
        """从 Windows 注册表中搜索已安装软件"""
        if self._registry_cache is None:
            self._registry_cache = self._load_registry_apps()

        keyword_lower = keyword.lower()
        for app in self._registry_cache:
            if keyword_lower in app.get("name", "").lower():
                install_loc = app.get("install_location", "")
                if install_loc and os.path.isdir(install_loc):
                    for exe in exe_names:
                        exe_path = os.path.join(install_loc, exe)
                        if os.path.isfile(exe_path):
                            return exe_path
                        # 也搜索子目录
                        for root, dirs, files in os.walk(install_loc):
                            if exe in files:
                                return os.path.join(root, exe)
                            # 只搜索前两层
                            if root.count(os.sep) - install_loc.count(os.sep) >= 2:
                                break
        return None

    def _load_registry_apps(self) -> list:
        """从注册表加载已安装应用列表"""
        apps = []
        reg_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
        ]
        for hkey, subkey in reg_paths:
            try:
                key = winreg.OpenKey(hkey, subkey)
                i = 0
                while True:
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        try:
                            sub_key = winreg.OpenKey(key, subkey_name)
                            name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                            install_loc = ""
                            try:
                                install_loc = winreg.QueryValueEx(sub_key, "InstallLocation")[0]
                            except FileNotFoundError:
                                pass
                            display_icon = ""
                            try:
                                display_icon = winreg.QueryValueEx(sub_key, "DisplayIcon")[0]
                            except FileNotFoundError:
                                pass
                            apps.append({
                                "name": name,
                                "install_location": install_loc,
                                "display_icon": display_icon,
                            })
                            winreg.CloseKey(sub_key)
                        except (FileNotFoundError, OSError):
                            pass
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
            except OSError:
                pass
        return apps

    def scan_installed(self) -> list:
        """扫描所有已安装的软件，返回可识别的软件列表"""
        found = []
        for soft_name, info in SOFTWARE_DB.items():
            path = self._resolve_path(info)
            if path:
                found.append({
                    "name": soft_name,
                    "aliases": info["aliases"],
                    "path": path,
                })
        return found

    def get_all_names(self) -> list:
        """获取所有支持的软件名称列表"""
        names = []
        for soft_name, info in SOFTWARE_DB.items():
            names.append(soft_name)
            names.extend(info["aliases"])
        return names


# 全局实例
discovery = SoftwareDiscovery()


def register_tool(mcp):
    @mcp.tool()
    def open_app_tool(argument: str, payload='') -> dict:
        """
        打开电脑上的应用程序。支持 200+ 热门软件，自动搜索已安装路径。

        使用方式：
            1. 直接说软件名称：open_app_tool('微信')
            2. 带参数打开：open_app_tool('浏览器', 'https://www.baidu.com')
            3. 直接指定路径：open_app_tool('C:\\Program Files\\app.exe')

        支持的软件分类：
            社交通讯：微信、QQ、钉钉、企业微信、飞书、Telegram、Discord
            浏览器：Chrome、Edge、Firefox、Brave、Opera、Arc
            办公：Word、Excel、PPT、WPS、Typora、Notion、有道云笔记
            开发：VS Code、Cursor、IntelliJ、PyCharm、Android Studio、Git、Python、Node
            影音：网易云音乐、QQ音乐、酷狗、Spotify、PotPlayer、VLC、mpv
            视频：B站、腾讯视频、爱奇艺、优酷、抖音、快手
            直播：OBS、虎牙直播、B站直播
            剪辑：剪映、Premiere、After Effects、达芬奇
            游戏：Steam、Epic、WeGame、Ubisoft、EA、暴雪、原神、星穹铁道
            下载：IDM、迅雷、Motrix、aria2
            网盘：百度网盘、阿里云盘、夸克、OneDrive、坚果云、123云盘
            远程：向日葵、ToDesk、TeamViewer、AnyDesk、RustDesk
            系统：记事本、画图、计算器、任务管理器、CMD、PowerShell、Windows Terminal
            安全：火绒、360、电脑管家
            设计：Photoshop、Illustrator、Figma、SolidWorks、AutoCAD、立创EDA
            输入法：搜狗、百度、微信输入法
            翻译：有道词典、DeepL
            代理：Clash、V2Ray
            虚拟机：VMware、VirtualBox
            终端：Tabby、Hyper、MobaXterm、Xshell
            工具：Everything、Snipaste、Bandizip、7-Zip、WinRAR、雨滴桌面、壁纸引擎

        参数：
            argument: 软件名称（中文/英文均可）或 exe 文件路径
            payload: 可选参数，如浏览器网址
        """
        argument = argument.strip()
        try:
            if system == 'Windows':
                app_path = discovery.find_software(argument)
                if app_path:
                    if payload:
                        subprocess.Popen([app_path, payload], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    else:
                        subprocess.Popen([app_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    return {"success": True, "result": f"已执行打开：{argument}"}
                else:
                    return {"success": False, "result": f"未找到应用：{argument}"}
            else:
                return {"success": False, "result": "当前仅支持 Windows 系统"}
        except Exception as e:
            return {"success": False, "result": f"打开失败：{str(e)}"}

    @mcp.tool()
    def list_installed_apps_tool() -> dict:
        """
        扫描并列出电脑上已安装的可识别软件。
        返回已安装软件的名称和路径列表。
        """
        try:
            found = discovery.scan_installed()
            result = []
            for app in found:
                result.append(f"✅ {app['name']} → {app['path']}")
            return {
                "success": True,
                "result": f"共发现 {len(found)} 个已安装软件：\n" + "\n".join(result)
            }
        except Exception as e:
            return {"success": False, "result": f"扫描失败：{str(e)}"}
