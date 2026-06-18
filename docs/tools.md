---
title: 工具
description: Python App、Windows 工具、Release 連結與使用筆記。
---

# 工具

本頁整理 DEV-BT 工作流程中可執行的工具、App 與相關使用說明。

## Release 檔案

可下載工具目前發布在母倉庫的 Release：

<https://github.com/elecar-project/DEV-BT/releases>

## 工具清單

| 工具 | 類型 | 用途 | 狀態 |
| --- | --- | --- | --- |
| Pre-process Workbench | Python/Streamlit | 匯入、清理、版本化與匯出資料集 | 母倉庫 `Pre-process/` |
| BERTopic Workbench | Python/Streamlit | 執行主題模型、參數探索與結果匯出 | 母倉庫 `BERTopic/` |
| HF-AUDIO | Python/Hugging Face | 批次 RMS 或音訊前處理 | A 系列歷史工具 |
| TXT Compare / TXTcp | Windows/Python 工具 | 比較新舊 ASR 或左右逐字稿輸出 | A 系列歷史工具 |
| Audio V2A | Windows/Python 工具 | 從影片檔抽取音訊 | A 系列歷史工具 |
| ASR Result | Windows/Python 工具 | 分割 txt 並轉成表格 | A 系列歷史工具 |
| ASR Analysis | Windows/Python 工具 | 依比例找出可能含 ASR 雜訊的文本 | A 系列歷史工具 |
| DB Compare | Windows/Python 工具 | 比對資料庫與逐字稿資訊 | A 系列歷史工具 |
| TXT Delete | Windows/Python 工具 | 批次刪除指定逐字稿檔案 | A 系列歷史工具 |
| LLM Clean | Windows/Python 工具 | 補標點與清理 Whisper 文本 | B 系列歷史工具 |
| TXT Filter | Windows/Python 工具 | 依條件篩選資料集 | B 系列歷史工具 |
| TXT Tokenizer | Windows/Python 工具 | 將逐字稿切分成句子資料集 | B 系列歷史工具 |
| BERTopic Deploy | Windows/Python 工具 | BERTopic 基本運行與互動調參 | C 系列歷史工具 |
| BERTopic Min & Elbow | Windows/Python 工具 | 測試 min_cluster_size 並畫 elbow 圖 | C 系列歷史工具 |
| BERTopic Batch | Windows/Python 工具 | 產生批次實驗 config 與 Python 腳本 | C 系列歷史工具 |

## 工作流程分組

| 階段 | 對應工具 | 研究用途 |
| --- | --- | --- |
| A. 音檔與 ASR 處理 | Audio V2A、Audio-tran、ASR-result、ASR-analysis、TXT Compare、TXT Delete | 取得逐字稿、檢查 ASR 品質、整理可用文本 |
| B. 資料清理與切分 | LLM Clean、TXTcp-2、TXT Filter、TXT Tokenizer、Pre-process Workbench | 清理逐字稿、建立資料集版本、切成 BERTopic 可用句子 |
| C. BERTopic 處理 | BERTopic Workbench、BERTopic Deploy、Min & Elbow、Batch | 訓練 topic model、調整參數、匯出主題結果 |

## 內部研究者筆記

- 若只需要執行工具，優先使用 Release 中的封裝檔。
- 只有在需要原始碼或歷史脈絡時，才回到母倉庫查找。
- 新增工具筆記時，本站保留簡要說明，細節可連回原始文件或程式碼。

## 可重現性筆記

- `Pre-process/app.py`：建議作為資料匯入、版本保存、LLM 清理、句子切分與 dataset 匯出的主入口。
- `BERTopic/app.py`：建議作為 BERTopic 訓練、參數探索、topic label 與視覺化輸出的主入口。
- 已封裝的 Windows 工具適合給不想直接跑 Python 的使用者；研究者若要追蹤細節，仍應回到 Python source 與 README。
