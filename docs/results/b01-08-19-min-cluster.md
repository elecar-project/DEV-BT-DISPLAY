---
title: B01｜2008-2019 min_cluster_size 掃描
description: B01｜2008-2019 min_cluster_size 掃描 的 HDBSCAN min_cluster_size 敏感度分析。
---

# B01｜2008-2019 min_cluster_size 掃描

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料來源

| 項目 | 設定 |
| --- | --- |
| 資料集 | `Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_08-19(240)_tok(para12-80)_dataset` |
| 使用欄位 | `sentence` |
| 可用句子 | 11,160 |
| 短句 | 0 筆少於 3 words |

### 固定模型設定

| 項目 | 設定 |
| --- | --- |
| Embedding | `all-MiniLM-L6-v2` |
| UMAP | neighbors 15 / components 5 / min dist 0 / cosine |
| HDBSCAN | euclidean / eom / prediction data |
| Vectorizer | English stop words / ngram 1-2 / min df 2 |
</aside>

<section markdown="1">
<div class="run-summary">
  <div class="run-stat"><strong>21</strong><span>測試參數組數</span></div>
  <div class="run-stat"><strong>50</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>0.41%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>5</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗固定 embedding 與 UMAP 設定，只掃描 HDBSCAN 的 `min_cluster_size`。自動選擇規則為：先保留至少兩個非 noise 主題，再選取 noise ratio 最低的設定。

> **判讀提醒：** 自動選擇的 `min_cluster_size=50` 最大非 noise 主題占 93.06%。noise ratio 是重要指標，但仍應搭配代表詞、代表句與主題大小分布進行人工審查。

<div class="result-figure-scroller" aria-label="B01｜2008-2019 min_cluster_size 掃描 圖表檢視">
  <figure><img src="{{ '/assets/results/b01-08-19-min-cluster/[B]01-(orig)_08-19(240)_tok(para12-80)_min_cluster_chart.png' | relative_url }}" alt="B01｜2008-2019 min_cluster_size 掃描 min cluster size 掃描圖"><figcaption>min_cluster_size 掃描圖</figcaption></figure>
</div>

## 參數掃描結果

<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>自動選擇</th></tr></thead>
  <tbody><tr class="selection-row"><td>50</td><td>5</td><td>0.41%</td><td>46</td><td>10,385</td><td>281</td><td><span class="scan-badge">自動選擇：最低雜訊</span></td></tr><tr><td>75</td><td>4</td><td>2.36%</td><td>263</td><td>10,245</td><td>257</td><td></td></tr><tr><td>100</td><td>4</td><td>2.54%</td><td>283</td><td>10,225</td><td>257</td><td></td></tr><tr><td>125</td><td>4</td><td>3.17%</td><td>354</td><td>10,160</td><td>251</td><td></td></tr><tr><td>150</td><td>4</td><td>3.66%</td><td>409</td><td>10,109</td><td>247</td><td></td></tr><tr><td>175</td><td>3</td><td>6.76%</td><td>754</td><td>9,924</td><td>245</td><td></td></tr><tr><td>200</td><td>3</td><td>9.38%</td><td>1,047</td><td>9,630</td><td>246</td><td></td></tr><tr><td>225</td><td>3</td><td>9.71%</td><td>1,084</td><td>9,597</td><td>245</td><td></td></tr><tr><td>250</td><td>2</td><td>43.36%</td><td>4,839</td><td>5,190</td><td>1,131</td><td></td></tr><tr><td>275</td><td>3</td><td>53.78%</td><td>6,002</td><td>3,396</td><td>1,097</td><td></td></tr><tr><td>300</td><td>3</td><td>53.75%</td><td>5,998</td><td>3,486</td><td>1,017</td><td></td></tr><tr><td>325</td><td>3</td><td>57.37%</td><td>6,403</td><td>3,275</td><td>946</td><td></td></tr><tr><td>350</td><td>3</td><td>56.52%</td><td>6,308</td><td>3,478</td><td>803</td><td></td></tr><tr><td>375</td><td>3</td><td>60.53%</td><td>6,755</td><td>3,168</td><td>669</td><td></td></tr><tr><td>400</td><td>3</td><td>64.55%</td><td>7,204</td><td>2,874</td><td>561</td><td></td></tr><tr><td>500</td><td>0</td><td>100.00%</td><td>11,160</td><td>0</td><td>0</td><td></td></tr><tr><td>600</td><td>0</td><td>100.00%</td><td>11,160</td><td>0</td><td>0</td><td></td></tr><tr><td>700</td><td>0</td><td>100.00%</td><td>11,160</td><td>0</td><td>0</td><td></td></tr><tr><td>800</td><td>0</td><td>100.00%</td><td>11,160</td><td>0</td><td>0</td><td></td></tr><tr><td>900</td><td>0</td><td>100.00%</td><td>11,160</td><td>0</td><td>0</td><td></td></tr><tr><td>1000</td><td>0</td><td>100.00%</td><td>11,160</td><td>0</td><td>0</td><td></td></tr></tbody>
</table>
</div>

## 自動選擇值的主題分布

<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody><tr><td>-1（noise）</td><td>46</td><td>0.41%</td><td>mustang, mustangs, went, everybody, really, love, like, going, people, got</td></tr><tr><td>0</td><td>10,385</td><td>93.06%</td><td>car, new, like, vehicle, just, really, electric, ve, design, going</td></tr><tr><td>1</td><td>281</td><td>2.52%</td><td>volvo, s60, new, xc90, new xc90, design, xc40, safety, car, new s60</td></tr><tr><td>2</td><td>237</td><td>2.12%</td><td>audi, tron, a7, a3, a8, audi tron, new, a6, electric, quattro</td></tr><tr><td>3</td><td>158</td><td>1.42%</td><td>polestar, electric, car, brand, electric car, volvo, performance, heart, customer, battery</td></tr><tr><td>4</td><td>53</td><td>0.47%</td><td>prius, toyota, hybrid, new, family, fuel, better, drive, wheel drive, fuel efficiency</td></tr></tbody>
</table>
</div>

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/b01-08-19-min-cluster/Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)-min_cluster_size.csv' | relative_url }}) | 參數掃描 CSV原始檔 |
| [主題摘要 CSV]({{ '/assets/results/b01-08-19-min-cluster/Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)-best_topic_info.csv' | relative_url }}) | 主題摘要 CSV原始檔 |
| [句子－主題對照 CSV]({{ '/assets/results/b01-08-19-min-cluster/Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)-best_document_topics.csv' | relative_url }}) | 句子－主題對照 CSV原始檔 |
| [run log JSON]({{ '/assets/results/b01-08-19-min-cluster/Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)-run_log.json' | relative_url }}) | run log JSON原始檔 |
| [實驗報告 Markdown]({{ '/assets/results/b01-08-19-min-cluster/Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80).md' | relative_url }}) | 實驗報告 Markdown原始檔 |
| [執行程式 Python]({{ '/assets/results/b01-08-19-min-cluster/run_06_13_Cmin_B01_orig_08_19_240_tok_para12_80.py' | relative_url }}) | 執行程式 Python原始檔 |

</section>
</div>
