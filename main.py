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

# ==========================================
#              語言字典 (Translations)
# ==========================================
TRANSLATIONS = {
    "繁體中文": {
        "tab1": " 📥 安裝部署 ", "tab2": " ⚙️ 規則設定 ", "tab3": " 🛡️ 權限管理 ", "tab4": " ℹ️ 關於 ", "tab5": " 📖 教學 ",
        "grp_basic": " 基礎配置 ", "lbl_path": "安裝路徑:", "btn_browse": "瀏覽...",
        "lbl_core": "核心類型:", "lbl_ver": "遊戲版本:", "lbl_ram": "記憶體 (Min/Max GB):",
        "btn_install": "開始安裝伺服器", "grp_log": "系統日誌",
        "grp_game": " 遊戲規則 ", "lbl_mode": "模式:", "lbl_diff": "難度:",
        "chk_pvp": "PVP (玩家傷害)", "chk_cmd": "指令方塊", "lbl_spawn": "重生點保護範圍:",
        "grp_net": " 連線設定 ", "lbl_port": "Port (端口):", "lbl_max": "最大人數:",
        "chk_online": "正版驗證 (Online Mode)", "lbl_motd": "MOTD (伺服器描述):",
        "btn_ip": "🔍 顯示 IP 連線資訊",
        "grp_op": " 👑 管理員 (OP) ", "grp_ban": " ⛔ 黑名單 (Ban) ", "grp_wl": " 🔒 白名單 ",
        "btn_add": "+", "btn_remove": "移除選取",
        "chk_wl": "啟用白名單限制", "lbl_wl_hint": "(未勾選則開放所有人)",
        "lbl_name": "軟體名稱:", "lbl_version": "版本:", "lbl_author": "發行:",
        "lbl_issue": "問題回報:", "btn_copy": "📋 複製", "lbl_lang": "語言 (Language):",
        "msg_install_ok": "安裝成功！\n路徑: ", "msg_install_err": "安裝發生錯誤: ",
        "msg_copy": "已複製到剪貼簿", "status_init": "系統初始化...", "status_ver_ok": "版本列表讀取完成",
        "val_survival": "生存", "val_creative": "創造", "val_adventure": "冒險",
        "val_peaceful": "和平", "val_easy": "簡單", "val_normal": "普通", "val_hard": "困難",
        "lbl_lan_ip": "🏠 區網 IP (同住家人連):", 
        "lbl_pub_ip": "🌏 公網 IP (給遠端朋友連):",
        "msg_ip_hint": "(遠端連線請配合路由器設定端口映射 Port Forwarding 25565)",
        "err_neoforge_ver": "NeoForge 僅支援 Minecraft 1.20.1 (含) 以上版本。\n請改選 Forge 或 Fabric。",
        "lbl_java_ver": "偵測到的 Java:",
        "msg_java_scanning": "正在掃描 Java...",
        "msg_java_found": "已找到 Java 版本: {}",
        "err_java_missing": "❌ 嚴重錯誤：找不到適合的 Java 版本！\n\nMinecraft {} 需要 Java {}。\n\n請去下載安裝 Java {}。",
        "msg_java_auto_bind": "✅ 已自動綁定 Java {} 路徑:\n{}",
        "tutorial_text": """【Minecraft 伺服器架設教學】

步驟 0：檢查 Java
請確認「基礎配置」上方顯示的 Java 版本符合需求：
- MC 1.20.5 以上 -> 需要 Java 21
- MC 1.18 - 1.20.4 -> 需要 Java 17
- MC 1.17 以下 -> 需要 Java 8 或 11

步驟 1：安裝伺服器
1. 在「📥 安裝部署」分頁，點擊「瀏覽」選擇一個空資料夾。
2. 選擇「Fabric」、「Forge」或「NeoForge」，並選擇遊戲版本。
3. 設定記憶體 (建議 4GB 以上) 並點擊「開始安裝」。

步驟 2：啟動伺服器
1. 安裝完成後，前往您選擇的資料夾。
2. 找到並點擊兩下 「start.bat」 檔案。
3. 等待黑色視窗跑完，出現 "Done!" 字樣即代表開啟成功。

步驟 3：連線進入遊戲
1. 本機連線 (你自己)：在多人遊戲輸入 「localhost」。
2. 家人連線 (同一個 Wi-Fi)：輸入您的 「區網 IP」。
3. 朋友連線 (不同網路)：輸入您的 「公網 IP」。
   (可在「⚙️ 規則設定」分頁點擊「🔍 顯示 IP」查詢)

⚠️ 重要：遠端連線 (朋友連不進來？)
若朋友無法連線，您必須進入家裡的「路由器後台 (Wi-Fi 機)」。
設定「端口映射 (Port Forwarding)」，將端口 25565 開放給您的區網 IP。

步驟 4：管理員與權限
1. 在「🛡️ 權限管理」分頁，輸入您的遊戲 ID 並加入「管理員 (OP)」。
2. 重新安裝一次 (會自動更新 ops.json) 或重啟伺服器即可生效。
"""
    },
    "English": {
        "tab1": " 📥 Install ", "tab2": " ⚙️ Settings ", "tab3": " 🛡️ Permissions ", "tab4": " ℹ️ About ", "tab5": " 📖 Tutorial ",
        "grp_basic": " Basic Config ", "lbl_path": "Install Path:", "btn_browse": "Browse...",
        "lbl_core": "Loader:", "lbl_ver": "Version:", "lbl_ram": "RAM (Min/Max GB):",
        "btn_install": "Start Installation", "grp_log": "System Log",
        "grp_game": " Game Rules ", "lbl_mode": "Gamemode:", "lbl_diff": "Difficulty:",
        "chk_pvp": "PVP Enabled", "chk_cmd": "Command Blocks", "lbl_spawn": "Spawn Protection:",
        "grp_net": " Network ", "lbl_port": "Server Port:", "lbl_max": "Max Players:",
        "chk_online": "Online Mode (Premium)", "lbl_motd": "MOTD (Description):",
        "btn_ip": "🔍 Show IP Info",
        "grp_op": " 👑 Operators (OP) ", "grp_ban": " ⛔ Banned Players ", "grp_wl": " 🔒 Whitelist ",
        "btn_add": "Add", "btn_remove": "Remove Selected",
        "chk_wl": "Enable Whitelist", "lbl_wl_hint": "(Everyone can join if unchecked)",
        "lbl_name": "Software:", "lbl_version": "Version:", "lbl_author": "Author:",
        "lbl_issue": "Report Issue:", "btn_copy": "📋 Copy", "lbl_lang": "Language:",
        "msg_install_ok": "Installation Complete!\nPath: ", "msg_install_err": "Error: ",
        "msg_copy": "Copied to clipboard", "status_init": "Initializing...", "status_ver_ok": "Versions loaded",
        "val_survival": "survival", "val_creative": "creative", "val_adventure": "adventure",
        "val_peaceful": "peaceful", "val_easy": "easy", "val_normal": "normal", "val_hard": "hard",
        "lbl_lan_ip": "🏠 LAN IP (Home Network):", 
        "lbl_pub_ip": "🌏 Public IP (Internet):",
        "msg_ip_hint": "(Requires Port Forwarding 25565 on your router for public access)",
        "err_neoforge_ver": "NeoForge only supports Minecraft 1.20.1 or newer.\nPlease use Forge or Fabric instead.",
        "lbl_java_ver": "Detected Java:",
        "msg_java_scanning": "Scanning Java...",
        "msg_java_found": "Found Java versions: {}",
        "err_java_missing": "❌ Critical Error: Compatible Java not found!\n\nMinecraft {} requires Java {}.\n\nPlease install Java {}.",
        "msg_java_auto_bind": "✅ Auto-bound Java {} path:\n{}",
        "tutorial_text": """【Minecraft Server Tutorial】

Step 0: Check Java
Ensure your Java version matches the game version:
- MC 1.20.5+ -> Requires Java 21
- MC 1.18 - 1.20.4 -> Requires Java 17
- MC 1.17 & older -> Requires Java 8 or 11

Step 1: Install Server
1. Select an empty folder.
2. Choose Loader and Version.
3. Click "Start Installation".

Step 2: Launch Server
1. Go to folder, run "start.bat".
2. Wait for "Done!".

Step 3: Join Game
1. Local (You): Connect to "localhost".
2. LAN (Family): Connect to "LAN IP".
3. Public (Friends): Connect to "Public IP".

⚠️ Issues? Use Port Forwarding (25565).
"""
    },
    "简体中文": {
        "tab1": " 📥 安装部署 ", "tab2": " ⚙️ 规则设定 ", "tab3": " 🛡️ 权限管理 ", "tab4": " ℹ️ 关于 ", "tab5": " 📖 教程 ",
        "grp_basic": " 基础配置 ", "lbl_path": "安装路径:", "btn_browse": "浏览...",
        "lbl_core": "核心类型:", "lbl_ver": "游戏版本:", "lbl_ram": "内存 (Min/Max GB):",
        "btn_install": "开始安装服务器", "grp_log": "系统日志",
        "grp_game": " 游戏规则 ", "lbl_mode": "模式:", "lbl_diff": "难度:",
        "chk_pvp": "PVP (玩家伤害)", "chk_cmd": "命令方块", "lbl_spawn": "出生点保护范围:",
        "grp_net": " 连线设定 ", "lbl_port": "Port (端口):", "lbl_max": "最大人数:",
        "chk_online": "正版验证 (Online Mode)", "lbl_motd": "MOTD (服务器描述):",
        "btn_ip": "🔍 显示 IP 连线信息",
        "grp_op": " 👑 管理员 (OP) ", "grp_ban": " ⛔ 黑名单 (Ban) ", "grp_wl": " 🔒 白名单 ",
        "btn_add": "+", "btn_remove": "移除选中",
        "chk_wl": "启用白名单限制", "lbl_wl_hint": "(未勾选则开放所有人)",
        "lbl_name": "软件名称:", "lbl_version": "版本:", "lbl_author": "发行:",
        "lbl_issue": "问题回报:", "btn_copy": "📋 复制", "lbl_lang": "语言 (Language):",
        "msg_install_ok": "安装成功！\n路径: ", "msg_install_err": "安装发生错误: ",
        "msg_copy": "已复制到剪贴簿", "status_init": "系统初始化...", "status_ver_ok": "版本列表读取完成",
        "val_survival": "生存", "val_creative": "创造", "val_adventure": "冒险",
        "val_peaceful": "和平", "val_easy": "简单", "val_normal": "普通", "val_hard": "困难",
        "lbl_lan_ip": "🏠 局域网 IP (同住家人连):", 
        "lbl_pub_ip": "🌏 公网 IP (给远端朋友连):",
        "msg_ip_hint": "(远端连线请配合路由器设定端口映射 Port Forwarding 25565)",
        "err_neoforge_ver": "NeoForge 仅支持 Minecraft 1.20.1 (含) 以上版本。\n请改选 Forge 或 Fabric。",
        "lbl_java_ver": "侦测到的 Java:",
        "msg_java_scanning": "正在扫描 Java...",
        "msg_java_found": "已找到 Java 版本: {}",
        "err_java_missing": "❌ 严重错误：找不到适合的 Java 版本！\n\nMinecraft {} 需要 Java {}。\n\n请去下载安装 Java {}。",
        "msg_java_auto_bind": "✅ 已自动绑定 Java {} 路径:\n{}",
        "tutorial_text": """【Minecraft 服务器架设教程】

步骤 0：检查 Java
请确认「基础配置」上方显示的 Java 版本符合需求：
- MC 1.20.5 以上 -> 需要 Java 21
- MC 1.18 - 1.20.4 -> 需要 Java 17
- MC 1.17 以下 -> 需要 Java 8 或 11

步骤 1：安装服务器
1. 在「📥 安装部署」分页，点击「浏览」选择一个空文件夹。
2. 选择「Fabric」、「Forge」或「NeoForge」，并选择游戏版本。
3. 设定内存 (建议 4GB 以上) 并点击「开始安装」。

步骤 2：启动服务器
1. 安装完成后，前往您选择的文件夹。
2. 找到并双击 「start.bat」 文件。
3. 等待黑色窗口跑完，出现 "Done!" 字样即代表开启成功。

步骤 3：连线进入游戏
1. 本机连线 (你自己)：在多人游戏输入 「localhost」。
2. 家人连线 (同一个 Wi-Fi)：输入您的 「局域网 IP」。
3. 朋友连线 (不同网络)：输入您的 「公网 IP」。
   (可在「⚙️ 规则设定」分页点击「🔍 显示 IP」查询)

⚠️ 重要：远端连线 (朋友连不进来？)
若朋友无法连线，您必须进入家里的「路由器后台 (Wi-Fi 机)」。
设定「端口映射 (Port Forwarding)」，将端口 25565 开放给您的局域网 IP。

步骤 4：管理员与权限
1. 在「🛡️ 权限管理」分页，输入您的游戏 ID 并加入「管理员 (OP)」。
2. 重新安装一次 (会自动更新 ops.json) 或重启服务器即可生效。
"""
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
        
        # 儲存找到的 Java 路徑字典 {版本號: 路徑}
        self.found_java_paths = {} 

        self.setup_ui()
        self.log(self.get_text("status_init"))
        
        # 啟動時掃描所有 Java
        threading.Thread(target=self.scan_all_java_versions, daemon=True).start()
        threading.Thread(target=self.load_versions_async, daemon=True).start()

    def get_text(self, key):
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
        self.f1.config(text=self.get_text("grp_basic"))
        self.lbl_path.config(text=self.get_text("lbl_path"))
        self.btn_browse.config(text=self.get_text("btn_browse"))
        self.lbl_core.config(text=self.get_text("lbl_core"))
        self.lbl_ver.config(text=self.get_text("lbl_ver"))
        self.lbl_ram.config(text=self.get_text("lbl_ram"))
        self.btn_run.config(text=self.get_text("btn_install"))
        self.lf_log.config(text=self.get_text("grp_log"))
        self.f2.config(text=self.get_text("grp_game"))
        self.lbl_mode.config(text=self.get_text("lbl_mode"))
        self.lbl_diff.config(text=self.get_text("lbl_diff"))
        self.chk_pvp_w.config(text=self.get_text("chk_pvp"))
        self.chk_cmd_w.config(text=self.get_text("chk_cmd"))
        self.lbl_spawn.config(text=self.get_text("lbl_spawn"))
        self.f3.config(text=self.get_text("grp_net"))
        self.lbl_port.config(text=self.get_text("lbl_port"))
        self.lbl_max.config(text=self.get_text("lbl_max"))
        self.chk_online_w.config(text=self.get_text("chk_online"))
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
        
        # 更新教學 Tab (加入 wrap=tk.WORD 解決跑版問題)
        self.txt_tutorial.config(state='normal')
        self.txt_tutorial.delete(1.0, tk.END)
        self.txt_tutorial.insert(tk.END, self.get_text("tutorial_text"))
        self.txt_tutorial.config(state='disabled')

    def log(self, message):
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        self.txt_log.config(state='normal')
        self.txt_log.insert(tk.END, f"[{timestamp}] {message}\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state='disabled')

    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        messagebox.showinfo("OK", self.get_text("msg_copy"))

    # --- 強力 Java 掃描邏輯 ---
    def check_java_version(self, java_path):
        """ 檢查指定 java.exe 的版本 """
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
        """ 掃描系統中所有可能的 Java 安裝 """
        self.root.after(0, lambda: self.lbl_java_val.config(text=self.get_text("msg_java_scanning"), foreground="blue"))
        
        found = {}
        
        # 1. 檢查系統預設 (PATH)
        sys_ver = self.check_java_version("java")
        if sys_ver > 0:
            found[sys_ver] = "java" # 標記為預設指令
        
        # 2. 暴力掃描常見路徑
        possible_roots = [
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Java"),
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Eclipse Adoptium"),
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Microsoft"),
            os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Zulu"),
            os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Java")
        ]

        for root in possible_roots:
            if os.path.exists(root):
                # 搜尋該目錄下所有的 java.exe
                # 使用 glob 遞迴搜尋 bin/java.exe
                for java_exe in glob.glob(os.path.join(root, "**", "bin", "java.exe"), recursive=True):
                    ver = self.check_java_version(java_exe)
                    if ver > 0 and ver not in found:
                        found[ver] = java_exe # 儲存絕對路徑
        
        self.found_java_paths = found
        self.root.after(0, self.update_java_ui)
        
        # Log 紀錄
        found_vers = sorted(found.keys())
        self.log(f"Java Scan Complete. Found: {found_vers}")

    def update_java_ui(self):
        """ 顯示找到的 Java 版本列表 """
        if self.found_java_paths:
            vers = sorted(self.found_java_paths.keys())
            txt = ", ".join([f"Java {v}" for v in vers])
            color = "green"
        else:
            txt = "None"
            color = "red"
        self.lbl_java_txt.config(text=self.get_text("lbl_java_ver"))
        self.lbl_java_val.config(text=txt, foreground=color)

    def get_required_java(self, mc_version):
        try:
            parts = [int(x) for x in mc_version.split('.')]
            major, minor = parts[0], parts[1]
            patch = parts[2] if len(parts) > 2 else 0
            
            if major == 1 and minor >= 21: return 21 # 1.21+
            if major == 1 and minor == 20 and patch >= 5: return 21 # 1.20.5+
            if major == 1 and minor >= 18: return 17 # 1.18 - 1.20.4
            if major == 1 and minor == 17: return 16 
            return 8 # 1.16.5 and below
        except:
            return 8

    # --- 網路與 API ---
    def get_minecraft_versions(self):
        url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            return [v["id"] for v in data["versions"] if v["type"] == "release"]
        except:
            return ["1.20.4", "1.20.1", "1.19.4", "1.18.2", "1.16.5"]

    def get_forge_build(self, mc_version):
        url = "https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json"
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=10)
            data = r.json()
            promos = data.get("promos", {})
            return promos.get(f"{mc_version}-recommended") or promos.get(f"{mc_version}-latest")
        except:
            return None

    def get_neoforge_version(self, mc_ver):
        api_url = "https://maven.neoforged.net/api/maven/versions/releases/net/neoforged/neoforge"
        try:
            r = requests.get(api_url, timeout=5)
            data = r.json()
            versions = data.get('versions', [])
            target_prefix = ""
            if mc_ver == "1.20.1":
                target_prefix = "1.20.1"
            else:
                parts = mc_ver.split('.')
                if len(parts) >= 2:
                    major = parts[1] 
                    minor = parts[2] if len(parts) > 2 else '0'
                    target_prefix = f"{major}.{minor}"
            candidates = [v for v in versions if v.startswith(target_prefix)]
            if candidates: return candidates[-1]
            return None
        except:
            return None

    def get_player_uuid(self, username):
        url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                raw = data['id']
                fmt = f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"
                return fmt, data['name']
            return None, None
        except:
            return None, None

    def load_versions_async(self):
        vers = self.get_minecraft_versions()
        self.root.after(0, lambda: self.combo_ver.config(values=vers))
        self.root.after(0, lambda: self.combo_ver.current(0) if vers else None)
        self.root.after(0, lambda: self.log(self.get_text("status_ver_ok")))

    def show_network_info(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            public_ip = requests.get('https://api.ipify.org', timeout=3).text
        except:
            local_ip = "Unknown"
            public_ip = "Unknown"
        msg = (f"{self.get_text('lbl_lan_ip')} {local_ip}\n"
               f"{self.get_text('lbl_pub_ip')} {public_ip}\n\n"
               f"{self.get_text('msg_ip_hint')}")
        messagebox.showinfo("IP Info", msg)

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
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", f"User not found: {name}"))
        threading.Thread(target=task).start()

    def remove_user(self, listbox, target_list):
        sel = listbox.curselection()
        if not sel: return
        idx = sel[0]
        removed = target_list.pop(idx)
        listbox.delete(idx)
        self.log(f"Removed: {removed['name']}")

    def run_cmd(self, cmd):
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        return subprocess.run(cmd, capture_output=True, text=True, startupinfo=info)

    def is_valid_neoforge_version(self, v):
        try:
            parts = v.split('.')
            if len(parts) < 2: return False
            major = int(parts[0])
            minor = int(parts[1])
            if major == 1 and minor >= 20:
                if minor == 20:
                    patch = int(parts[2]) if len(parts) > 2 else 0
                    return patch >= 1 
                return True
            return False
        except:
            return False

    def install_process(self, s):
        target = s['path']
        mc_ver = s['version']
        
        # 1. NeoForge 防呆
        if s['loader'] == "NeoForge":
            if not self.is_valid_neoforge_version(mc_ver):
                messagebox.showerror("Error", self.get_text("err_neoforge_ver"))
                self.btn_run.config(state=tk.NORMAL)
                return

        # 2. 強制 Java 版本匹配
        req_java = self.get_required_java(mc_ver)
        selected_java_path = "java" # 預設使用系統環境變數

        match_found = False
        
        # 先找完全匹配的
        if req_java in self.found_java_paths:
            selected_java_path = self.found_java_paths[req_java]
            match_found = True
        # 沒找到完全匹配，試試看有沒有更新的 (例如需要 17，但有 21，通常向下相容)
        elif req_java >= 17:
             for v in sorted(self.found_java_paths.keys()):
                 if v >= req_java:
                     selected_java_path = self.found_java_paths[v]
                     match_found = True
                     break
        
        # 如果還是沒找到，檢查系統預設是否剛好符合
        if not match_found:
             sys_ver = self.check_java_version("java")
             if sys_ver > 0 and (sys_ver == req_java or (req_java >= 17 and sys_ver >= req_java)):
                 selected_java_path = "java"
                 match_found = True

        # 如果最終還是沒找到合適的 Java -> 阻擋
        if not match_found:
            msg = self.get_text("err_java_missing").format(mc_ver, req_java, req_java)
            messagebox.showerror("Java Error", msg)
            self.log(f"❌ Aborted: Missing Java {req_java}")
            self.btn_run.config(state=tk.NORMAL)
            return

        final_java_cmd = f'"{selected_java_path}"' if " " in selected_java_path else selected_java_path

        if not os.path.exists(target):
            try: os.makedirs(target)
            except: self.log(self.get_text("msg_install_err") + "Create dir failed"); return
        cwd = os.getcwd()
        os.chdir(target)
        try:
            self.log(f"Target: {target}")
            self.log(self.get_text("msg_java_auto_bind").format(req_java, selected_java_path))

            if s['loader'] == "Fabric": 
                self.install_fabric(mc_ver)
            elif s['loader'] == "NeoForge":
                self.install_neoforge(mc_ver)
            else: 
                self.install_forge(mc_ver)
            
            with open("eula.txt", "w") as f: f.write("eula=true\n")
            self.gen_props(s)
            self.gen_json()
            # 傳入決定的 java 指令
            self.gen_bat(s['loader'], s['ram_min'], s['ram_max'], final_java_cmd)
            
            if not os.path.exists("mods"): os.makedirs("mods")
            self.log(self.get_text("msg_install_ok"))
            messagebox.showinfo("OK", self.get_text("msg_install_ok") + target)
        except Exception as e:
            self.log(self.get_text("msg_install_err") + str(e))
            messagebox.showerror("Error", str(e))
        finally:
            os.chdir(cwd)
            self.btn_run.config(state=tk.NORMAL)
            self.prog['value'] = 100

    def install_fabric(self, v):
        name = "fabric-installer.jar"
        url = "https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.0/fabric-installer-1.0.0.jar"
        self.log("Download Fabric...")
        with open(name, 'wb') as f: f.write(requests.get(url).content)
        self.log(f"Install Fabric {v}...")
        cmd = ["java", "-jar", name, "server", "-mcversion", v, "-downloadMinecraft"]
        if self.run_cmd(cmd).returncode != 0: raise Exception("Fabric Install Failed")
        if os.path.exists(name): os.remove(name)

    def install_forge(self, v):
        self.log(f"Check Forge {v}...")
        build = self.get_forge_build(v)
        if not build: raise Exception(f"Forge {v} not found")
        full = f"{v}-{build}"
        name = f"forge-{full}-installer.jar"
        url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{full}/{name}"
        self.log(f"Download Forge ({build})...")
        r = requests.get(url)
        if r.status_code != 200: raise Exception("Forge Download Failed")
        with open(name, 'wb') as f: f.write(r.content)
        self.log("Install Forge...")
        if self.run_cmd(["java", "-jar", name, "--installServer"]).returncode != 0: raise Exception("Forge Install Failed")
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
        if self.run_cmd(["java", "-jar", name, "--installServer"]).returncode != 0: raise Exception("NeoForge Install Failed")
        if os.path.exists(name): os.remove(name)
        if os.path.exists(name+".log"): os.remove(name+".log")

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
        """ 產生 start.bat，並使用指定的 Java 路徑 """
        txt = ""
        # 移除引號以便判斷
        clean_java_path = java_path.replace('"', '')
        
        if os.path.exists("run.bat") or os.path.exists("run.sh"):
            # 如果是 run.bat 結構，我們透過環境變數傳遞 JAVA_HOME 給它 (如果可以) 
            # 或者直接在 user_jvm_args.txt 寫記憶體
            with open("user_jvm_args.txt", "w") as f: f.write(f"-Xms{min_r}G\n-Xmx{max_r}G\n")
            
            # Forge/NeoForge 的 run.bat 通常會抓 JAVA_HOME 或 PATH
            # 我們這裡強制指定 PATH
            txt = f'@echo off\nset PATH={os.path.dirname(clean_java_path)};%PATH%\ncall run.bat\npause'
        else:
            jar = "server.jar"
            for f in os.listdir("."):
                if f.startswith("forge") and f.endswith(".jar") and "installer" not in f: jar = f; break
                if f == "fabric-server-launch.jar": jar = f; break
            
            # 使用我們偵測到的絕對路徑 java_path
            txt = f'@echo off\n{java_path} -Xms{min_r}G -Xmx{max_r}G -jar {jar} nogui\npause'
            
        with open("start.bat", "w") as f: f.write(txt)

    def select_dir(self):
        d = filedialog.askdirectory()
        if d: self.ent_path.delete(0, tk.END); self.ent_path.insert(0, d)

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
            'wl': self.var_wl.get()
        }
        
        if not s['ram_min'].isdigit() or not s['ram_max'].isdigit():
            messagebox.showwarning("Error", "RAM must be number"); return

        # 安裝程序會在內部進行 Java 檢查
        self.btn_run.config(state=tk.DISABLED)
        self.prog['value'] = 0
        self.txt_log.config(state='normal'); self.txt_log.delete(1.0, tk.END); self.txt_log.config(state='disabled')
        threading.Thread(target=self.install_process, args=(s,)).start()

    # ==========================================
    #              介面設計區 (Frontend)
    # ==========================================
    def setup_ui(self):
        self.root.title("MinecraftServerInstaller v0.0.2")
        self.root.geometry("620x780")
        
        if os.path.exists("logo.ico"):
            try: self.root.iconbitmap("logo.ico")
            except: pass

        style = ttk.Style()
        style.theme_use('vista')

        self.nb = ttk.Notebook(self.root)
        self.nb.pack(pady=10, padx=10, fill="both", expand=True)
        self.t1, self.t2, self.t3, self.t4, self.t5 = ttk.Frame(self.nb), ttk.Frame(self.nb), ttk.Frame(self.nb), ttk.Frame(self.nb), ttk.Frame(self.nb)
        self.nb.add(self.t1, text=""); self.nb.add(self.t2, text=""); self.nb.add(self.t3, text=""); self.nb.add(self.t4, text=""); self.nb.add(self.t5, text="")

        # --- Tab 1 ---
        self.f1 = ttk.LabelFrame(self.t1, text="")
        self.f1.pack(padx=10, pady=10, fill="x")
        
        # Java 偵測顯示列
        r_java = ttk.Frame(self.f1); r_java.pack(fill="x", pady=5)
        self.lbl_java_txt = ttk.Label(r_java, text="", font=("Microsoft YaHei", 9, "bold")); self.lbl_java_txt.pack(side=tk.LEFT)
        self.lbl_java_val = ttk.Label(r_java, text="", font=("Microsoft YaHei", 9, "bold")); self.lbl_java_val.pack(side=tk.LEFT, padx=5)

        r0 = ttk.Frame(self.f1); r0.pack(fill="x", pady=5)
        self.lbl_path = ttk.Label(r0, text="")
        self.lbl_path.pack(side=tk.LEFT)
        self.ent_path = ttk.Entry(r0); self.ent_path.pack(side=tk.LEFT, fill="x", expand=True, padx=5)
        self.btn_browse = ttk.Button(r0, text="", command=self.select_dir)
        self.btn_browse.pack(side=tk.RIGHT)

        r1 = ttk.Frame(self.f1); r1.pack(fill="x", pady=5)
        self.lbl_core = ttk.Label(r1, text="")
        self.lbl_core.pack(side=tk.LEFT)
        self.var_load = tk.StringVar(value="Fabric")
        ttk.Radiobutton(r1, text="Fabric", variable=self.var_load, value="Fabric").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(r1, text="Forge", variable=self.var_load, value="Forge").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(r1, text="NeoForge", variable=self.var_load, value="NeoForge").pack(side=tk.LEFT)
        self.lbl_ver = ttk.Label(r1, text="")
        self.lbl_ver.pack(side=tk.LEFT, padx=10)
        self.combo_ver = ttk.Combobox(r1, state="readonly", width=12); self.combo_ver.pack(side=tk.LEFT)

        r2 = ttk.Frame(self.f1); r2.pack(fill="x", pady=5)
        self.lbl_ram = ttk.Label(r2, text="")
        self.lbl_ram.pack(side=tk.LEFT)
        self.ent_min = ttk.Entry(r2, width=3); self.ent_min.insert(0,"2"); self.ent_min.pack(side=tk.LEFT, padx=2)
        ttk.Label(r2, text="/").pack(side=tk.LEFT)
        self.ent_max = ttk.Entry(r2, width=3); self.ent_max.insert(0,"4"); self.ent_max.pack(side=tk.LEFT, padx=2)

        self.btn_run = ttk.Button(self.t1, text="", command=self.start_install)
        self.btn_run.pack(pady=5, ipadx=20, ipady=5)
        self.prog = ttk.Progressbar(self.t1, mode="determinate"); self.prog.pack(fill="x", padx=20)
        
        self.lf_log = ttk.LabelFrame(self.t1, text="")
        self.lf_log.pack(fill="both", expand=True, padx=10, pady=5)
        self.txt_log = scrolledtext.ScrolledText(self.lf_log, height=8, state='disabled', font=("Consolas", 9)); self.txt_log.pack(fill="both", expand=True)

        # --- Tab 2 ---
        self.f2 = ttk.LabelFrame(self.t2, text="")
        self.f2.pack(padx=10, pady=10, fill="x")
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

        self.f3 = ttk.LabelFrame(self.t2, text="")
        self.f3.pack(padx=10, pady=10, fill="x")
        row_n = ttk.Frame(self.f3); row_n.pack(fill="x", pady=5)
        self.lbl_port = ttk.Label(row_n, text=""); self.lbl_port.pack(side=tk.LEFT)
        self.ent_port = ttk.Entry(row_n, width=6); self.ent_port.insert(0,"25565"); self.ent_port.pack(side=tk.LEFT)
        self.lbl_max = ttk.Label(row_n, text=""); self.lbl_max.pack(side=tk.LEFT, padx=5)
        self.ent_max_p = ttk.Entry(row_n, width=4); self.ent_max_p.insert(0,"20"); self.ent_max_p.pack(side=tk.LEFT)
        self.var_online = tk.BooleanVar(value=True)
        self.chk_online_w = ttk.Checkbutton(row_n, variable=self.var_online); self.chk_online_w.pack(side=tk.LEFT, padx=10)
        
        self.lbl_motd = ttk.Label(self.f3, text=""); self.lbl_motd.pack(anchor='w', padx=5)
        self.ent_motd = ttk.Entry(self.f3); self.ent_motd.insert(0,"My Custom Server"); self.ent_motd.pack(fill="x", padx=5, pady=(0,5))
        
        self.btn_ip = ttk.Button(self.f3, text="", command=self.show_network_info)
        self.btn_ip.pack(pady=10)

        # --- Tab 3 ---
        paned = ttk.PanedWindow(self.t3, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True, padx=5, pady=5)
        pf1, pf2 = ttk.Frame(paned), ttk.Frame(paned)
        paned.add(pf1, weight=1); paned.add(pf2, weight=1)

        self.gb_op = ttk.LabelFrame(pf1, text="")
        self.gb_op.pack(fill="both", expand=True, pady=2)
        fi_op = ttk.Frame(self.gb_op); fi_op.pack(fill="x")
        self.ent_op = ttk.Entry(fi_op); self.ent_op.pack(side=tk.LEFT, fill="x", expand=True)
        self.btn_op_add = ttk.Button(fi_op, text="", width=3, command=lambda: self.add_user(self.ent_op, self.lb_op, self.ops_list, "OP"))
        self.btn_op_add.pack(side=tk.RIGHT)
        self.lb_op = tk.Listbox(self.gb_op, height=6); self.lb_op.pack(fill="both", expand=True)
        self.btn_op_del = ttk.Button(self.gb_op, text="", command=lambda: self.remove_user(self.lb_op, self.ops_list))
        self.btn_op_del.pack(fill="x")

        self.gb_ban = ttk.LabelFrame(pf1, text="")
        self.gb_ban.pack(fill="both", expand=True, pady=2)
        fi_ban = ttk.Frame(self.gb_ban); fi_ban.pack(fill="x")
        self.ent_ban = ttk.Entry(fi_ban); self.ent_ban.pack(side=tk.LEFT, fill="x", expand=True)
        self.btn_ban_add = ttk.Button(fi_ban, text="", width=3, command=lambda: self.add_user(self.ent_ban, self.lb_ban, self.banned_list, "BAN"))
        self.btn_ban_add.pack(side=tk.RIGHT)
        self.lb_ban = tk.Listbox(self.gb_ban, height=6); self.lb_ban.pack(fill="both", expand=True)
        self.btn_ban_del = ttk.Button(self.gb_ban, text="", command=lambda: self.remove_user(self.lb_ban, self.banned_list))
        self.btn_ban_del.pack(fill="x")

        self.gb_wl = ttk.LabelFrame(pf2, text="")
        self.gb_wl.pack(fill="both", expand=True, pady=2, padx=(5,0))
        self.var_wl = tk.BooleanVar(value=False)
        self.chk_wl_w = ttk.Checkbutton(self.gb_wl, variable=self.var_wl); self.chk_wl_w.pack(anchor='w')
        self.lbl_wl_hint = ttk.Label(self.gb_wl, text="", foreground="gray"); self.lbl_wl_hint.pack(anchor='w')
        
        fi_wl = ttk.Frame(self.gb_wl); fi_wl.pack(fill="x")
        self.ent_wl = ttk.Entry(fi_wl); self.ent_wl.pack(side=tk.LEFT, fill="x", expand=True)
        self.btn_wl_add = ttk.Button(fi_wl, text="", width=3, command=lambda: self.add_user(self.ent_wl, self.lb_wl, self.whitelist_list, "WL"))
        self.btn_wl_add.pack(side=tk.RIGHT)
        self.lb_wl = tk.Listbox(self.gb_wl, height=15); self.lb_wl.pack(fill="both", expand=True)
        self.btn_wl_del = ttk.Button(self.gb_wl, text="", command=lambda: self.remove_user(self.lb_wl, self.whitelist_list))
        self.btn_wl_del.pack(fill="x")

        # --- Tab 4: 關於 ---
        f_about = ttk.Frame(self.t4); f_about.pack(expand=True)
        ttk.Label(f_about, text="MinecraftServerInstaller", font=("Impact", 24)).pack(pady=10)
        
        f_info = ttk.Frame(f_about); f_info.pack(pady=5)
        
        r_ver = ttk.Frame(f_info); r_ver.pack(fill="x", pady=2)
        self.lbl_ver_t = ttk.Label(r_ver, font=("微軟正黑體", 11)); self.lbl_ver_t.pack(side=tk.LEFT)
        ttk.Label(r_ver, text=" 0.0.2", font=("Arial", 11)).pack(side=tk.LEFT)
        
        r_auth = ttk.Frame(f_info); r_auth.pack(fill="x", pady=2)
        self.lbl_author_t = ttk.Label(r_auth, font=("微軟正黑體", 11)); self.lbl_author_t.pack(side=tk.LEFT)
        ttk.Label(r_auth, text=" 奶香威士忌", font=("微軟正黑體", 11)).pack(side=tk.LEFT)

        self.lbl_name_t = ttk.Label(self.t4) # 隱藏使用(為了字典)

        f_mail = ttk.Frame(f_about); f_mail.pack(pady=15)
        self.lbl_issue_t = ttk.Label(f_mail, font=("微軟正黑體", 10)); self.lbl_issue_t.pack(side=tk.LEFT)
        ttk.Label(f_mail, text=" marker0921230@gmail.com", font=("Arial", 10)).pack(side=tk.LEFT)
        self.btn_copy = ttk.Button(f_mail, text="", command=lambda: self.copy_to_clipboard("marker0921230@gmail.com"))
        self.btn_copy.pack(side=tk.LEFT, padx=10)

        # 語言選擇
        f_lang = ttk.Frame(f_about); f_lang.pack(pady=20)
        self.lbl_lang = ttk.Label(f_lang, text=""); self.lbl_lang.pack(side=tk.LEFT)
        self.combo_lang = ttk.Combobox(f_lang, values=["繁體中文", "English", "简体中文"], state="readonly", width=10)
        self.combo_lang.current(0)
        self.combo_lang.pack(side=tk.LEFT, padx=5)
        self.combo_lang.bind("<<ComboboxSelected>>", self.change_language)

        # --- Tab 5: 教學 ---
        f_tut = ttk.Frame(self.t5); f_tut.pack(fill="both", expand=True, padx=10, pady=10)
        self.txt_tutorial = scrolledtext.ScrolledText(f_tut, font=("微軟正黑體", 10), state='disabled', wrap=tk.WORD)
        self.txt_tutorial.pack(fill="both", expand=True)

        # 初始化文字
        self.update_ui_texts()
        self.cb_mode.current(0); self.cb_diff.current(2)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerInstallerApp(root)
    root.mainloop()