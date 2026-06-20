# BERTopic UMAP + HDBSCAN 多參數檢測報告 - 06.03_A04-8(orig)_tok(para12-80)

## 1. Dataset 資訊

| dataset_dir | columns | text_col | title_col | source_rows | used_rows | empty_rows_count | short_rows_lt_3_words_count | min_text_len | max_text_len | avg_text_len | min_word_count | max_word_count | avg_word_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset | ['title', 'source_row', 'paragraph_id', 'sentence_start_id', 'sentence_end_id', 'sentence_count', 'sentence', 'word_count', 'char_count'] | sentence | title | 11136 | 11136 | 0 | 14 | 4 | 2044 | 249.1193 | 1 | 389 | 43.4003 |

## 2. Embedding / UMAP / HDBSCAN 參數設定

- embedding_model: `all-MiniLM-L6-v2`
- embeddings cache: `embeddings_all-MiniLM-L6-v2.npy`
- UMAP 第一階段: n_neighbors=[5, 10, 15, 30, 50, 75, 100], n_components=[5, 10, 15], min_dist=[0.0, 0.05, 0.1, 0.25], metric=cosine, random_state=42
- HDBSCAN 第一階段: min_cluster_size=[50, 75, 100, 125, 150, 175, 200, 225, 250, 300], min_samples=[None, 10, 30], method=eom, epsilon=0.0
- HDBSCAN 第二階段: min_cluster_size=[50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 500, 600, 700, 800, 900, 1000], min_samples=[None, 5, 10, 15, 30, 50, 75, 100], method=['eom', 'leaf'], epsilon=[0.0, 0.05, 0.1, 0.2]

## 3. 第一階段測試結果摘要

- 總列數: 2520
- 成功列數: 2520

| umap_n_neighbors | umap_n_components | umap_min_dist | hdbscan_min_cluster_size | hdbscan_min_samples | n_clusters | noise_ratio | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 5 | 0.0500 | 50 | 10.0000 | 60 | 0.3041 | 0.0445 | 0.1035 | 0.9554 | 0.8747 |
| 5 | 10 | 0.0000 | 50 | 10.0000 | 66 | 0.3186 | 0.0419 | 0.0903 | 0.9605 | 0.8738 |
| 5 | 10 | 0.0500 | 50 | 10.0000 | 58 | 0.3425 | 0.0418 | 0.1049 | 0.9510 | 0.8637 |
| 10 | 5 | 0.0000 | 50 | 10.0000 | 52 | 0.3321 | 0.0518 | 0.1111 | 0.9551 | 0.8626 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | 58 | 0.2601 | 0.0924 | 0.1651 | 0.9262 | 0.8612 |
| 5 | 15 | 0.0500 | 50 | 10.0000 | 57 | 0.3426 | 0.0480 | 0.1140 | 0.9510 | 0.8600 |
| 10 | 10 | 0.0500 | 50 | 10.0000 | 53 | 0.3428 | 0.0515 | 0.1191 | 0.9517 | 0.8579 |
| 10 | 15 | 0.0000 | 50 | 10.0000 | 52 | 0.2767 | 0.0798 | 0.1783 | 0.9163 | 0.8574 |
| 10 | 5 | 0.0500 | 50 | 10.0000 | 52 | 0.3542 | 0.0494 | 0.1092 | 0.9604 | 0.8571 |
| 15 | 10 | 0.0500 | 50 | 10.0000 | 50 | 0.3563 | 0.0486 | 0.1085 | 0.9530 | 0.8568 |
| 5 | 15 | 0.0000 | 50 | 10.0000 | 55 | 0.2521 | 0.1039 | 0.1908 | 0.9118 | 0.8550 |
| 5 | 10 | 0.1000 | 50 | 10.0000 | 52 | 0.3801 | 0.0369 | 0.0996 | 0.9559 | 0.8550 |
| 15 | 10 | 0.0000 | 75 | 10.0000 | 36 | 0.2815 | 0.0832 | 0.1786 | 0.9412 | 0.8548 |
| 15 | 10 | 0.0000 | 50 | 10.0000 | 47 | 0.2927 | 0.0832 | 0.1683 | 0.9284 | 0.8535 |
| 30 | 5 | 0.0000 | 50 | 10.0000 | 47 | 0.3784 | 0.0445 | 0.1095 | 0.9537 | 0.8512 |

## 4. 第二階段測試結果摘要

- 總列數: 13440
- 成功列數: 13440

| umap_n_neighbors | umap_n_components | umap_min_dist | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | n_clusters | noise_ratio | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.2000 | 62 | 0.2768 | 0.0407 | 0.1061 | 0.9524 | 0.8835 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 62 | 0.2768 | 0.0407 | 0.1061 | 0.9524 | 0.8835 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 66 | 0.2780 | 0.0483 | 0.1025 | 0.9568 | 0.8816 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.2000 | 66 | 0.2780 | 0.0483 | 0.1025 | 0.9568 | 0.8816 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 66 | 0.2862 | 0.0407 | 0.1043 | 0.9561 | 0.8811 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 66 | 0.2862 | 0.0407 | 0.1043 | 0.9561 | 0.8811 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 66 | 0.2862 | 0.0407 | 0.1043 | 0.9561 | 0.8811 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 68 | 0.2874 | 0.0483 | 0.0963 | 0.9610 | 0.8800 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 68 | 0.2874 | 0.0483 | 0.0963 | 0.9610 | 0.8800 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 68 | 0.2874 | 0.0483 | 0.0963 | 0.9610 | 0.8800 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | leaf | 0.0500 | 72 | 0.3323 | 0.0254 | 0.0673 | 0.9724 | 0.8792 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | leaf | 0.0000 | 72 | 0.3323 | 0.0254 | 0.0673 | 0.9724 | 0.8792 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | leaf | 0.1000 | 72 | 0.3323 | 0.0254 | 0.0673 | 0.9724 | 0.8792 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.0000 | 73 | 0.3337 | 0.0286 | 0.0663 | 0.9742 | 0.8781 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.1000 | 73 | 0.3337 | 0.0286 | 0.0663 | 0.9742 | 0.8781 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.0500 | 73 | 0.3337 | 0.0286 | 0.0663 | 0.9742 | 0.8781 |
| 5 | 15 | 0.0500 | 50 | 5.0000 | eom | 0.1000 | 61 | 0.3053 | 0.0413 | 0.0964 | 0.9566 | 0.8767 |
| 5 | 15 | 0.0500 | 50 | 5.0000 | eom | 0.0500 | 61 | 0.3053 | 0.0413 | 0.0964 | 0.9566 | 0.8767 |
| 5 | 15 | 0.0500 | 50 | 5.0000 | eom | 0.0000 | 61 | 0.3053 | 0.0413 | 0.0964 | 0.9566 | 0.8767 |
| 5 | 15 | 0.0500 | 50 | 5.0000 | eom | 0.2000 | 61 | 0.3053 | 0.0413 | 0.0964 | 0.9566 | 0.8767 |

## 5. 最低 noise 設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lowest_noise | 最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。 | stage2 | 15 | 10 | 0.0500 | cosine | 42 | 225 | 5.0000 | eom | 0.0000 | euclidean | ok | 完成 | 2 | 0.0055 | 61 | 272 | 10803 | 10803 | 0.9701 | 0.9945 | 0.1663 | 0.3244 |

## 6. 最多有效主題設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| most_topics | 在可接受 noise_ratio 下保留最多有效主題。 | stage2 | 5 | 5 | 0.0000 | cosine | 42 | 50 | 5.0000 | leaf | 0.0000 | euclidean | ok | 完成 | 73 | 0.3337 | 3716 | 52 | 88 | 318 | 0.0286 | 0.0663 | 0.9742 | 0.8781 |

## 7. 最佳平衡設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| best_balance | 符合指定最佳平衡條件後取最高 balance_score。 | stage2 | 5 | 5 | 0.0000 | cosine | 42 | 50 | 5.0000 | eom | 0.2000 | euclidean | ok | 完成 | 62 | 0.2768 | 3083 | 251 | 52 | 453 | 0.0407 | 0.1061 | 0.9524 | 0.8835 |

## 8. 為什麼不只用 min_cluster_size 判斷

只調整 min_cluster_size 會把問題壓縮成單一維度：降低 noise_ratio 時容易讓大量文本被併入少數大主題；追求較多主題時又可能導致 noise_ratio 上升。UMAP 的 n_neighbors、n_components、min_dist 會改變語意向量在低維空間中的局部/全域結構，HDBSCAN 的 min_samples、cluster_selection_method 與 epsilon 會改變保守程度與群集切分方式。因此本次以 balance_score 同時納入 noise、主題數、最大主題集中度與前三主題集中度，避免只選到低 noise 但不可解釋的過度集中結果。

## 9. 與 A03-8 及語料策略比較

- A03-8 基準：n_clusters=2、noise_ratio=0.0515、最大非 noise topic 約 10308/11136=0.9256，屬於低 noise 但高度集中。
- A04-8 最佳平衡設定相較 A03-8 有改善：有效主題數高於 2，且最大主題比例低於 A03-8 的 0.9256。
- 最佳平衡設定為 n_clusters=62, noise_ratio=0.2768, largest_topic_ratio=0.0407, top3_topic_ratio=0.1061。
- 原始品牌車款詞彙是否造成吸附：有。正式 BERTopic 的 topic words 顯示 orig 語料仍明顯受品牌/車款詞彙吸引：best_balance 有 36/63 個 topics 出現品牌/車款 hits，平均 top words hit ratio=0.1175，最高 hit ratio=0.7000。這表示 UMAP/HDBSCAN 已改善主題大小平衡，但 orig 的部分主題仍會以 Lexus、Audi、Hyundai、Volvo、Kia 等品牌/車款為聚類錨點。
- 語料策略建議：建議以 repl 作為主要語料策略，del 作為敏感性/驗證版本，orig 作為對照與品牌/車款專題分析。理由是 A04-8 證明 orig 在調參後可以取得比 A03-8 更好的主題平衡，但 topic words 仍保留明顯品牌/車款錨點；repl 較適合保留「這裡有品牌/車款實體」的語意位置，同時降低特定名稱吸附，del 則可用來確認非品牌敘事是否穩定。

### A03 para12-80 基準摘要

| dataset | best_min_cluster_size | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | png | svg |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A03-3(del)_tok(para12-80) | 50 | 3 | 0.0112 | 123 | 71 | 67 | Result/06.03_A03_min-test/min_cluster_charts/A03-3(del)_tok(para12-80)_min_cluster_chart.png | Result/06.03_A03_min-test/min_cluster_charts/A03-3(del)_tok(para12-80)_min_cluster_chart.svg |
| A03-6(repl)_tok(para12-80) | 50 | 2 | 0.0007 | 8 | 67 | 10903 | Result/06.03_A03_min-test/min_cluster_charts/A03-6(repl)_tok(para12-80)_min_cluster_chart.png | Result/06.03_A03_min-test/min_cluster_charts/A03-6(repl)_tok(para12-80)_min_cluster_chart.svg |
| A03-8(orig)_tok(para12-80) | 200 | 2 | 0.0515 | 574 | 254 | 10308 | Result/06.03_A03_min-test/min_cluster_charts/A03-8(orig)_tok(para12-80)_min_cluster_chart.png | Result/06.03_A03_min-test/min_cluster_charts/A03-8(orig)_tok(para12-80)_min_cluster_chart.svg |

### 品牌/車款詞彙檢查

| selection_label | topics_checked | topics_with_brand_model_hits | mean_brand_model_hit_ratio | max_brand_model_hit_ratio |
| --- | --- | --- | --- | --- |
| best_balance | 63 | 36 | 0.1175 | 0.7000 |
| lowest_noise | 3 | 2 | 0.2333 | 0.4000 |
| most_topics | 74 | 39 | 0.1068 | 0.7000 |


## 10. 各圖表連結

- [parameter_heatmap.png](charts/parameter_heatmap.png)
- [min_cluster_size_dual_axis.png](charts/min_cluster_size_dual_axis.png)
- [min_samples_noise_ratio.png](charts/min_samples_noise_ratio.png)
- [n_neighbors_largest_topic_ratio.png](charts/n_neighbors_largest_topic_ratio.png)
- [n_components_n_clusters.png](charts/n_components_n_clusters.png)
- [cluster_selection_method_comparison.png](charts/cluster_selection_method_comparison.png)
- [best_balance_topic_size_bar.png](charts/best_balance_topic_size_bar.png)
- [selected_topic_size_distributions.png](charts/selected_topic_size_distributions.png)
- [best_three_comparison.png](charts/best_three_comparison.png)

## 11. 最終 BERTopic 訓練輸出

| balance_score | largest_topic_count | largest_topic_ratio | n_clusters | n_topics_including_noise | noise_ratio | output_dir | selection_label | status | top3_topic_ratio | topic_-1_count | topic_0_count | topic_1_count | topic_entropy | topic_info_rows |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.3244 | 10803 | 0.9701 | 2 | 3 | 0.0055 | final_models/lowest_noise | lowest_noise | ok | 0.9945 | 61 | 10803 | 272 | 0.1663 | 3 |
| 0.8781 | 318 | 0.0286 | 73 | 74 | 0.3337 | final_models/most_topics | most_topics | ok | 0.0663 | 3716 | 318 | 214 | 0.9742 | 74 |
| 0.8835 | 453 | 0.0407 | 62 | 63 | 0.2768 | final_models/best_balance | best_balance | ok | 0.1061 | 3083 | 453 | 390 | 0.9524 | 63 |


- final_configs.json: `final_configs.json`
- comparison_summary.csv: `comparison_summary.csv`

## 12. 穩定性檢測摘要

| stability_rank | noise_ratio_mean | noise_ratio_std | n_clusters_mean | n_clusters_std | largest_topic_ratio_mean | largest_topic_ratio_std |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.2267 | 0.0337 | 58.2000 | 4.1473 | 0.0655 | 0.0330 |
| 2 | 0.2480 | 0.0210 | 60.8000 | 0.8367 | 0.0439 | 0.0045 |
| 3 | 0.2607 | 0.0216 | 63.8000 | 3.5637 | 0.0455 | 0.0093 |
| 4 | 0.2402 | 0.0329 | 61.0000 | 3.7417 | 0.0662 | 0.0335 |
| 5 | 0.2362 | 0.0331 | 60.8000 | 4.9699 | 0.0655 | 0.0330 |
| 6 | 0.2362 | 0.0331 | 60.8000 | 4.9699 | 0.0655 | 0.0330 |
| 7 | 0.2362 | 0.0331 | 60.8000 | 4.9699 | 0.0655 | 0.0330 |
| 8 | 0.2505 | 0.0370 | 62.8000 | 3.8341 | 0.0660 | 0.0336 |
| 9 | 0.2505 | 0.0370 | 62.8000 | 3.8341 | 0.0660 | 0.0336 |
| 10 | 0.2505 | 0.0370 | 62.8000 | 3.8341 | 0.0660 | 0.0336 |

## 錯誤輸出

### 檢測發現與建議

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 1. 環境套件可載入，A04 UMAP + HDBSCAN 多參數檢測已完成。 |
| 資料載入 | 1. 有 14 筆少於 3 words 的短句保留，可能增加離群值。 |
| Embedding | 1. 偵測到既有 embeddings 快取，已直接共用。 |
| UMAP | 無 |
| HDBSCAN | 無 |
| BERTopic | 無 |
| 圖表輸出 | 無 |

### 整體錯誤輸出

無阻斷性失敗。

### 可改進

1. 可加入中文或領域專用 stopwords，提升 topic words 可解釋性。
2. 可用 c-TF-IDF 後處理、MMR 或人工合併相近主題，降低語意相近語料造成的主題碎裂。
3. 若穩定性檢測顯示不同 random_state 差異大，建議優先採用標準差較低的平衡設定，而不是只看單次最高分。
4. 若最佳平衡設定仍有最大主題過大，可後續針對最大主題單獨進行二階段 BERTopic。
