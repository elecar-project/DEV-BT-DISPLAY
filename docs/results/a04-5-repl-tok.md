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
## 三種候選策略

最低雜訊、最多主題與最佳平衡代表不同的研究取捨；本頁保留三者，避免以單一 noise ratio 取代語意品質判讀。各策略的選擇方法列於表格最後一列。

<div class="table-scroll"><table class="candidate-table">
<thead><tr><th>策略</th><th>UMAP</th><th>HDBSCAN</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th></tr></thead>
<tbody><tr class="candidate-lowest_noise"><td>最低雜訊</td><td>n_neighbors 15 / components 5 / min dist 0.25</td><td>cluster 50 / samples 75.0 / eom / eps 0.0</td><td>2</td><td>0.00%</td><td>99.65%</td><td>0.3143903755197917</td></tr><tr class="candidate-most_topics"><td>最多主題</td><td>n_neighbors 5 / components 15 / min dist 0.0</td><td>cluster 50 / samples 5.0 / leaf / eps 0.0</td><td>181</td><td>42.00%</td><td>1.86%</td><td>0.861333841221471</td></tr><tr class="candidate-best_balance"><td>最佳平衡</td><td>n_neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.1</td><td>155</td><td>34.30%</td><td>2.61%</td><td>0.8759705424880171</td></tr></tbody>
<tfoot><tr><th>選擇方法</th><td colspan="6"><code>最低雜訊</code> 在有效結果中選取 noise ratio 最低的設定；若相同，優先較低的最大主題比例與較多主題。<code>最多主題</code> 在可接受的離群比例下，保留有效主題數最多的設定。<code>最佳平衡</code> 則在預設平衡條件下，選取 balance score 最高者；此分數同時考量離群比例、主題數與主題集中程度。</td></tr></tfoot>
</table></div>

## 圖表檢視

候選策略比較圖用來並列三種策略的主題數、noise ratio 與主題集中度；參數熱圖或選定設定比較圖則用來觀察不同 UMAP／HDBSCAN 組合對分群結果的影響。

<div class="result-figure-scroller"><figure><img src="{{ '/assets/results/a04-5-repl-tok/plots/06_selected_configs_comparison.png' | relative_url }}" alt="06_selected_configs_comparison"><figcaption>06 selected configs comparison</figcaption></figure></div>

## 原始輸出

可下載：[comparison_summary.csv]({{ '/assets/results/a04-5-repl-tok/comparison_summary.csv' | relative_url }})、[final_configs.json]({{ '/assets/results/a04-5-repl-tok/final_configs.json' | relative_url }})、[Result_06.03_A04-5(repl)_tok.md]({{ '/assets/results/a04-5-repl-tok/Result_06.03_A04-5(repl)_tok.md' | relative_url }})、[selected_configs_summary.csv]({{ '/assets/results/a04-5-repl-tok/selected_configs_summary.csv' | relative_url }})、[stability_top10_results.csv]({{ '/assets/results/a04-5-repl-tok/stability_top10_results.csv' | relative_url }})、[stability_top10_summary.csv]({{ '/assets/results/a04-5-repl-tok/stability_top10_summary.csv' | relative_url }})、[stage1_top10_umap_configs.csv]({{ '/assets/results/a04-5-repl-tok/stage1_top10_umap_configs.csv' | relative_url }})、[stage1_umap_hdbscan_results.csv]({{ '/assets/results/a04-5-repl-tok/stage1_umap_hdbscan_results.csv' | relative_url }})、[stage2_hdbscan_deep_results.csv]({{ '/assets/results/a04-5-repl-tok/stage2_hdbscan_deep_results.csv' | relative_url }})
</section>
</div>
