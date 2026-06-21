---
title: A04-2｜del + tok UMAP 搜尋
description: A04-2｜del + tok 的 UMAP 與 HDBSCAN 聯合參數搜尋。
---

# A04-2｜del + tok｜UMAP 搜尋

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(del)_tok_dataset</code></td></tr>
<tr><td>可用句子</td><td>-</td></tr>
<tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code></td></tr>
<tr><td>UMAP</td><td>cosine / random state 42</td></tr>
</tbody></table>

### 搜尋流程

<table class="settings-table"><thead><tr><th>階段</th><th>設定</th></tr></thead><tbody>
<tr><td>第一階段</td><td>2520 組廣泛搜尋</td></tr>
<tr><td>第二階段</td><td>13440 組候選深入搜尋</td></tr>
<tr><td>候選策略</td><td>最低雜訊 / 最多主題 / 最佳平衡</td></tr>
</tbody></table>
</aside>

<section markdown="1">
## UMAP 測試目的


本測試在固定語意向量模型後，同時探索 UMAP 降維與 HDBSCAN 分群設定，檢查目前資料版本能否比前一階段的 min_cluster_size 掃描取得更平衡的主題結構。UMAP 的 `n_neighbors` 調整局部與全域結構的取捨，`n_components` 決定降維後的維度數，`min_dist` 則控制群集在低維空間中的緊密程度；後續再搭配 HDBSCAN 的群集大小、保守程度與切分方式進行評估。

## UMAP 參數設定

### 共通設定

<table class="umap-config-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code>；每個資料集僅計算一次並快取</td></tr>
<tr><td>距離度量</td><td>UMAP：<code>cosine</code>；HDBSCAN：<code>euclidean</code></td></tr>
<tr><td>基準 random state</td><td><code>42</code></td></tr>
<tr><td>穩定性檢測</td><td>前 10 組候選使用 <code>42</code>、<code>123</code>、<code>2026</code>、<code>3407</code>、<code>20240603</code></td></tr>
</tbody></table>

### 第一階段：廣泛搜尋

<table class="umap-config-table"><thead><tr><th>模組</th><th>測試設定</th></tr></thead><tbody>
<tr><td>UMAP</td><td><code>n_neighbors</code>：5、10、15、30、50、75、100；<code>n_components</code>：5、10、15；<code>min_dist</code>：0.0、0.05、0.1、0.25</td></tr>
<tr><td>HDBSCAN</td><td><code>min_cluster_size</code>：50 至 300 的 10 組；<code>min_samples</code>：None、10、30；<code>method</code>：eom；<code>epsilon</code>：0.0</td></tr>
</tbody></table>

### 第二階段：候選深入搜尋

<table class="umap-config-table"><thead><tr><th>模組</th><th>測試設定</th></tr></thead><tbody>
<tr><td>UMAP</td><td>取第一階段前 10 組 UMAP 設定</td></tr>
<tr><td>HDBSCAN</td><td><code>min_cluster_size</code>：50 至 1000 的 21 組；<code>min_samples</code>：None、5、10、15、30、50、75、100；<code>method</code>：eom、leaf；<code>epsilon</code>：0.0、0.05、0.1、0.2</td></tr>
<tr><td>每組統計</td><td>UMAP／HDBSCAN 參數、主題數、noise ratio、離群筆數、最大主題比例、前三主題比例、entropy、balance score、狀態與備註</td></tr>
</tbody></table>

## 三種候選策略

最低雜訊、最多主題與最佳平衡代表不同的研究取捨；本頁保留三者，避免以單一 noise ratio 取代語意品質判讀。

<div class="table-scroll"><table class="candidate-table">
<thead><tr><th>策略</th><th>選擇方法</th><th>UMAP</th><th>HDBSCAN</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th></tr></thead>
<tbody><tr class="candidate-lowest_noise"><td>最低雜訊</td><td>有效結果中 noise ratio 最低；同分時優先較低最大主題比例與較多主題。</td><td>n_neighbors 15 / components 10 / min dist 0.0</td><td>cluster 100 / samples 30.0 / eom / eps 0.0</td><td>2</td><td>0.00%</td><td>99.68%</td><td>0.3142865010273029</td></tr><tr class="candidate-most_topics"><td>最多主題</td><td>在可接受離群比例下，保留有效主題數最多者。</td><td>n_neighbors 5 / components 15 / min dist 0.0</td><td>cluster 50 / samples 5.0 / leaf / eps 0.0</td><td>166</td><td>41.88%</td><td>1.26%</td><td>0.8641767808349747</td></tr><tr class="candidate-best_balance"><td>最佳平衡</td><td>在預設平衡條件下選取最高分：n_clusters ≥ 4、noise ≤ 0.35、最大主題比例 ≤ 0.65、前三主題比例 ≤ 0.85。<br>balance score = 0.30 × (1 − noise ratio) + 0.30 × (1 − 最大主題比例) + 0.20 × (1 − 前三主題比例) + 0.20 × min(主題數 / 25, 1)。</td><td>n_neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.0</td><td>148</td><td>34.16%</td><td>2.76%</td><td>0.8762121115841646</td></tr></tbody>
</table></div>

## 圖表檢視

候選策略比較圖用來並列三種策略的主題數、noise ratio 與主題集中度；參數熱圖或選定設定比較圖則用來觀察不同 UMAP／HDBSCAN 組合對分群結果的影響。

<div class="result-figure-scroller"><figure><img src="{{ '/assets/results/a04-2-del-tok/charts/best_three_comparison.png' | relative_url }}" alt="best_three_comparison"><figcaption>best three comparison</figcaption></figure><figure><img src="{{ '/assets/results/a04-2-del-tok/charts/parameter_heatmap.png' | relative_url }}" alt="parameter_heatmap"><figcaption>parameter heatmap</figcaption></figure></div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a04-2-del-tok/embeddings_all-MiniLM-L6-v2.meta.json' | relative_url }}">embeddings_all-MiniLM-L6-v2.meta.json</a></td><td>設定或中間候選資料</td></tr><tr><td><a href="{{ '/assets/results/a04-2-del-tok/Result_06.03_A04-2(del)_tok.md' | relative_url }}">Result_06.03_A04-2(del)_tok.md</a></td><td>原始實驗報告</td></tr><tr><td><a href="{{ '/assets/results/a04-2-del-tok/run_06.03_A04_2_del_tok_umap_hdbscan.py' | relative_url }}">run_06.03_A04_2_del_tok_umap_hdbscan.py</a></td><td>本次 UMAP + HDBSCAN 實驗的執行程式</td></tr><tr><td><a href="{{ '/assets/results/a04-2-del-tok/run_log.json' | relative_url }}">run_log.json</a></td><td>執行紀錄與資料統計</td></tr><tr><td><a href="{{ '/assets/results/a04-2-del-tok/selected_configs.csv' | relative_url }}">selected_configs.csv</a></td><td>三種候選策略的選定參數與指標</td></tr><tr><td><a href="{{ '/assets/results/a04-2-del-tok/stability_results.csv' | relative_url }}">stability_results.csv</a></td><td>前段候選在不同 random state 下的穩定性結果</td></tr><tr><td><a href="{{ '/assets/results/a04-2-del-tok/stage1_results.csv' | relative_url }}">stage1_results.csv</a></td><td>第一階段 UMAP 與精簡 HDBSCAN 的廣泛搜尋結果</td></tr><tr><td><a href="{{ '/assets/results/a04-2-del-tok/stage2_results.csv' | relative_url }}">stage2_results.csv</a></td><td>第二階段候選 UMAP 的深入 HDBSCAN 搜尋結果</td></tr><tr><td><a href="{{ '/assets/results/a04-2-del-tok/stage2_umap_candidates.json' | relative_url }}">stage2_umap_candidates.json</a></td><td>第二階段候選 UMAP 的深入 HDBSCAN 搜尋結果</td></tr></tbody></table>
</section>
</div>
