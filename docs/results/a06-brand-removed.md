---
title: A06 有刪除廠商車款
description: A06 BERTopic run with brand/model removal.
---

# A06 有刪除廠商車款

<div class="results-layout" markdown="1">
<aside class="results-sidebar" markdown="1">
## 結果導覽

<div class="result-nav-group" markdown="1">
<a href="{{ '/results.html' | relative_url }}">結果總覽</a>
<a href="{{ '/results/a08-no-brand-removal.html' | relative_url }}">A08 無刪除廠商車款</a>
<a href="{{ '/results/a07-no-brand-removal.html' | relative_url }}">A07 無刪除廠商車款</a>
<a href="{{ '/results/a07-brand-removed.html' | relative_url }}">A07 有刪除廠商車款</a>
<a href="{{ '/results/a06-no-brand-removal.html' | relative_url }}">A06 無刪除廠商車款</a>
<a class="active" href="{{ '/results/a06-brand-removed.html' | relative_url }}">A06 有刪除廠商車款</a>
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
  <div class="run-stat"><strong>3</strong><span>topic_info 筆數，含 outlier</span></div>
  <div class="run-stat"><strong>26,978</strong><span>最後輸入 BERTopic 句子數</span></div>
  <div class="run-stat"><strong>561</strong><span>移除用詞合計</span></div>
  <div class="run-stat"><strong>已刪除</strong><span>啟用品牌/車款詞移除</span></div>
</div>

## Run 資料

| 項目 | 內容 |
| --- | --- |
| 母倉庫來源 | `Result/Result_06.02_A06-有刪除廠商車款.md`、`Result/Result_06.02_A06-有刪除廠商車款-topic_info.csv` |
| 輸入資料 | `#TXT_DATA/05.24_txt-test_deleted(434)` |
| 品牌/車款刪除 | 開啟 |
| 刪除詞來源 | `#TXT_DATA/ver.5.5_EVcar-URL.db` |
| 移除詞摘要 | 廠商名稱 45 筆，唯一車款名稱 517 筆，移除用詞合計 561 筆 |

## 主題摘要

| Topic | Count | OpenRouter 標籤 | 代表詞方向 |
| ---: | ---: | --- | --- |
| -1 | 1,191 | Vehicle Warranties and Maintenance | warranty、corolla、crown、connect |
| 0 | 25,530 | Innovative Hybrid Electric Vehicles | car、new、vehicle、electric |
| 1 | 257 | Volvo XC90 and S60 Updates | xc90、s60、xc40、recharge |

## 初步判讀

A06 有刪除版本與 A07 有刪除版本相當接近，可作為品牌詞控制後的早期 baseline。
它的主題數偏少，若要呈現給內部研究者，建議搭配 A08 閱讀。

</section>
</div>
