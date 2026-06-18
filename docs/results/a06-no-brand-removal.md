---
title: A06 無刪除廠商車款
description: A06 BERTopic run without brand/model removal.
---

# A06 無刪除廠商車款

<div class="results-layout" markdown="1">
<aside class="results-sidebar" markdown="1">
## 結果導覽

<div class="result-nav-group" markdown="1">
<a href="{{ '/results.html' | relative_url }}">結果總覽</a>
<a href="{{ '/results/a08-no-brand-removal.html' | relative_url }}">A08 無刪除廠商車款</a>
<a href="{{ '/results/a07-no-brand-removal.html' | relative_url }}">A07 無刪除廠商車款</a>
<a href="{{ '/results/a07-brand-removed.html' | relative_url }}">A07 有刪除廠商車款</a>
<a class="active" href="{{ '/results/a06-no-brand-removal.html' | relative_url }}">A06 無刪除廠商車款</a>
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
  <div class="run-stat"><strong>4</strong><span>topic_info 筆數，含 outlier</span></div>
  <div class="run-stat"><strong>26,978</strong><span>最後輸入 BERTopic 句子數</span></div>
  <div class="run-stat"><strong>434</strong><span>輸入 TXT 檔案數</span></div>
  <div class="run-stat"><strong>未刪除</strong><span>保留廠商與車款詞</span></div>
</div>

## Run 資料

| 項目 | 內容 |
| --- | --- |
| 母倉庫來源 | `Result/Result_06.02_A06-無刪除廠商車款.md`、`Result/Result_06.02_A06-無刪除廠商車款-topic_info.csv` |
| 輸入資料 | `#TXT_DATA/05.24_txt-test_deleted(434)` |
| 品牌/車款刪除 | 關閉 |
| Embedding | `sentence-transformers/all-MiniLM-L6-v2` |
| CountVectorizer | `stop_words=english`、`min_df=2`、`ngram_range=(1, 2)` |

## 主題摘要

| Topic | Count | OpenRouter 標籤 | 代表詞方向 |
| ---: | ---: | --- | --- |
| -1 | 576 | Mustang Car Enthusiasm | polestar、mustang、q50、s60 |
| 0 | 25,102 | Advanced Car Design Features | car、new、electric、design |
| 1 | 1,014 | Toyota Safety and Connectivity Features | prius、toyota、rav4、hybrid |
| 2 | 286 | Volvo Safety and New Models | volvo、xc90、xc40、recharge |

## 初步判讀

A06 無刪除版本保留明顯品牌訊號，形成 Toyota 與 Volvo 等子題。與 A07 無刪除相比，
此版本主題更少，適合作為較早期 baseline。

</section>
</div>
