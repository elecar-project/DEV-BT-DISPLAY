# BERTopic UMAP + HDBSCAN 多參數檢測報告 - 06.03_A04-6(repl)_tok(para12-80)

## 0. 研究結論

- 是否改善 topic 過度集中：是。判斷依據為最佳平衡設定是否同時滿足 n_clusters >= 4、noise_ratio <= 0.35、largest_topic_ratio <= 0.60、top3_topic_ratio <= 0.85。
- 最低 noise 設定是否仍然不可用：是，最低 noise 設定仍有過度集中或主題數不足風險。
- 最佳平衡設定：UMAP(n_neighbors=5, n_components=5, min_dist=0.0); HDBSCAN(min_cluster_size=50, min_samples=5.0, method=eom, epsilon=0.2); n_clusters=40, noise_ratio=0.2838, largest_topic_ratio=0.0629, top3_topic_ratio=0.1733, balance_score=0.8724。
- 是否建議使用 para12-80 作為正式研究語料：建議，可進入正式語意檢查與人工命名。

## 1. Dataset 資訊

| dataset_dir | columns | text_col | title_col | source_rows | used_rows | empty_rows_count | short_rows_lt_3_words_count | min_text_len | max_text_len | avg_text_len | min_word_count | max_word_count | avg_word_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok(para12-80)_dataset | ['title', 'source_row', 'paragraph_id', 'sentence_start_id', 'sentence_end_id', 'sentence_count', 'sentence', 'word_count', 'char_count'] | sentence | title | 10978 | 10978 | 0 | 9 | 8 | 676 | 250.5139 | 2 | 142 | 43.6150 |

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
| 5 | 5 | 0.0000 | 50 | 10.0000 | 45 | 0.3621 | 0.0539 | 0.1419 | 0.9389 | 0.8622 |
| 10 | 15 | 0.0000 | 75 | 10.0000 | 27 | 0.3705 | 0.0698 | 0.1648 | 0.9320 | 0.8500 |
| 10 | 10 | 0.0000 | 75 | 10.0000 | 26 | 0.3566 | 0.0904 | 0.1989 | 0.9226 | 0.8394 |
| 15 | 5 | 0.0000 | 50 | 10.0000 | 40 | 0.4749 | 0.0540 | 0.1410 | 0.9268 | 0.8342 |
| 10 | 5 | 0.0000 | 75 | 10.0000 | 24 | 0.3880 | 0.0766 | 0.1943 | 0.9179 | 0.8293 |
| 75 | 15 | 0.0000 | 50 | 10.0000 | 29 | 0.5419 | 0.0422 | 0.1211 | 0.9218 | 0.8256 |
| 50 | 15 | 0.0000 | 50 | 30.0000 | 26 | 0.5226 | 0.0502 | 0.1394 | 0.9139 | 0.8239 |
| 75 | 10 | 0.0000 | 50 | 30.0000 | 25 | 0.5090 | 0.0610 | 0.1473 | 0.9042 | 0.8219 |
| 15 | 5 | 0.0000 | 75 | 10.0000 | 24 | 0.3739 | 0.0877 | 0.2334 | 0.8850 | 0.8211 |
| 30 | 5 | 0.0000 | 50 | 10.0000 | 29 | 0.4905 | 0.0733 | 0.1567 | 0.9069 | 0.8204 |
| 50 | 10 | 0.0000 | 50 | 30.0000 | 27 | 0.5036 | 0.0718 | 0.1625 | 0.8969 | 0.8165 |
| 10 | 15 | 0.0000 | 100 | 10.0000 | 22 | 0.4100 | 0.0698 | 0.1648 | 0.9445 | 0.8161 |
| 50 | 15 | 0.0000 | 50 | 10.0000 | 26 | 0.4806 | 0.0734 | 0.1930 | 0.8750 | 0.8155 |
| 30 | 15 | 0.0000 | 50 | 10.0000 | 29 | 0.4789 | 0.0856 | 0.1825 | 0.8875 | 0.8138 |
| 5 | 10 | 0.0000 | 50 | 10.0000 | 35 | 0.3727 | 0.1387 | 0.2238 | 0.8758 | 0.8135 |

## 4. 第二階段測試結果摘要

- 總列數: 13440
- 成功列數: 13440

| umap_n_neighbors | umap_n_components | umap_min_dist | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | n_clusters | noise_ratio | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.2000 | 40 | 0.2838 | 0.0629 | 0.1733 | 0.9225 | 0.8724 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.2000 | 40 | 0.2838 | 0.0629 | 0.1733 | 0.9225 | 0.8724 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.0000 | 44 | 0.3060 | 0.0629 | 0.1733 | 0.9241 | 0.8669 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.0500 | 44 | 0.3060 | 0.0629 | 0.1733 | 0.9241 | 0.8669 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | eom | 0.1000 | 44 | 0.3060 | 0.0629 | 0.1733 | 0.9241 | 0.8669 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.1000 | 57 | 0.4427 | 0.0251 | 0.0721 | 0.9741 | 0.8661 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.0500 | 57 | 0.4427 | 0.0251 | 0.0721 | 0.9741 | 0.8661 |
| 5 | 5 | 0.0000 | 50 | 5.0000 | leaf | 0.0000 | 57 | 0.4427 | 0.0251 | 0.0721 | 0.9741 | 0.8661 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | eom | 0.2000 | 44 | 0.3533 | 0.0539 | 0.1419 | 0.9382 | 0.8644 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | leaf | 0.1000 | 53 | 0.4570 | 0.0233 | 0.0664 | 0.9737 | 0.8643 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | leaf | 0.0000 | 53 | 0.4570 | 0.0233 | 0.0664 | 0.9737 | 0.8643 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | leaf | 0.0500 | 53 | 0.4570 | 0.0233 | 0.0664 | 0.9737 | 0.8643 |
| 5 | 5 | 0.0000 | 75 | 5.0000 | leaf | 0.2000 | 31 | 0.3223 | 0.0629 | 0.1733 | 0.9321 | 0.8628 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | eom | 0.0000 | 45 | 0.3621 | 0.0539 | 0.1419 | 0.9389 | 0.8622 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | eom | 0.0500 | 45 | 0.3621 | 0.0539 | 0.1419 | 0.9389 | 0.8622 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | eom | 0.1000 | 45 | 0.3621 | 0.0539 | 0.1419 | 0.9389 | 0.8622 |
| 5 | 5 | 0.0000 | 50 | 10.0000 | leaf | 0.2000 | 46 | 0.3819 | 0.0539 | 0.1196 | 0.9491 | 0.8617 |
| 5 | 5 | 0.0000 | 50 | 15.0000 | leaf | 0.0500 | 53 | 0.4876 | 0.0230 | 0.0664 | 0.9713 | 0.8567 |
| 5 | 5 | 0.0000 | 50 | 15.0000 | leaf | 0.0000 | 53 | 0.4876 | 0.0230 | 0.0664 | 0.9713 | 0.8567 |
| 5 | 5 | 0.0000 | 50 | 15.0000 | leaf | 0.1000 | 53 | 0.4876 | 0.0230 | 0.0664 | 0.9713 | 0.8567 |

## 5. 最低 noise 設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lowest_noise | 最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。 | stage2 | 75 | 10 | 0.0000 | cosine | 42 | 50 | 5.0000 | eom | 0.0000 | euclidean | ok | 完成 | 2 | 0.0000 | 0 | 63 | 10915 | 10915 | 0.9943 | 1.0000 | 0.0510 | 0.2680 |

## 6. 最多有效主題設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| most_topics | 在可接受 noise_ratio 下保留最多有效主題。 | stage2 | 5 | 5 | 0.0000 | cosine | 42 | 50 | 5.0000 | leaf | 0.0000 | euclidean | ok | 完成 | 57 | 0.4427 | 4860 | 72 | 70 | 276 | 0.0251 | 0.0721 | 0.9741 | 0.8661 |

## 7. 最佳平衡設定

| selection_label | selection_reason | stage | umap_n_neighbors | umap_n_components | umap_min_dist | umap_metric | umap_random_state | hdbscan_min_cluster_size | hdbscan_min_samples | hdbscan_cluster_selection_method | hdbscan_cluster_selection_epsilon | hdbscan_metric | status | note | n_clusters | noise_ratio | topic_-1_count | topic_0_count | topic_1_count | largest_topic_count | largest_topic_ratio | top3_topic_ratio | topic_entropy | balance_score |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| best_balance | 符合原始平衡條件後取最高 balance_score。 | stage2 | 5 | 5 | 0.0000 | cosine | 42 | 50 | 5.0000 | eom | 0.2000 | euclidean | ok | 完成 | 40 | 0.2838 | 3116 | 72 | 70 | 690 | 0.0629 | 0.1733 | 0.9225 | 0.8724 |

## 8. 為什麼不只用 min_cluster_size 判斷

只調整 min_cluster_size 會把問題壓縮成單一維度：降低 noise_ratio 時容易讓大量文本被併入少數大主題；追求較多主題時又可能導致 noise_ratio 上升。UMAP 的 n_neighbors、n_components、min_dist 會改變語意向量在低維空間中的局部/全域結構，HDBSCAN 的 min_samples、cluster_selection_method 與 epsilon 會改變保守程度與群集切分方式。因此本次以 balance_score 同時納入 noise、主題數、最大主題集中度與前三主題集中度，避免只選到低 noise 但不可解釋的過度集中結果。

## 9. 各圖表連結

- [min_cluster_size_dual_axis.png](charts/min_cluster_size_dual_axis.png)
- [largest_topic_ratio_parameter_comparison.png](charts/largest_topic_ratio_parameter_comparison.png)
- [min_samples_noise_ratio.png](charts/min_samples_noise_ratio.png)
- [n_neighbors_largest_topic_ratio.png](charts/n_neighbors_largest_topic_ratio.png)
- [n_components_n_clusters.png](charts/n_components_n_clusters.png)
- [best_three_topic_size_distribution.png](charts/best_three_topic_size_distribution.png)
- [parameter_heatmap.png](charts/parameter_heatmap.png)
- [best_balance_topic_size_bar.png](charts/best_balance_topic_size_bar.png)
- [best_three_comparison.png](charts/best_three_comparison.png)

## 10. 最終 BERTopic 訓練輸出

| balance_score | document_topics | final_config | largest_topic_ratio | n_clusters | noise_ratio | output_dir | representative_docs | selection_label | selection_reason | status | top3_topic_ratio | topic_entropy | topic_info | topic_info_rows | topic_size_distribution | topic_words |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.2680 | final_models/lowest_noise/document_topics.csv | final_models/lowest_noise/final_config.json | 0.9943 | 2 | 0.0000 | final_models/lowest_noise | final_models/lowest_noise/representative_docs.csv | lowest_noise | 最低 noise_ratio，並以較低 largest_topic_ratio 與較高 n_clusters 作為 tie-break。 | ok | 1.0000 | 0.0510 | final_models/lowest_noise/topic_info.csv | 2 | final_models/lowest_noise/topic_size_distribution.csv | final_models/lowest_noise/topic_words.csv |
| 0.8661 | final_models/most_topics/document_topics.csv | final_models/most_topics/final_config.json | 0.0251 | 57 | 0.4427 | final_models/most_topics | final_models/most_topics/representative_docs.csv | most_topics | 在可接受 noise_ratio 下保留最多有效主題。 | ok | 0.0721 | 0.9741 | final_models/most_topics/topic_info.csv | 58 | final_models/most_topics/topic_size_distribution.csv | final_models/most_topics/topic_words.csv |
| 0.8724 | final_models/best_balance/document_topics.csv | final_models/best_balance/final_config.json | 0.0629 | 40 | 0.2838 | final_models/best_balance | final_models/best_balance/representative_docs.csv | best_balance | 符合原始平衡條件後取最高 balance_score。 | ok | 0.1733 | 0.9225 | final_models/best_balance/topic_info.csv | 41 | final_models/best_balance/topic_size_distribution.csv | final_models/best_balance/topic_words.csv |

- final_configs.json: `final_configs.json`
- comparison_summary.csv: `comparison_summary.csv`
- combined topic_info.csv: `topic_info.csv`
- combined document_topics.csv: `document_topics.csv`
- combined representative_docs.csv: `representative_docs.csv`
- combined topic_words.csv: `topic_words.csv`
- all_results.csv: `Result_06.03_A04-6(repl)_tok(para12-80)-all_results.csv`

## 11. 穩定性檢測摘要

| stability_rank | noise_ratio_mean | noise_ratio_std | n_clusters_mean | n_clusters_std | largest_topic_ratio_mean | largest_topic_ratio_std |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 0.2928 | 0.0101 | 41.4000 | 1.9494 | 0.0637 | 0.0130 |
| 2 | 0.2841 | 0.0084 | 40.4000 | 2.3022 | 0.0793 | 0.0175 |
| 3 | 0.3197 | 0.0259 | 47.6000 | 5.0299 | 0.0709 | 0.0226 |
| 4 | 0.3197 | 0.0259 | 47.6000 | 5.0299 | 0.0709 | 0.0226 |
| 5 | 0.3197 | 0.0259 | 47.6000 | 5.0299 | 0.0709 | 0.0226 |
| 6 | 0.4304 | 0.0147 | 60.0000 | 2.5495 | 0.0275 | 0.0032 |
| 7 | 0.4304 | 0.0147 | 60.0000 | 2.5495 | 0.0275 | 0.0032 |
| 8 | 0.4304 | 0.0147 | 60.0000 | 2.5495 | 0.0275 | 0.0032 |
| 9 | 0.3628 | 0.0267 | 43.2000 | 4.3243 | 0.0696 | 0.0179 |
| 10 | 0.4754 | 0.0167 | 55.8000 | 2.3875 | 0.0253 | 0.0031 |

## 錯誤輸出

### 檢測發現與建議

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 1. 環境套件可載入，開始 A04 UMAP + HDBSCAN 多參數檢測。 |
| 資料載入 | 1. 有 9 筆少於 3 words 的短句保留，可能增加離群值。 |
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
