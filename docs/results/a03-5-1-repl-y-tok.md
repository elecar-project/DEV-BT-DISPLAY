---
title: A03-5.1｜repl-y + tok
description: A03-5.1｜repl-y + tok 的 HDBSCAN min_cluster_size 敏感度分析。
experiment_id: a03-5-1-repl-y-tok
---

# A03-5.1｜repl-y + tok

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
<div class="run-summary">
  <div class="run-stat"><strong>21</strong><span>測試參數組數</span></div>
  <div class="run-stat"><strong>100</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>0.70%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>4</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗固定 embedding 與 UMAP 設定，只掃描 HDBSCAN 的 `min_cluster_size`。自動選擇規則為：先保留至少兩個非 noise 主題，再選取 noise ratio 最低的設定。

> **判讀提醒：** 自動選擇的 `min_cluster_size=100` 最大非 noise 主題占 98.19%。noise ratio 是重要指標，但仍應搭配代表詞、代表句與主題大小分布進行人工審查。

<div class="result-figure-scroller" aria-label="A03-5.1｜repl-y + tok 圖表檢視">
  <figure><img src="{{ '/assets/results/a03-5-1-repl-y-tok/A03-5.1(repl-y)_tok_min_cluster_chart.png' | relative_url }}" alt="A03-5.1｜repl-y + tok min cluster size 掃描圖"><figcaption>min_cluster_size 掃描圖</figcaption></figure>
</div>

## 參數掃描結果

<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>自動選擇</th></tr></thead>
  <tbody><tr><td>50</td><td>79</td><td>51.64%</td><td>16,269</td><td>1,493</td><td>848</td><td></td></tr><tr><td>75</td><td>47</td><td>48.75%</td><td>15,357</td><td>1,643</td><td>1,637</td><td></td></tr><tr class="selection-row"><td>100</td><td>4</td><td>0.70%</td><td>219</td><td>30,934</td><td>136</td><td><span class="scan-badge">自動選擇：最低雜訊</span></td></tr><tr><td>125</td><td>2</td><td>1.47%</td><td>463</td><td>30,904</td><td>136</td><td></td></tr><tr><td>150</td><td>20</td><td>45.13%</td><td>14,218</td><td>3,390</td><td>2,969</td><td></td></tr><tr><td>175</td><td>14</td><td>44.94%</td><td>14,156</td><td>4,367</td><td>3,007</td><td></td></tr><tr><td>200</td><td>13</td><td>42.97%</td><td>13,537</td><td>4,340</td><td>3,265</td><td></td></tr><tr><td>225</td><td>11</td><td>45.49%</td><td>14,332</td><td>4,290</td><td>3,330</td><td></td></tr><tr><td>250</td><td>10</td><td>47.23%</td><td>14,880</td><td>4,408</td><td>3,079</td><td></td></tr><tr><td>275</td><td>10</td><td>48.63%</td><td>15,320</td><td>4,400</td><td>3,064</td><td></td></tr><tr><td>300</td><td>9</td><td>45.48%</td><td>14,328</td><td>4,391</td><td>3,033</td><td></td></tr><tr><td>325</td><td>2</td><td>17.90%</td><td>5,639</td><td>21,463</td><td>4,401</td><td></td></tr><tr><td>350</td><td>2</td><td>18.79%</td><td>5,920</td><td>21,260</td><td>4,323</td><td></td></tr><tr><td>375</td><td>2</td><td>21.80%</td><td>6,868</td><td>20,398</td><td>4,237</td><td></td></tr><tr><td>400</td><td>2</td><td>22.06%</td><td>6,948</td><td>20,301</td><td>4,254</td><td></td></tr><tr><td>500</td><td>2</td><td>22.37%</td><td>7,048</td><td>20,316</td><td>4,139</td><td></td></tr><tr><td>600</td><td>3</td><td>27.12%</td><td>8,545</td><td>19,844</td><td>2,333</td><td></td></tr><tr><td>700</td><td>2</td><td>23.02%</td><td>7,253</td><td>20,172</td><td>4,078</td><td></td></tr><tr><td>800</td><td>2</td><td>25.99%</td><td>8,189</td><td>19,395</td><td>3,919</td><td></td></tr><tr><td>900</td><td>2</td><td>30.82%</td><td>9,709</td><td>18,330</td><td>3,464</td><td></td></tr><tr><td>1000</td><td>2</td><td>28.74%</td><td>9,055</td><td>19,211</td><td>3,237</td><td></td></tr></tbody>
</table>
</div>

## 自動選擇值的主題分布

<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody><tr><td>-1（noise）</td><td>219</td><td>0.70%</td><td>crown, thank, google, thank thank, android, music, addition wireless, google maps, easy stay, compatibility makes</td></tr><tr><td>0</td><td>30,934</td><td>98.19%</td><td>car, new, like, just, vehicle, really, electric, design, drive, driving</td></tr><tr><td>1</td><td>136</td><td>0.43%</td><td>warranty, 000, mile, year, whichever, whichever comes, maintenance, 000 miles, 100 000, years</td></tr><tr><td>2</td><td>111</td><td>0.35%</td><td>thank thank, thank, thank thanks, thanks thank, thanks, irv, thanks thanks, , , </td></tr><tr><td>3</td><td>103</td><td>0.33%</td><td>absolutely, yeah, absolutely absolutely, yeah yeah, absolutely yeah, yeah absolutely, yep, huh, , </td></tr></tbody>
</table>
</div>

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/a03-5-1-repl-y-tok/Result_06.03_A03-5.1(repl-y)_tok-min_cluster_size.csv' | relative_url }}) | 參數掃描 CSV原始檔 |
| [主題摘要 CSV]({{ '/assets/results/a03-5-1-repl-y-tok/Result_06.03_A03-5.1(repl-y)_tok-best_topic_info.csv' | relative_url }}) | 主題摘要 CSV原始檔 |
| [句子－主題對照 CSV]({{ '/assets/results/a03-5-1-repl-y-tok/Result_06.03_A03-5.1(repl-y)_tok-best_document_topics.csv' | relative_url }}) | 句子－主題對照 CSV原始檔 |
| [run log JSON]({{ '/assets/results/a03-5-1-repl-y-tok/Result_06.03_A03-5.1(repl-y)_tok-run_log.json' | relative_url }}) | run log JSON原始檔 |
| [實驗報告 Markdown]({{ '/assets/results/a03-5-1-repl-y-tok/Result_06.03_A03-5.1(repl-y)_tok.md' | relative_url }}) | 實驗報告 Markdown原始檔 |
| [執行程式 Python]({{ '/assets/results/a03-5-1-repl-y-tok/run_06.03_A03_5_1_repl_y_tok.py' | relative_url }}) | 執行程式 Python原始檔 |

</section>
</div>
