---
title: A03-3｜del + tok + 段落 12-80
description: A03-3｜del + tok + 段落 12-80 的 HDBSCAN min_cluster_size 敏感度分析。
experiment_id: a03-3-del-tok-para12-80
---

# A03-3｜del + tok + 段落 12-80

<div class="result-detail-layout" markdown="1">
{% include result-settings.html id=page.experiment_id %}

<section markdown="1">
<div class="run-summary">
  <div class="run-stat"><strong>21</strong><span>測試參數組數</span></div>
  <div class="run-stat"><strong>50</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>1.12%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>3</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗固定 embedding 與 UMAP 設定，只掃描 HDBSCAN 的 `min_cluster_size`。自動選擇規則為：先保留至少兩個非 noise 主題，再選取 noise ratio 最低的設定。

> **判讀提醒：** 自動選擇的 `min_cluster_size=50` 最大非 noise 主題占 97.62%。noise ratio 是重要指標，但仍應搭配代表詞、代表句與主題大小分布進行人工審查。

<div class="result-figure-scroller" aria-label="A03-3｜del + tok + 段落 12-80 圖表檢視">
  <figure><img src="{{ '/assets/results/a03-3-del-tok-para12-80/A03-3(del)_tok(para12-80)_min_cluster_chart.png' | relative_url }}" alt="A03-3｜del + tok + 段落 12-80 min cluster size 掃描圖"><figcaption>min_cluster_size 掃描圖</figcaption></figure>
</div>

## 參數掃描結果

<div class="table-scroll">
<table class="scan-table">
  <thead><tr><th>min cluster size</th><th>非 noise 主題數</th><th>noise ratio</th><th>離群句數</th><th>主題 0</th><th>主題 1</th><th>自動選擇</th></tr></thead>
  <tbody><tr class="selection-row"><td>50</td><td>3</td><td>1.12%</td><td>123</td><td>71</td><td>67</td><td><span class="scan-badge">自動選擇：最低雜訊</span></td></tr><tr><td>75</td><td>2</td><td>7.26%</td><td>795</td><td>91</td><td>10,059</td><td></td></tr><tr><td>100</td><td>10</td><td>43.21%</td><td>4,729</td><td>225</td><td>337</td><td></td></tr><tr><td>125</td><td>7</td><td>41.11%</td><td>4,499</td><td>163</td><td>333</td><td></td></tr><tr><td>150</td><td>6</td><td>37.59%</td><td>4,114</td><td>520</td><td>334</td><td></td></tr><tr><td>175</td><td>5</td><td>34.23%</td><td>3,746</td><td>1,391</td><td>4,451</td><td></td></tr><tr><td>200</td><td>5</td><td>35.45%</td><td>3,880</td><td>1,375</td><td>4,360</td><td></td></tr><tr><td>225</td><td>5</td><td>38.85%</td><td>4,252</td><td>1,340</td><td>4,172</td><td></td></tr><tr><td>250</td><td>4</td><td>37.83%</td><td>4,141</td><td>1,325</td><td>3,988</td><td></td></tr><tr><td>275</td><td>3</td><td>38.25%</td><td>4,186</td><td>1,324</td><td>1,499</td><td></td></tr><tr><td>300</td><td>3</td><td>40.57%</td><td>4,440</td><td>1,291</td><td>3,821</td><td></td></tr><tr><td>325</td><td>3</td><td>43.09%</td><td>4,716</td><td>1,177</td><td>1,303</td><td></td></tr><tr><td>350</td><td>3</td><td>46.59%</td><td>5,099</td><td>1,096</td><td>3,666</td><td></td></tr><tr><td>375</td><td>3</td><td>46.88%</td><td>5,131</td><td>1,060</td><td>3,675</td><td></td></tr><tr><td>400</td><td>3</td><td>45.94%</td><td>5,028</td><td>1,169</td><td>3,675</td><td></td></tr><tr><td>500</td><td>2</td><td>40.48%</td><td>4,431</td><td>1,030</td><td>5,484</td><td></td></tr><tr><td>600</td><td>2</td><td>41.22%</td><td>4,511</td><td>885</td><td>5,549</td><td></td></tr><tr><td>700</td><td>0</td><td>100.00%</td><td>10,945</td><td>0</td><td>0</td><td></td></tr><tr><td>800</td><td>0</td><td>100.00%</td><td>10,945</td><td>0</td><td>0</td><td></td></tr><tr><td>900</td><td>0</td><td>100.00%</td><td>10,945</td><td>0</td><td>0</td><td></td></tr><tr><td>1000</td><td>0</td><td>100.00%</td><td>10,945</td><td>0</td><td>0</td><td></td></tr></tbody>
</table>
</div>

## 自動選擇值的主題分布

<div class="table-scroll">
<table class="topic-table">
  <thead><tr><th>Topic</th><th>句數</th><th>比例</th><th>前十個代表詞</th></tr></thead>
  <tbody><tr><td>-1（noise）</td><td>123</td><td>1.12%</td><td>prime, mach, hybrid, ex90, plug, plug hybrid, saw, available, new, standard</td></tr><tr><td>0</td><td>10,684</td><td>97.62%</td><td>car, new, like, just, vehicle, really, electric, design, drive, driving</td></tr><tr><td>1</td><td>71</td><td>0.65%</td><td>warranty, 000, 000 mile, year, mile, whichever comes, whichever, 000 miles, hybrid, years</td></tr><tr><td>2</td><td>67</td><td>0.61%</td><td>candy, k23, electric, america, vehicles, ev, affordable, auto evolution, today, electric vehicles</td></tr></tbody>
</table>
</div>

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/a03-3-del-tok-para12-80/Result_06.03_A03-3(del)_tok(para12-80)-min_cluster_size.csv' | relative_url }}) | 參數掃描 CSV原始檔 |
| [主題摘要 CSV]({{ '/assets/results/a03-3-del-tok-para12-80/Result_06.03_A03-3(del)_tok(para12-80)-best_topic_info.csv' | relative_url }}) | 主題摘要 CSV原始檔 |
| [句子－主題對照 CSV]({{ '/assets/results/a03-3-del-tok-para12-80/Result_06.03_A03-3(del)_tok(para12-80)-best_document_topics.csv' | relative_url }}) | 句子－主題對照 CSV原始檔 |
| [run log JSON]({{ '/assets/results/a03-3-del-tok-para12-80/Result_06.03_A03-3(del)_tok(para12-80)-run_log.json' | relative_url }}) | run log JSON原始檔 |
| [實驗報告 Markdown]({{ '/assets/results/a03-3-del-tok-para12-80/Result_06.03_A03-3(del)_tok(para12-80).md' | relative_url }}) | 實驗報告 Markdown原始檔 |
| [執行程式 Python]({{ '/assets/results/a03-3-del-tok-para12-80/run_06.03_A03_3_del_tok_para12_80.py' | relative_url }}) | 執行程式 Python原始檔 |

</section>
</div>
