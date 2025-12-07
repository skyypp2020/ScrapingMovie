# 電影資料爬蟲與視覺化專案 (Movie Scraping & Visualization)

**DemoSite**: [https://scrapingmovie-8vjsku3ytxrttwnnqqhap2.streamlit.app/](https://scrapingmovie-8vjsku3ytxrttwnnqqhap2.streamlit.app/)

本專案採用 **CRISP-DM (Cross-Industry Standard Process for Data Mining)** 跨產業資料探勘標準流程進行開發，旨在自動化抓取網路上的電影資料，進行資料儲存，並透過互動式網頁應用程式進行資料展示與分析。

## 1. 商業理解 (Business Understanding)
- **目標**: 自動化收集 [SSR1 Scrape Center](https://ssr1.scrape.center/) 上的電影資訊，建立本地端資料庫，以利後續的資料分析與查詢。
- **需求**:
    - 自動抓取電影名稱、評分、分類、國家、時長、上映日期等資訊。
    - 支援多頁面 (Page 1-10) 批量抓取。
    - 資料需持久化儲存於 CSV 文件與 SQLite 資料庫。
    - 提供使用者友善的介面 (Streamlit App) 進行資料瀏覽與篩選。

## 2. 資料理解 (Data Understanding)
- **資料來源**: [SSR1 Scrape Center](https://ssr1.scrape.center/)
- **資料欄位**:
    - `title`: 電影名稱 (中英文)
    - `score`: 電影評分 (0.0 - 10.0)
    - `categories`: 電影分類 (如：劇情/愛情/犯罪)
    - `country`: 製作國家/地區
    - `duration`: 電影時長
    - `release_date`: 上映日期
- **資料量**: 約 100 筆資料 (10 頁 x 10 筆/頁)

## 3. 資料準備 (Data Preparation)
- **資料蒐集**: 使用 Python 的 `requests` 與 `BeautifulSoup` 套件進行網路爬蟲。
- **資料清理**:
    - 去除 HTML 標籤。
    - 標準化日期格式。
    - 處理多個國家或分類的字串分割與合併。
- **資料儲存**:
    - **CSV**: `movie.csv` (原始爬取結果)
    - **SQLite**: `data.db` (結構化儲存，方便查詢)

## 4. 模型/應用建置 (Modeling/Application Build)
本專案不涉及機器學習模型訓練，核心應用為資料展示系統：
- **資料庫建置**: 使用 `create_db.py` 將 CSV 資料匯入 SQLite 資料庫。
- **網頁應用程式**: 使用 `Streamlit` 框架開發 `app.py`。
    - **功能**:
        - 顯示完整電影資料表。
        - 支援依「電影名稱」關鍵字搜尋。
        - 支援依「最低評分」滑桿篩選。
        - 提供篩選後資料的 CSV 下載功能。

## 5. 評估 (Evaluation)
- **資料完整性**: 確認成功抓取 100 筆資料，且欄位無缺漏。
- **系統功能**:
    - 爬蟲腳本可穩定執行並處理網路請求。
    - 資料庫建立腳本能正確處理資料型態與轉碼。
    - Streamlit 應用程式操作流暢，篩選邏輯正確。

## 6. 部署 (Deployment)
- **環境需求**: Python 3.x, `pip`
- **套件安裝**:
  ```bash
  pip install requests beautifulsoup4 pandas streamlit
  ```
- **執行步驟**:
  1. **執行爬蟲**:
     ```bash
     python scrape_movies.py
     ```
     (產出 `movie.csv`)
  2. **建立資料庫**:
     ```bash
     python create_db.py
     ```
     (產出 `data.db`)
  3. **啟動網頁應用**:
     ```bash
     streamlit run app.py
     ```

## 7. 專案檔案結構 (Project Structure)

```
ScrapingMovie/
│
├── scrape_movies.py    # [資料準備] 網路爬蟲主程式，抓取資料並存為 CSV
├── create_db.py        # [資料準備] 資料庫建置程式，將 CSV 匯入 SQLite
├── app.py              # [應用建置] Streamlit 網頁應用程式主程式
│
├── movie.csv           # [資料儲存] 爬取的原始數據文件
├── data.db             # [資料儲存] SQLite 資料庫文件
│
├── prompt.md           # [專案紀錄] 開發過程與 AI 對話日誌
├── 資料表說明.md       # [專案文件] 資料庫 Schema 說明文件
├── README.md           # [專案文件] 專案說明文件 (本文件)
└── .gitignore          # [組態設定] Git 忽略檔案設定
```
