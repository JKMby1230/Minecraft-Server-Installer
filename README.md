# 🛠️ Minecraft Server Installer

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-win.svg)](https://microsoft.com/windows)
[![Release](https://img.shields.io/github/v/release/JKMby1230/Minecraft-Server-Installer?label=Latest%20Version)](https://github.com/JKMby1230/Minecraft-Server-Installer/releases)

一個輕量、全自動化的 Minecraft 伺服器架設工具。專為不想面對繁雜指令的玩家設計，支援 **Fabric**、**Forge** 與 **NeoForge** 核心，內建智慧環境配置與連線偵測功能。

## ✨ 主要特色 (Key Features)

* **⚡ 全自動安裝**：一鍵下載並安裝 Fabric / Forge / NeoForge 伺服器核心。
* **☕ 智慧環境配置**：自動偵測並下載適合該遊戲版本的 Java 環境 (Portable)，無需手動安裝 Java。
* **🧠 智慧記憶體偵測**：自動顯示電腦可用 RAM，並在設定過高時發出防當機警告。
* **🌐 全能連線支援**：
    * 支援 **IPv6 直連** 偵測 (免開 Port)。
    * 支援 **Radmin VPN** 虛擬 IP 自動抓取。
    * 支援傳統 IPv4 公網/區網顯示。
* **📂 快捷操作中心**：一鍵打開伺服器目錄、Mods 資料夾，管理模組更輕鬆。
* **🔓 彈性驗證**：支援開啟/關閉正版驗證 (Online Mode)，方便離線或非正版玩家加入。
* **🌱 自訂地圖**：支援輸入種子碼 (Seed) 生成特定地圖。
* **📖 雙模式教學**：內建「快速指南」與「詳細教學」文檔。
* **🌍 多語言支援**：繁體中文 / English / 简体中文。

## 📥 下載與安裝 (Download)

1.  前往 [**Releases 頁面**](https://github.com/JKMby1230/Minecraft-Server-Installer/releases)。
2.  下載最新版本的 `MinecraftServerInstaller.exe`。
3.  將檔案放入一個空資料夾 (推薦)，直接執行即可，**無需安裝 Python**。

## 🚀 快速開始 (Quick Start)

1.  **選擇路徑**：點擊「瀏覽」選擇一個空資料夾作為伺服器目錄。
2.  **選擇版本**：選擇您要的核心 (如 Fabric) 與遊戲版本 (如 1.20.1)。
3.  **開始安裝**：點擊按鈕，程式會自動處理所有下載與設定。
4.  **啟動伺服器**：安裝完成後，點擊「📂 打開伺服器資料夾」，執行 `start.bat`。
5.  **連線**：點擊軟體上的「🔍 顯示 IP」，將 IPv6 或 Radmin IP 複製給朋友即可連線。

---

## 📜 更新日誌 (Changelog)

### v0.0.18 (Latest Stable)
* **🛠️ 介面修復**：修正軟體圖示 (Logo) 在打包後無法顯示的問題，改為強制從暫存區讀取資源。
* **✨ 穩定性優化**：確認所有核心功能運作正常，為目前的最終穩定版本。

### v0.0.17
* **🐛 打包修正**：加入 `resource_path` 函式，解決 PyInstaller 打包後找不到圖片與資源路徑的問題。
* **📦 封裝優化**：更新打包指令配置，確保單一執行檔 (.exe) 能正確運作。

### v0.0.16 (UX Revolution)
* **🧠 智慧偵測**：新增「記憶體自動偵測」功能，直接顯示電腦可用 RAM 總量。
* **🛡️ 防呆機制**：當設定記憶體超過系統可用量 50% 時，跳出警告視窗防止電腦當機。
* **📂 快捷操作**：新增「打開伺服器資料夾」與「打開 Mods 資料夾」按鈕，方便安裝模組與管理檔案。
* **🗣️ 用語優化**：將「Online Mode」選項改為更直覺的「🔓 開放盜版/離線登入 (Cracked)」。

### v0.0.15
* **🔤 相容性修正**：移除介面與教學中的特殊 Emoji 符號，解決部分 Windows 系統顯示為方塊亂碼的問題。
* **📝 排版微調**：將教學步驟編號標準化，提升閱讀體驗。

### v0.0.14
* **📖 教學重構**：將教學分頁改為「雙模式」設計：
    * **⚡ 快速指南**：針對老手提供 5 步驟懶人包。
    * **📚 詳細教學**：包含除錯資訊與連線原理的完整手冊。

### v0.0.13
* **🌱 新增功能**：在規則設定中加入「地圖種子碼 (Seed)」欄位，允許使用者指定地圖生成樣貌。

### v0.0.12
* **🛡️ 網路優化**：為所有下載請求加入 `User-Agent` 標頭，解決 Mojang 與 Forge 伺服器拒絕連線 (403 Forbidden) 的問題。
* **⚡ 啟動加速**：優化版本列表讀取邏輯，大幅加快軟體啟動速度。
* **☕ 資訊更新**：更新贊助連結。

### v0.0.11
* **⚡ 非同步處理**：修復點擊「顯示 IP」時介面卡死 (白屏) 的問題，改為背景多執行緒讀取。
* **📋 互動優化**：IP 複製按鈕新增「✅ OK」回饋動畫，確認複製成功。

### v0.0.10
* **📊 下載體驗**：Java 下載器新增「即時百分比進度條」，解決下載大檔案時看似當機的問題。
* **🖱️ 介面優化**：IP 資訊視窗新增「一鍵複製」按鈕，省去手動選取文字的麻煩。

### v0.0.9 (Hybrid Network)
* **🌐 全能連線版**：整合多種連線偵測邏輯，適應不同網路環境。
    * 優先偵測 **IPv6** (免軟體直連)。
    * 若無 IPv6，自動抓取 **Radmin VPN** 的虛擬 IP。
    * 保留傳統 **IPv4** 顯示。

### v0.0.8
* **🔗 Radmin 整合**：針對無 IPv6 且無法設定路由器的用戶，新增 Radmin VPN IP 自動偵測功能。
* **🐛 嚴重修復**：補回 v0.0.5 版本遺失的設定檔生成函式，解決安裝時閃退報錯的問題。

### v0.0.7
* **➖ 移除依賴**：移除 `playit.gg` 相關功能，回歸純淨版 (專注於 IPv6 與傳統開 Port)，減少軟體體積與複雜度。

### v0.0.6
* **🚀 IPv6 支援**：首度新增公網 IPv6 偵測功能，提供免開 Port 的連線方案。

### v0.0.5
* **⚙️ 核心修復**：修復 NeoForge 核心的安裝邏輯與版本判斷。
* **🧪 實驗性功能**：嘗試整合 Playit.gg 通道工具 (後於 v0.0.7 移除)。

### v0.0.3 ~ v0.0.4
* **🏗️ 基礎建設**：
    * 建立基本的 GUI 圖形介面。
    * 實作 Fabric / Forge / NeoForge 自動下載器。
    * 實作 Java 環境自動檢測與下載配置功能。

---

## ☕ 支持開發者 (Support)

如果您覺得這個工具對您有幫助，歡迎請我喝杯咖啡，這將支持我繼續開發更多功能！

<a href="https://buymeacoffee.com/jkmby1230" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

* **Author**: 奶香威士忌 (JKMby1230)
* **Contact**: marker0921230@gmail.com
