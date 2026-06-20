# BERTopic UMAP + HDBSCAN 多參數檢測報告 - 06.03_A04-2(del)_tok

## 1. Dataset 資訊

| dataset_dir | columns | text_col | title_col | source_rows | used_rows | empty_rows_count | short_rows_lt_3_words_count | min_text_len | max_text_len | avg_text_len | min_word_count | max_word_count | avg_word_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Result/06.03_A02/R06.03_A02-pre_LLM(del)_tok_dataset | ['title', 'source_row', 'sentence_id', 'sentence', 'word_count', 'char_count'] | sentence | title | 31474 | 31474 | 0 | 1417 | 2 | 664 | 84.8887 | 1 | 142 | 14.9064 |

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
| 5 | 10 | 0.0000 | 50 | 10.0000 | 128 | 0.3591 | 0.0310 | 0.0809 | 0.9391 | 0.8668 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | 145 | 0.3977 | 0.0248 | 0.0599 | 0.9539 | 0.8613 |
| 5 | 15 | 0.0000 | 50 | 10.0000 | 131 | 0.3740 | 0.0334 | 0.0854 | 0.9357 | 0.8607 |
| 5 | 5 | 0.0000 | 75 | 10.0000 | 88 | 0.3850 | 0.0302 | 0.0842 | 0.9435 | 0.8586 |
| 5 | 15 | 0.0000 | 75 | 10.0000 | 82 | 0.3843 | 0.0334 | 0.0936 | 0.9391 | 0.8560 |
| 10 | 5 | 0.0000 | 50 | 10.0000 | 120 | 0.3949 | 0.0301 | 0.0828 | 0.9273 | 0.8559 |
| 10 | 15 | 0.0000 | 50 | 10.0000 | 118 | 0.3924 | 0.0315 | 0.0895 | 0.9184 | 0.8549 |
| 5 | 10 | 0.0000 | 75 | 10.0000 | 92 | 0.3793 | 0.0404 | 0.0972 | 0.9353 | 0.8547 |
| 5 | 10 | 0.0500 | 50 | 10.0000 | 125 | 0.4043 | 0.0303 | 0.0845 | 0.9356 | 0.8527 |
| 5 | 15 | 0.0500 | 50 | 10.0000 | 123 | 0.4127 | 0.0302 | 0.0731 | 0.9392 | 0.8525 |
| 10 | 10 | 0.0000 | 50 | 10.0000 | 134 | 0.4158 | 0.0298 | 0.0756 | 0.9365 | 0.8512 |
| 5 | 5 | 0.0000 | 100 | 10.0000 | 69 | 0.4058 | 0.0315 | 0.0903 | 0.9466 | 0.8508 |
| 5 | 5 | 0.0500 | 50 | 10.0000 | 130 | 0.4246 | 0.0302 | 0.0646 | 0.9454 | 0.8506 |
| 15 | 10 | 0.0000 | 50 | 10.0000 | 109 | 0.4264 | 0.0261 | 0.0737 | 0.9355 | 0.8495 |
| 15 | 15 | 0.0000 | 50 | 10.0000 | 115 | 0.4236 | 0.0278 | 0.0781 | 0.9296 | 0.8489 |

## 4. 第二階段測試結果摘要

- 總列數: 13440
- 成功列數: 13440

| umap_n_neighbors | umap_n_components | umap_min_dist | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | n_clusters | noise_ratio | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 148 | 0.3416 | 0.0276 | 0.0651 | 0.9486 | 0.8762 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 148 | 0.3416 | 0.0276 | 0.0651 | 0.9486 | 0.8762 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 148 | 0.3416 | 0.0276 | 0.0651 | 0.9486 | 0.8762 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | eom | 0.2000 | 112 | 0.3043 | 0.0438 | 0.1026 | 0.9097 | 0.8750 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | leaf | 0.2000 | 113 | 0.3048 | 0.0438 | 0.1026 | 0.9088 | 0.8749 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 142 | 0.3442 | 0.0297 | 0.0703 | 0.9483 | 0.8738 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 142 | 0.3442 | 0.0297 | 0.0703 | 0.9483 | 0.8738 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 142 | 0.3442 | 0.0297 | 0.0703 | 0.9483 | 0.8738 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 105 | 0.2582 | 0.0696 | 0.1444 | 0.8711 | 0.8728 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.2000 | 105 | 0.2582 | 0.0696 | 0.1444 | 0.8711 | 0.8728 |
| 5 | 10 | 0.0000 | 50 | 10.0000 | eom | 0.2000 | 110 | 0.3172 | 0.0383 | 0.1077 | 0.9095 | 0.8718 |
| 5 | 10 | 0.0000 | 50 | 10.0000 | leaf | 0.2000 | 112 | 0.3198 | 0.0383 | 0.1077 | 0.9078 | 0.8710 |
| 5 | 15 | 0.0000 | 50 | 10.0000 | eom | 0.2000 | 116 | 0.3370 | 0.0334 | 0.0926 | 0.9191 | 0.8703 |
| 5 | 15 | 0.0000 | 50 | 10.0000 | leaf | 0.2000 | 118 | 0.3461 | 0.0307 | 0.0838 | 0.9228 | 0.8702 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.1000 | 157 | 0.3846 | 0.0182 | 0.0499 | 0.9617 | 0.8692 |
| 5 | 5 | 0.0000 | 75 | 5.0000 | eom | 0.0500 | 94 | 0.3479 | 0.0322 | 0.0849 | 0.9422 | 0.8690 |
| 5 | 5 | 0.0000 | 75 | 5.0000 | eom | 0.1000 | 94 | 0.3479 | 0.0322 | 0.0849 | 0.9422 | 0.8690 |
| 5 | 5 | 0.0000 | 75 | 5.0000 | eom | 0.0000 | 94 | 0.3479 | 0.0322 | 0.0849 | 0.9422 | 0.8690 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 142 | 0.3357 | 0.0401 | 0.0924 | 0.9316 | 0.8688 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 142 | 0.3357 | 0.0401 | 0.0924 | 0.9316 | 0.8688 |

## 5. 最低 noise 設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lowest_noise | 最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。 | stage2 | 15 | 10 | 0.0000 | cosine | 42 | 100 | 30.0000 | eom | 0.0000 | euclidean | ok | 完成 | 2 | 0.0000 | 0 | 100 | 31374 | 31374 | 0.9968 | 1.0000 | 0.0309 | 0.3143 |

## 6. 最多有效主題設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| most_topics | 在可接受 noise_ratio 下保留最多有效主題。 | stage2 | 5 | 15 | 0.0000 | cosine | 42 | 50 | 5.0000 | leaf | 0.0000 | euclidean | ok | 完成 | 166 | 0.4188 | 13182 | 54 | 54 | 395 | 0.0126 | 0.0321 | 0.9732 | 0.8642 |

## 7. 最佳平衡設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| best_balance | 符合嚴格平衡條件後取最高 balance_score。 | stage2 | 5 | 5 | 0.0000 | cosine | 42 | 50 | 5.0000 | eom | 0.0000 | euclidean | ok | 完成 | 148 | 0.3416 | 10753 | 53 | 52 | 868 | 0.0276 | 0.0651 | 0.9486 | 0.8762 |

## 8. 為什麼不只用 min_cluster_size 判斷

只調整 min_cluster_size 會把問題壓縮成單一維度：降低 noise_ratio 時容易讓大量文本被併入少數大主題；追求較多主題時又可能導致 noise_ratio 上升。UMAP 的 n_neighbors、n_components、min_dist 會改變語意向量在低維空間中的局部/全域結構，HDBSCAN 的 min_samples、cluster_selection_method 與 epsilon 會改變保守程度與群集切分方式。因此本次以 balance_score 同時納入 noise、主題數、最大主題集中度與前三主題集中度，避免只選到低 noise 但不可解釋的過度集中結果。

## 9. 各圖表連結

- [parameter_heatmap.png](charts/parameter_heatmap.png)
- [min_cluster_size_dual_axis.png](charts/min_cluster_size_dual_axis.png)
- [min_samples_noise_ratio.png](charts/min_samples_noise_ratio.png)
- [n_neighbors_largest_topic_ratio.png](charts/n_neighbors_largest_topic_ratio.png)
- [n_components_n_clusters.png](charts/n_components_n_clusters.png)
- [best_balance_topic_size_bar.png](charts/best_balance_topic_size_bar.png)
- [best_three_comparison.png](charts/best_three_comparison.png)

## 10. 最終 BERTopic 訓練輸出

| n_topics_including_noise | output_dir | selection_label | status | topic_info_rows |
| --- | --- | --- | --- | --- |
| 2 | final_models/lowest_noise | lowest_noise | ok | 2 |
| 174 | final_models/most_topics | most_topics | ok | 174 |
| 153 | final_models/best_balance | best_balance | ok | 153 |

## 11. 穩定性檢測摘要

| stability_rank | noise_ratio_mean | noise_ratio_std | n_clusters_mean | n_clusters_std | largest_topic_ratio_mean | largest_topic_ratio_std |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.3514 | 0.0160 | 153.2000 | 6.5345 | 0.0298 | 0.0062 |
| 2 | 0.3537 | 0.0178 | 154.0000 | 7.5166 | 0.0298 | 0.0062 |
| 3 | 0.3537 | 0.0178 | 154.0000 | 7.5166 | 0.0298 | 0.0062 |
| 4 | 0.3053 | 0.0058 | 115.6000 | 4.5056 | 0.0460 | 0.0070 |
| 5 | 0.3096 | 0.0081 | 116.8000 | 3.7683 | 0.0460 | 0.0070 |
| 6 | 0.3517 | 0.0083 | 147.4000 | 7.7330 | 0.0311 | 0.0047 |
| 7 | 0.3517 | 0.0083 | 147.4000 | 7.7330 | 0.0311 | 0.0047 |
| 8 | 0.3517 | 0.0083 | 147.4000 | 7.7330 | 0.0311 | 0.0047 |
| 9 | 0.2629 | 0.0060 | 107.8000 | 2.5884 | 0.0803 | 0.0250 |
| 10 | 0.2629 | 0.0060 | 107.8000 | 2.5884 | 0.0803 | 0.0250 |

## 錯誤輸出

### 檢測發現與建議

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 1. 環境套件可載入，開始 A04 UMAP + HDBSCAN 多參數檢測。 |
| 資料載入 | 1. 有 1417 筆少於 3 words 的短句保留，可能增加離群值。 |
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
