# BERTopic UMAP + HDBSCAN 多參數檢測報告 - [D]01-(orig)_08-19_tok(para12-80)

## 1. Dataset 資訊

| dataset_dir | columns | text_col | title_col | source_rows | used_rows | empty_rows_count | short_rows_lt_3_words_count | min_text_len | max_text_len | avg_text_len | min_word_count | max_word_count | avg_word_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_08-19(240)_tok(para12-80)_dataset | ['title', 'source_row', 'paragraph_id', 'sentence_start_id', 'sentence_end_id', 'sentence_count', 'sentence', 'word_count', 'char_count'] | sentence | title | 11160 | 11160 | 0 | 0 | 46 | 523 | 123.6016 | 5 | 80 | 21.8513 |

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
| 5 | 15 | 0.0000 | 50 | 10.0000 | 65 | 0.3149 | 0.0486 | 0.0999 | 0.9604 | 0.8710 |
| 10 | 5 | 0.0000 | 50 | 10.0000 | 61 | 0.3332 | 0.0358 | 0.0974 | 0.9598 | 0.8698 |
| 10 | 10 | 0.0000 | 50 | 10.0000 | 57 | 0.3350 | 0.0446 | 0.0964 | 0.9577 | 0.8668 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | 59 | 0.3080 | 0.0554 | 0.1301 | 0.9447 | 0.8650 |
| 5 | 10 | 0.0000 | 50 | 10.0000 | 53 | 0.2551 | 0.0893 | 0.1771 | 0.9202 | 0.8613 |
| 5 | 15 | 0.0500 | 50 | 10.0000 | 54 | 0.3166 | 0.0576 | 0.1358 | 0.9414 | 0.8606 |
| 10 | 15 | 0.0000 | 50 | 10.0000 | 52 | 0.3154 | 0.0625 | 0.1311 | 0.9404 | 0.8604 |
| 5 | 5 | 0.0500 | 50 | 10.0000 | 57 | 0.3530 | 0.0433 | 0.1050 | 0.9507 | 0.8601 |
| 10 | 5 | 0.0000 | 75 | 10.0000 | 38 | 0.3587 | 0.0418 | 0.1152 | 0.9621 | 0.8568 |
| 5 | 15 | 0.0000 | 75 | 10.0000 | 41 | 0.3447 | 0.0538 | 0.1220 | 0.9589 | 0.8560 |
| 15 | 5 | 0.0000 | 50 | 10.0000 | 59 | 0.4002 | 0.0303 | 0.0790 | 0.9695 | 0.8551 |
| 10 | 5 | 0.0000 | 100 | 10.0000 | 29 | 0.3634 | 0.0418 | 0.1185 | 0.9710 | 0.8548 |
| 10 | 5 | 0.0500 | 50 | 10.0000 | 56 | 0.3830 | 0.0410 | 0.0989 | 0.9559 | 0.8530 |
| 5 | 15 | 0.0500 | 75 | 10.0000 | 36 | 0.3430 | 0.0576 | 0.1395 | 0.9552 | 0.8519 |
| 5 | 5 | 0.0000 | 75 | 10.0000 | 37 | 0.3081 | 0.0740 | 0.1693 | 0.9448 | 0.8515 |

## 4. 第二階段測試結果摘要

- 總列數: 13440
- 成功列數: 13440

| umap_n_neighbors | umap_n_components | umap_min_dist | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | n_clusters | noise_ratio | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 15 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 66 | 0.2887 | 0.0324 | 0.0891 | 0.9660 | 0.8858 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.2000 | 63 | 0.2711 | 0.0453 | 0.1019 | 0.9594 | 0.8847 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 65 | 0.2785 | 0.0453 | 0.0999 | 0.9629 | 0.8829 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 65 | 0.2785 | 0.0453 | 0.0999 | 0.9629 | 0.8829 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 65 | 0.2785 | 0.0453 | 0.0999 | 0.9629 | 0.8829 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | leaf | 0.1000 | 71 | 0.3284 | 0.0220 | 0.0600 | 0.9790 | 0.8829 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | leaf | 0.0500 | 71 | 0.3284 | 0.0220 | 0.0600 | 0.9790 | 0.8829 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | leaf | 0.0000 | 71 | 0.3284 | 0.0220 | 0.0600 | 0.9790 | 0.8829 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 59 | 0.2918 | 0.0367 | 0.1035 | 0.9609 | 0.8807 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 61 | 0.2859 | 0.0399 | 0.1096 | 0.9533 | 0.8803 |
| 5 | 15 | 0.0500 | 50 | 5.0000 | eom | 0.0000 | 63 | 0.3197 | 0.0307 | 0.0844 | 0.9650 | 0.8780 |
| 5 | 15 | 0.0500 | 50 | 5.0000 | eom | 0.1000 | 63 | 0.3197 | 0.0307 | 0.0844 | 0.9650 | 0.8780 |
| 5 | 15 | 0.0500 | 50 | 5.0000 | eom | 0.0500 | 63 | 0.3197 | 0.0307 | 0.0844 | 0.9650 | 0.8780 |
| 5 | 15 | 0.0500 | 50 | 5.0000 | eom | 0.2000 | 63 | 0.3197 | 0.0307 | 0.0844 | 0.9650 | 0.8780 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.2000 | 54 | 0.2387 | 0.0672 | 0.1553 | 0.9315 | 0.8772 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.2000 | 57 | 0.2665 | 0.0573 | 0.1300 | 0.9503 | 0.8768 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 58 | 0.2669 | 0.0573 | 0.1300 | 0.9492 | 0.8767 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 58 | 0.2669 | 0.0573 | 0.1300 | 0.9492 | 0.8767 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 58 | 0.2669 | 0.0573 | 0.1300 | 0.9492 | 0.8767 |
| 5 | 15 | 0.0500 | 50 | 5.0000 | leaf | 0.2000 | 65 | 0.3263 | 0.0307 | 0.0844 | 0.9643 | 0.8760 |

## 5. 最低 noise 設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lowest_noise | 最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。 | stage2 | 5 | 5 | 0.0000 | cosine | 42 | 200 | 10.0000 | eom | 0.0000 | euclidean | ok | 完成 | 2 | 0.0022 | 24 | 10921 | 215 | 10921 | 0.9786 | 0.9978 | 0.1375 | 0.3222 |

## 6. 最多有效主題設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| most_topics | 在可接受 noise_ratio 下保留最多有效主題。 | stage2 | 5 | 5 | 0.0000 | cosine | 42 | 50 | 5.0000 | leaf | 0.0000 | euclidean | ok | 完成 | 73 | 0.3486 | 3890 | 253 | 251 | 253 | 0.0227 | 0.0650 | 0.9768 | 0.8756 |

## 7. 最佳平衡設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| best_balance | 符合指定最佳平衡條件後取最高 balance_score。 | stage2 | 5 | 15 | 0.0000 | cosine | 42 | 50 | 5.0000 | leaf | 0.2000 | euclidean | ok | 完成 | 66 | 0.2887 | 3222 | 362 | 323 | 362 | 0.0324 | 0.0891 | 0.9660 | 0.8858 |

## 8. 為什麼不只用 min_cluster_size 判斷

只調整 min_cluster_size 會把問題壓縮成單一維度：降低 noise_ratio 時容易讓大量文本被併入少數大主題；追求較多主題時又可能導致 noise_ratio 上升。UMAP 的 n_neighbors、n_components、min_dist 會改變語意向量在低維空間中的局部/全域結構，HDBSCAN 的 min_samples、cluster_selection_method 與 epsilon 會改變保守程度與群集切分方式。因此本次以 balance_score 同時納入 noise、主題數、最大主題集中度與前三主題集中度，避免只選到低 noise 但不可解釋的過度集中結果。

## 9. 與 [C]min 及語料策略比較

- [C]min 基準：固定 UMAP(n_neighbors=15, n_components=5, min_dist=0.0) 並只掃 HDBSCAN min_cluster_size，屬於低 noise 但高度集中。
- 是否比 [C]min 產生更平衡的 noise 與主題數：是。[D] best_balance 的 balance_score=0.8858，[C]min baseline=0.3642；n_clusters 5 -> 66，noise_ratio 0.0041 -> 0.2887。
- 是否降低最大主題集中度：是。largest_topic_ratio 0.9306 -> 0.0324；top3_topic_ratio 0.9770 -> 0.0891，前三主題集中度也降低。
- 最佳平衡設定為 UMAP(n_neighbors=5, n_components=15, min_dist=0.00)，HDBSCAN(min_cluster_size=50, min_samples=5, method=leaf, epsilon=0.20)。
- 原始品牌車款詞彙是否造成吸附：有。正式 BERTopic 的 topic words 顯示 orig 語料仍明顯受品牌/車款詞彙吸引：best_balance 有 29/67 個 topics 出現品牌/車款 hits，平均 top words hit ratio=0.1045，最高 hit ratio=0.6000。這表示 UMAP/HDBSCAN 已改善主題大小平衡，但 orig 的部分主題仍會以 Lexus、Audi、Hyundai、Volvo、Kia 等品牌/車款為聚類錨點。
- 語料策略建議：建議以 repl 作為主要語料策略，del 作為敏感性/驗證版本，orig 作為對照與品牌/車款專題分析。理由是本次只使用 orig 已能透過 UMAP/HDBSCAN 調參改善最大主題集中度，但 topic words 仍可能保留品牌/車款錨點；repl 較適合保留「這裡有品牌/車款實體」的語意位置，同時降低特定名稱吸附，del 則可用來確認非品牌敘事是否穩定。

### [C]min 基準摘要

| baseline | source | umap_n_neighbors | umap_n_components | umap_min_dist | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [C]min best | Result/06.13_[C]min/[B]01-(orig)_08-19(240)_tok(para12-80)/Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)-best_topic_info.csv | 15 | 5 | 0.0000 | 50 |  | eom | 0.0000 | 5 | 0.0041 | 46 | 10385 | 281 | 10385 | 0.9306 | 0.9770 | 0.2016 | 0.3642 |

### 品牌/車款詞彙檢查

| selection_label | topics_checked | topics_with_brand_model_hits | mean_brand_model_hit_ratio | max_brand_model_hit_ratio |
| --- | --- | --- | --- | --- |
| best_balance | 67 | 29 | 0.1045 | 0.6000 |
| lowest_noise | 3 | 2 | 0.1667 | 0.4000 |
| most_topics | 74 | 30 | 0.0905 | 0.5000 |


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
| 0.3222 | 10921 | 0.9786 | 2 | 3 | 0.0022 | final_models/lowest_noise | lowest_noise | ok | 0.9978 | 24 | 10921 | 215 | 0.1375 | 3 |
| 0.8756 | 253 | 0.0227 | 73 | 74 | 0.3486 | final_models/most_topics | most_topics | ok | 0.0650 | 3890 | 253 | 251 | 0.9768 | 74 |
| 0.8858 | 362 | 0.0324 | 66 | 67 | 0.2887 | final_models/best_balance | best_balance | ok | 0.0891 | 3222 | 362 | 323 | 0.9660 | 67 |


- final_configs.json: `final_configs.json`
- comparison_summary.csv: `comparison_summary.csv`

## 12. 穩定性檢測摘要

| stability_rank | noise_ratio_mean | noise_ratio_std | n_clusters_mean | n_clusters_std | largest_topic_ratio_mean | largest_topic_ratio_std |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.2959 | 0.0234 | 65.0000 | 1.7321 | 0.0386 | 0.0064 |
| 2 | 0.2661 | 0.0275 | 62.0000 | 2.2361 | 0.0509 | 0.0054 |
| 3 | 0.2757 | 0.0281 | 63.4000 | 2.4083 | 0.0509 | 0.0054 |
| 4 | 0.2757 | 0.0281 | 63.4000 | 2.4083 | 0.0509 | 0.0054 |
| 5 | 0.2757 | 0.0281 | 63.4000 | 2.4083 | 0.0509 | 0.0054 |
| 6 | 0.3503 | 0.0193 | 72.2000 | 1.3038 | 0.0242 | 0.0027 |
| 7 | 0.3503 | 0.0193 | 72.2000 | 1.3038 | 0.0242 | 0.0027 |
| 8 | 0.3503 | 0.0193 | 72.2000 | 1.3038 | 0.0242 | 0.0027 |
| 9 | 0.2858 | 0.0121 | 63.4000 | 4.0988 | 0.0340 | 0.0045 |
| 10 | 0.2870 | 0.0224 | 63.0000 | 1.8708 | 0.0451 | 0.0109 |

## 錯誤輸出

### 檢測發現與建議

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 1. 環境套件可載入，開始 [D] UMAP + HDBSCAN 多參數檢測。 |
| 資料載入 | 無 |
| Embedding | 1. 已完成 embeddings 計算並建立快取。 |
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
