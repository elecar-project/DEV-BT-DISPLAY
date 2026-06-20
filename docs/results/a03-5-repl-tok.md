---
title: A03-5｜repl + tok
description: A03-5｜repl + tok 的 HDBSCAN min_cluster_size 敏感度分析。
---

# A03-5｜repl + tok

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table">
  <thead><tr><th>項目</th><th>設定</th></tr></thead>
  <tbody>
    <tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok_dataset</code></td></tr>
    <tr><td>使用欄位</td><td><code>sentence</code></td></tr>
    <tr><td>可用句子</td><td>31,503</td></tr>
    <tr><td>短句</td><td>1,386 筆少於 3 words</td></tr>
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
  <div class="run-stat"><strong>100</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>1.05%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>4</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗固定 embedding 與 UMAP 設定，只掃描 HDBSCAN 的 `min_cluster_size`。自動選擇規則為：先保留至少兩個非 noise 主題，再選取 noise ratio 最低的設定。

> **判讀提醒：** 自動選擇的 `min_cluster_size=100` 最大非 noise 主題占 97.84%。noise ratio 是重要指標，但仍應搭配代表詞、代表句與主題大小分布進行人工審查。

<div class="result-figure-scroller" aria-label="A03-5｜repl + tok 圖表檢視">
  <figure><img src="{{ '/assets/results/a03-5-repl-tok/A03-5(repl)_tok_min_cluster_chart.png' | relative_url }}" alt="A03-5｜repl + tok min cluster size 掃描圖"><figcaption>min_cluster_size 掃描圖</figcaption></figure>
</div>

## 參數掃描結果

<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>自動選擇</th></tr></thead>
  <tbody><tr><td>50</td><td>77</td><td>49.37%</td><td>15,552</td><td>111</td><td>51</td><td></td></tr><tr><td>75</td><td>47</td><td>48.82%</td><td>15,380</td><td>111</td><td>135</td><td></td></tr><tr class="selection-row"><td>100</td><td>4</td><td>1.05%</td><td>330</td><td>111</td><td>135</td><td><span class="scan-badge">自動選擇：最低雜訊</span></td></tr><tr><td>125</td><td>2</td><td>1.39%</td><td>438</td><td>135</td><td>30,930</td><td></td></tr><tr><td>150</td><td>22</td><td>51.55%</td><td>16,239</td><td>201</td><td>789</td><td></td></tr><tr><td>175</td><td>21</td><td>53.42%</td><td>16,829</td><td>190</td><td>773</td><td></td></tr><tr><td>200</td><td>17</td><td>54.22%</td><td>17,081</td><td>754</td><td>363</td><td></td></tr><tr><td>225</td><td>2</td><td>18.86%</td><td>5,941</td><td>4,340</td><td>21,222</td><td></td></tr><tr><td>250</td><td>2</td><td>16.52%</td><td>5,204</td><td>4,399</td><td>21,900</td><td></td></tr><tr><td>275</td><td>2</td><td>13.74%</td><td>4,327</td><td>4,472</td><td>22,704</td><td></td></tr><tr><td>300</td><td>2</td><td>13.99%</td><td>4,406</td><td>4,471</td><td>22,626</td><td></td></tr><tr><td>325</td><td>2</td><td>15.34%</td><td>4,834</td><td>4,433</td><td>22,236</td><td></td></tr><tr><td>350</td><td>9</td><td>46.14%</td><td>14,537</td><td>4,418</td><td>1,813</td><td></td></tr><tr><td>375</td><td>2</td><td>15.58%</td><td>4,907</td><td>4,377</td><td>22,219</td><td></td></tr><tr><td>400</td><td>3</td><td>22.81%</td><td>7,185</td><td>21,235</td><td>777</td><td></td></tr><tr><td>500</td><td>3</td><td>24.65%</td><td>7,765</td><td>20,640</td><td>787</td><td></td></tr><tr><td>600</td><td>3</td><td>29.88%</td><td>9,412</td><td>19,020</td><td>771</td><td></td></tr><tr><td>700</td><td>5</td><td>54.32%</td><td>17,111</td><td>2,268</td><td>738</td><td></td></tr><tr><td>800</td><td>2</td><td>28.84%</td><td>9,085</td><td>3,655</td><td>18,763</td><td></td></tr><tr><td>900</td><td>2</td><td>37.08%</td><td>11,681</td><td>2,888</td><td>16,934</td><td></td></tr><tr><td>1000</td><td>2</td><td>44.70%</td><td>14,082</td><td>2,164</td><td>15,257</td><td></td></tr></tbody>
</table>
</div>

## 自動選擇值的主題分布

<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody><tr><td>-1（noise）</td><td>330</td><td>1.05%</td><td>absolutely, crown, thank, yeah, google, android, thank thank, wow, music, yeah yeah</td></tr><tr><td>0</td><td>30,823</td><td>97.84%</td><td>model, brand, car, new, like, just, vehicle, electric, design, drive</td></tr><tr><td>1</td><td>135</td><td>0.43%</td><td>warranty, 000, mile, year, whichever, whichever comes, maintenance, 000 miles, 100 000, years</td></tr><tr><td>2</td><td>111</td><td>0.35%</td><td>thank thank, thank, thank thanks, thanks, thanks thanks, irv, , , , </td></tr><tr><td>3</td><td>104</td><td>0.33%</td><td>okay, okay okay, yes, right, right okay, okay right, yes yes, right right, yes right, yep</td></tr></tbody>
</table>
</div>

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/a03-5-repl-tok/Result_06.03_A03-5(repl)_tok-min_cluster_size.csv' | relative_url }}) | 參數掃描 CSV原始檔 |
| [主題摘要 CSV]({{ '/assets/results/a03-5-repl-tok/Result_06.03_A03-5(repl)_tok-best_topic_info.csv' | relative_url }}) | 主題摘要 CSV原始檔 |
| [句子－主題對照 CSV]({{ '/assets/results/a03-5-repl-tok/Result_06.03_A03-5(repl)_tok-best_document_topics.csv' | relative_url }}) | 句子－主題對照 CSV原始檔 |
| [run log JSON]({{ '/assets/results/a03-5-repl-tok/Result_06.03_A03-5(repl)_tok-run_log.json' | relative_url }}) | run log JSON原始檔 |
| [實驗報告 Markdown]({{ '/assets/results/a03-5-repl-tok/Result_06.03_A03-5(repl)_tok.md' | relative_url }}) | 實驗報告 Markdown原始檔 |
| [執行程式 Python]({{ '/assets/results/a03-5-repl-tok/run_06.03_A03_5_repl_tok.py' | relative_url }}) | 執行程式 Python原始檔 |

</section>
</div>
