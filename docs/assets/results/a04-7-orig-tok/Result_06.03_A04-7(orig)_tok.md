# BERTopic UMAP + HDBSCAN 多參數檢測報告 - 06.03_A04-7(orig)_tok

## 1. Dataset 資訊

| dataset_dir | columns | text_col | title_col | source_rows | used_rows | empty_rows_count | short_rows_lt_3_words_count | min_text_len | max_text_len | avg_text_len | min_word_count | max_word_count | avg_word_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok_dataset | ['title', 'source_row', 'sentence_id', 'sentence', 'word_count', 'char_count'] | sentence | title | 31883 | 31883 | 0 | 1471 | 2 | 2044 | 86.3609 | 1 | 389 | 15.1587 |

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
| 5 | 5 | 0.0000 | 50 | 10.0000 | 154 | 0.3513 | 0.0229 | 0.0646 | 0.9479 | 0.8748 |
| 5 | 15 | 0.0000 | 50 | 10.0000 | 147 | 0.3417 | 0.0328 | 0.0857 | 0.9383 | 0.8705 |
| 10 | 15 | 0.0000 | 50 | 10.0000 | 131 | 0.3547 | 0.0282 | 0.0733 | 0.9339 | 0.8705 |
| 10 | 10 | 0.0000 | 50 | 10.0000 | 128 | 0.3544 | 0.0294 | 0.0754 | 0.9335 | 0.8698 |
| 5 | 5 | 0.0000 | 75 | 10.0000 | 97 | 0.3656 | 0.0296 | 0.0734 | 0.9469 | 0.8668 |
| 5 | 10 | 0.0500 | 50 | 10.0000 | 134 | 0.3716 | 0.0257 | 0.0724 | 0.9402 | 0.8663 |
| 5 | 10 | 0.0000 | 50 | 10.0000 | 144 | 0.3495 | 0.0425 | 0.0826 | 0.9388 | 0.8659 |
| 10 | 15 | 0.0000 | 75 | 10.0000 | 91 | 0.3560 | 0.0373 | 0.0867 | 0.9368 | 0.8647 |
| 10 | 5 | 0.0000 | 50 | 10.0000 | 136 | 0.3510 | 0.0465 | 0.0862 | 0.9380 | 0.8635 |
| 10 | 15 | 0.0500 | 50 | 10.0000 | 119 | 0.3811 | 0.0273 | 0.0705 | 0.9352 | 0.8634 |
| 15 | 5 | 0.0000 | 50 | 10.0000 | 134 | 0.3735 | 0.0308 | 0.0809 | 0.9356 | 0.8625 |
| 10 | 10 | 0.0000 | 75 | 10.0000 | 92 | 0.3759 | 0.0294 | 0.0797 | 0.9411 | 0.8625 |
| 5 | 15 | 0.0000 | 75 | 10.0000 | 96 | 0.3900 | 0.0236 | 0.0682 | 0.9509 | 0.8623 |
| 5 | 10 | 0.1000 | 50 | 10.0000 | 125 | 0.3956 | 0.0223 | 0.0636 | 0.9394 | 0.8619 |
| 15 | 10 | 0.0000 | 50 | 10.0000 | 128 | 0.3835 | 0.0295 | 0.0771 | 0.9361 | 0.8607 |

## 4. 第二階段測試結果摘要

- 總列數: 13440
- 成功列數: 13440

| umap_n_neighbors | umap_n_components | umap_min_dist | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | n_clusters | noise_ratio | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 10 | 0.0000 | 50 | 10.0000 | leaf | 0.2000 | 130 | 0.3136 | 0.0301 | 0.0768 | 0.9325 | 0.8815 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 163 | 0.3343 | 0.0238 | 0.0621 | 0.9517 | 0.8801 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 163 | 0.3343 | 0.0238 | 0.0621 | 0.9517 | 0.8801 |
| 5 | 10 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 163 | 0.3343 | 0.0238 | 0.0621 | 0.9517 | 0.8801 |
| 10 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 133 | 0.3184 | 0.0298 | 0.0772 | 0.9348 | 0.8801 |
| 10 | 5 | 0.0000 | 50 | 10.0000 | eom | 0.2000 | 89 | 0.2687 | 0.0465 | 0.1269 | 0.8835 | 0.8801 |
| 10 | 5 | 0.0000 | 50 | 10.0000 | leaf | 0.2000 | 89 | 0.2687 | 0.0465 | 0.1269 | 0.8835 | 0.8801 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 157 | 0.3236 | 0.0271 | 0.0756 | 0.9465 | 0.8797 |
| 10 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 135 | 0.3206 | 0.0298 | 0.0772 | 0.9344 | 0.8794 |
| 10 | 15 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 135 | 0.3206 | 0.0298 | 0.0772 | 0.9344 | 0.8794 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 159 | 0.3262 | 0.0271 | 0.0756 | 0.9464 | 0.8789 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 160 | 0.3271 | 0.0271 | 0.0756 | 0.9460 | 0.8786 |
| 5 | 15 | 0.0000 | 50 | 10.0000 | leaf | 0.2000 | 136 | 0.3272 | 0.0299 | 0.0784 | 0.9353 | 0.8772 |
| 5 | 10 | 0.0000 | 50 | 10.0000 | eom | 0.2000 | 127 | 0.3051 | 0.0425 | 0.0932 | 0.9244 | 0.8771 |
| 5 | 10 | 0.0500 | 50 | 5.0000 | eom | 0.2000 | 130 | 0.3072 | 0.0416 | 0.0943 | 0.9220 | 0.8765 |
| 5 | 15 | 0.0000 | 50 | 5.0000 | leaf | 0.1000 | 165 | 0.3667 | 0.0159 | 0.0438 | 0.9638 | 0.8765 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.1000 | 165 | 0.3617 | 0.0191 | 0.0474 | 0.9634 | 0.8763 |
| 10 | 15 | 0.0000 | 50 | 10.0000 | eom | 0.2000 | 101 | 0.3042 | 0.0376 | 0.1070 | 0.8962 | 0.8760 |
| 10 | 15 | 0.0000 | 50 | 10.0000 | leaf | 0.2000 | 101 | 0.3042 | 0.0376 | 0.1070 | 0.8962 | 0.8760 |
| 5 | 15 | 0.0000 | 50 | 10.0000 | eom | 0.2000 | 135 | 0.3235 | 0.0328 | 0.0857 | 0.9318 | 0.8760 |

## 5. 最低 noise 設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lowest_noise | 最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。 | stage2 | 15 | 5 | 0.0000 | cosine | 42 | 300 | 50.0000 | eom | 0.0000 | euclidean | ok | 完成 | 2 | 0.0084 | 267 | 550 | 31066 | 31066 | 0.9744 | 0.9916 | 0.1266 | 0.3202 |

## 6. 最多有效主題設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| most_topics | 在可接受 noise_ratio 下保留最多有效主題。 | stage2 | 5 | 10 | 0.0000 | cosine | 42 | 50 | 5.0000 | leaf | 0.0000 | euclidean | ok | 完成 | 183 | 0.3943 | 12573 | 82 | 97 | 478 | 0.0150 | 0.0390 | 0.9719 | 0.8694 |

## 7. 最佳平衡設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| best_balance | 符合嚴格平衡條件後取最高 balance_score。 | stage2 | 5 | 10 | 0.0000 | cosine | 42 | 50 | 10.0000 | leaf | 0.2000 | euclidean | ok | 完成 | 130 | 0.3136 | 9999 | 82 | 139 | 959 | 0.0301 | 0.0768 | 0.9325 | 0.8815 |

## 8. 為什麼不只用 min_cluster_size 判斷

只調整 min_cluster_size 會把問題壓縮成單一維度：降低 noise_ratio 時容易讓大量文本被併入少數大主題；追求較多主題時又可能導致 noise_ratio 上升。UMAP 的 n_neighbors、n_components、min_dist 會改變語意向量在低維空間中的局部/全域結構，HDBSCAN 的 min_samples、cluster_selection_method 與 epsilon 會改變保守程度與群集切分方式。因此本次以 balance_score 同時納入 noise、主題數、最大主題集中度與前三主題集中度，避免只選到低 noise 但不可解釋的過度集中結果。

## 9. 與 A03-7 比較與建議

- A03-7 最低 noise 設定: min_cluster_size=175, n_clusters=2, noise_ratio=0.0143, 估計最大主題集中度=0.9740。
- A04-7 最佳平衡設定: n_clusters=130, noise_ratio=0.3136, largest_topic_ratio=0.0301, top3_topic_ratio=0.0768, balance_score=0.8815。
- 是否更平衡: 是。A04-7 最佳平衡設定把有效主題數從 A03-7 的 2 個提高到 130 個，雖然 noise_ratio 從 0.0143 上升到 0.3136，但仍符合本次嚴格條件 noise_ratio <= 0.35，且主題分布不再被單一大主題支配。
- 是否成功降低最大主題集中度: 是。A03-7 估計最大主題集中度約 0.9740，A04-7 最佳平衡設定降到 0.0301，前三大主題集中度也只有 0.0768；這是本次相對 A03-7 最明確的改善。
- 是否建議保留原始品牌車款詞彙進入 BERTopic: 建議保留一版原始品牌/車款詞彙作為主分析或對照分析，因為汽車文本中的品牌、車款、平台與動力系統詞常是語意聚類的重要錨點；但若研究問題聚焦於跨品牌敘事框架，則可另跑刪除/替換版避免品牌詞支配 topic words。

## 10. 各圖表連結

- [parameter_heatmap.png](charts/parameter_heatmap.png)
- [min_cluster_size_dual_axis.png](charts/min_cluster_size_dual_axis.png)
- [min_samples_noise_ratio.png](charts/min_samples_noise_ratio.png)
- [n_neighbors_largest_topic_ratio.png](charts/n_neighbors_largest_topic_ratio.png)
- [n_components_n_clusters.png](charts/n_components_n_clusters.png)
- [cluster_selection_method_comparison.png](charts/cluster_selection_method_comparison.png)
- [best_balance_topic_size_bar.png](charts/best_balance_topic_size_bar.png)
- [best_three_comparison.png](charts/best_three_comparison.png)
- [best_three_topic_size_distribution.png](charts/best_three_topic_size_distribution.png)

## 11. 最終 BERTopic 訓練輸出

| document_topics_csv | n_topics_including_noise | output_dir | representative_docs_csv | selection_label | status | topic_info_csv | topic_info_rows | topic_words_csv |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| final_models/lowest_noise/document_topics.csv | 3 | final_models/lowest_noise | final_models/lowest_noise/representative_docs.csv | lowest_noise | ok | final_models/lowest_noise/topic_info.csv | 3 | final_models/lowest_noise/topic_words.csv |
| final_models/most_topics/document_topics.csv | 177 | final_models/most_topics | final_models/most_topics/representative_docs.csv | most_topics | ok | final_models/most_topics/topic_info.csv | 177 | final_models/most_topics/topic_words.csv |
| final_models/best_balance/document_topics.csv | 134 | final_models/best_balance | final_models/best_balance/representative_docs.csv | best_balance | ok | final_models/best_balance/topic_info.csv | 134 | final_models/best_balance/topic_words.csv |

## 12. 穩定性檢測摘要

| stability_rank | noise_ratio_mean | noise_ratio_std | n_clusters_mean | n_clusters_std | largest_topic_ratio_mean | largest_topic_ratio_std |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.3020 | 0.0152 | 134.4000 | 3.0496 | 0.0316 | 0.0043 |
| 2 | 0.3172 | 0.0158 | 162.6000 | 2.3022 | 0.0286 | 0.0080 |
| 3 | 0.3172 | 0.0158 | 162.6000 | 2.3022 | 0.0286 | 0.0080 |
| 4 | 0.3168 | 0.0155 | 162.0000 | 2.5495 | 0.0286 | 0.0080 |
| 5 | 0.3320 | 0.0088 | 135.8000 | 5.6303 | 0.0326 | 0.0037 |
| 6 | 0.2587 | 0.0128 | 87.8000 | 5.2631 | 0.0706 | 0.0177 |
| 7 | 0.2587 | 0.0129 | 88.0000 | 5.0990 | 0.0706 | 0.0177 |
| 8 | 0.3023 | 0.0170 | 155.4000 | 7.6354 | 0.0319 | 0.0092 |
| 9 | 0.3346 | 0.0082 | 137.8000 | 5.1672 | 0.0326 | 0.0037 |
| 10 | 0.3346 | 0.0082 | 137.8000 | 5.1672 | 0.0326 | 0.0037 |

## 錯誤輸出

### 檢測發現與建議

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 1. 環境套件可載入，開始 A04 UMAP + HDBSCAN 多參數檢測。 |
| 資料載入 | 1. 有 1471 筆少於 3 words 的短句保留，可能增加離群值。 |
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
