import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import requests
import threading
import os
import subprocess
import json
import datetime
import socket
import re
import glob
import webbrowser
import zipfile
import io
import time
import ctypes
import sys 

# ==========================================
#              設定與常數
# ==========================================
CURRENT_VERSION = "v0.0.18"
GITHUB_REPO = "JKMby1230/Minecraft-Server-Installer"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# ==========================================
#              資源路徑處理
# ==========================================
def resource_path(relative_path):
    """ 獲取資源的絕對路徑，兼容開發環境與 PyInstaller 打包後的 exe """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ==========================================
#              語言字典 (Translations)
# ==========================================
TRANSLATIONS = {
    "繁體中文": {
        "tab1": " 📥 安裝部署 ", "tab2": " ⚙️ 規則設定 ", "tab3": " 🛡️ 權限管理 ", "tab4": " ℹ️ 關於 ", "tab5": " 📖 教學 ",
        "tab_quick": "⚡ 快速指南", "tab_detail": "📚 詳細教學",
        "grp_basic": " 基礎配置 ", "lbl_path": "安裝路徑:", "btn_browse": "瀏覽...",
        "lbl_core": "核心類型:", "lbl_ver": "遊戲版本:", 
        "lbl_ram": "記憶體 (電腦共有 {} GB):",
        "btn_install": "開始安裝伺服器", "grp_log": "系統日誌 (即時輸出)",
        "grp_shortcuts": " 📂 快捷操作 ",
        "btn_open_dir": "打開伺服器資料夾", 
        "btn_open_mods": "打開 Mods 資料夾",
        "grp_game": " 遊戲規則 ", "lbl_mode": "模式:", "lbl_diff": "難度:",
        "chk_pvp": "PVP (玩家傷害)", "chk_cmd": "指令方塊", "lbl_spawn": "重生點保護範圍:",
        "lbl_seed": "地圖種子碼 (Seed):",
        "grp_net": " 連線設定 ", "lbl_port": "Port (端口):", "lbl_max": "最大人數:",
        "chk_offline": "🔓 開放盜版/離線登入 (Cracked)",
        "lbl_motd": "MOTD (伺服器描述):",
        "btn_ip": "🔍 顯示 IP (含 IPv6)",
        "grp_op": " 👑 管理員 (OP) ", "grp_ban": " ⛔ 黑名單 (Ban) ", "grp_wl": " 🔒 白名單 ",
        "btn_add": "+", "btn_remove": "移除選取",
        "chk_wl": "啟用白名單限制", "lbl_wl_hint": "(未勾選則開放所有人)",
        "lbl_name": "軟體名稱:", "lbl_version": "版本:", "lbl_author": "發行:",
        "lbl_issue": "問題回報:", "btn_copy": "📋 複製", "lbl_lang": "語言 (Language):",
        "btn_donate": "☕ 請作者喝咖啡 (贊助)",
        "msg_install_ok": "安裝成功！\n路徑: ", "msg_install_err": "安裝發生錯誤: ",
        "msg_copy": "已複製到剪貼簿", "status_init": "系統初始化...", "status_ver_ok": "版本列表讀取完成",
        "val_survival": "生存", "val_creative": "創造", "val_adventure": "冒險",
        "val_peaceful": "和平", "val_easy": "簡單", "val_normal": "普通", "val_hard": "困難",
        "lbl_lan_ip": "🏠 區網 IPv4:", 
        "lbl_pub_ip": "🌏 公網 IPv4:",
        "lbl_ipv6": "🚀 公網 IPv6:",
        "lbl_radmin": "🔗 Radmin VPN:",
        "msg_ip_hint": "(正在掃描網路資訊... 請稍候)",
        "msg_ip_done": "(點擊按鈕即可複製 IP)",
        "err_neoforge_ver": "NeoForge 僅支援 Minecraft 1.20.1 (含) 以上版本。\n請改選 Forge 或 Fabric。",
        "lbl_java_ver": "Java 環境:", "btn_java_manual": "📂 手動指定",
        "msg_java_scanning": "正在掃描...", "msg_java_found": "自動: Java {}", "msg_java_manual": "手動: {}",
        "err_java_missing": "❌ 找不到適合的 Java！\n\nMinecraft {} 需要 Java {}。\n\n是否讓程式自動下載「免安裝版 Java」到伺服器資料夾？\n(這將花費一點時間)",
        "msg_java_downloading": "正在下載 Java {} ({})... {:.1f}%",
        "msg_java_unzipping": "正在解壓縮 Java...",
        "msg_java_auto_bind": "✅ 使用 Java 路徑:\n{}",
        "msg_new_version": "發現新版本 {}！\n(目前版本: {})\n\n是否前往下載？",
        "warn_ram": "⚠️ 警告：您設定的記憶體 ({}GB) 超過了電腦可用的一半。\n這可能會導致電腦卡頓，確定要繼續嗎？",
        "err_no_path": "請先設定安裝路徑！",
        "quick_text": "...", "tutorial_text": "..."
    },
    "English": {
        "tab1": " Install ", "tab2": " Settings ", "tab3": " Permissions ", "tab4": " About ", "tab5": " Tutorial ",
        "tab_quick": "⚡ Quick Guide", "tab_detail": "📚 Detailed",
        "grp_basic": " Basic Config ", "lbl_path": "Install Path:", "btn_browse": "Browse...",
        "lbl_core": "Loader:", "lbl_ver": "Version:", 
        "lbl_ram": "RAM (Total: {} GB):",
        "btn_install": "Start Installation", "grp_log": "System Log (Real-time)",
        "grp_shortcuts": " 📂 Shortcuts ",
        "btn_open_dir": "Open Server Folder",
        "btn_open_mods": "Open Mods Folder",
        "grp_game": " Game Rules ", "lbl_mode": "Gamemode:", "lbl_diff": "Difficulty:",
        "chk_pvp": "PVP Enabled", "chk_cmd": "Command Blocks", "lbl_spawn": "Spawn Protection:",
        "lbl_seed": "Level Seed:",
        "grp_net": " Network ", "lbl_port": "Port:", "lbl_max": "Max Players:",
        "chk_offline": "Allow Cracked/Offline Mode",
        "lbl_motd": "MOTD:",
        "btn_ip": "🔍 Show IPs",
        "grp_op": " Operators ", "grp_ban": " Banned ", "grp_wl": " Whitelist ",
        "btn_add": "Add", "btn_remove": "Remove",
        "chk_wl": "Enable Whitelist", "lbl_wl_hint": "(Open to all if unchecked)",
        "lbl_name": "Software:", "lbl_version": "Version:", "lbl_author": "Author:",
        "lbl_issue": "Report:", "btn_copy": "Copy", "lbl_lang": "Language:",
        "btn_donate": "☕ Donate",
        "msg_install_ok": "Success!\nPath: ", "msg_install_err": "Error: ",
        "msg_copy": "Copied", "status_init": "Initializing...", "status_ver_ok": "Versions loaded",
        "val_survival": "survival", "val_creative": "creative", "val_adventure": "adventure",
        "val_peaceful": "peaceful", "val_easy": "easy", "val_normal": "normal", "val_hard": "hard",
        "lbl_lan_ip": "LAN IPv4:", "lbl_pub_ip": "Public IPv4:", "lbl_ipv6": "Public IPv6:", "lbl_radmin": "Radmin VPN:",
        "msg_ip_hint": "(Scanning network...)",
        "msg_ip_done": "(Click to copy)",
        "err_neoforge_ver": "NeoForge requires MC 1.20.1+.",
        "lbl_java_ver": "Java Env:", "btn_java_manual": "📂 Manual",
        "msg_java_scanning": "Scanning...", "msg_java_found": "Auto: Java {}", "msg_java_manual": "Manual: {}",
        "err_java_missing": "Java {} not found!\n\nDownload portable Java automatically?",
        "msg_java_downloading": "Downloading Java {} ({})... {:.1f}%",
        "msg_java_unzipping": "Unzipping Java...",
        "msg_java_auto_bind": "Using Java:\n{}",
        "msg_new_version": "New version {} available!\n(Current: {})\n\nDownload now?",
        "warn_ram": "⚠️ Warning: {}GB RAM is more than half of your system RAM.",
        "err_no_path": "Please set Install Path first!",
        "quick_text": "...", "tutorial_text": "..."
    },
    "简体中文": {
        "tab1": " 📥 安装部署 ", "tab2": " ⚙️ 规则设定 ", "tab3": " 🛡️ 权限管理 ", "tab4": " ℹ️ 关于 ", "tab5": " 📖 教程 ",
        "tab_quick": "⚡ 快速指南", "tab_detail": "📚 详细教程",
        "grp_basic": " 基础配置 ", "lbl_path": "安装路径:", "btn_browse": "浏览...",
        "lbl_core": "核心类型:", "lbl_ver": "游戏版本:", 
        "lbl_ram": "内存 (电脑共有 {} GB):",
        "btn_install": "开始安装服务器", "grp_log": "系统日志 (即时输出)",
        "grp_shortcuts": " 📂 快捷操作 ",
        "btn_open_dir": "打开服务器文件夹",
        "btn_open_mods": "打开 Mods 文件夹",
        "grp_game": " 游戏规则 ", "lbl_mode": "模式:", "lbl_diff": "难度:",
        "chk_pvp": "PVP (玩家伤害)", "chk_cmd": "命令方块", "lbl_spawn": "出生点保护范围:",
        "lbl_seed": "地图种子码 (Seed):",
        "grp_net": " 连线设定 ", "lbl_port": "Port (端口):", "lbl_max": "最大人数:",
        "chk_offline": "🔓 开放盗版/离线登录 (Cracked)",
        "lbl_motd": "MOTD (服务器描述):",
        "btn_ip": "🔍 显示 IP (含复制功能)",
        "grp_op": " 👑 管理员 (OP) ", "grp_ban": " ⛔ 黑名单 (Ban) ", "grp_wl": " 🔒 白名单 ",
        "btn_add": "+", "btn_remove": "移除选中",
        "chk_wl": "启用白名单限制", "lbl_wl_hint": "(未勾选则开放所有人)",
        "lbl_name": "软件名称:", "lbl_version": "版本:", "lbl_author": "发行:",
        "lbl_issue": "问题回报:", "btn_copy": "📋 复制", "lbl_lang": "语言 (Language):",
        "btn_donate": "☕ 请作者喝咖啡 (赞助)",
        "msg_install_ok": "安装成功！\n路径: ", "msg_install_err": "安装发生错误: ",
        "msg_copy": "已复制", "status_init": "系统初始化...", "status_ver_ok": "版本列表读取完成",
        "val_survival": "生存", "val_creative": "创造", "val_adventure": "冒险",
        "val_peaceful": "和平", "val_easy": "简单", "val_normal": "普通", "val_hard": "困难",
        "lbl_lan_ip": "🏠 局域网 IPv4:", 
        "lbl_pub_ip": "🌏 公网 IPv4:",
        "lbl_ipv6": "🚀 公网 IPv6:",
        "lbl_radmin": "🔗 Radmin VPN:",
        "msg_ip_hint": "(正在扫描网络... 请稍候)",
        "msg_ip_done": "(点击按钮即可复制 IP)",
        "err_neoforge_ver": "NeoForge 仅支持 Minecraft 1.20.1 (含) 以上版本。\n请改选 Forge 或 Fabric。",
        "lbl_java_ver": "Java 环境:", "btn_java_manual": "📂 手动指定",
        "msg_java_scanning": "正在扫描...", "msg_java_found": "自动: Java {}", "msg_java_manual": "手动: {}",
        "err_java_missing": "❌ 找不到适合的 Java！\n\nMinecraft {} 需要 Java {}。\n\n是否让程式自动下载「免安装版 Java」到服务器文件夹？\n(这将花费一点时间)",
        "msg_java_downloading": "正在下载 Java {} ({})... {:.1f}%",
        "msg_java_unzipping": "正在解压缩 Java...",
        "msg_java_auto_bind": "✅ 使用 Java 路径:\n{}",
        "msg_new_version": "发现新版本 {}！\n(目前版本: {})\n\n是否前往下载？",
        "warn_ram": "⚠️ 警告：您设定的内存 ({}GB) 超过了电脑可用的一半。\n这可能会导致电脑卡顿，确定要继续吗？",
        "err_no_path": "请先设定安装路径！",
        "quick_text": "...", "tutorial_text": "..."
    }
}

# ==========================================
#              核心邏輯區 (Backend)
# ==========================================

class ServerInstallerApp:
    def __init__(self, root):
        self.root = root
        self.ops_list = []
        self.whitelist_list = []
        self.banned_list = []
        self.current_lang = "繁體中文"
        
        self.found_java_paths = {} 
        self.manual_java_path = None
        self.system_ram_gb = self.get_system_memory()

        self.setup_ui()
        self.log(self.get_text("status_init"))
        
        threading.Thread(target=self.scan_all_java_versions, daemon=True).start()
        threading.Thread(target=self.load_versions_async, daemon=True).start()
        threading.Thread(target=self.check_for_updates, daemon=True).start()

    def get_system_memory(self):
        try:
            kernel32 = ctypes.windll.kernel32
            c_ulonglong = ctypes.c_ulonglong
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ('dwLength', ctypes.c_ulong),
                    ('dwMemoryLoad', ctypes.c_ulong),
                    ('ullTotalPhys', c_ulonglong),
                    ('ullAvailPhys', c_ulonglong),
                    ('ullTotalPageFile', c_ulonglong),
                    ('ullAvailPageFile', c_ulonglong),
                    ('ullTotalVirtual', c_ulonglong),
                    ('ullAvailVirtual', c_ulonglong),
                    ('ullAvailExtendedVirtual', c_ulonglong),
                ]
            mem = MEMORYSTATUSEX()
            mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            kernel32.GlobalMemoryStatusEx(ctypes.byref(mem))
            return round(mem.ullTotalPhys / (1024**3), 1)
        except:
            return 0 

    def get_text(self, key):
        if key == "tutorial_text":
             return """【 Minecraft 伺服器架設完全手冊 】

=== 第一階段：安裝與設置 ===
1. 準備環境：
   - 確保電腦已連上網路。
   - 準備一個全新的空資料夾 (建議放在桌面，命名為 Server)。

2. 軟體操作：
   - 在「📥 安裝部署」分頁，點擊「瀏覽」選取剛才的資料夾。
   - 選擇模組核心 (Fabric 輕量 / Forge 經典 / NeoForge 新版)。
   - 選擇遊戲版本 (如 1.20.1)。
   - 記憶體建議：至少 4GB (Min: 2, Max: 4)。
   - 點擊「開始安裝伺服器」，若缺少 Java 程式會自動下載，請耐心等待。

=== 第二階段：啟動伺服器 ===
1. 安裝完成後，打開您的 Server 資料夾。
2. 找到「start.bat」檔案，滑鼠左鍵雙擊執行。
3. 會跳出一個黑色視窗 (CMD)，初次啟動需要跑一段時間。
4. 當看到 "Done!" 字樣，代表伺服器已成功開啟。

=== 第三階段：連線教學 ===
【方案 A：IPv6 直連 (最快)】
1. 點擊本軟體下方的「🔍 顯示 IP」。
2. 複製「🚀 公網 IPv6」地址。
3. 朋友在多人遊戲輸入： [你的IPv6地址] (要有中括號)

【方案 B：Radmin VPN (最穩)】
1. 雙方安裝 Radmin VPN 並加入同個網路。
2. 複製本軟體顯示的「🔗 Radmin VPN」IP。
3. 朋友輸入該 IP 即可連線。
"""
        if key == "quick_text":
            return """【 5 步驟快速開服 】

1. 選路徑：選擇一個空資料夾。
2. 選版本：選擇 Fabric/Forge 與遊戲版本。
3. 按安裝：點擊「開始安裝伺服器」並等待完成。
4. 啟動它：點擊「📂 打開伺服器資料夾」，執行「start.bat」。
5. 給 IP：點擊軟體上的「🔍 顯示 IP」，複製 IPv6 或 Radmin IP 給朋友。"""
        
        return TRANSLATIONS[self.current_lang].get(key, key)

    def change_language(self, event=None):
        self.current_lang = self.combo_lang.get()
        self.update_ui_texts()
        self.update_java_ui()

    def update_ui_texts(self):
        self.nb.tab(self.t1, text=self.get_text("tab1"))
        self.nb.tab(self.t2, text=self.get_text("tab2"))
        self.nb.tab(self.t3, text=self.get_text("tab3"))
        self.nb.tab(self.t4, text=self.get_text("tab4"))
        self.nb.tab(self.t5, text=self.get_text("tab5"))
        self.nb_tut.tab(self.t5_quick, text=self.get_text("tab_quick"))
        self.nb_tut.tab(self.t5_detail, text=self.get_text("tab_detail"))
        
        self.f1.config(text=self.get_text("grp_basic"))
        self.lbl_path.config(text=self.get_text("lbl_path"))
        self.btn_browse.config(text=self.get_text("btn_browse"))
        self.lbl_core.config(text=self.get_text("lbl_core"))
        self.lbl_ver.config(text=self.get_text("lbl_ver"))
        self.lbl_ram.config(text=self.get_text("lbl_ram").format(self.system_ram_gb))
        self.btn_run.config(text=self.get_text("btn_install"))
        self.lf_log.config(text=self.get_text("grp_log"))
        
        self.lf_sc.config(text=self.get_text("grp_shortcuts"))
        self.btn_open_dir.config(text=self.get_text("btn_open_dir"))
        self.btn_open_mods.config(text=self.get_text("btn_open_mods"))

        self.f2.config(text=self.get_text("grp_game"))
        self.lbl_mode.config(text=self.get_text("lbl_mode"))
        self.lbl_diff.config(text=self.get_text("lbl_diff"))
        self.chk_pvp_w.config(text=self.get_text("chk_pvp"))
        self.chk_cmd_w.config(text=self.get_text("chk_cmd"))
        self.lbl_spawn.config(text=self.get_text("lbl_spawn"))
        self.lbl_seed.config(text=self.get_text("lbl_seed"))
        self.f3.config(text=self.get_text("grp_net"))
        self.lbl_port.config(text=self.get_text("lbl_port"))
        self.lbl_max.config(text=self.get_text("lbl_max"))
        self.chk_offline_w.config(text=self.get_text("chk_offline")) 
        self.lbl_motd.config(text=self.get_text("lbl_motd"))
        self.btn_ip.config(text=self.get_text("btn_ip"))
        self.cb_mode['values'] = [self.get_text("val_survival"), self.get_text("val_creative"), self.get_text("val_adventure")]
        self.cb_diff['values'] = [self.get_text("val_peaceful"), self.get_text("val_easy"), self.get_text("val_normal"), self.get_text("val_hard")]
        self.gb_op.config(text=self.get_text("grp_op"))
        self.btn_op_add.config(text=self.get_text("btn_add"))
        self.btn_op_del.config(text=self.get_text("btn_remove"))
        self.gb_ban.config(text=self.get_text("grp_ban"))
        self.btn_ban_add.config(text=self.get_text("btn_add"))
        self.btn_ban_del.config(text=self.get_text("btn_remove"))
        self.gb_wl.config(text=self.get_text("grp_wl"))
        self.chk_wl_w.config(text=self.get_text("chk_wl"))
        self.lbl_wl_hint.config(text=self.get_text("lbl_wl_hint"))
        self.btn_wl_add.config(text=self.get_text("btn_add"))
        self.btn_wl_del.config(text=self.get_text("btn_remove"))
        self.lbl_name_t.config(text=self.get_text("lbl_name"))
        self.lbl_ver_t.config(text=self.get_text("lbl_version"))
        self.lbl_author_t.config(text=self.get_text("lbl_author"))
        self.lbl_issue_t.config(text=self.get_text("lbl_issue"))
        self.btn_copy.config(text=self.get_text("btn_copy"))
        self.lbl_lang.config(text=self.get_text("lbl_lang"))
        self.txt_tut_quick.config(state='normal'); self.txt_tut_quick.delete(1.0, tk.END); self.txt_tut_quick.insert(tk.END, self.get_text("quick_text")); self.txt_tut_quick.config(state='disabled')
        self.txt_tut_detail.config(state='normal'); self.txt_tut_detail.delete(1.0, tk.END); self.txt_tut_detail.insert(tk.END, self.get_text("tutorial_text")); self.txt_tut_detail.config(state='disabled')
        self.btn_donate.config(text=self.get_text("btn_donate"))
        self.lbl_java_txt.config(text=self.get_text("lbl_java_ver"))
        self.btn_java_manual.config(text=self.get_text("btn_java_manual"))

    def log(self, message):
        def _update():
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            self.txt_log.config(state='normal')
            self.txt_log.insert(tk.END, f"[{timestamp}] {message}\n")
            self.txt_log.see(tk.END)
            self.txt_log.config(state='disabled')
        self.root.after(0, _update)

    def log_raw(self, message):
        def _update():
            self.txt_log.config(state='normal')
            self.txt_log.insert(tk.END, message)
            self.txt_log.see(tk.END)
            self.txt_log.config(state='disabled')
        self.root.after(0, _update)

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        messagebox.showinfo("OK", self.get_text("msg_copy"))

    def check_for_updates(self):
        try:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
            r = requests.get(url, headers=HEADERS, timeout=3)
            if r.status_code == 200:
                data = r.json()
                latest_tag = data['tag_name']
                if latest_tag != CURRENT_VERSION:
                    msg = self.get_text("msg_new_version").format(latest_tag, CURRENT_VERSION)
                    if messagebox.askyesno("Update", msg):
                        webbrowser.open(data['html_url'])
        except:
            pass

    def select_manual_java(self):
        path = filedialog.askopenfilename(title="Select java.exe", filetypes=[("Java Executable", "java.exe"), ("All Files", "*.*")])
        if path:
            self.manual_java_path = path
            fname = os.path.basename(path)
            self.lbl_java_val.config(text=self.get_text("msg_java_manual").format(fname), foreground="purple")
            self.log(f"Manual Java selected: {path}")

    def check_java_version(self, java_path):
        try:
            cmd = subprocess.run([java_path, "-version"], capture_output=True, text=True, startupinfo=subprocess.STARTUPINFO())
            output = cmd.stderr + cmd.stdout
            match = re.search(r'version "(\d+)(\.(\d+))?.*"', output)
            if match:
                major = int(match.group(1))
                minor = int(match.group(3)) if match.group(3) else 0
                return 8 if major == 1 and minor == 8 else major
        except:
            pass
        return 0

    def scan_all_java_versions(self):
        self.root.after(0, lambda: self.lbl_java_val.config(text=self.get_text("msg_java_scanning"), foreground="blue"))
        found = {}
        sys_ver = self.check_java_version("java")
        if sys_ver > 0: found[sys_ver] = "java"
        possible_roots = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Java"),
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Eclipse Adoptium"),
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Microsoft"),
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Zulu"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Java")
        ]
        for root in possible_roots:
            if os.path.exists(root):
                for java_exe in glob.glob(os.path.join(root, "**", "bin", "java.exe"), recursive=True):
                    ver = self.check_java_version(java_exe)
                    if ver > 0 and ver not in found:
                        found[ver] = java_exe
        self.found_java_paths = found
        self.root.after(0, self.update_java_ui)
        self.log(f"Java Scan Complete. Found: {sorted(found.keys())}")

    def update_java_ui(self):
        if self.manual_java_path: return
        if self.found_java_paths:
            vers = sorted(self.found_java_paths.keys())
            txt = self.get_text("msg_java_found").format(", ".join([str(v) for v in vers]))
            color = "green"
        else:
            txt = "No Java Found"
            color = "red"
        self.lbl_java_txt.config(text=self.get_text("lbl_java_ver"))
        self.lbl_java_val.config(text=txt, foreground=color)

    def get_required_java(self, mc_version):
        try:
            parts = [int(x) for x in mc_version.split('.')]
            major, minor = parts[0], parts[1]
            patch = parts[2] if len(parts) > 2 else 0
            if major == 1 and minor >= 21: return 21
            if major == 1 and minor == 20 and patch >= 5: return 21
            if major == 1 and minor >= 18: return 17
            if major == 1 and minor == 17: return 16 
            return 8
        except: return 8

    def download_portable_java(self, version, target_dir):
        feature_ver = version
        if version == 8: feature_ver = 8
        api_url = f"https://api.adoptium.net/v3/binary/latest/{feature_ver}/ga/windows/x64/jdk/hotspot/normal/eclipse"
        self.log(self.get_text("msg_java_downloading").format(version, "Adoptium", 0.0))
        try:
            r = requests.get(api_url, headers=HEADERS, stream=True)
            total_size = int(r.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 1024 * 1024 
            zip_data = io.BytesIO()
            for data in r.iter_content(chunk_size=chunk_size):
                zip_data.write(data)
                downloaded += len(data)
                percent = (downloaded / total_size) * 100 if total_size > 0 else 0
                self.root.after(0, lambda p=percent: self.prog.configure(value=p))
                if int(percent) % 10 == 0:
                     self.log(f"Downloading Java... {int(percent)}%")
            self.log(self.get_text("msg_java_unzipping"))
            with zipfile.ZipFile(zip_data) as zf:
                root_folder = zf.namelist()[0].split('/')[0]
                zf.extractall(target_dir)
            extracted_path = os.path.join(target_dir, root_folder, "bin", "java.exe")
            if os.path.exists(extracted_path):
                self.log(f"Java {version} installed at: {extracted_path}")
                return extracted_path
            else:
                raise Exception("Java executable not found after unzip")
        except Exception as e:
            self.log(f"Java Download Error: {e}")
            return None

    def get_minecraft_versions(self):
        url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        try:
            response = requests.get(url, headers=HEADERS, timeout=5)
            data = response.json()
            return [v["id"] for v in data["versions"] if v["type"] == "release"]
        except: return ["1.20.4", "1.20.1", "1.19.4", "1.18.2", "1.16.5"]

    def get_forge_build(self, mc_version):
        url = "https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json"
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            data = r.json()
            promos = data.get("promos", {})
            return promos.get(f"{mc_version}-recommended") or promos.get(f"{mc_version}-latest")
        except: return None

    def get_neoforge_version(self, mc_ver):
        api_url = "https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/neoforge"
        try:
            r = requests.get(api_url, headers=HEADERS, timeout=5)
            data = r.json()
            versions = data.get('versions', [])
            target_prefix = ""
            if mc_ver == "1.20.1": target_prefix = "1.20.1"
            else:
                parts = mc_ver.split('.')
                if len(parts) >= 2:
                    major = parts[1]; minor = parts[2] if len(parts) > 2 else '0'
                    target_prefix = f"{major}.{minor}"
            candidates = [v for v in versions if v.startswith(target_prefix)]
            if candidates: return candidates[-1]
            return None
        except: return None

    def get_player_uuid(self, username):
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=5)
            if r.status_code == 200:
                data = r.json()
                raw = data['id']
                fmt = f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"
                return fmt, data['name']
            return None, None
        except: return None, None

    def load_versions_async(self):
        vers = self.get_minecraft_versions()
        self.root.after(0, lambda: self.combo_ver.config(values=vers))
        self.root.after(0, lambda: self.combo_ver.current(0) if vers else None)
        self.root.after(0, lambda: self.log(self.get_text("status_ver_ok")))

    def get_public_ipv6(self):
        try:
            s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
            s.connect(("2001:4860:4860::8888", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "Not Detected"

    def get_radmin_ip(self):
        try:
            info = socket.getaddrinfo(socket.gethostname(), None)
            for item in info:
                ip = item[4][0]
                if ip.startswith("26."):
                    return ip
        except: pass
        return "Not Detected"

    def show_network_info(self):
        win = tk.Toplevel(self.root)
        win.title("Network Information")
        win.geometry("450x350")
        pad_opts = {'padx': 10, 'pady': 5}
        ttk.Label(win, text="Network Information", font=("Arial", 12, "bold")).pack(pady=10)
        var_lan = tk.StringVar(value="⏳ Loading...")
        var_pub = tk.StringVar(value="⏳ Loading...")
        var_v6 = tk.StringVar(value="⏳ Loading...")
        var_rad = tk.StringVar(value="⏳ Loading...")
        def create_row(label_text, var_obj):
            f = ttk.Frame(win); f.pack(fill='x', **pad_opts)
            ttk.Label(f, text=label_text, width=20, anchor='e').pack(side='left')
            ent = ttk.Entry(f, width=25, textvariable=var_obj, state='readonly')
            ent.pack(side='left', padx=5)
            def copy_action():
                val = var_obj.get()
                if "Loading" not in val and "Detected" not in val:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(val)
                    self.root.update()
                    btn.config(text="✅ OK") 
                    win.after(1000, lambda: btn.config(text="Copy"))
            btn = ttk.Button(f, text="Copy", width=6, command=copy_action)
            btn.pack(side='left')
        create_row(self.get_text('lbl_lan_ip'), var_lan)
        create_row(self.get_text('lbl_pub_ip'), var_pub)
        create_row(self.get_text('lbl_ipv6'), var_v6)
        create_row(self.get_text('lbl_radmin'), var_rad)
        status_lbl = ttk.Label(win, text=self.get_text('msg_ip_hint'), foreground="gray")
        status_lbl.pack(pady=10)
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=5)
        def fetch_data():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                lan = s.getsockname()[0]; s.close()
            except: lan = "Unknown"
            try: pub = requests.get('https://api.ipify.org', headers=HEADERS, timeout=3).text
            except: pub = "Timeout"
            v6 = self.get_public_ipv6()
            rad = self.get_radmin_ip()
            win.after(0, lambda: [
                var_lan.set(lan), var_pub.set(pub), var_v6.set(v6), var_rad.set(rad),
                status_lbl.config(text=self.get_text('msg_ip_done'), foreground="green")
            ])
        threading.Thread(target=fetch_data, daemon=True).start()

    def add_user(self, entry, listbox, target_list, mode):
        name = entry.get().strip()
        if not name: return
        def task():
            self.log(f"Check UUID: {name}...")
            uuid, real_name = self.get_player_uuid(name)
            if uuid:
                for u in target_list:
                    if u['uuid'] == uuid: self.log(f"{real_name} exists."); return
                user_data = {'uuid': uuid, 'name': real_name}
                if mode == "OP": user_data.update({'level': 4, 'bypassesPlayerLimit': False})
                elif mode == "BAN":
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S +0800")
                    user_data.update({'created': now, 'source': 'Installer', 'expires': 'forever', 'reason': 'Banned'})
                target_list.append(user_data)
                self.root.after(0, lambda: listbox.insert(tk.END, f"{real_name}"))
                self.root.after(0, lambda: entry.delete(0, tk.END))
                self.root.after(0, lambda: self.log(f"Added {mode}: {real_name}"))
            else: self.root.after(0, lambda: messagebox.showerror("Error", f"User not found: {name}"))
        threading.Thread(target=task).start()

    def remove_user(self, listbox, target_list):
        sel = listbox.curselection()
        if not sel: return
        idx = sel[0]
        removed = target_list.pop(idx); listbox.delete(idx)
        self.log(f"Removed: {removed['name']}")

    def run_cmd_realtime(self, cmd):
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, startupinfo=info)
        for line in process.stdout:
            self.log_raw(line) 
        process.wait()
        return process.returncode

    def is_valid_neoforge_version(self, v):
        try:
            parts = v.split('.')
            if len(parts) < 2: return False
            major = int(parts[0]); minor = int(parts[1])
            if major == 1 and minor >= 20:
                if minor == 20:
                    patch = int(parts[2]) if len(parts) > 2 else 0
                    return patch >= 1 
                return True
            return False
        except: return False

    def start_install(self):
        path = self.ent_path.get()
        if not path: messagebox.showwarning("Warning", "Check Path"); return
        mc_ver = self.combo_ver.get()
        s = {
            'loader': self.var_load.get(), 'version': mc_ver, 'path': path,
            'ram_min': self.ent_min.get(), 'ram_max': self.ent_max.get(),
            'port': self.ent_port.get(), 'max': self.ent_max_p.get(), 'online': self.var_online.get(),
            'mode': self.cb_mode.get(), 'diff': self.cb_diff.get(), 'pvp': self.var_pvp.get(),
            'cmd': self.var_cmd.get(), 'spawn': self.ent_spawn.get(), 'motd': self.ent_motd.get(),
            'seed': self.ent_seed.get(), # 新增
            'wl': self.var_wl.get()
        }
        if not s['ram_min'].isdigit() or not s['ram_max'].isdigit():
            messagebox.showwarning("Error", "RAM must be number"); return
        self.btn_run.config(state=tk.DISABLED); self.prog['value'] = 0
        self.txt_log.config(state='normal'); self.txt_log.delete(1.0, tk.END); self.txt_log.config(state='disabled')
        threading.Thread(target=self.install_process, args=(s,)).start()

    def gen_props(self, s):
        mode_map = {self.get_text("val_survival"): "survival", self.get_text("val_creative"): "creative", self.get_text("val_adventure"): "adventure"}
        diff_map = {self.get_text("val_peaceful"): "peaceful", self.get_text("val_easy"): "easy", self.get_text("val_normal"): "normal", self.get_text("val_hard"): "hard"}
        mode = mode_map.get(s['mode'], s['mode'].lower())
        diff = diff_map.get(s['diff'], s['diff'].lower())
        c = f"""server-port={s['port']}
max-players={s['max']}
online-mode={str(s['online']).lower()}
gamemode={mode}
difficulty={diff}
pvp={str(s['pvp']).lower()}
enable-command-block={str(s['cmd']).lower()}
spawn-protection={s['spawn']}
motd={s['motd']}
level-seed={s['seed']}
white-list={str(s['wl']).lower()}
enforce-whitelist={str(s['wl']).lower()}
"""
        with open("server.properties", "w", encoding="utf-8") as f: f.write(c)

    def gen_json(self):
        with open("ops.json", "w") as f: json.dump(self.ops_list, f, indent=4)
        with open("banned-players.json", "w") as f: json.dump(self.banned_list, f, indent=4)
        wl = [{'uuid': u['uuid'], 'name': u['name']} for u in self.whitelist_list]
        with open("whitelist.json", "w") as f: json.dump(wl, f, indent=4)

    def gen_bat(self, loader, min_r, max_r, java_path):
        txt = ""
        clean_java_path = java_path.replace('"', '')
        if os.path.exists("run.bat") or os.path.exists("run.sh"):
            with open("user_jvm_args.txt", "w") as f: f.write(f"-Xms{min_r}G\n-Xmx{max_r}G\n")
            txt = f'@echo off\nset PATH={os.path.dirname(clean_java_path)};%PATH%\ncall run.bat\npause'
        else:
            jar = "server.jar"
            for f in os.listdir("."):
                if f.startswith("forge") and f.endswith(".jar") and "installer" not in f: jar = f; break
                if f == "fabric-server-launch.jar": jar = f; break
            txt = f'@echo off\n{java_path} -Xms{min_r}G -Xmx{max_r}G -jar {jar} nogui\npause'
        with open("start.bat", "w") as f: f.write(txt)

    def install_process(self, s):
        target = s['path']; mc_ver = s['version']
        if s['loader'] == "NeoForge":
            if not self.is_valid_neoforge_version(mc_ver):
                messagebox.showerror("Error", self.get_text("err_neoforge_ver"))
                self.btn_run.config(state=tk.NORMAL); return

        req_java = self.get_required_java(mc_ver)
        selected_java_path = None
        
        if self.manual_java_path and os.path.exists(self.manual_java_path):
            selected_java_path = self.manual_java_path
        
        if not selected_java_path:
            match_found = False
            if req_java in self.found_java_paths:
                selected_java_path = self.found_java_paths[req_java]; match_found = True
            elif req_java >= 17:
                 for v in sorted(self.found_java_paths.keys()):
                     if v >= req_java:
                         selected_java_path = self.found_java_paths[v]; match_found = True; break
            if not match_found:
                 sys_ver = self.check_java_version("java")
                 if sys_ver > 0 and (sys_ver == req_java or (req_java >= 17 and sys_ver >= req_java)):
                     selected_java_path = "java"; match_found = True
        
        if not selected_java_path:
            msg = self.get_text("err_java_missing").format(mc_ver, req_java)
            if messagebox.askyesno("Java Missing", msg):
                java_runtime_dir = os.path.join(target, "runtime")
                downloaded_java = self.download_portable_java(req_java, java_runtime_dir)
                if downloaded_java:
                    selected_java_path = downloaded_java
                else:
                    self.log("Java Download Failed."); self.btn_run.config(state=tk.NORMAL); return
            else:
                self.log(f"❌ Aborted: Missing Java {req_java}"); self.btn_run.config(state=tk.NORMAL); return

        final_java_cmd = f'"{selected_java_path}"' if " " in selected_java_path else selected_java_path

        if not os.path.exists(target):
            try: os.makedirs(target)
            except: self.log(self.get_text("msg_install_err") + "Create dir failed"); return
        cwd = os.getcwd(); os.chdir(target)
        try:
            self.log(f"Target: {target}")
            self.log(self.get_text("msg_java_auto_bind").format(final_java_cmd))
            if s['loader'] == "Fabric": self.install_fabric(mc_ver)
            elif s['loader'] == "NeoForge": self.install_neoforge(mc_ver)
            else: self.install_forge(mc_ver)
            with open("eula.txt", "w") as f: f.write("eula=true\n")
            self.gen_props(s); self.gen_json()
            self.gen_bat(s['loader'], s['ram_min'], s['ram_max'], final_java_cmd)
            if not os.path.exists("mods"): os.makedirs("mods")
            self.log(self.get_text("msg_install_ok"))
            messagebox.showinfo("OK", self.get_text("msg_install_ok") + target)
        except Exception as e:
            self.log(self.get_text("msg_install_err") + str(e))
            messagebox.showerror("Error", str(e))
        finally:
            os.chdir(cwd); self.btn_run.config(state=tk.NORMAL); self.prog['value'] = 100

    def install_fabric(self, v):
        name = "fabric-installer.jar"
        url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.0/fabric-installer-1.0.0.jar"
        self.log("Download Fabric...")
        with open(name, 'wb') as f: f.write(requests.get(url).content)
        self.log(f"Install Fabric {v}...")
        cmd = ["java", "-jar", name, "server", "-mcversion", v, "-downloadMinecraft"]
        if self.run_cmd_realtime(cmd) != 0: raise Exception("Fabric Install Failed")
        if os.path.exists(name): os.remove(name)

    def install_forge(self, v):
        self.log(f"Check Forge {v}...")
        build = self.get_forge_build(v)
        if not build: raise Exception(f"Forge {v} not found")
        full = f"{v}-{build}"; name = f"forge-{full}-installer.jar"
        url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{full}/{name}"
        self.log(f"Download Forge ({build})...")
        r = requests.get(url)
        if r.status_code != 200: raise Exception("Forge Download Failed")
        with open(name, 'wb') as f: f.write(r.content)
        self.log("Install Forge...")
        if self.run_cmd_realtime(["java", "-jar", name, "--installServer"]) != 0: raise Exception("Forge Install Failed")
        if os.path.exists(name): os.remove(name)
        if os.path.exists(name+".log"): os.remove(name+".log")

    def install_neoforge(self, v):
        self.log(f"Check NeoForge {v}...")
        nf_version = self.get_neoforge_version(v)
        if not nf_version: raise Exception(f"NeoForge not found for MC {v}")
        name = f"neoforge-{nf_version}-installer.jar"
        url = f"https://maven.neoforged.net/releases/net/neoforged/neoforge/{nf_version}/{name}"
        self.log(f"Download NeoForge ({nf_version})...")
        r = requests.get(url)
        if r.status_code != 200: raise Exception("NeoForge Download Failed")
        with open(name, 'wb') as f: f.write(r.content)
        self.log("Install NeoForge...")
        if self.run_cmd_realtime(["java", "-jar", name, "--installServer"]) != 0: raise Exception("NeoForge Install Failed")
        if os.path.exists(name): os.remove(name)
        if os.path.exists(name+".log"): os.remove(name+".log")

    def gen_bat(self, loader, min_r, max_r, java_path):
        txt = ""
        clean_java_path = java_path.replace('"', '')
        if os.path.exists("run.bat") or os.path.exists("run.sh"):
            with open("user_jvm_args.txt", "w") as f: f.write(f"-Xms{min_r}G\n-Xmx{max_r}G\n")
            txt = f'@echo off\nset PATH={os.path.dirname(clean_java_path)};%PATH%\ncall run.bat\npause'
        else:
            jar = "server.jar"
            for f in os.listdir("."):
                if f.startswith("forge") and f.endswith(".jar") and "installer" not in f: jar = f; break
                if f == "fabric-server-launch.jar": jar = f; break
            txt = f'@echo off\n{java_path} -Xms{min_r}G -Xmx{max_r}G -jar {jar} nogui\npause'
        with open("start.bat", "w") as f: f.write(txt)

    def select_dir(self):
        d = filedialog.askdirectory()
        if d: self.ent_path.delete(0, tk.END); self.ent_path.insert(0, d)

    def open_donate(self):
        webbrowser.open("https://www.buymeacoffee.com/marker0921230")

    def setup_ui(self):
        self.root.title(f"MinecraftServerInstaller {CURRENT_VERSION}")
        self.root.geometry("620x780")
        if os.path.exists("logo.ico"):
            try: self.root.iconbitmap(resource_path("logo.ico"))
            except: pass
        style = ttk.Style(); style.theme_use('vista')
        self.nb = ttk.Notebook(self.root); self.nb.pack(pady=10, padx=10, fill="both", expand=True)
        self.t1, self.t2, self.t3, self.t4, self.t5 = ttk.Frame(self.nb), ttk.Frame(self.nb), ttk.Frame(self.nb), ttk.Frame(self.nb), ttk.Frame(self.nb)
        self.nb.add(self.t1, text=""); self.nb.add(self.t2, text=""); self.nb.add(self.t3, text=""); self.nb.add(self.t4, text=""); self.nb.add(self.t5, text="")

        # Tab 1
        self.f1 = ttk.LabelFrame(self.t1, text=""); self.f1.pack(padx=10, pady=10, fill="x")
        r_java = ttk.Frame(self.f1); r_java.pack(fill="x", pady=5)
        self.lbl_java_txt = ttk.Label(r_java, text="", font=("Microsoft YaHei", 9, "bold")); self.lbl_java_txt.pack(side=tk.LEFT)
        self.lbl_java_val = ttk.Label(r_java, text="", font=("Microsoft YaHei", 9, "bold")); self.lbl_java_val.pack(side=tk.LEFT, padx=5)
        self.btn_java_manual = ttk.Button(r_java, text="", command=self.select_manual_java); self.btn_java_manual.pack(side=tk.RIGHT)
        r0 = ttk.Frame(self.f1); r0.pack(fill="x", pady=5)
        self.lbl_path = ttk.Label(r0, text=""); self.lbl_path.pack(side=tk.LEFT)
        self.ent_path = ttk.Entry(r0); self.ent_path.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        self.btn_browse = ttk.Button(r0, text="", command=self.select_dir); self.btn_browse.pack(side=tk.RIGHT)
        r1 = ttk.Frame(self.f1); r1.pack(fill="x", pady=5)
        self.lbl_core = ttk.Label(r1, text=""); self.lbl_core.pack(side=tk.LEFT)
        self.var_load = tk.StringVar(value="Fabric")
        ttk.Radiobutton(r1, text="Fabric", variable=self.var_load, value="Fabric").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(r1, text="Forge", variable=self.var_load, value="Forge").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(r1, text="NeoForge", variable=self.var_load, value="NeoForge").pack(side=tk.LEFT)
        self.lbl_ver = ttk.Label(r1, text=""); self.lbl_ver.pack(side=tk.LEFT, padx=10)
        self.combo_ver = ttk.Combobox(r1, state="readonly", width=12); self.combo_ver.pack(side=tk.LEFT)
        r2 = ttk.Frame(self.f1); r2.pack(fill="x", pady=5)
        self.lbl_ram = ttk.Label(r2, text=""); self.lbl_ram.pack(side=tk.LEFT)
        self.ent_min = ttk.Entry(r2, width=3); self.ent_min.insert(0,"2"); self.ent_min.pack(side=tk.LEFT, padx=2)
        ttk.Label(r2, text="/").pack(side=tk.LEFT)
        self.ent_max = ttk.Entry(r2, width=3); self.ent_max.insert(0,"4"); self.ent_max.pack(side=tk.LEFT, padx=2)
        self.btn_run = ttk.Button(self.t1, text="", command=self.start_install); self.btn_run.pack(pady=5, ipadx=20, ipady=5)
        self.prog = ttk.Progressbar(self.t1, mode="determinate"); self.prog.pack(fill="x", padx=20)
        self.lf_log = ttk.LabelFrame(self.t1, text=""); self.lf_log.pack(fill="both", expand=True, padx=10, pady=5)
        self.txt_log = scrolledtext.ScrolledText(self.lf_log, height=8, state='disabled', font=("Consolas", 9)); self.txt_log.pack(fill="both", expand=True)

        # Tab 2
        self.f2 = ttk.LabelFrame(self.t2, text=""); self.f2.pack(padx=10, pady=10, fill="x")
        row_g = ttk.Frame(self.f2); row_g.pack(fill="x", pady=5)
        self.lbl_mode = ttk.Label(row_g, text=""); self.lbl_mode.pack(side=tk.LEFT)
        self.cb_mode = ttk.Combobox(row_g, state="readonly", width=8); self.cb_mode.pack(side=tk.LEFT, padx=5)
        self.lbl_diff = ttk.Label(row_g, text=""); self.lbl_diff.pack(side=tk.LEFT)
        self.cb_diff = ttk.Combobox(row_g, state="readonly", width=8); self.cb_diff.pack(side=tk.LEFT, padx=5)
        row_b = ttk.Frame(self.f2); row_b.pack(fill="x", pady=5)
        self.var_pvp = tk.BooleanVar(value=True)
        self.chk_pvp_w = ttk.Checkbutton(row_b, variable=self.var_pvp); self.chk_pvp_w.pack(side=tk.LEFT, padx=5)
        self.var_cmd = tk.BooleanVar(value=True)
        self.chk_cmd_w = ttk.Checkbutton(row_b, variable=self.var_cmd); self.chk_cmd_w.pack(side=tk.LEFT, padx=10)
        self.lbl_spawn = ttk.Label(row_b, text=""); self.lbl_spawn.pack(side=tk.LEFT, padx=10)
        self.ent_spawn = ttk.Entry(row_b, width=3); self.ent_spawn.insert(0,"16"); self.ent_spawn.pack(side=tk.LEFT)
        self.f3 = ttk.LabelFrame(self.t2, text=""); self.f3.pack(padx=10, pady=10, fill="x")
        row_n = ttk.Frame(self.f3); row_n.pack(fill="x", pady=5)
        self.lbl_port = ttk.Label(row_n, text=""); self.lbl_port.pack(side=tk.LEFT)
        self.ent_port = ttk.Entry(row_n, width=6); self.ent_port.insert(0,"25565"); self.ent_port.pack(side=tk.LEFT)
        self.lbl_max = ttk.Label(row_n, text=""); self.lbl_max.pack(side=tk.LEFT, padx=5)
        self.ent_max_p = ttk.Entry(row_n, width=4); self.ent_max_p.insert(0,"20"); self.ent_max_p.pack(side=tk.LEFT)
        self.var_online = tk.BooleanVar(value=True)
        self.chk_online_w = ttk.Checkbutton(row_n, variable=self.var_online); self.chk_online_w.pack(side=tk.LEFT, padx=10)
        self.lbl_motd = ttk.Label(self.f3, text=""); self.lbl_motd.pack(anchor='w', padx=5)
        self.ent_motd = ttk.Entry(self.f3); self.ent_motd.insert(0,"My Custom Server"); self.ent_motd.pack(fill="x", padx=5, pady=(0,5))
        self.btn_ip = ttk.Button(self.f3, text="", command=self.show_network_info); self.btn_ip.pack(pady=10)

        # Tab 3
        paned = ttk.PanedWindow(self.t3, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True, padx=5, pady=5)
        pf1, pf2 = ttk.Frame(paned), ttk.Frame(paned)
        paned.add(pf1, weight=1); paned.add(pf2, weight=1)
        self.gb_op = ttk.LabelFrame(pf1, text=""); self.gb_op.pack(fill="both", expand=True, pady=2)
        fi_op = ttk.Frame(self.gb_op); fi_op.pack(fill="x")
        self.ent_op = ttk.Entry(fi_op); self.ent_op.pack(side=tk.LEFT, fill="x", expand=True)
        self.btn_op_add = ttk.Button(fi_op, text="", width=3, command=lambda: self.add_user(self.ent_op, self.lb_op, self.ops_list, "OP")); self.btn_op_add.pack(side=tk.RIGHT)
        self.lb_op = tk.Listbox(self.gb_op, height=6); self.lb_op.pack(fill="both", expand=True)
        self.btn_op_del = ttk.Button(self.gb_op, text="", command=lambda: self.remove_user(self.lb_op, self.ops_list)); self.btn_op_del.pack(fill="x")
        self.gb_ban = ttk.LabelFrame(pf1, text=""); self.gb_ban.pack(fill="both", expand=True, pady=2)
        fi_ban = ttk.Frame(self.gb_ban); fi_ban.pack(fill="x")
        self.ent_ban = ttk.Entry(fi_ban); self.ent_ban.pack(side=tk.LEFT, fill="x", expand=True)
        self.btn_ban_add = ttk.Button(fi_ban, text="", width=3, command=lambda: self.add_user(self.ent_ban, self.lb_ban, self.banned_list, "BAN")); self.btn_ban_add.pack(side=tk.RIGHT)
        self.lb_ban = tk.Listbox(self.gb_ban, height=6); self.lb_ban.pack(fill="both", expand=True)
        self.btn_ban_del = ttk.Button(self.gb_ban, text="", command=lambda: self.remove_user(self.lb_ban, self.banned_list)); self.btn_ban_del.pack(fill="x")
        self.gb_wl = ttk.LabelFrame(pf2, text=""); self.gb_wl.pack(fill="both", expand=True, pady=2, padx=(5,0))
        self.var_wl = tk.BooleanVar(value=False)
        self.chk_wl_w = ttk.Checkbutton(self.gb_wl, variable=self.var_wl); self.chk_wl_w.pack(anchor='w')
        self.lbl_wl_hint = ttk.Label(self.gb_wl, text="", foreground="gray"); self.lbl_wl_hint.pack(anchor='w')
        fi_wl = ttk.Frame(self.gb_wl); fi_wl.pack(fill="x")
        self.ent_wl = ttk.Entry(fi_wl); self.ent_wl.pack(side=tk.LEFT, fill="x", expand=True)
        self.btn_wl_add = ttk.Button(fi_wl, text="", width=3, command=lambda: self.add_user(self.ent_wl, self.lb_wl, self.whitelist_list, "WL")); self.btn_wl_add.pack(side=tk.RIGHT)
        self.lb_wl = tk.Listbox(self.gb_wl, height=15); self.lb_wl.pack(fill="both", expand=True)
        self.btn_wl_del = ttk.Button(self.gb_wl, text="", command=lambda: self.remove_user(self.lb_wl, self.whitelist_list)); self.btn_wl_del.pack(fill="x")

        # Tab 4
        f_about = ttk.Frame(self.t4); f_about.pack(expand=True)
        ttk.Label(f_about, text="MinecraftServerInstaller", font=("Impact", 24)).pack(pady=10)
        f_info = ttk.Frame(f_about); f_info.pack(pady=5)
        r_ver = ttk.Frame(f_info); r_ver.pack(fill="x", pady=2)
        self.lbl_ver_t = ttk.Label(r_ver, font=("微軟正黑體", 11)); self.lbl_ver_t.pack(side=tk.LEFT)
        ttk.Label(r_ver, text=f" {CURRENT_VERSION}", font=("Arial", 11)).pack(side=tk.LEFT)
        r_auth = ttk.Frame(f_info); r_auth.pack(fill="x", pady=2)
        self.lbl_author_t = ttk.Label(r_auth, font=("微軟正黑體", 11)); self.lbl_author_t.pack(side=tk.LEFT)
        ttk.Label(r_auth, text=" 奶香威士忌", font=("微軟正黑體", 11)).pack(side=tk.LEFT)
        self.lbl_name_t = ttk.Label(self.t4) 
        f_mail = ttk.Frame(f_about); f_mail.pack(pady=15)
        self.lbl_issue_t = ttk.Label(f_mail, font=("微軟正黑體", 10)); self.lbl_issue_t.pack(side=tk.LEFT)
        ttk.Label(f_mail, text=" marker0921230@gmail.com", font=("Arial", 10)).pack(side=tk.LEFT)
        self.btn_copy = ttk.Button(f_mail, text="", command=lambda: self.copy_to_clipboard("marker0921230@gmail.com")); self.btn_copy.pack(side=tk.LEFT, padx=10)
        self.btn_donate = ttk.Button(f_about, text="", command=self.open_donate)
        self.btn_donate.pack(pady=10, ipadx=10, ipady=2)
        f_lang = ttk.Frame(f_about); f_lang.pack(pady=20)
        self.lbl_lang = ttk.Label(f_lang, text=""); self.lbl_lang.pack(side=tk.LEFT)
        self.combo_lang = ttk.Combobox(f_lang, values=["繁體中文", "English", "简体中文"], state="readonly", width=10)
        self.combo_lang.current(0)
        self.combo_lang.pack(side=tk.LEFT, padx=5)
        self.combo_lang.bind("<<ComboboxSelected>>", self.change_language)

        # Tab 5 (Updated with Notebook)
        self.nb_tut = ttk.Notebook(self.t5)
        self.nb_tut.pack(fill="both", expand=True, padx=10, pady=10)
        self.t5_quick = ttk.Frame(self.nb_tut)
        self.t5_detail = ttk.Frame(self.nb_tut)
        self.nb_tut.add(self.t5_quick, text="")
        self.nb_tut.add(self.t5_detail, text="")
        
        self.txt_tut_quick = scrolledtext.ScrolledText(self.t5_quick, font=("微軟正黑體", 11), state='disabled', wrap=tk.WORD)
        self.txt_tut_quick.pack(fill="both", expand=True)
        self.txt_tut_detail = scrolledtext.ScrolledText(self.t5_detail, font=("微軟正黑體", 10), state='disabled', wrap=tk.WORD)
        self.txt_tut_detail.pack(fill="both", expand=True)

        self.update_ui_texts()
        self.update_java_ui()
        self.cb_mode.current(0); self.cb_diff.current(2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerInstallerApp(root)
    root.mainloop()