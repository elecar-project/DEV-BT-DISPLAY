---
title: A07 無刪除廠商車款
description: A07 BERTopic run with min_cluster_size 200 and no brand/model removal.
---

# A07 無刪除廠商車款

<div class="results-layout" markdown="1">
<aside class="results-sidebar" markdown="1">
## 結果導覽

<div class="result-nav-group" markdown="1">
<a href="{{ '/results.html' | relative_url }}">結果總覽</a>
<a href="{{ '/results/a08-no-brand-removal.html' | relative_url }}">A08 無刪除廠商車款</a>
<a class="active" href="{{ '/results/a07-no-brand-removal.html' | relative_url }}">A07 無刪除廠商車款</a>
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
</aside>

<section class="results-content" markdown="1">

<div class="run-summary">
  <div class="run-stat"><strong>200</strong><span>HDBSCAN min_cluster_size</span></div>
  <div class="run-stat"><strong>7</strong><span>topic_info 筆數，含 outlier</span></div>
  <div class="run-stat"><strong>26,978</strong><span>最後輸入 BERTopic 句子數</span></div>
  <div class="run-stat"><strong>未刪除</strong><span>保留廠商與車款詞</span></div>
</div>

## Run 資料

| 項目 | 內容 |
| --- | --- |
| 母倉庫來源 | `Result/Result_06.02_A07-無刪除廠商車款.md`、`Result/Result_06.02_A07-無刪除廠商車款-topic_info.csv` |
| 固定參數 | `HDBSCAN min_cluster_size=200` |
| 輸入資料 | `#TXT_DATA/05.24_txt-test_deleted(434)` |
| 資料數量 | 434 個 TXT 檔，45 個廠商前綴 |
| 品牌/車款刪除 | 關閉 |
| Topic label | OpenRouter / `openai/gpt-4o-mini` |

## 主題摘要

| Topic | Count | OpenRouter 標籤 | 代表詞方向 |
| ---: | ---: | --- | --- |
| -1 | 1,859 | Car Subscriptions and Warranties | warranty、subscription、hybrid |
| 0 | 22,673 | Electric Vehicle Autonomous Driving Features | car、electric、design、driving |
| 1 | 907 | Toyota Safety and Connectivity Features | prius、rav4、corolla、safety |
| 2 | 631 | BMW 5 Series and i Models | bmw、series、i3、i8 |
| 3 | 310 | Nissan LEAF Electric Vehicle Launch | nissan、leaf、aria、ev |
| 4 | 304 | Audi E-Tron Special Features | audi、etron、quattro、q8 |
| 5 | 294 | Volvo Cars and Safety Innovations | volvo、xc90、xc40、safety |

## 初步判讀

A07 無刪除版本顯示品牌與車款詞會明顯影響 topic 結構，例如 BMW、Nissan、
Audi、Volvo 各自形成較清楚的子題。這個結果適合用來理解品牌訊號，但若研究問題
更關心跨品牌語意，應與刪除版一起閱讀。

</section>
</div>
