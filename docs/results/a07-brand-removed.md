---
title: A07 有刪除廠商車款
description: A07 BERTopic run with min_cluster_size 200 and brand/model removal.
---

# A07 有刪除廠商車款

<div class="results-layout" markdown="1">
<aside class="results-sidebar" markdown="1">
## 結果導覽

<div class="result-nav-group" markdown="1">
<a href="{{ '/results.html' | relative_url }}">結果總覽</a>
<a href="{{ '/results/a08-no-brand-removal.html' | relative_url }}">A08 無刪除廠商車款</a>
<a href="{{ '/results/a07-no-brand-removal.html' | relative_url }}">A07 無刪除廠商車款</a>
<a class="active" href="{{ '/results/a07-brand-removed.html' | relative_url }}">A07 有刪除廠商車款</a>
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
  <div class="run-stat"><strong>3</strong><span>topic_info 筆數，含 outlier</span></div>
  <div class="run-stat"><strong>7,117</strong><span>文本命中移除詞次數</span></div>
  <div class="run-stat"><strong>已刪除</strong><span>啟用品牌/車款詞移除</span></div>
</div>

## Run 資料

| 項目 | 內容 |
| --- | --- |
| 母倉庫來源 | `Result/Result_06.02_A07-有刪除廠商車款.md`、`Result/Result_06.02_A07-有刪除廠商車款-topic_info.csv` |
| 開始時間 | 2026-06-02T13:55:09 |
| 完成時間 | 2026-06-02T13:57:27 |
| 固定參數 | `HDBSCAN min_cluster_size=200` |
| 輸入資料 | `#TXT_DATA/05.24_txt-test_deleted(434)` |
| 品牌/車款刪除 | 開啟 |
| 刪除詞來源 | `#TXT_DATA/ver.5.5_EVcar-URL.db` |
| Topic label | OpenRouter / `openai/gpt-4o-mini` |

## 主題摘要

| Topic | Count | OpenRouter 標籤 | 代表詞方向 |
| ---: | ---: | --- | --- |
| -1 | 1,191 | Hybrid Vehicle Warranties and Maintenance | warranty、corolla、years、connect |
| 0 | 25,530 | Innovative Electric Vehicle Technology | car、new、vehicle、electric |
| 1 | 257 | New XC90 and S60 Design | xc90、s60、xc40、recharge |

## 初步判讀

這個版本移除品牌與車款詞後，主題數大幅收斂。它適合作為「品牌訊號控制組」，
但 `min_cluster_size=200` 可能太粗，使許多可解釋子題被併入大型 topic。

</section>
</div>
