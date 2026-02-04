# 🛠️ Minecraft Server Installer (MCS Installer)
> 一鍵架設 Minecraft 伺服器！支援 Fabric/Forge、多國語言、權限管理。

![軟體截圖](https://你的截圖圖片網址.png) 
*(這裡建議你截一張軟體運作的圖，上傳到 GitHub Issues 或 Imgur，然後把連結貼過來)*

## 🌟 軟體特色
這款工具是為了讓開服變得更簡單而開發的 Python 應用程式：
- **雙核心支援**：自動下載最新版 Fabric 或 Forge。
- **全版本支援**：從 1.20.4 到舊版 1.12.2 皆可查詢。
- **權限管理**：圖形化介面新增 OP、白名單、黑名單 (自動查詢 UUID)。
- **網路工具**：內建 IP 查詢，分辨區網 (LAN) 與公網 (Public) IP。
- **多國語言**：繁體中文 / English / 簡體中文。

## 📥 下載與安裝
前往 **[Releases 頁面](這裡貼上你剛剛第二階段的Releases網址)** 下載最新的 `.exe` 檔案。

**使用方法：**
1. 下載後直接執行 `.exe` (無需安裝 Python)。
2. 選擇安裝路徑與版本。
3. 點擊「開始安裝」。
4. 安裝完成後，點擊資料夾內的 `start.bat` 即可啟動伺服器！

## 🧑‍💻 開發技術 (給開發者)
本軟體使用以下技術構建：
- **語言**: Python 3.12
- **介面**: Tkinter (ttk)
- **打包**: PyInstaller
- **網路**: Requests, Socket

如果你對原始碼感興趣，歡迎 **Fork** 或點擊右上角的 **Star** ⭐ 支持我！

## 📄 授權
本專案採用 [MIT License](LICENSE) 開源授權。
