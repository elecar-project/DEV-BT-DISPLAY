---
title: A08 無刪除廠商車款
description: A08 BERTopic run with min_cluster_size 150 and no brand/model removal.
---

# A08 無刪除廠商車款

<div class="results-layout" markdown="1">
<aside class="results-sidebar" markdown="1">
## 結果導覽

<div class="result-nav-group" markdown="1">
<a href="{{ '/results.html' | relative_url }}">結果總覽</a>
<a class="active" href="{{ '/results/a08-no-brand-removal.html' | relative_url }}">A08 無刪除廠商車款</a>
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
</aside>

<section class="results-content" markdown="1">

<div class="run-summary">
  <div class="run-stat"><strong>150</strong><span>HDBSCAN min_cluster_size</span></div>
  <div class="run-stat"><strong>32</strong><span>topic_info 筆數，含 outlier</span></div>
  <div class="run-stat"><strong>26,978</strong><span>最後輸入 BERTopic 句子數</span></div>
  <div class="run-stat"><strong>未刪除</strong><span>保留廠商與車款詞</span></div>
</div>

## Run 資料

| 項目 | 內容 |
| --- | --- |
| 母倉庫來源 | `Result/Result_06.02_A08-無刪除廠商車款.md`、`Result/Result_06.02_A08-無刪除廠商車款-topic_info.csv` |
| 開始時間 | 2026-06-02T14:47:50 |
| 完成時間 | 2026-06-02T14:50:35 |
| 輸入資料 | `#TXT_DATA/05.24_txt-test_deleted(434)` |
| 資料數量 | 434 個 TXT 檔，45 個廠商前綴 |
| 前處理 | 短句過濾 `min_words=6`，移除 URL、HTML、字幕提示與口語雜訊 |
| 品牌/車款刪除 | 關閉 |
| Embedding | `sentence-transformers/all-MiniLM-L6-v2` |
| Topic label | OpenRouter / `openai/gpt-4o-mini` |

## 主題節錄

| Topic | Count | OpenRouter 標籤 | 代表詞方向 |
| ---: | ---: | --- | --- |
| -1 | 12,814 | Vehicle Performance and Technology | new、drive、available、vehicle |
| 0 | 2,203 | SUV Driving Experience Comparison | car、cars、drive、vehicle |
| 2 | 1,219 | Advanced In-Car Display Technology | display、screen、navigation、phone |
| 3 | 747 | Rear Seat Cargo Space Expansion | seats、rear、cargo、passenger |
| 4 | 654 | Advanced Driver Assistance Features | assist、lane、blind spot、camera |
| 7 | 560 | Electric Vehicle Charging Options | charging、charge、stations、plug |
| 8 | 430 | Engine Power and Electric Motors | horsepower、engine、torque、motor |

## 初步判讀

A08 是目前最適合做內部探索的結果。相較 A06/A07，`min_cluster_size=150`
讓主題切分更細，也更容易看到車內顯示、座椅空間、ADAS、充電、馬達與動力等子題。
缺點是因為未刪除廠商與車款詞，仍需要與刪除版本對照，確認主題不是單純由品牌名稱驅動。

</section>
</div>
