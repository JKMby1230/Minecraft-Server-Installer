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
import webbrowser # <--- 新增這個

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
        "btn_donate": "☕ 請作者喝咖啡 (贊助)", # 新增翻譯
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
        "tutorial_text": """【Minecraft 伺服器架設教學】...""" # 略
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
        "btn_donate": "☕ Buy me a coffee (Donate)", # 新增翻譯
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
        "tutorial_text": "..."
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
        "btn_donate": "☕ 请作者喝咖啡 (赞助)", # 新增翻譯
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
        "tutorial_text": "..."
    }
}

# ... (中間的 ServerInstallerApp Class 等邏輯保持不變，直接複製原本的即可) ...
# 為節省篇幅，我直接顯示修改過的 setup_ui 部分
# 請確保你的 class ServerInstallerApp 裡面包含以下 update_ui_texts 和 setup_ui 的更新

class ServerInstallerApp:
    # ... (前面的 __init__, log, install_process 等方法都一樣) ...
    def __init__(self, root):
        self.root = root
        self.ops_list = []
        self.whitelist_list = []
        self.banned_list = []
        self.current_lang = "繁體中文"
        self.found_java_paths = {} 
        self.setup_ui()
        self.log(self.get_text("status_init"))
        threading.Thread(target=self.scan_all_java_versions, daemon=True).start()
        threading.Thread(target=self.load_versions_async, daemon=True).start()
        
    def get_text(self, key):
        if key == "tutorial_text":
             return TRANSLATIONS[self.current_lang].get(key, "Tutorial...")
        return TRANSLATIONS[self.current_lang].get(key, key)

    def change_language(self, event=None):
        self.current_lang = self.combo_lang.get()
        self.update_ui_texts()
        self.update_java_ui()

    def update_ui_texts(self):
        # ... (前面的 tab update 都一樣) ...
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
        
        # 更新教學 Tab
        self.txt_tutorial.config(state='normal')
        self.txt_tutorial.delete(1.0, tk.END)
        self.txt_tutorial.insert(tk.END, self.get_text("tutorial_text"))
        self.txt_tutorial.config(state='disabled')
        
        # 更新贊助按鈕文字
        self.btn_donate.config(text=self.get_text("btn_donate"))

    def open_donate(self):
        # 請把這裡改成你的連結
        webbrowser.open("https://jkmby1230.github.io/Minecraft-Server-Installer/")

    # ... (其他方法如 scan_all_java_versions 等保持不變) ...
    # 以下省略重複代碼，請直接看到 setup_ui 的修改

    # ... (略過重複代碼，請確保複製完整的程式碼結構) ...

    # 為了方便，這裡提供完整的 setup_ui 方法
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

        # ... (Tab 1, 2, 3 程式碼完全一樣，省略) ...
        # Tab 1
        self.f1 = ttk.LabelFrame(self.t1, text="")
        self.f1.pack(padx=10, pady=10, fill="x")
        r_java = ttk.Frame(self.f1); r_java.pack(fill="x", pady=5)
        self.lbl_java_txt = ttk.Label(r_java, text="", font=("Microsoft YaHei", 9, "bold")); self.lbl_java_txt.pack(side=tk.LEFT)
        self.lbl_java_val = ttk.Label(r_java, text="", font=("Microsoft YaHei", 9, "bold")); self.lbl_java_val.pack(side=tk.LEFT, padx=5)
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
        self.lbl_name_t = ttk.Label(self.t4) 

        f_mail = ttk.Frame(f_about); f_mail.pack(pady=15)
        self.lbl_issue_t = ttk.Label(f_mail, font=("微軟正黑體", 10)); self.lbl_issue_t.pack(side=tk.LEFT)
        ttk.Label(f_mail, text=" marker0921230@gmail.com", font=("Arial", 10)).pack(side=tk.LEFT)
        self.btn_copy = ttk.Button(f_mail, text="", command=lambda: self.copy_to_clipboard("marker0921230@gmail.com")); self.btn_copy.pack(side=tk.LEFT, padx=10)

        # 🔥 新增贊助按鈕 🔥
        self.btn_donate = ttk.Button(f_about, text="", command=self.open_donate)
        self.btn_donate.pack(pady=10, ipadx=10, ipady=2)

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

        self.update_ui_texts()
        self.update_java_ui()
        self.cb_mode.current(0); self.cb_diff.current(2)

    # 記得補上其他方法，如 copy_to_clipboard, check_java_version, scan_all_java_versions 等等
    # (為了確保程式能跑，請務必把上面的完整代碼複製下來，不要只複製 setup_ui)