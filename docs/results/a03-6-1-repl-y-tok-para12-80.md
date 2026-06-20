---
title: A03-6.1｜repl-y + tok + 段落 12-80
description: A03-6.1｜repl-y + tok + 段落 12-80 的 HDBSCAN min_cluster_size 敏感度分析。
---

# A03-6.1｜repl-y + tok + 段落 12-80

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table">
  <thead><tr><th>項目</th><th>設定</th></tr></thead>
  <tbody>
    <tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok(para12-80)_dataset</code></td></tr>
    <tr><td>使用欄位</td><td><code>sentence</code></td></tr>
    <tr><td>可用句子</td><td>10,978</td></tr>
    <tr><td>短句</td><td>9 筆少於 3 words</td></tr>
  </tbody>
</table>

### 固定模型設定



<table class="settings-table">
  <thead><tr><th>項目</th><th>設定</th></tr></thead>
  <tbody>
    <tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code></td></tr>
    <tr><td>UMAP</td><td>neighbors 15 / components 5 / min dist 0 / cosine</td></tr>
    <tr><td>HDBSCAN</td><td>euclidean / eom / prediction data</td></tr>
    <tr><td>Vectorizer</td><td>English stop words / ngram 1-2 / min df 2</td></tr>
  </tbody>
</table>
</aside>

<section markdown="1">
<div class="run-summary">
  <div class="run-stat"><strong>21</strong><span>測試參數組數</span></div>
  <div class="run-stat"><strong>50</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>0.07%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>2</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗固定 embedding 與 UMAP 設定，只掃描 HDBSCAN 的 `min_cluster_size`。自動選擇規則為：先保留至少兩個非 noise 主題，再選取 noise ratio 最低的設定。

> **判讀提醒：** 自動選擇的 `min_cluster_size=50` 最大非 noise 主題占 99.32%。noise ratio 是重要指標，但仍應搭配代表詞、代表句與主題大小分布進行人工審查。

<div class="result-figure-scroller" aria-label="A03-6.1｜repl-y + tok + 段落 12-80 圖表檢視">
  <figure><img src="{{ '/assets/results/a03-6-1-repl-y-tok-para12-80/A03-6.1(repl-y)_tok(para12-80)_min_cluster_chart.png' | relative_url }}" alt="A03-6.1｜repl-y + tok + 段落 12-80 min cluster size 掃描圖"><figcaption>min_cluster_size 掃描圖</figcaption></figure>
</div>

## 參數掃描結果

<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>自動選擇</th></tr></thead>
  <tbody><tr class="selection-row"><td>50</td><td>2</td><td>0.07%</td><td>8</td><td>67</td><td>10,903</td><td><span class="scan-badge">自動選擇：最低雜訊</span></td></tr><tr><td>75</td><td>14</td><td>38.81%</td><td>4,261</td><td>75</td><td>477</td><td></td></tr><tr><td>100</td><td>8</td><td>36.02%</td><td>3,954</td><td>2,057</td><td>247</td><td></td></tr><tr><td>125</td><td>8</td><td>40.09%</td><td>4,401</td><td>2,031</td><td>211</td><td></td></tr><tr><td>150</td><td>5</td><td>36.01%</td><td>3,953</td><td>2,002</td><td>150</td><td></td></tr><tr><td>175</td><td>2</td><td>24.13%</td><td>2,649</td><td>1,955</td><td>6,374</td><td></td></tr><tr><td>200</td><td>2</td><td>26.90%</td><td>2,953</td><td>1,921</td><td>6,104</td><td></td></tr><tr><td>225</td><td>2</td><td>29.19%</td><td>3,205</td><td>1,849</td><td>5,924</td><td></td></tr><tr><td>250</td><td>4</td><td>38.91%</td><td>4,272</td><td>1,793</td><td>3,956</td><td></td></tr><tr><td>275</td><td>3</td><td>37.21%</td><td>4,085</td><td>1,726</td><td>1,212</td><td></td></tr><tr><td>300</td><td>3</td><td>39.06%</td><td>4,288</td><td>1,683</td><td>1,139</td><td></td></tr><tr><td>325</td><td>3</td><td>41.02%</td><td>4,503</td><td>1,605</td><td>1,071</td><td></td></tr><tr><td>350</td><td>3</td><td>43.55%</td><td>4,781</td><td>1,526</td><td>986</td><td></td></tr><tr><td>375</td><td>3</td><td>45.73%</td><td>5,020</td><td>1,424</td><td>3,637</td><td></td></tr><tr><td>400</td><td>3</td><td>48.07%</td><td>5,277</td><td>1,324</td><td>816</td><td></td></tr><tr><td>500</td><td>3</td><td>50.07%</td><td>5,497</td><td>873</td><td>993</td><td></td></tr><tr><td>600</td><td>2</td><td>63.43%</td><td>6,963</td><td>692</td><td>3,323</td><td></td></tr><tr><td>700</td><td>0</td><td>100.00%</td><td>10,978</td><td>0</td><td>0</td><td></td></tr><tr><td>800</td><td>0</td><td>100.00%</td><td>10,978</td><td>0</td><td>0</td><td></td></tr><tr><td>900</td><td>0</td><td>100.00%</td><td>10,978</td><td>0</td><td>0</td><td></td></tr><tr><td>1000</td><td>0</td><td>100.00%</td><td>10,978</td><td>0</td><td>0</td><td></td></tr></tbody>
</table>
</div>

## 自動選擇值的主題分布

<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody><tr><td>-1（noise）</td><td>8</td><td>0.07%</td><td>sentra, new, testament, redesign, forward, emergency braking, active safety, 2016, sedans, warning</td></tr><tr><td>0</td><td>10,903</td><td>99.32%</td><td>car, new, like, just, vehicle, electric, design, drive, driving, available</td></tr><tr><td>1</td><td>67</td><td>0.61%</td><td>warranty, 000, 000 mile, year, mile, whichever comes, whichever, 000 miles, years, hybrid</td></tr></tbody>
</table>
</div>

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/a03-6-1-repl-y-tok-para12-80/Result_06.03_A03-6.1(repl-y)_tok(para12-80)-min_cluster_size.csv' | relative_url }}) | 參數掃描 CSV原始檔 |
| [主題摘要 CSV]({{ '/assets/results/a03-6-1-repl-y-tok-para12-80/Result_06.03_A03-6.1(repl-y)_tok(para12-80)-best_topic_info.csv' | relative_url }}) | 主題摘要 CSV原始檔 |
| [句子－主題對照 CSV]({{ '/assets/results/a03-6-1-repl-y-tok-para12-80/Result_06.03_A03-6.1(repl-y)_tok(para12-80)-best_document_topics.csv' | relative_url }}) | 句子－主題對照 CSV原始檔 |
| [run log JSON]({{ '/assets/results/a03-6-1-repl-y-tok-para12-80/Result_06.03_A03-6.1(repl-y)_tok(para12-80)-run_log.json' | relative_url }}) | run log JSON原始檔 |
| [實驗報告 Markdown]({{ '/assets/results/a03-6-1-repl-y-tok-para12-80/Result_06.03_A03-6.1(repl-y)_tok(para12-80).md' | relative_url }}) | 實驗報告 Markdown原始檔 |
| [執行程式 Python]({{ '/assets/results/a03-6-1-repl-y-tok-para12-80/run_06.03_A03_6_1_repl_y_tok_para12_80.py' | relative_url }}) | 執行程式 Python原始檔 |

</section>
</div>
