---
title: DB Filter 篩選結果
description: Duration and manufacturer-trimmed dataset filter outputs.
---

# DB Filter 篩選結果

<div class="results-layout" markdown="1">
<aside class="results-sidebar" markdown="1">
## 結果導覽

<div class="result-nav-group" markdown="1">
<a href="{{ '/results.html' | relative_url }}">結果總覽</a>
<a href="{{ '/results/a08-no-brand-removal.html' | relative_url }}">A08 無刪除廠商車款</a>
<a href="{{ '/results/a07-no-brand-removal.html' | relative_url }}">A07 無刪除廠商車款</a>
<a href="{{ '/results/a07-brand-removed.html' | relative_url }}">A07 有刪除廠商車款</a>
<a href="{{ '/results/a06-no-brand-removal.html' | relative_url }}">A06 無刪除廠商車款</a>
<a href="{{ '/results/a06-brand-removed.html' | relative_url }}">A06 有刪除廠商車款</a>
</div>

<div class="result-nav-group" markdown="1">
<a href="{{ '/results/pre-llm-a02.html' | relative_url }}">06.03 A02 LLM 前處理</a>
<a href="{{ '/results/year-match-a02.html' | relative_url }}">06.13 A02 年份比對</a>
<a class="active" href="{{ '/results/db-filter.html' | relative_url }}">DB Filter 篩選結果</a>
<a href="{{ '/results/non-english-check.html' | relative_url }}">非英文與特殊符號檢查</a>
</div>
</aside>

<section class="results-content" markdown="1">

<div class="run-summary">
  <div class="run-stat"><strong>103</strong><span>600-2159 秒篩選資料</span></div>
  <div class="run-stat"><strong>237</strong><span>廠商去頭尾各 5 家資料</span></div>
  <div class="run-stat"><strong>30</strong><span>60 秒長度區間列</span></div>
  <div class="run-stat"><strong>CSV/MD</strong><span>同時保留表格與報告</span></div>
</div>

## 來源檔

| 檔案 | 用途 |
| --- | --- |
| `Result/DB_Filter/duration_interval_summary.md` | 每 60 秒長度區間的數量與廠商摘要 |
| `Result/DB_Filter/duration_interval_manufacturer_counts.csv` | 長度區間與廠商交叉統計 |
| `Result/DB_Filter/06.03_600-2159_copy_manifest.*` | 長度篩選後複製清單 |
| `Result/DB_Filter/06.03_manufacturer_trimmed_copy_manifest.*` | 廠商去頭尾各 5 家後複製清單 |
| `Result/DB_Filter/filtered_video_detail.*` | 篩選後影片細節 |

## 長度區間範例

| 區間 | 筆數 | 主要廠商 |
| --- | ---: | --- |
| 600-659 | 20 | BMW、Mercedes-Benz、Toyota、Audi、McLaren、Porsche 等 |
| 660-719 | 6 | BMW、Mercedes-Benz、Lexus、Volvo |
| 720-779 | 7 | BMW、Chevrolet、Mercedes-Benz、Cadillac |
| 840-899 | 9 | Volvo、BMW、Hyundai、Infiniti、Lexus、Nissan |

## 用途

DB Filter 結果適合用來建立更均衡或更可比較的 BERTopic 輸入資料。例如：
長度篩選可降低極短或極長影片的影響；廠商去頭尾則可避免某些廠商資料量過多，
讓主題比較更接近研究設計。

</section>
</div>
