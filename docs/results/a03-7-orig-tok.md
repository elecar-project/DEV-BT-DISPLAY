---
title: A03-7｜orig + tok
description: A03-7｜orig + tok 的 HDBSCAN min_cluster_size 敏感度分析。
---

# A03-7｜orig + tok

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table">
  <thead><tr><th>項目</th><th>設定</th></tr></thead>
  <tbody>
    <tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok_dataset</code></td></tr>
    <tr><td>使用欄位</td><td><code>sentence</code></td></tr>
    <tr><td>可用句子</td><td>31,883</td></tr>
    <tr><td>短句</td><td>1,471 筆少於 3 words</td></tr>
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
  <div class="run-stat"><strong>175</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>1.43%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>2</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗固定 embedding 與 UMAP 設定，只掃描 HDBSCAN 的 `min_cluster_size`。自動選擇規則為：先保留至少兩個非 noise 主題，再選取 noise ratio 最低的設定。

> **判讀提醒：** 自動選擇的 `min_cluster_size=175` 最大非 noise 主題占 97.40%。noise ratio 是重要指標，但仍應搭配代表詞、代表句與主題大小分布進行人工審查。

<div class="result-figure-scroller" aria-label="A03-7｜orig + tok 圖表檢視">
  <figure><img src="{{ '/assets/results/a03-7-orig-tok/A03-7(orig)_tok_min_cluster_chart.png' | relative_url }}" alt="A03-7｜orig + tok min cluster size 掃描圖"><figcaption>min_cluster_size 掃描圖</figcaption></figure>
</div>

## 參數掃描結果

<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>自動選擇</th></tr></thead>
  <tbody><tr><td>50</td><td>96</td><td>46.77%</td><td>14,911</td><td>111</td><td>51</td><td></td></tr><tr><td>75</td><td>63</td><td>47.47%</td><td>15,134</td><td>111</td><td>113</td><td></td></tr><tr><td>100</td><td>48</td><td>45.80%</td><td>14,604</td><td>111</td><td>374</td><td></td></tr><tr><td>125</td><td>39</td><td>49.99%</td><td>15,939</td><td>374</td><td>144</td><td></td></tr><tr><td>150</td><td>26</td><td>45.97%</td><td>14,656</td><td>374</td><td>156</td><td></td></tr><tr class="selection-row"><td>175</td><td>2</td><td>1.43%</td><td>455</td><td>374</td><td>31,054</td><td><span class="scan-badge">自動選擇：最低雜訊</span></td></tr><tr><td>200</td><td>2</td><td>1.58%</td><td>505</td><td>374</td><td>31,004</td><td></td></tr><tr><td>225</td><td>2</td><td>1.67%</td><td>534</td><td>374</td><td>30,975</td><td></td></tr><tr><td>250</td><td>2</td><td>1.68%</td><td>535</td><td>374</td><td>30,974</td><td></td></tr><tr><td>275</td><td>2</td><td>1.68%</td><td>535</td><td>374</td><td>30,974</td><td></td></tr><tr><td>300</td><td>2</td><td>1.73%</td><td>550</td><td>374</td><td>30,959</td><td></td></tr><tr><td>325</td><td>2</td><td>1.73%</td><td>552</td><td>374</td><td>30,957</td><td></td></tr><tr><td>350</td><td>2</td><td>1.89%</td><td>603</td><td>374</td><td>30,906</td><td></td></tr><tr><td>375</td><td>3</td><td>14.53%</td><td>4,633</td><td>389</td><td>634</td><td></td></tr><tr><td>400</td><td>3</td><td>17.15%</td><td>5,468</td><td>631</td><td>546</td><td></td></tr><tr><td>500</td><td>2</td><td>19.28%</td><td>6,147</td><td>611</td><td>25,125</td><td></td></tr><tr><td>600</td><td>4</td><td>64.95%</td><td>20,707</td><td>2,676</td><td>5,309</td><td></td></tr><tr><td>700</td><td>4</td><td>68.06%</td><td>21,700</td><td>2,402</td><td>4,951</td><td></td></tr><tr><td>800</td><td>3</td><td>63.13%</td><td>20,128</td><td>1,911</td><td>5,765</td><td></td></tr><tr><td>900</td><td>3</td><td>67.01%</td><td>21,365</td><td>5,636</td><td>1,029</td><td></td></tr><tr><td>1000</td><td>2</td><td>69.49%</td><td>22,154</td><td>5,159</td><td>4,570</td><td></td></tr></tbody>
</table>
</div>

## 自動選擇值的主題分布

<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody><tr><td>-1（noise）</td><td>455</td><td>1.43%</td><td>thank, crown, thank thank, toyota crown, absolutely, toyota, yeah, google, android, yeah yeah</td></tr><tr><td>0</td><td>31,054</td><td>97.40%</td><td>car, new, like, just, vehicle, really, electric, design, drive, driving</td></tr><tr><td>1</td><td>374</td><td>1.17%</td><td>volvo, xc90, s60, new, xc40, new xc90, ex90, xc40 recharge, cars, recharge</td></tr></tbody>
</table>
</div>

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/a03-7-orig-tok/Result_06.03_A03-7(orig)_tok-min_cluster_size.csv' | relative_url }}) | 參數掃描 CSV原始檔 |
| [主題摘要 CSV]({{ '/assets/results/a03-7-orig-tok/Result_06.03_A03-7(orig)_tok-best_topic_info.csv' | relative_url }}) | 主題摘要 CSV原始檔 |
| [句子－主題對照 CSV]({{ '/assets/results/a03-7-orig-tok/Result_06.03_A03-7(orig)_tok-best_document_topics.csv' | relative_url }}) | 句子－主題對照 CSV原始檔 |
| [run log JSON]({{ '/assets/results/a03-7-orig-tok/Result_06.03_A03-7(orig)_tok-run_log.json' | relative_url }}) | run log JSON原始檔 |
| [實驗報告 Markdown]({{ '/assets/results/a03-7-orig-tok/Result_06.03_A03-7(orig)_tok.md' | relative_url }}) | 實驗報告 Markdown原始檔 |
| [執行程式 Python]({{ '/assets/results/a03-7-orig-tok/run_06.03_A03_7_orig_tok.py' | relative_url }}) | 執行程式 Python原始檔 |

</section>
</div>
