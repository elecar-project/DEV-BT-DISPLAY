---
title: B01｜2020-2025 min_cluster_size 掃描
description: B01｜2020-2025 min_cluster_size 掃描 的 HDBSCAN min_cluster_size 敏感度分析。
---

# B01｜2020-2025 min_cluster_size 掃描

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table">
  <thead><tr><th>項目</th><th>設定</th></tr></thead>
  <tbody>
    <tr><td>資料集</td><td><code>Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_20-25(194)_tok(para12-80)_dataset</code></td></tr>
    <tr><td>使用欄位</td><td><code>sentence</code></td></tr>
    <tr><td>可用句子</td><td>10,680</td></tr>
    <tr><td>短句</td><td>0 筆少於 3 words</td></tr>
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
  <div class="run-stat"><strong>125</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>7.40%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>2</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗固定 embedding 與 UMAP 設定，只掃描 HDBSCAN 的 `min_cluster_size`。自動選擇規則為：先保留至少兩個非 noise 主題，再選取 noise ratio 最低的設定。

> **判讀提醒：** 自動選擇的 `min_cluster_size=125` 最大非 noise 主題占 91.11%。noise ratio 是重要指標，但仍應搭配代表詞、代表句與主題大小分布進行人工審查。

<div class="result-figure-scroller" aria-label="B01｜2020-2025 min_cluster_size 掃描 圖表檢視">
  <figure><img src="{{ '/assets/results/b01-20-25-min-cluster/[B]01-(orig)_20-25(194)_tok(para12-80)_min_cluster_chart.png' | relative_url }}" alt="B01｜2020-2025 min_cluster_size 掃描 min cluster size 掃描圖"><figcaption>min_cluster_size 掃描圖</figcaption></figure>
</div>

## 參數掃描結果

<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>自動選擇</th></tr></thead>
  <tbody><tr><td>50</td><td>43</td><td>39.15%</td><td>4,181</td><td>794</td><td>363</td><td></td></tr><tr><td>75</td><td>33</td><td>44.98%</td><td>4,804</td><td>819</td><td>480</td><td></td></tr><tr><td>100</td><td>4</td><td>8.39%</td><td>896</td><td>9,420</td><td>129</td><td></td></tr><tr class="selection-row"><td>125</td><td>2</td><td>7.40%</td><td>790</td><td>9,731</td><td>159</td><td><span class="scan-badge">自動選擇：最低雜訊</span></td></tr><tr><td>150</td><td>3</td><td>16.31%</td><td>1,742</td><td>8,187</td><td>596</td><td></td></tr><tr><td>175</td><td>2</td><td>21.20%</td><td>2,264</td><td>8,115</td><td>301</td><td></td></tr><tr><td>200</td><td>7</td><td>63.30%</td><td>6,760</td><td>1,207</td><td>843</td><td></td></tr><tr><td>225</td><td>7</td><td>61.26%</td><td>6,543</td><td>1,304</td><td>878</td><td></td></tr><tr><td>250</td><td>3</td><td>49.08%</td><td>5,242</td><td>4,708</td><td>456</td><td></td></tr><tr><td>275</td><td>2</td><td>50.86%</td><td>5,432</td><td>4,800</td><td>448</td><td></td></tr><tr><td>300</td><td>2</td><td>52.08%</td><td>5,562</td><td>4,679</td><td>439</td><td></td></tr><tr><td>325</td><td>2</td><td>56.47%</td><td>6,031</td><td>4,218</td><td>431</td><td></td></tr><tr><td>350</td><td>2</td><td>57.27%</td><td>6,116</td><td>4,133</td><td>431</td><td></td></tr><tr><td>375</td><td>2</td><td>58.73%</td><td>6,272</td><td>3,986</td><td>422</td><td></td></tr><tr><td>400</td><td>2</td><td>59.96%</td><td>6,404</td><td>3,868</td><td>408</td><td></td></tr><tr><td>500</td><td>0</td><td>100.00%</td><td>10,680</td><td>0</td><td>0</td><td></td></tr><tr><td>600</td><td>0</td><td>100.00%</td><td>10,680</td><td>0</td><td>0</td><td></td></tr><tr><td>700</td><td>0</td><td>100.00%</td><td>10,680</td><td>0</td><td>0</td><td></td></tr><tr><td>800</td><td>0</td><td>100.00%</td><td>10,680</td><td>0</td><td>0</td><td></td></tr><tr><td>900</td><td>0</td><td>100.00%</td><td>10,680</td><td>0</td><td>0</td><td></td></tr><tr><td>1000</td><td>0</td><td>100.00%</td><td>10,680</td><td>0</td><td>0</td><td></td></tr></tbody>
</table>
</div>

## 自動選擇值的主題分布

<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody><tr><td>-1（noise）</td><td>790</td><td>7.40%</td><td>000, warranty, crown, year, camry, mustang, years, 000 mile, hybrid, mile</td></tr><tr><td>0</td><td>9,731</td><td>91.11%</td><td>car, new, like, just, drive, electric, driving, rear, really, vehicle</td></tr><tr><td>1</td><td>159</td><td>1.49%</td><td>elantra, sonata, accord, hybrid, hyundai, camry, new, new elantra, sonata hybrid, like</td></tr></tbody>
</table>
</div>

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/b01-20-25-min-cluster/Result_06.13_[C]min_[B]01-(orig)_20-25(194)_tok(para12-80)-min_cluster_size.csv' | relative_url }}) | 參數掃描 CSV原始檔 |
| [主題摘要 CSV]({{ '/assets/results/b01-20-25-min-cluster/Result_06.13_[C]min_[B]01-(orig)_20-25(194)_tok(para12-80)-best_topic_info.csv' | relative_url }}) | 主題摘要 CSV原始檔 |
| [句子－主題對照 CSV]({{ '/assets/results/b01-20-25-min-cluster/Result_06.13_[C]min_[B]01-(orig)_20-25(194)_tok(para12-80)-best_document_topics.csv' | relative_url }}) | 句子－主題對照 CSV原始檔 |
| [run log JSON]({{ '/assets/results/b01-20-25-min-cluster/Result_06.13_[C]min_[B]01-(orig)_20-25(194)_tok(para12-80)-run_log.json' | relative_url }}) | run log JSON原始檔 |
| [實驗報告 Markdown]({{ '/assets/results/b01-20-25-min-cluster/Result_06.13_[C]min_[B]01-(orig)_20-25(194)_tok(para12-80).md' | relative_url }}) | 實驗報告 Markdown原始檔 |
| [執行程式 Python]({{ '/assets/results/b01-20-25-min-cluster/run_06_13_Cmin_B01_orig_20_25_194_tok_para12_80.py' | relative_url }}) | 執行程式 Python原始檔 |

</section>
</div>
