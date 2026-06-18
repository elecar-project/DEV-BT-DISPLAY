---
title: 06.13 A02 年份比對
description: Dataset to database upload-year matching reports.
---

# 06.13 A02 年份比對

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
<a class="active" href="{{ '/results/year-match-a02.html' | relative_url }}">06.13 A02 年份比對</a>
<a href="{{ '/results/db-filter.html' | relative_url }}">DB Filter 篩選結果</a>
<a href="{{ '/results/non-english-check.html' | relative_url }}">非英文與特殊符號檢查</a>
</div>
</aside>

<section class="results-content" markdown="1">

<div class="run-summary">
  <div class="run-stat"><strong>434</strong><span>match report 筆數</span></div>
  <div class="run-stat"><strong>100%</strong><span>範例列 match_score</span></div>
  <div class="run-stat"><strong>08-19</strong><span>其中一組年份 bucket</span></div>
  <div class="run-stat"><strong>DB</strong><span>以 upload year 作為主要來源</span></div>
</div>

## Run 資料

| 項目 | 內容 |
| --- | --- |
| 母倉庫來源 | `Result/06.13_A02/` |
| 主要檔案 | `06.13_A02-match_report(434).csv` |
| 其他版本 | pre-2008 as 2008、08-17/18-25、08-18/19-25、08-20/21-25 |
| 比對欄位 | dataset title、DB title、upload year、upload date、uploader、video URL |

## 用途

年份比對可用來建立時間切分後的主題比較，例如早期電動車敘事與較近期電動車敘事的差異。
目前頁面先記錄 match report 的存在與用途，後續若產生時間切分 BERTopic 結果，
可以在這裡加入各時段 topic 對照。

</section>
</div>
