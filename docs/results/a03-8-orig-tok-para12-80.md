---
title: A03-8｜orig + tok + 段落 12-80
description: A03-8｜orig + tok + 段落 12-80 的 HDBSCAN min_cluster_size 敏感度分析。
experiment_id: a03-8-orig-tok-para12-80
---

# A03-8｜orig + tok + 段落 12-80

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
<div class="run-summary">
  <div class="run-stat"><strong>21</strong><span>測試參數組數</span></div>
  <div class="run-stat"><strong>200</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>5.15%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>2</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗固定 embedding 與 UMAP 設定，只掃描 HDBSCAN 的 `min_cluster_size`。自動選擇規則為：先保留至少兩個非 noise 主題，再選取 noise ratio 最低的設定。

> **判讀提醒：** 自動選擇的 `min_cluster_size=200` 最大非 noise 主題占 92.56%。noise ratio 是重要指標，但仍應搭配代表詞、代表句與主題大小分布進行人工審查。

<div class="result-figure-scroller" aria-label="A03-8｜orig + tok + 段落 12-80 圖表檢視">
  <figure><img src="{{ '/assets/results/a03-8-orig-tok-para12-80/A03-8(orig)_tok(para12-80)_min_cluster_chart.png' | relative_url }}" alt="A03-8｜orig + tok + 段落 12-80 min cluster size 掃描圖"><figcaption>min_cluster_size 掃描圖</figcaption></figure>
</div>

## 參數掃描結果

<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>自動選擇</th></tr></thead>
  <tbody><tr><td>50</td><td>41</td><td>40.84%</td><td>4,548</td><td>254</td><td>204</td><td></td></tr><tr><td>75</td><td>27</td><td>42.85%</td><td>4,772</td><td>254</td><td>204</td><td></td></tr><tr><td>100</td><td>18</td><td>39.76%</td><td>4,428</td><td>254</td><td>204</td><td></td></tr><tr><td>125</td><td>14</td><td>41.77%</td><td>4,652</td><td>254</td><td>204</td><td></td></tr><tr><td>150</td><td>3</td><td>5.65%</td><td>629</td><td>254</td><td>204</td><td></td></tr><tr><td>175</td><td>3</td><td>5.78%</td><td>644</td><td>254</td><td>204</td><td></td></tr><tr class="selection-row"><td>200</td><td>2</td><td>5.15%</td><td>574</td><td>254</td><td>10,308</td><td><span class="scan-badge">自動選擇：最低雜訊</span></td></tr><tr><td>225</td><td>2</td><td>7.67%</td><td>854</td><td>254</td><td>10,028</td><td></td></tr><tr><td>250</td><td>2</td><td>10.52%</td><td>1,171</td><td>254</td><td>9,711</td><td></td></tr><tr><td>275</td><td>2</td><td>29.23%</td><td>3,255</td><td>408</td><td>7,473</td><td></td></tr><tr><td>300</td><td>2</td><td>30.87%</td><td>3,438</td><td>393</td><td>7,305</td><td></td></tr><tr><td>325</td><td>2</td><td>32.84%</td><td>3,657</td><td>7,107</td><td>372</td><td></td></tr><tr><td>350</td><td>2</td><td>33.74%</td><td>3,757</td><td>393</td><td>6,986</td><td></td></tr><tr><td>375</td><td>2</td><td>33.80%</td><td>3,764</td><td>430</td><td>6,942</td><td></td></tr><tr><td>400</td><td>2</td><td>35.10%</td><td>3,909</td><td>406</td><td>6,821</td><td></td></tr><tr><td>500</td><td>0</td><td>100.00%</td><td>11,136</td><td>0</td><td>0</td><td></td></tr><tr><td>600</td><td>0</td><td>100.00%</td><td>11,136</td><td>0</td><td>0</td><td></td></tr><tr><td>700</td><td>0</td><td>100.00%</td><td>11,136</td><td>0</td><td>0</td><td></td></tr><tr><td>800</td><td>0</td><td>100.00%</td><td>11,136</td><td>0</td><td>0</td><td></td></tr><tr><td>900</td><td>0</td><td>100.00%</td><td>11,136</td><td>0</td><td>0</td><td></td></tr><tr><td>1000</td><td>0</td><td>100.00%</td><td>11,136</td><td>0</td><td>0</td><td></td></tr></tbody>
</table>
</div>

## 自動選擇值的主題分布

<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody><tr><td>-1（noise）</td><td>574</td><td>5.15%</td><td>polestar, crown, mustang, new, candy, car, q50, toyota, just, electric</td></tr><tr><td>0</td><td>10,308</td><td>92.56%</td><td>car, new, like, just, vehicle, really, electric, drive, design, driving</td></tr><tr><td>1</td><td>254</td><td>2.28%</td><td>volvo, xc90, new, car, s60, xc40, safety, new xc90, cars, design</td></tr></tbody>
</table>
</div>

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/a03-8-orig-tok-para12-80/Result_06.03_A03-8(orig)_tok(para12-80)-min_cluster_size.csv' | relative_url }}) | 參數掃描 CSV原始檔 |
| [主題摘要 CSV]({{ '/assets/results/a03-8-orig-tok-para12-80/Result_06.03_A03-8(orig)_tok(para12-80)-best_topic_info.csv' | relative_url }}) | 主題摘要 CSV原始檔 |
| [句子－主題對照 CSV]({{ '/assets/results/a03-8-orig-tok-para12-80/Result_06.03_A03-8(orig)_tok(para12-80)-best_document_topics.csv' | relative_url }}) | 句子－主題對照 CSV原始檔 |
| [run log JSON]({{ '/assets/results/a03-8-orig-tok-para12-80/Result_06.03_A03-8(orig)_tok(para12-80)-run_log.json' | relative_url }}) | run log JSON原始檔 |
| [實驗報告 Markdown]({{ '/assets/results/a03-8-orig-tok-para12-80/Result_06.03_A03-8(orig)_tok(para12-80).md' | relative_url }}) | 實驗報告 Markdown原始檔 |
| [執行程式 Python]({{ '/assets/results/a03-8-orig-tok-para12-80/run_06.03_A03_8_orig_tok_para12_80.py' | relative_url }}) | 執行程式 Python原始檔 |

</section>
</div>
