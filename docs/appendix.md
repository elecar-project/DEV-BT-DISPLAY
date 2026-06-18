---
title: 附錄
description: 延伸紀錄、實驗筆記與歷史脈絡。
---

# 附錄

本頁放置對內部研究者有用、但對公開或投稿版本來說過於詳細的延伸紀錄。

## 建議收錄內容

- 實驗執行紀錄。
- 參數表。
- 被排除或執行失敗的實驗。
- 母倉庫中的歷史資料夾對照。
- Release 封裝與資料搬遷筆記。

## 母倉庫對照

| 母倉庫區域 | 預計整理位置 |
| --- | --- |
| `Pre-process/` | 方法、工具與可重現性筆記 |
| `BERTopic/` | 方法、工具與 BERTopic 設定筆記 |
| `Result/` | 整理後的結果頁面與外部成果包 |
| `#TXT_DATA/` 與 `TXT_DATA/` | 資料集清單與外部資料連結 |
| 歷史工具資料夾 | 工具頁與附錄筆記 |

## 目前已盤點的母倉庫區域

| 區域 | 內容摘要 | 本站整理位置 |
| --- | --- | --- |
| `#A1-7【音檔ASR】...` | ASR、音檔抽取、逐字稿比較、DB 比對、刪除工具等歷史版本 | 工具 |
| `#B1-4【資料清理與切分】...` | LLM 清理、資料集比較、篩選、句子切分工具 | 工具、方法 |
| `#C1-3【BERTopic處理】...` | BERTopic 基本運行、min/elbow、批次腳本工具 | 工具、結果 |
| `Pre-process/` | 目前較正式的前處理 Streamlit app | 方法、工具 |
| `BERTopic/` | 目前較正式的 BERTopic Streamlit app | 方法、工具、結果 |
| `#TXT_DATA/` | 逐字稿、Hugging Face Dataset、SQLite DB、車廠車款詞表 | 資料集 |
| `Result/` | BERTopic 試跑報告、topic_info、資料篩選、品質檢查、年份比對 | 結果、資料集 |
| `docs/REPO_ORGANIZATION_PLAN.md` | 倉庫分工與發布規劃 | 首頁與附錄 |

## 目前不直接搬進本站的大型或衍生資料

| 類型 | 原因 | 建議處理 |
| --- | --- | --- |
| `.txt` 逐字稿全集 | 數量多，會讓展示 repo 逐漸膨脹 | 放 Hugging Face Dataset、Release 或母倉庫 |
| `.db` SQLite | 不適合直接作為 GitHub Pages 展示內容 | 保留下載連結與版本說明 |
| `.arrow` Dataset | 靜態網站無法直接查詢 | 放 Hugging Face Dataset 或 Release |
| 完整 CSV 結果 | 有些表格很長，不適合直接塞進頁面 | 摘要放本站，完整檔案用外部連結 |
| exe 或 zip | GitHub Pages 不適合管理 release artifacts | 使用母倉庫 GitHub Release |
