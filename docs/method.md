---
title: 方法
description: DEV-BT 的研究流程與處理管線。
---

# 方法

本頁整理從原始逐字稿收集、資料清理、資料切分到主題模型產出的研究流程。

## 流程總覽

1. 收集或匯入逐字稿資料。
2. 清理 ASR 雜訊與低資訊量文字。
3. 將逐字稿切分成句子層級資料。
4. 建立適合 BERTopic 使用的資料集。
5. 以可控參數設定執行 BERTopic 實驗。
6. 比較主題品質、離群文件、主題標籤，以及時間或產品分組差異。
7. 整理最終成果，供內部研究檢視與後續公開摘要使用。

## 目前母倉庫中的實際流程

| 階段 | 目前對應資料或工具 | 產出 |
| --- | --- | --- |
| 原始逐字稿整理 | `#TXT_DATA/2. 文字稿－txt/`、A 系列 ASR 工具 | 454 個原始逐字稿 |
| 人工/規則式刪除後資料 | `#TXT_DATA/05.24_txt-test_deleted(434)/` | 434 個主要分析逐字稿 |
| LLM 逐字稿清理 | `Result/06.03_A02/`、Pre-process Workbench | 434 筆 OpenRouter 清理結果 |
| 資料集匯出 | Hugging Face Dataset / Arrow | `title`、`transcript` 欄位資料集 |
| 篩選資料建立 | DB Filter 結果 | 103 筆長度篩選資料、237 筆廠商去頭尾資料 |
| BERTopic 實驗 | `BERTopic/app.py`、C 系列工具 | A06、A07、A08 試跑報告與 topic_info |
| 時間/年份對照 | `Result/06.13_A02/` | 434 筆 match report 與不同年份切分版本 |

## 目前採用的 BERTopic 設定摘要

| 參數 | 目前紀錄中的設定 |
| --- | --- |
| Embedding | `sentence-transformers/all-MiniLM-L6-v2` |
| UMAP | `n_neighbors=15`、`n_components=5`、`min_dist=0.0`、`metric=cosine`、`random_state=42` |
| HDBSCAN | `metric=euclidean`、`cluster_selection_method=eom`、`prediction_data=True` |
| CountVectorizer | `stop_words=english`、`min_df=2`、`ngram_range=(1, 2)` |
| Topic label | OpenRouter / `openai/gpt-4o-mini` |
| 實驗變化 | A07 固定 `min_cluster_size=200`；A08 固定 `min_cluster_size=150` |

## 待搬移內容

- 母倉庫中的 ASR 與逐字稿處理筆記。
- Pre-process App 的使用方式與資料匯出規則。
- BERTopic App 的參數設定與實驗預設值。
- 停用詞、品牌移除、句子切分、主題標籤等研究決策。
- A06、A07、A08 的完整圖表與互動式 HTML 輸出。
- 06.13 年份切分後是否有進一步 BERTopic 結果。

## 待確認事項

- 定義正式採用的前處理流程。
- 定義最終 BERTopic 參數組，或建立參數比較矩陣。
- 連結可重現所選實驗的腳本與執行說明。
- 決定公開版是否保留品牌/車款移除對照，或只呈現主模型。
