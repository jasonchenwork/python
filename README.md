
# 📈 台灣股市資料抓取與財報分析工具

本專案是一套使用 Python 製作的台灣股市數據爬蟲與資料分析工具，能自動抓取公開資訊觀測站（MOPS）與台灣證券交易所（TWSE）的歷史股價、月營收、損益表、殖利率與 EPS 等資料，並整理為乾淨的 `DataFrame`，匯出成 CSV。

---

## 📌 功能說明

### 1. 日期與數據轉換
- `transform_date(date)`：將民國日期（如112/01/01）轉為西元格式（如2023/01/01）
- `transform_data(data)`：清洗原始 HTML/JSON 內的股價資料，轉換成數值格式
- `transform(data)`：批次清洗所有 row 資料

---

### 2. 股價歷史資料查詢
- `get_stock_history(date, stock_no)`  
  > 抓取指定年月與股票代號的股價資料（來源：TWSE）

- `create_df(date, stock_no)`  
  > 將抓取的股價資料轉成 `DataFrame`，新增股票代碼與月份欄位

---

### 3. 財報查詢（損益表/資產負債表/營益分析）
- `financial_statement(year, season, type='綜合損益彙總表', TYPEK='sii')`  
  > 抓取財報彙總表，可選：
  - `綜合損益彙總表`
  - `資產負債彙總表`
  - `營益分析彙總表`
  - `TYPEK` 參數可設為 `sii`（上市）或 `otc`（上櫃）

---

### 4. 每月營收報表（公司月營收）
- `monthly_report(year, month, type='sii')`  
  > 抓取每月營收報表，適用於上市/上櫃公司（含營收、YOY、QoQ）

- `get_oneyear_monthly_report()`  
  > 自動抓取過去 12 個月的營收資料並輸出：
  - `月營收.csv`
  - `YOY.csv`
  - `QoQ.csv`

---

### 5. 各季財報統計指標
- `get_allseason_profit_report()`  
  > 抓取過去幾季的財報並分析：
  - 毛利率 (%)
  - 營業利益率 (%)
  - 稅前/稅後純益率 (%)

- `get_allseason_EPS_report()`  
  > 抓取每股盈餘（EPS），合併上市與上櫃資料

---

### 6. 個股評價指標資料（殖利率/本益比/PBR）
- `download()`  
  > 抓取每日更新的個股殖利率、P/E、P/B（來源：TWSE）

---

## 🔁 自動化流程

主程式會在執行時自動執行以下任務：
```python
get_oneyear_monthly_report()
get_allseason_profit_report()
#get_allseason_EPS_report()
```

可根據需求打開或註解部分函式執行。

---

## 💾 匯出資料說明

執行後會匯出以下 CSV 檔案：
- `月營收.csv`
- `YOY.csv`
- `QoQ.csv`
- `毛利率(%).csv`
- `營業利益率(%).csv`
- `稅前純益率(%).csv`
- `稅後純益率(%).csv`
- `基本每股盈餘.csv`
- `個股日本益比.csv`

---

## 🔧 相依套件

請先安裝以下套件：
```bash
pip install pandas requests beautifulsoup4
```

---

## 📝 備註與改進建議

- 某些網頁資料未提供 API，會需要更好的錯誤處理
- 建議加入 try-except 機制避免程式因資料缺失中斷
- 可進一步整理為 class 與模組結構，便於維護與測試
