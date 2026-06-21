---
title: A04-5｜repl + tok UMAP 搜尋
description: A04-5｜repl + tok 的 UMAP 與 HDBSCAN 聯合參數搜尋。
---

# A04-5｜repl + tok｜UMAP 搜尋

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>-</code></td></tr>
<tr><td>可用句子</td><td>-</td></tr>
<tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code></td></tr>
<tr><td>UMAP</td><td>cosine / random state 42</td></tr>
</tbody></table>

### 搜尋流程

<table class="settings-table"><thead><tr><th>階段</th><th>設定</th></tr></thead><tbody>
<tr><td>第一階段</td><td>10 組廣泛搜尋</td></tr>
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
<tbody><tr class="candidate-lowest_noise"><td>最低雜訊</td><td>有效結果中 noise ratio 最低；同分時優先較低最大主題比例與較多主題。</td><td>n_neighbors 15 / components 5 / min dist 0.25</td><td>cluster 50 / samples 75.0 / eom / eps 0.0</td><td>2</td><td>0.00%</td><td>99.65%</td><td>0.3143903755197917</td></tr><tr class="candidate-most_topics"><td>最多主題</td><td>在可接受離群比例下，保留有效主題數最多者。</td><td>n_neighbors 5 / components 15 / min dist 0.0</td><td>cluster 50 / samples 5.0 / leaf / eps 0.0</td><td>181</td><td>42.00%</td><td>1.86%</td><td>0.861333841221471</td></tr><tr class="candidate-best_balance"><td>最佳平衡</td><td>在預設平衡條件下，選取 balance score 最高者。</td><td>n_neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.1</td><td>155</td><td>34.30%</td><td>2.61%</td><td>0.8759705424880171</td></tr></tbody>
</table></div>
<aside class="table-note"><strong>註記｜最佳平衡的判定：</strong>先篩選 <code>n_clusters ≥ 4</code>、<code>noise ratio ≤ 0.35</code>、<code>最大主題比例 ≤ 0.65</code>、<code>前三主題比例 ≤ 0.85</code> 的組合；再以 <code>balance score = 0.30 × (1 − noise ratio) + 0.30 × (1 − 最大主題比例) + 0.20 × (1 − 前三主題比例) + 0.20 × min(主題數 / 25, 1)</code> 選取最高分。</aside>

## 穩定性檢測

<div class="stability-summary">
<div><span>測試 seed</span><strong>5</strong></div>
<div><span>主題數範圍</span><strong>139–155</strong></div>
<div><span>noise ratio 範圍</span><strong>32.05%–36.96%</strong></div>
<div><span>balance score 範圍</span><strong>0.863–0.876</strong></div>
</div>
<p class="stability-note">以最佳平衡參數在不同 random state 下重跑；範圍用於檢視分群結果對初始化的敏感程度。</p>

## 最佳平衡的主題語意摘要

<p class="section-intro">以下為最佳平衡結果的前 8 個有效主題；每列保留前 10 個代表詞與第一則代表句，供快速判讀語意品質。</p>
<div class="table-scroll"><table class="semantic-table"><thead><tr><th>主題</th><th>代表詞（前 10）</th><th>代表句</th></tr></thead><tbody><tr><td>0</td><td>model, brand model, new model, model model, allnew, allnew model, new, model new, brand, model brand</td><td>This is what the Brand Model is all about.</td></tr><tr><td>1</td><td>charging, charge, stations, charger, dc, charging stations, station, level, fast, hours</td><td>For Brand Model vehicles equipped with the DC fast charging SAE option, a DC public charging station will charge the Brand Model to an 80% state of charge in 20 to 30 minutes depending on the charging station.</td></tr><tr><td>2</td><td>brand, brand brand, year, products, company, brand thats, product, year brand, global, brand stands</td><td>Brand.</td></tr><tr><td>3</td><td>electric, electric car, electrification, electric vehicle, electrified, electric cars, electric vehicles, vehicles, allelectric, electrified vehicles</td><td>Now, what is the heart of an electric car?</td></tr><tr><td>4</td><td>cool, amazing, thats, awesome, oh, doing, sounds, good, pretty, great</td><td>Oh, cool.</td></tr><tr><td>5</td><td>horsepower, engine, torque, poundfeet, v6, turbo, liter, fourcylinder, poundfeet torque, engines</td><td>This starts with its two modern powertrains, a 203-horsepower, 2.5-liter, 4-cylinder engine on gas grades, and the available Brand Hybrid system with 219 net combined horsepower on hybrid grades.</td></tr><tr><td>6</td><td>hi, thank, hello, welcome, hey, andy, im, tom, alex, gian</td><td>Hi, Ede.</td></tr><tr><td>7</td><td>question, questions, answer, talk, little bit, bit, tell, say, question question, little</td><td>First question.</td></tr></tbody></table></div>



## 圖表檢視

候選策略比較圖用來並列三種策略的主題數、noise ratio 與主題集中度；參數熱圖或選定設定比較圖則用來觀察不同 UMAP／HDBSCAN 組合對分群結果的影響。

<div class="result-figure-scroller"><figure><img src="{{ '/assets/results/a04-5-repl-tok/plots/06_selected_configs_comparison.png' | relative_url }}" alt="06 selected configs comparison"><figcaption>06 selected configs comparison</figcaption></figure></div>

<details class="result-chart-details">
<summary>完整參數圖表（5 張）</summary>
<p>用於追查各 UMAP／HDBSCAN 參數與主題數、離群比例、主題集中度之間的關係。</p>
<div class="result-figure-scroller"><figure><img src="{{ '/assets/results/a04-5-repl-tok/plots/01_min_cluster_size_dual_axis.png' | relative_url }}" alt="01 min cluster size dual axis"><figcaption>01 min cluster size dual axis</figcaption></figure><figure><img src="{{ '/assets/results/a04-5-repl-tok/plots/02_min_samples_noise_ratio.png' | relative_url }}" alt="02 min samples noise ratio"><figcaption>02 min samples noise ratio</figcaption></figure><figure><img src="{{ '/assets/results/a04-5-repl-tok/plots/03_n_neighbors_largest_topic_ratio.png' | relative_url }}" alt="03 n neighbors largest topic ratio"><figcaption>03 n neighbors largest topic ratio</figcaption></figure><figure><img src="{{ '/assets/results/a04-5-repl-tok/plots/04_n_components_n_clusters.png' | relative_url }}" alt="04 n components n clusters"><figcaption>04 n components n clusters</figcaption></figure><figure><img src="{{ '/assets/results/a04-5-repl-tok/plots/05_cluster_selection_method_comparison.png' | relative_url }}" alt="05 cluster selection method comparison"><figcaption>05 cluster selection method comparison</figcaption></figure></div>
</details>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a04-5-repl-tok/comparison_summary.csv' | relative_url }}">comparison_summary.csv</a></td><td>三種候選策略的最終比較摘要</td></tr><tr><td><a href="{{ '/assets/results/a04-5-repl-tok/final_configs.json' | relative_url }}">final_configs.json</a></td><td>最終 BERTopic 訓練的設定檔</td></tr><tr><td><a href="{{ '/assets/results/a04-5-repl-tok/Result_06.03_A04-5(repl)_tok.md' | relative_url }}">Result_06.03_A04-5(repl)_tok.md</a></td><td>原始實驗報告</td></tr><tr><td><a href="{{ '/assets/results/a04-5-repl-tok/selected_configs_summary.csv' | relative_url }}">selected_configs_summary.csv</a></td><td>三種候選策略的選定參數與指標</td></tr><tr><td><a href="{{ '/assets/results/a04-5-repl-tok/stability_top10_results.csv' | relative_url }}">stability_top10_results.csv</a></td><td>前段候選在不同 random state 下的穩定性結果</td></tr><tr><td><a href="{{ '/assets/results/a04-5-repl-tok/stability_top10_summary.csv' | relative_url }}">stability_top10_summary.csv</a></td><td>前段候選在不同 random state 下的穩定性結果</td></tr><tr><td><a href="{{ '/assets/results/a04-5-repl-tok/stage1_top10_umap_configs.csv' | relative_url }}">stage1_top10_umap_configs.csv</a></td><td>第一階段 UMAP 與精簡 HDBSCAN 的廣泛搜尋結果</td></tr><tr><td><a href="{{ '/assets/results/a04-5-repl-tok/stage1_umap_hdbscan_results.csv' | relative_url }}">stage1_umap_hdbscan_results.csv</a></td><td>第一階段 UMAP 與精簡 HDBSCAN 的廣泛搜尋結果</td></tr><tr><td><a href="{{ '/assets/results/a04-5-repl-tok/stage2_hdbscan_deep_results.csv' | relative_url }}">stage2_hdbscan_deep_results.csv</a></td><td>第二階段候選 UMAP 的深入 HDBSCAN 搜尋結果</td></tr></tbody></table>
</section>
</div>
