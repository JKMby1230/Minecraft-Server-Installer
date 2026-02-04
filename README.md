# 🛠️ Minecraft Server Installer (v0.0.2)

> **最簡單、最直覺的 Minecraft 伺服器架設工具。** > 支援 Fabric、Forge、NeoForge 三大核心，內建 Java 版本自動偵測與路徑綁定。

![GitHub release (latest by date)](https://img.shields.io/github/v/release/JKMby1230/Minecraft-Server-Installer)
![GitHub downloads](https://img.shields.io/github/downloads/JKMby1230/Minecraft-Server-Installer/total)
![License](https://img.shields.io/github/license/JKMby1230/Minecraft-Server-Installer)

## 🚀 v0.0.2 更新重點
* **🆕 新增 NeoForge 支援**：現在可以安裝最新的 NeoForge 模組核心 (支援 1.20.1+)。
* **☕ 智慧 Java 偵測**：自動掃描系統中的 Java 版本，若版本不符會跳出警告。
* **🔗 自動路徑綁定**：啟動腳本 (`start.bat`) 現在會強制綁定正確的 Java 路徑，解決多版本衝突問題。
* **🐛 介面優化**：修復教學頁面排版，優化多國語言顯示。

---

## ✨ 軟體特色

### 1. 核心與版本全支援
* **三大載入器**：支援 **Fabric**、**Forge** 與 **NeoForge**。
* **全版本覆蓋**：從最新的 1.21+ 到經典的 1.12.2 皆可一鍵安裝。

### 2. 視覺化設定 (GUI)
* **參數調整**：直接在介面上設定記憶體 (RAM)、Port、PVP、難度、正版驗證。
* **權限管理**：圖形化新增管理員 (OP)、白名單、黑名單，自動查詢玩家 UUID。
* **無需編輯文字檔**：告別繁瑣的 `server.properties` 修改。

### 3. 智慧網路與環境工具
* **Java 檢查**：自動判斷 Minecraft 版本所需的 Java，並掃描電腦中的安裝路徑。
* **IP 查詢**：一鍵顯示 **區網 IP (LAN)** 與 **公網 IP (Public)**，方便分辨連線位置。

---

## 📥 下載與安裝

無需安裝 Python，下載執行檔即可使用。

1.  前往 **[Releases 頁面](https://github.com/JKMby1230/Minecraft-Server-Installer/releases)**。
2.  下載最新的 **`MinecraftServerInstaller_v0.0.2.zip`**。
3.  解壓縮後，雙擊執行程式。

---

## 📖 使用教學

### 步驟 1：選擇與安裝
1.  選擇一個空的資料夾作為安裝路徑。
2.  選擇核心 (Fabric/Forge/NeoForge) 與遊戲版本。
3.  設定記憶體 (建議 4GB 以上)，點擊 **「開始安裝」**。

### 步驟 2：啟動伺服器
1.  安裝完成後，進入資料夾。
2.  點擊 **`start.bat`** 啟動伺服器。
3.  等待黑色視窗跑完，出現 `Done!` 即代表開服成功。

### 步驟 3：Java 版本對照表
本軟體會自動偵測，但請確保您電腦已安裝對應的 Java 版本：

| Minecraft 版本 | 需要的 Java 版本 |
| :--- | :--- |
| **1.20.5 - 1.21+** | **Java 21** |
| **1.18 - 1.20.4** | **Java 17** |
| **1.17** | Java 16 (或 17) |
| **1.16.5 以下** | **Java 8** |

---

## 📬 問題回報 & 參與開發

這是一個開源專案，歡迎任何形式的貢獻！

* **發現 Bug？** 請到 [Issues 頁面](https://github.com/JKMby1230/Minecraft-Server-Installer/issues) 回報。
* **聯絡作者**：`marker0921230@gmail.com`
* **開發技術**：Python 3.12, Tkinter, Requests, PyInstaller.

---

<p align="center">Made with ❤️ by 奶香威士忌</p>
