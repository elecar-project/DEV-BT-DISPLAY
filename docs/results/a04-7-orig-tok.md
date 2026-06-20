---
title: A04-7｜orig + tok UMAP 搜尋
description: A04-7｜orig + tok 的 UMAP 與 HDBSCAN 聯合參數搜尋。
---

# A04-7｜orig + tok｜UMAP 搜尋

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok_dataset</code></td></tr>
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
## 三種候選策略

最低雜訊、最多主題與最佳平衡代表不同的研究取捨；本頁保留三者，避免以單一 noise ratio 取代語意品質判讀。各策略的選擇方法列於表格最後一列。

<div class="table-scroll"><table class="candidate-table">
<thead><tr><th>策略</th><th>UMAP</th><th>HDBSCAN</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th></tr></thead>
<tbody><tr class="candidate-lowest_noise"><td>最低雜訊</td><td>n_neighbors 15 / components 5 / min dist 0.0</td><td>cluster 300 / samples 50.0 / eom / eps 0.0</td><td>2</td><td>0.84%</td><td>97.44%</td><td>0.3201833788121151</td></tr><tr class="candidate-most_topics"><td>最多主題</td><td>n_neighbors 5 / components 10 / min dist 0.0</td><td>cluster 50 / samples 5.0 / leaf / eps 0.0</td><td>183</td><td>39.43%</td><td>1.50%</td><td>0.8694006210206067</td></tr><tr class="candidate-best_balance"><td>最佳平衡</td><td>n_neighbors 5 / components 10 / min dist 0.0</td><td>cluster 50 / samples 10.0 / leaf / eps 0.2</td><td>130</td><td>31.36%</td><td>3.01%</td><td>0.8815293416554277</td></tr></tbody>
<tfoot><tr><th>選擇方法</th><td colspan="6"><code>最低雜訊</code> 在有效結果中選取 noise ratio 最低的設定；若相同，優先較低的最大主題比例與較多主題。<code>最多主題</code> 在可接受的離群比例下，保留有效主題數最多的設定。<code>最佳平衡</code> 則在預設平衡條件下，選取 balance score 最高者；此分數同時考量離群比例、主題數與主題集中程度。</td></tr></tfoot>
</table></div>

## 圖表檢視

候選策略比較圖用來並列三種策略的主題數、noise ratio 與主題集中度；參數熱圖或選定設定比較圖則用來觀察不同 UMAP／HDBSCAN 組合對分群結果的影響。

<div class="result-figure-scroller"><figure><img src="{{ '/assets/results/a04-7-orig-tok/charts/best_three_comparison.png' | relative_url }}" alt="best_three_comparison"><figcaption>best three comparison</figcaption></figure><figure><img src="{{ '/assets/results/a04-7-orig-tok/charts/best_three_topic_size_distribution.png' | relative_url }}" alt="best_three_topic_size_distribution"><figcaption>best three topic size distribution</figcaption></figure><figure><img src="{{ '/assets/results/a04-7-orig-tok/charts/parameter_heatmap.png' | relative_url }}" alt="parameter_heatmap"><figcaption>parameter heatmap</figcaption></figure></div>

## 原始輸出

可下載：[comparison_summary.csv]({{ '/assets/results/a04-7-orig-tok/comparison_summary.csv' | relative_url }})、[embeddings_all-MiniLM-L6-v2.meta.json]({{ '/assets/results/a04-7-orig-tok/embeddings_all-MiniLM-L6-v2.meta.json' | relative_url }})、[final_configs.json]({{ '/assets/results/a04-7-orig-tok/final_configs.json' | relative_url }})、[Result_06.03_A04-7(orig)_tok.md]({{ '/assets/results/a04-7-orig-tok/Result_06.03_A04-7(orig)_tok.md' | relative_url }})、[run_06.03_A04_7_orig_tok_umap_hdbscan.py]({{ '/assets/results/a04-7-orig-tok/run_06.03_A04_7_orig_tok_umap_hdbscan.py' | relative_url }})、[run_log.json]({{ '/assets/results/a04-7-orig-tok/run_log.json' | relative_url }})、[selected_configs.csv]({{ '/assets/results/a04-7-orig-tok/selected_configs.csv' | relative_url }})、[stability_results.csv]({{ '/assets/results/a04-7-orig-tok/stability_results.csv' | relative_url }})、[stage1_results.csv]({{ '/assets/results/a04-7-orig-tok/stage1_results.csv' | relative_url }})、[stage2_results.csv]({{ '/assets/results/a04-7-orig-tok/stage2_results.csv' | relative_url }})、[stage2_umap_candidates.json]({{ '/assets/results/a04-7-orig-tok/stage2_umap_candidates.json' | relative_url }})
</section>
</div>
