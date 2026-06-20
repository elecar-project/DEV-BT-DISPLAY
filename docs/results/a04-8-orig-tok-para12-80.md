---
title: A04-8｜orig + tok + 段落 12-80 UMAP 搜尋
description: A04-8｜orig + tok + 段落 12-80 的 UMAP 與 HDBSCAN 聯合參數搜尋。
---

# A04-8｜orig + tok + 段落 12-80｜UMAP 搜尋

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset</code></td></tr>
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

最低雜訊、最多主題與最佳平衡代表不同的研究取捨；本頁保留三者，避免以單一 noise ratio 取代語意品質判讀。

<div class="table-scroll"><table class="candidate-table">
<thead><tr><th>策略</th><th>UMAP</th><th>HDBSCAN</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th></tr></thead>
<tbody><tr class="candidate-lowest_noise"><td>最低雜訊</td><td>n_neighbors 15 / components 10 / min dist 0.05</td><td>cluster 225 / samples 5.0 / eom / eps 0.0</td><td>2</td><td>0.55%</td><td>97.01%</td><td>0.324423132183908</td></tr><tr class="candidate-most_topics"><td>最多主題</td><td>n_neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / leaf / eps 0.0</td><td>73</td><td>33.37%</td><td>2.86%</td><td>0.8780711206896552</td></tr><tr class="candidate-best_balance"><td>最佳平衡</td><td>n_neighbors 5 / components 5 / min dist 0.0</td><td>cluster 50 / samples 5.0 / eom / eps 0.2</td><td>62</td><td>27.68%</td><td>4.07%</td><td>0.8835308908045976</td></tr></tbody></table></div>

## 圖表檢視

<div class="result-figure-scroller"><figure><img src="{{ '/assets/results/a04-8-orig-tok-para12-80/charts/best_three_comparison.png' | relative_url }}" alt="best_three_comparison"><figcaption>best three comparison</figcaption></figure><figure><img src="{{ '/assets/results/a04-8-orig-tok-para12-80/charts/parameter_heatmap.png' | relative_url }}" alt="parameter_heatmap"><figcaption>parameter heatmap</figcaption></figure></div>

## 原始輸出

可下載：[brand_model_topic_word_check.csv]({{ '/assets/results/a04-8-orig-tok-para12-80/brand_model_topic_word_check.csv' | relative_url }})、[comparison_summary.csv]({{ '/assets/results/a04-8-orig-tok-para12-80/comparison_summary.csv' | relative_url }})、[embeddings_all-MiniLM-L6-v2.meta.json]({{ '/assets/results/a04-8-orig-tok-para12-80/embeddings_all-MiniLM-L6-v2.meta.json' | relative_url }})、[final_configs.json]({{ '/assets/results/a04-8-orig-tok-para12-80/final_configs.json' | relative_url }})、[Result_06.03_A04-8(orig)_tok(para12-80).md]({{ '/assets/results/a04-8-orig-tok-para12-80/Result_06.03_A04-8(orig)_tok(para12-80).md' | relative_url }})、[run_06.03_A04_8_orig_tok_para12_80_umap_hdbscan.py]({{ '/assets/results/a04-8-orig-tok-para12-80/run_06.03_A04_8_orig_tok_para12_80_umap_hdbscan.py' | relative_url }})、[run_log.json]({{ '/assets/results/a04-8-orig-tok-para12-80/run_log.json' | relative_url }})、[selected_configs.csv]({{ '/assets/results/a04-8-orig-tok-para12-80/selected_configs.csv' | relative_url }})、[stability_results.csv]({{ '/assets/results/a04-8-orig-tok-para12-80/stability_results.csv' | relative_url }})、[stage1_results.csv]({{ '/assets/results/a04-8-orig-tok-para12-80/stage1_results.csv' | relative_url }})、[stage2_results.csv]({{ '/assets/results/a04-8-orig-tok-para12-80/stage2_results.csv' | relative_url }})、[stage2_umap_candidates.json]({{ '/assets/results/a04-8-orig-tok-para12-80/stage2_umap_candidates.json' | relative_url }})
</section>
</div>
