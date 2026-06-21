---
title: A04-6｜repl + tok + 段落 12-80 UMAP 搜尋
description: A04-6｜repl + tok + 段落 12-80 的 UMAP 與 HDBSCAN 聯合參數搜尋。
---

# A04-6｜repl + tok + 段落 12-80｜UMAP 搜尋

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok(para12-80)_dataset</code></td></tr>
<tr><td>來源資料夾</td><td><code>#運行BERTopic整理/#4. UMAP（未整理）/A04-6(repl)_tok(para12-80)</code></td></tr>
<tr><td>可用句子</td><td>10978</td></tr>
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
<tbody><tr class="candidate-lowest_noise"><td>最低雜訊</td><td>有效結果中 noise ratio 最低；同分時優先較低最大主題比例與較多主題。</td><td>n_neighbors 75 / components 10 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.0</td><td>2</td><td>0.00%</td><td>99.43%</td><td>0.2680085625797049</td></tr><tr class="candidate-most_topics"><td>最多主題</td><td>在可接受離群比例下，保留有效主題數最多者。</td><td>n_neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / leaf / eps 0.0</td><td>57</td><td>44.27%</td><td>2.51%</td><td>0.8661140462743668</td></tr><tr class="candidate-best_balance"><td>最佳平衡</td><td>在預設平衡條件下，選取 balance score 最高者。</td><td>n_neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.2</td><td>40</td><td>28.38%</td><td>6.29%</td><td>0.8723902350154855</td></tr></tbody>
</table></div>
<aside class="table-note"><strong>註記｜最佳平衡的判定：</strong>先篩選 <code>n_clusters ≥ 4</code>、<code>noise ratio ≤ 0.35</code>、<code>最大主題比例 ≤ 0.65</code>、<code>前三主題比例 ≤ 0.85</code> 的組合；再以 <code>balance score = 0.30 × (1 − noise ratio) + 0.30 × (1 − 最大主題比例) + 0.20 × (1 − 前三主題比例) + 0.20 × min(主題數 / 25, 1)</code> 選取最高分。</aside>

## 穩定性檢測

<div class="stability-summary">
<div><span>測試 seed</span><strong>5</strong></div>
<div><span>主題數範圍</span><strong>37–43</strong></div>
<div><span>noise ratio 範圍</span><strong>27.59%–29.82%</strong></div>
<div><span>balance score 範圍</span><strong>0.852–0.875</strong></div>
</div>
<p class="stability-note">以最佳平衡參數在不同 random state 下重跑；範圍用於檢視分群結果對初始化的敏感程度。</p>

## 最佳平衡的主題語意摘要

<p class="section-intro">以下為最佳平衡結果的前 8 個有效主題；每列保留前 10 個代表詞與第一則代表句，供快速判讀語意品質。</p>
<div class="table-scroll"><table class="semantic-table"><thead><tr><th>主題</th><th>代表詞（前 10）</th><th>代表句</th></tr></thead><tbody><tr><td>0</td><td>seats, interior, seat, space, leather, rear, heated, inside, cargo, model</td><td>Model continues to strike the perfect balance between convenience and comfort for 2023, which can be seen in features like its available dual-zone climate control system, available heated and ventilated front seats, a...</td></tr><tr><td>1</td><td>brand, new, brand brand, market, year, customers, product, cars, welcome, sales</td><td>Those who got in early, like us, have benefited more than others. Brand, Brand, Brand, Brand and Brand are other brands with greater sales in China than here in the US. As we do in the US, we sell regional products fo...</td></tr><tr><td>2</td><td>assist, safety, lane, spot, alert, parking, blind, collision, blind spot, traffic</td><td>To that end, the latest Brand Safety Sense 3.0 Suite offers great peace of mind and confidence through features like a Pre-Collision System, Lane Departure Alert, Automatic High Beams, Full-Speed Range Dynamic Radar C...</td></tr><tr><td>3</td><td>grille, rear, led, light, design, headlights, look, car, lights, new</td><td>Elements like that elongated, wide, sporty front grille, that elegant swooping hood, and those stunning full LED headlights that include daytime running lights that I love. This seamlessly integrates into the main veh...</td></tr><tr><td>4</td><td>electric, ev, brand, vehicles, electric car, model, electrification, electric vehicle, new, electrified</td><td>We also know the transition to EV will be swift, as more people fully realize the benefits of an EV lifestyle. Let me be clear, electric vehicles are very good. And Brand &#x27;s electric vehicles are very, very good.</td></tr><tr><td>5</td><td>drive, don, know, right, let, yeah, going, don know, want, car</td><td>It produces the typical smooth and superior driving feeling that this car is known for. Let me just enjoy this, because you don&#x27;t get to do this every day, right? Okay, I didn&#x27;t just shut my mouth for a while because...</td></tr><tr><td>6</td><td>thank, good, today, bye, joining, doing, thanks, hope, welcome, great</td><td>Thank you.</td></tr><tr><td>7</td><td>charging, charge, stations, level, charging stations, home, plug, station, cable, public</td><td>There are several ways to charge your Brand Model &#x27;s high voltage battery, giving you a variety of convenient home and public charging options. Level 2 charging from a Level 2 home or public charging station, Level 1...</td></tr></tbody></table></div>



## 圖表檢視

候選策略比較圖用來並列三種策略的主題數、noise ratio 與主題集中度；參數熱圖或選定設定比較圖則用來觀察不同 UMAP／HDBSCAN 組合對分群結果的影響。

<div class="result-figure-scroller"><figure><img src="{{ '/assets/results/a04-6-repl-tok-para12-80/charts/best_three_comparison.png' | relative_url }}" alt="三種候選策略比較"><figcaption>三種候選策略比較</figcaption></figure><figure><img src="{{ '/assets/results/a04-6-repl-tok-para12-80/charts/best_three_topic_size_distribution.png' | relative_url }}" alt="best three topic size distribution"><figcaption>best three topic size distribution</figcaption></figure><figure><img src="{{ '/assets/results/a04-6-repl-tok-para12-80/charts/parameter_heatmap.png' | relative_url }}" alt="參數組合熱圖"><figcaption>參數組合熱圖</figcaption></figure></div>

<details class="result-chart-details">
<summary>完整參數圖表（6 張）</summary>
<p>用於追查各 UMAP／HDBSCAN 參數與主題數、離群比例、主題集中度之間的關係。</p>
<div class="result-figure-scroller"><figure><img src="{{ '/assets/results/a04-6-repl-tok-para12-80/charts/best_balance_topic_size_bar.png' | relative_url }}" alt="最佳平衡的主題規模分布"><figcaption>最佳平衡的主題規模分布</figcaption></figure><figure><img src="{{ '/assets/results/a04-6-repl-tok-para12-80/charts/largest_topic_ratio_parameter_comparison.png' | relative_url }}" alt="largest topic ratio parameter comparison"><figcaption>largest topic ratio parameter comparison</figcaption></figure><figure><img src="{{ '/assets/results/a04-6-repl-tok-para12-80/charts/min_cluster_size_dual_axis.png' | relative_url }}" alt="min_cluster_size 與主題數／noise ratio"><figcaption>min_cluster_size 與主題數／noise ratio</figcaption></figure><figure><img src="{{ '/assets/results/a04-6-repl-tok-para12-80/charts/min_samples_noise_ratio.png' | relative_url }}" alt="min_samples 與 noise ratio"><figcaption>min_samples 與 noise ratio</figcaption></figure><figure><img src="{{ '/assets/results/a04-6-repl-tok-para12-80/charts/n_components_n_clusters.png' | relative_url }}" alt="n_components 與主題數"><figcaption>n_components 與主題數</figcaption></figure><figure><img src="{{ '/assets/results/a04-6-repl-tok-para12-80/charts/n_neighbors_largest_topic_ratio.png' | relative_url }}" alt="n_neighbors 與最大主題比例"><figcaption>n_neighbors 與最大主題比例</figcaption></figure></div>
</details>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/comparison_summary.csv' | relative_url }}">comparison_summary.csv</a></td><td>三種候選策略的最終比較摘要</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/embeddings_all-MiniLM-L6-v2.meta.json' | relative_url }}">embeddings_all-MiniLM-L6-v2.meta.json</a></td><td>設定或中間候選資料</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/final_configs.json' | relative_url }}">final_configs.json</a></td><td>最終 BERTopic 訓練的設定檔</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/representative_docs.csv' | relative_url }}">representative_docs.csv</a></td><td>代表句輸出</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/Result_06.03_A04-6(repl)_tok(para12-80)-all_results.csv' | relative_url }}">Result_06.03_A04-6(repl)_tok(para12-80)-all_results.csv</a></td><td>實驗輸出資料</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/Result_06.03_A04-6(repl)_tok(para12-80)-stage1_umap_hdbscan.csv' | relative_url }}">Result_06.03_A04-6(repl)_tok(para12-80)-stage1_umap_hdbscan.csv</a></td><td>第一階段 UMAP 與精簡 HDBSCAN 的廣泛搜尋結果</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/Result_06.03_A04-6(repl)_tok(para12-80)-stage2_hdbscan_deep.csv' | relative_url }}">Result_06.03_A04-6(repl)_tok(para12-80)-stage2_hdbscan_deep.csv</a></td><td>第二階段候選 UMAP 的深入 HDBSCAN 搜尋結果</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/Result_06.03_A04-6(repl)_tok(para12-80)-top10_stability.csv' | relative_url }}">Result_06.03_A04-6(repl)_tok(para12-80)-top10_stability.csv</a></td><td>前段候選在不同 random state 下的穩定性結果</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/Result_06.03_A04-6(repl)_tok(para12-80).md' | relative_url }}">Result_06.03_A04-6(repl)_tok(para12-80).md</a></td><td>原始實驗報告</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/run_06.03_A04_6_repl_tok_para12_80.py' | relative_url }}">run_06.03_A04_6_repl_tok_para12_80.py</a></td><td>本次 UMAP + HDBSCAN 實驗的執行程式</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/run_log.json' | relative_url }}">run_log.json</a></td><td>執行紀錄與資料統計</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/selected_configs.csv' | relative_url }}">selected_configs.csv</a></td><td>三種候選策略的選定參數與指標</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/stage2_umap_candidates.json' | relative_url }}">stage2_umap_candidates.json</a></td><td>第二階段候選 UMAP 的深入 HDBSCAN 搜尋結果</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/topic_info.csv' | relative_url }}">topic_info.csv</a></td><td>最終主題資訊摘要</td></tr><tr><td><a href="{{ '/assets/results/a04-6-repl-tok-para12-80/topic_words.csv' | relative_url }}">topic_words.csv</a></td><td>主題關鍵詞輸出</td></tr></tbody></table>
</section>
</div>
