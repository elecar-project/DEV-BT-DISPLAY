# BERTopic UMAP + HDBSCAN 多參數檢測報告 - 06.13_[D]UMAP_[B]01-(orig)_20-25_tok(para12-80)

## 1. Dataset 資訊

| dataset_dir | columns | text_col | title_col | source_rows | used_rows | empty_rows_count | short_rows_lt_3_words_count | min_text_len | max_text_len | avg_text_len | min_word_count | max_word_count | avg_word_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_20-25(194)_tok(para12-80)_dataset | ['title', 'source_row', 'paragraph_id', 'sentence_start_id', 'sentence_end_id', 'sentence_count', 'sentence', 'word_count', 'char_count'] | sentence | title | 10680 | 10680 | 0 | 0 | 47 | 535 | 129.0809 | 10 | 80 | 22.3301 |

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
| 5 | 5 | 0.0000 | 50 | 10.0000 | 53 | 0.2645 | 0.0449 | 0.1203 | 0.9549 | 0.8831 |
| 5 | 10 | 0.0000 | 75 | 10.0000 | 39 | 0.2274 | 0.0708 | 0.1581 | 0.9473 | 0.8789 |
| 5 | 5 | 0.0500 | 50 | 10.0000 | 50 | 0.2841 | 0.0431 | 0.1210 | 0.9501 | 0.8777 |
| 5 | 15 | 0.0000 | 50 | 10.0000 | 57 | 0.2463 | 0.0635 | 0.1493 | 0.9414 | 0.8772 |
| 5 | 10 | 0.0000 | 50 | 10.0000 | 52 | 0.2615 | 0.0596 | 0.1469 | 0.9442 | 0.8743 |
| 5 | 5 | 0.0000 | 75 | 10.0000 | 40 | 0.2860 | 0.0463 | 0.1318 | 0.9593 | 0.8740 |
| 10 | 5 | 0.0000 | 50 | 10.0000 | 54 | 0.3162 | 0.0412 | 0.1007 | 0.9637 | 0.8726 |
| 5 | 10 | 0.0500 | 50 | 10.0000 | 53 | 0.3041 | 0.0413 | 0.1191 | 0.9586 | 0.8726 |
| 5 | 15 | 0.0500 | 50 | 10.0000 | 54 | 0.3235 | 0.0416 | 0.1030 | 0.9648 | 0.8699 |
| 5 | 10 | 0.0500 | 75 | 10.0000 | 41 | 0.3132 | 0.0413 | 0.1191 | 0.9621 | 0.8698 |
| 5 | 15 | 0.0000 | 75 | 10.0000 | 41 | 0.2770 | 0.0635 | 0.1493 | 0.9523 | 0.8680 |
| 5 | 5 | 0.0000 | 100 | 10.0000 | 33 | 0.2875 | 0.0590 | 0.1501 | 0.9539 | 0.8660 |
| 15 | 15 | 0.0000 | 50 | 10.0000 | 52 | 0.3338 | 0.0435 | 0.1041 | 0.9600 | 0.8660 |
| 10 | 10 | 0.0500 | 50 | 10.0000 | 51 | 0.3454 | 0.0406 | 0.0944 | 0.9682 | 0.8653 |
| 5 | 5 | 0.0500 | 75 | 10.0000 | 40 | 0.3294 | 0.0431 | 0.1155 | 0.9675 | 0.8651 |

## 4. 第二階段測試結果摘要

- 總列數: 13440
- 成功列數: 13440

| umap_n_neighbors | umap_n_components | umap_min_dist | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | n_clusters | noise_ratio | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.2000 | 59 | 0.2160 | 0.0449 | 0.1275 | 0.9541 | 0.8962 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 60 | 0.2175 | 0.0449 | 0.1275 | 0.9536 | 0.8958 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 62 | 0.2317 | 0.0449 | 0.1275 | 0.9577 | 0.8915 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 62 | 0.2317 | 0.0449 | 0.1275 | 0.9577 | 0.8915 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 62 | 0.2317 | 0.0449 | 0.1275 | 0.9577 | 0.8915 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.2000 | 52 | 0.2133 | 0.0581 | 0.1459 | 0.9378 | 0.8894 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | leaf | 0.1000 | 70 | 0.2900 | 0.0304 | 0.0774 | 0.9776 | 0.8884 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | leaf | 0.0500 | 70 | 0.2900 | 0.0304 | 0.0774 | 0.9776 | 0.8884 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | leaf | 0.0000 | 70 | 0.2900 | 0.0304 | 0.0774 | 0.9776 | 0.8884 |
| 5 | 15 | 0.0000 | 75 | 5.0000 | eom | 0.2000 | 44 | 0.2214 | 0.0581 | 0.1459 | 0.9488 | 0.8869 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 60 | 0.2608 | 0.0449 | 0.1135 | 0.9618 | 0.8856 |
| 5 | 5 | 0.0500 | 50 | 5.0000 | eom | 0.2000 | 54 | 0.2549 | 0.0462 | 0.1207 | 0.9559 | 0.8856 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 55 | 0.2307 | 0.0581 | 0.1434 | 0.9426 | 0.8847 |
| 5 | 5 | 0.0500 | 50 | 5.0000 | leaf | 0.2000 | 56 | 0.2731 | 0.0444 | 0.1029 | 0.9618 | 0.8842 |
| 5 | 5 | 0.0500 | 50 | 5.0000 | eom | 0.1000 | 55 | 0.2606 | 0.0462 | 0.1207 | 0.9557 | 0.8838 |
| 5 | 5 | 0.0500 | 50 | 5.0000 | eom | 0.0500 | 55 | 0.2606 | 0.0462 | 0.1207 | 0.9557 | 0.8838 |
| 5 | 5 | 0.0500 | 50 | 5.0000 | eom | 0.0000 | 55 | 0.2606 | 0.0462 | 0.1207 | 0.9557 | 0.8838 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | eom | 0.1000 | 53 | 0.2645 | 0.0449 | 0.1203 | 0.9549 | 0.8831 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | eom | 0.0500 | 53 | 0.2645 | 0.0449 | 0.1203 | 0.9549 | 0.8831 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | eom | 0.0000 | 53 | 0.2645 | 0.0449 | 0.1203 | 0.9549 | 0.8831 |

## 5. 最低 noise 設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lowest_noise | 最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。 | stage2 | 10 | 10 | 0.0500 | cosine | 42 | 100 | 50.0000 | eom | 0.0000 | euclidean | ok | 完成 | 6 | 0.0122 | 130 | 9939 | 173 | 9939 | 0.9306 | 0.9581 | 0.1748 | 0.3736 |

## 6. 最多有效主題設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| most_topics | 在可接受 noise_ratio 下保留最多有效主題。 | stage2 | 5 | 15 | 0.0000 | cosine | 42 | 50 | 5.0000 | leaf | 0.0000 | euclidean | ok | 完成 | 70 | 0.2900 | 3097 | 325 | 302 | 325 | 0.0304 | 0.0774 | 0.9776 | 0.8884 |

## 7. 最佳平衡設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| best_balance | 符合指定最佳平衡條件後取最高 balance_score。 | stage2 | 5 | 15 | 0.0000 | cosine | 42 | 50 | 5.0000 | eom | 0.2000 | euclidean | ok | 完成 | 59 | 0.2160 | 2307 | 479 | 458 | 479 | 0.0449 | 0.1275 | 0.9541 | 0.8962 |

## 8. 為什麼不只用 min_cluster_size 判斷

只調整 min_cluster_size 會把問題壓縮成單一維度：降低 noise_ratio 時容易讓大量文本被併入少數大主題；追求較多主題時又可能導致 noise_ratio 上升。UMAP 的 n_neighbors、n_components、min_dist 會改變語意向量在低維空間中的局部/全域結構，HDBSCAN 的 min_samples、cluster_selection_method 與 epsilon 會改變保守程度與群集切分方式。因此本次以 balance_score 同時納入 noise、主題數、最大主題集中度與前三主題集中度，避免只選到低 noise 但不可解釋的過度集中結果。

## 9. 與 06.13_[C]min 基準及語料策略比較

- 06.13_[C]min 基準來源：`Result/06.13_[C]min/[B]01-(orig)_20-25(194)_tok(para12-80)`。
- 是否比 06.13_[C]min 產生更平衡的 noise 與主題數：是。[D] best_balance n_clusters=59, noise_ratio=0.2160, balance_score=0.8962；[C]min baseline n_clusters=2, noise_ratio=0.0740, balance_score=0.3353。
- 是否降低最大主題集中度：是。[D] largest_topic_ratio=0.0449, top3_topic_ratio=0.1275；[C]min largest_topic_ratio=0.9111, top3_topic_ratio=0.9260。
- 原始品牌車款詞彙是否造成吸附：有。正式 BERTopic 的 topic words 顯示 orig 語料仍明顯受品牌/車款詞彙吸引：best_balance 有 24/60 個 topics 出現品牌/車款 hits，平均 top words hit ratio=0.0867，最高 hit ratio=0.6000。這表示 UMAP/HDBSCAN 已改善主題大小平衡，但 orig 的部分主題仍會以 Lexus、Audi、Hyundai、Volvo、Kia 等品牌/車款為聚類錨點。
- 語料策略建議：建議以 repl 作為主要語料策略，del 作為敏感性/驗證版本，orig 作為對照與品牌/車款專題分析。理由是本次 orig 在 UMAP/HDBSCAN 調參後可以改善主題大小平衡，但 topic words 仍保留明顯品牌/車款錨點；repl 較適合保留「這裡有品牌/車款實體」的語意位置，同時降低特定名稱吸附，del 則可用來確認非品牌敘事是否穩定。

### 06.13_[C]min 基準摘要

| baseline | min_cluster_size | n_clusters | noise_ratio | topic_-1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score | source_dir |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 06.13_[C]min best | 125 | 2 | 0.0740 | 790 | 9731 | 0.9111 | 0.9260 | 0.1188 | 0.3353 | Result/06.13_[C]min/[B]01-(orig)_20-25(194)_tok(para12-80) |

### 品牌/車款詞彙檢查

| selection_label | topics_checked | topics_with_brand_model_hits | mean_brand_model_hit_ratio | max_brand_model_hit_ratio |
| --- | --- | --- | --- | --- |
| best_balance | 60 | 24 | 0.0867 | 0.6000 |
| lowest_noise | 7 | 4 | 0.2143 | 0.5000 |
| most_topics | 71 | 26 | 0.0775 | 0.6000 |


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
| 0.3736 | 9939 | 0.9306 | 6 | 7 | 0.0122 | final_models/lowest_noise | lowest_noise | ok | 0.9581 | 130 | 9939 | 173 | 0.1748 | 7 |
| 0.8884 | 325 | 0.0304 | 70 | 71 | 0.2900 | final_models/most_topics | most_topics | ok | 0.0774 | 3097 | 325 | 302 | 0.9776 | 71 |
| 0.8962 | 479 | 0.0449 | 59 | 60 | 0.2160 | final_models/best_balance | best_balance | ok | 0.1275 | 2307 | 479 | 458 | 0.9541 | 60 |


- final_configs.json: `final_configs.json`
- comparison_summary.csv: `comparison_summary.csv`

## 12. 穩定性檢測摘要

| stability_rank | noise_ratio_mean | noise_ratio_std | n_clusters_mean | n_clusters_std | largest_topic_ratio_mean | largest_topic_ratio_std |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.2332 | 0.0214 | 56.4000 | 3.7815 | 0.0580 | 0.0251 |
| 2 | 0.2532 | 0.0303 | 58.8000 | 2.1679 | 0.0446 | 0.0116 |
| 3 | 0.2413 | 0.0258 | 58.6000 | 2.6077 | 0.0580 | 0.0251 |
| 4 | 0.2413 | 0.0258 | 58.6000 | 2.6077 | 0.0580 | 0.0251 |
| 5 | 0.2413 | 0.0258 | 58.6000 | 2.6077 | 0.0580 | 0.0251 |
| 6 | 0.2404 | 0.0189 | 55.8000 | 2.7749 | 0.0490 | 0.0098 |
| 7 | 0.3276 | 0.0280 | 68.2000 | 2.3875 | 0.0272 | 0.0038 |
| 8 | 0.3293 | 0.0312 | 68.4000 | 2.5100 | 0.0272 | 0.0038 |
| 9 | 0.3293 | 0.0312 | 68.4000 | 2.5100 | 0.0272 | 0.0038 |
| 10 | 0.2530 | 0.0318 | 40.8000 | 1.9235 | 0.0749 | 0.0239 |

## 錯誤輸出

### 檢測發現與建議

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 1. 環境套件可載入，開始 06.13_[D]UMAP 多參數檢測。 |
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
