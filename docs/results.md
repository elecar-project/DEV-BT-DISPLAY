---
title: 結果
description: 整理後的 BERTopic 輸出與解釋筆記。
---

# 結果

<div class="results-layout" markdown="1">
<aside class="results-sidebar" markdown="1">
## 結果導覽

<div class="result-nav-group" markdown="1">
<a class="active" href="{{ '/results.html' | relative_url }}">結果總覽</a>
<a href="{{ '/results/a08-no-brand-removal.html' | relative_url }}">A08 無刪除廠商車款</a>
<a href="{{ '/results/a07-no-brand-removal.html' | relative_url }}">A07 無刪除廠商車款</a>
<a href="{{ '/results/a07-brand-removed.html' | relative_url }}">A07 有刪除廠商車款</a>
<a href="{{ '/results/a06-no-brand-removal.html' | relative_url }}">A06 無刪除廠商車款</a>
<a href="{{ '/results/a06-brand-removed.html' | relative_url }}">A06 有刪除廠商車款</a>
</div>

<div class="result-nav-group" markdown="1">
<a href="{{ '/results/pre-llm-a02.html' | relative_url }}">06.03 A02 LLM 前處理</a>
<a href="{{ '/results/year-match-a02.html' | relative_url }}">06.13 A02 年份比對</a>
<a href="{{ '/results/db-filter.html' | relative_url }}">DB Filter 篩選結果</a>
<a href="{{ '/results/non-english-check.html' | relative_url }}">非英文與特殊符號檢查</a>
</div>

<div class="result-nav-group" markdown="1">
<a href="{{ '/results/historical-index.html' | relative_url }}">歷史結果索引</a>
</div>
</aside>

<section class="results-content" markdown="1">

本頁收集目前已盤點的 BERTopic 結果、前處理結果與資料篩選結果，供內部研究討論與檢視。左側導覽列可切換到每一次 run 或資料處理結果的獨立頁面。

<div class="run-summary">
  <div class="run-stat"><strong>5</strong><span>BERTopic topic_info 結果組</span></div>
  <div class="run-stat"><strong>434</strong><span>主要逐字稿資料數</span></div>
  <div class="run-stat"><strong>26,978</strong><span>A06-A08 最終輸入句子數</span></div>
  <div class="run-stat"><strong>A08</strong><span>目前最適合深入檢視的細粒度結果</span></div>
</div>

## 結果整理原則

這個展示倉庫應呈現經篩選、可閱讀的結果摘要。完整產出檔可放在
Release bundle、資料集平台或封存資料夾，並由本站提供連結與說明。

## 結果清單

| 實驗 | 品牌/車款處理 | HDBSCAN `min_cluster_size` | topic_info 筆數 | 主要觀察 |
| --- | --- | ---: | ---: | --- |
| A06 | 有刪除 | 參數測試 | 3 | 主要 topic 極集中，另有 Volvo/XC 系列小 topic |
| A06 | 無刪除 | 參數測試 | 4 | Toyota、Volvo 等品牌詞較明顯進入 topic |
| A07 | 有刪除 | 200 | 3 | 結構與 A06 有刪除接近，主題數偏少 |
| A07 | 無刪除 | 200 | 7 | 品牌與車款 topic 增加，例如 BMW、Nissan、Audi、Volvo |
| A08 | 無刪除 | 150 | 32 | 主題切得更細，出現 display、seat、ADAS、charging、engine 等較具語意的子題 |

## A08 主題樣貌節錄

| Topic | Count | OpenRouter 標籤 | 代表詞方向 |
| ---: | ---: | --- | --- |
| -1 | 12,814 | Vehicle Performance and Technology | new、drive、available、vehicle |
| 0 | 2,203 | SUV Driving Experience Comparison | car、cars、drive、vehicle |
| 2 | 1,219 | Advanced In-Car Display Technology | display、screen、navigation、phone |
| 3 | 747 | Rear Seat Cargo Space Expansion | seats、rear、cargo、passenger |
| 4 | 654 | Advanced Driver Assistance Features | assist、lane、blind spot、camera |
| 7 | 560 | Electric Vehicle Charging Options | charging、charge、stations、plug |
| 8 | 430 | Engine Power and Electric Motors | horsepower、engine、torque、motor |

## 前處理與資料品質摘要

| 項目 | 數值或結論 | 來源 |
| --- | --- | --- |
| A06-A08 原始句子數 | 31,883 | BERTopic 試跑報告 |
| A06-A08 最終輸入句子數 | 26,978 | BERTopic 試跑報告 |
| A06-A08 句子保留率 | 84.62% | BERTopic 試跑報告 |
| 廠商名稱 | 45 筆 | BERTopic 試跑報告 |
| 唯一車款名稱 | 517 筆 | BERTopic 試跑報告 |
| 移除用詞合計 | 561 筆 | BERTopic 試跑報告 |
| LLM 清理成功筆數 | 434 / 434 | `Result/06.03_A02/` |
| 非 ASCII / 特殊字元檔案 | 33 / 434 | `Result/txt_non_english_analysis_05.24.md` |
| 外語 script 檔案 | 1 / 434 | `Result/txt_non_english_analysis_05.24.md` |

## 建議檢視問題

- 哪一次實驗應被視為主要結果？
- 哪些主題在不同參數設定下仍然穩定？
- 哪些主題可能受到 ASR 雜訊或品牌／產品詞影響？
- 哪些圖表之後適合移到公開或投稿用倉庫？

## 初步判讀

目前 A08 的 `min_cluster_size=150` 產生較細的主題切分，對內部探索比較有幫助；
A07/A06 的結果則更像粗粒度 baseline。若目標是整理成投稿或公開版本，
可以優先從 A08 挑選可解釋性較高的主題，再與「有刪除廠商車款」版本比對，
確認主題不是單純由品牌名稱驅動。

</section>
</div>
