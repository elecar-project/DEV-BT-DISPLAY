---
title: 資料集
description: 資料版本、篩選規則與存取位置。
---

# 資料集

本頁追蹤 DEV-BT 研究流程中已出現的主要資料集版本、篩選規則與存放位置。

## 資料集原則

大型資料集不建議直接放進這個展示倉庫。本站應以紀錄資料版本、
處理規則與外部連結為主，實際資料可放在 Hugging Face Datasets、Zenodo、
GitHub Release 或其他合適的儲存位置。

## 資料集清單

| 資料集 | 說明 | 位置 | 狀態 |
| --- | --- | --- | --- |
| 原始逐字稿 | 454 個 `.txt`，作為後續清理與篩選的起點 | `#TXT_DATA/2. 文字稿－txt/` | 已盤點 |
| 主要清理後逐字稿 | 434 個 `.txt`，目前多數 BERTopic 實驗的主資料來源 | `#TXT_DATA/05.24_txt-test_deleted(434)/` | 已盤點 |
| Hugging Face Dataset 版本 | 434 筆，欄位為 `title`、`transcript`，以 Arrow 格式保存 | `#TXT_DATA/05.24_txt-test_deleted(434)_dataset/` | 已盤點 |
| 600-2159 秒篩選資料 | 103 個 `.txt`，依影片長度區間篩選 | `#TXT_DATA/06.03_600-2159sec(103)/` | 已盤點 |
| 廠商去頭尾資料 | 237 個 `.txt`，每個廠商去除頭尾各 5 筆後保留 | `#TXT_DATA/06.03_廠商去頭尾各5家(237)/` | 已盤點 |
| 車廠/車款詞表 | 用於品牌與型號移除或替換的詞表 | `#TXT_DATA/man-model.md` | 已盤點 |
| EVcar URL SQLite | `ver.5.5`、`ver.5.6`、`ver.5.7` 等資料庫版本 | `#TXT_DATA/*.db` | 已盤點 |

## 目前可用的數量摘要

| 項目 | 數量 |
| --- | ---: |
| 原始逐字稿 `.txt` | 454 |
| 主要清理後逐字稿 `.txt` | 434 |
| Hugging Face Dataset 筆數 | 434 |
| 600-2159 秒篩選資料 | 103 |
| 廠商去頭尾各 5 家資料 | 237 |
| A06-A08 BERTopic 原始句子數 | 31,883 |
| A06-A08 BERTopic 最終輸入句子數 | 26,978 |
| A06-A08 句子保留率 | 84.62% |

## 主要處理紀錄

| 紀錄 | 摘要 | 來源 |
| --- | --- | --- |
| 非英文與特殊符號檢查 | 434 筆中有 33 筆含非 ASCII 或特殊字元；外語 script 僅 1 筆 | `Result/txt_non_english_analysis_05.24.md` |
| LLM 前處理 | OpenRouter 清理 434 筆，成功 434 筆；總 token 約 1,232,982；估計 cost 3.093731 | `Result/06.03_A02/R06.03_A02-pre-LLM-result.md` |
| 長度區間篩選 | 600-2159 秒區間共 103 筆，並建立每 60 秒區間摘要 | `Result/DB_Filter/duration_interval_summary.md` |
| 廠商去頭尾 | 建立 237 筆 copy manifest，保留 source/target 對照與影片 URL | `Result/DB_Filter/06.03_manufacturer_trimmed_copy_manifest.md` |
| 年份比對 | 434 筆逐字稿與資料庫 upload year 進行 match report | `Result/06.13_A02/` |

## 建議紀錄欄位

- 資料集名稱與版本。
- 文件數或句子數。
- 原始資料的時間範圍。
- 已套用的清理步驟。
- 納入與排除規則。
- 已知限制。
- 下載或存取連結。

## 後續建議

資料頁下一步可以補上兩類內容：第一類是每個資料集版本的「產生方式」，
第二類是「是否適合放到公開／投稿用版本」。目前本站先保留內部研究者需要的
路徑、數量與處理紀錄，避免一開始就複製大量原始資料。
