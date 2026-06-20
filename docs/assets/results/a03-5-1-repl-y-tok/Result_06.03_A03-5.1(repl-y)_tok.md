# BERTopic min_cluster_size 檢測報告 - 06.03_A03-5.1(repl-y)_tok

- 建立時間：2026-06-04 14:21:33 UTC
- 資料來源：`Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok_dataset`
- 使用欄位：`sentence`
- 原始筆數：31503
- 可用 documents：31503
- 文本長度：min=2, avg=86.6, max=676
- word_count：min=1, avg=15.2, max=142

## BERTopic 參數設定

| 參數 | 設定 | 統計/原因 |
| --- | --- | --- |
| Dataset | Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok_dataset | 31503 usable documents; text_col=sentence |
| Embedding Model | all-MiniLM-L6-v2 | 通用英文語意向量模型，與既有專案設定一致 |
| UMAP | n_neighbors=15, n_components=5, min_dist=0.0, metric=cosine, random_state=42 | 固定降維設定，讓不同 min_cluster_size 可比較 |
| HDBSCAN | metric=euclidean, cluster_selection_method=eom, prediction_data=True | 對固定 UMAP 結果測試 min_cluster_size；topic count 依 BERTopic 風格由大到小重編號 |
| CountVectorizer | custom stop_words=english + brand + model, ngram_range=(1, 2), min_df=2 | 最佳參數 BERTopic 訓練時使用，並在 c-TF-IDF/topic words 階段移除 brand、model |
| min_cluster_size 測試範圍 | 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 500, 600, 700, 800, 900, 1000 | 依使用者指定完整測試 |
| 最佳 min_cluster_size | 100 | n_clusters=4, noise_ratio=0.0070, topic -1 count=219, topic 0 count=30934, topic 1 count=136 |

## min_cluster_size 不同參數測試結果

> 註：主題 0/1 count 依 BERTopic 最終 topic id 邏輯統計；非離群群集會先按大小重編號，最大群集為 topic 0。

| min_cluster_size | n_clusters | noise_ratio | 主題 -1 count | 主題 0 count | 主題 1 count | 狀態 | 備註 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 79 | 0.5164 | 16269 | 1493 | 848 | ok | 完成 |
| 75 | 47 | 0.4875 | 15357 | 1643 | 1637 | ok | 完成 |
| 100 | 4 | 0.0070 | 219 | 30934 | 136 | ok | 完成 |
| 125 | 2 | 0.0147 | 463 | 30904 | 136 | ok | 完成 |
| 150 | 20 | 0.4513 | 14218 | 3390 | 2969 | ok | 完成 |
| 175 | 14 | 0.4494 | 14156 | 4367 | 3007 | ok | 完成 |
| 200 | 13 | 0.4297 | 13537 | 4340 | 3265 | ok | 完成 |
| 225 | 11 | 0.4549 | 14332 | 4290 | 3330 | ok | 完成 |
| 250 | 10 | 0.4723 | 14880 | 4408 | 3079 | ok | 完成 |
| 275 | 10 | 0.4863 | 15320 | 4400 | 3064 | ok | 完成 |
| 300 | 9 | 0.4548 | 14328 | 4391 | 3033 | ok | 完成 |
| 325 | 2 | 0.1790 | 5639 | 21463 | 4401 | ok | 完成 |
| 350 | 2 | 0.1879 | 5920 | 21260 | 4323 | ok | 完成 |
| 375 | 2 | 0.2180 | 6868 | 20398 | 4237 | ok | 完成 |
| 400 | 2 | 0.2206 | 6948 | 20301 | 4254 | ok | 完成 |
| 500 | 2 | 0.2237 | 7048 | 20316 | 4139 | ok | 完成 |
| 600 | 3 | 0.2712 | 8545 | 19844 | 2333 | ok | 完成 |
| 700 | 2 | 0.2302 | 7253 | 20172 | 4078 | ok | 完成 |
| 800 | 2 | 0.2599 | 8189 | 19395 | 3919 | ok | 完成 |
| 900 | 2 | 0.3082 | 9709 | 18330 | 3464 | ok | 完成 |
| 1000 | 2 | 0.2874 | 9055 | 19211 | 3237 | ok | 完成 |

## 測試結論

`min_cluster_size=100` 在本次掃描中離群值最低且保留有效主題。選擇規則為：優先選擇 n_clusters >= 2 且 noise_ratio 最低者；若並列，選 n_clusters 較多者，再選 min_cluster_size 較小者。
此設定的統計為 n_clusters=4、noise_ratio=0.0070、主題 -1 count=219、主題 0 count=30934、主題 1 count=136。

- 最佳參數 topic info CSV：`Result/06.03_A03_min-test/A03-5.1(repl-y)_tok/Result_06.03_A03-5.1(repl-y)_tok-best_topic_info.csv`
- 最佳參數 document-topic CSV：`Result/06.03_A03_min-test/A03-5.1(repl-y)_tok/Result_06.03_A03-5.1(repl-y)_tok-best_document_topics.csv`
- 完整 min_cluster_size CSV：`Result/06.03_A03_min-test/A03-5.1(repl-y)_tok/Result_06.03_A03-5.1(repl-y)_tok-min_cluster_size.csv`

## 錯誤輸出

### 檢測發現與建議
> 在運行過程中遇到的所有問題，用表格紀錄。

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 環境套件可載入，開始 BERTopic min_cluster_size 檢測。 |
| 前處理 | 有 1386 筆少於 3 words 的短句保留在測試中，可能增加離群值。 |
| BERTopic 停用詞 | CountVectorizer custom stop_words 已加入 brand、model；此設定作用於 c-TF-IDF/topic words 階段，不改動原始文本與 embeddings。 |
| Embedding | 偵測到既有 embeddings 快取，已直接共用。 |
| UMAP | 偵測到既有 UMAP 快取，已直接共用。 |

### 整體錯誤輸出
> 最後嘗試還是失敗，需要更改的功能。

無。BERTopic min_cluster_size 掃描已完成。

### 可改進
> 不影響流程，但改了可以讓流程更順，或讓結果更好的建議。

1. 短句比例可能影響 HDBSCAN 密度判斷，可測試排除少於 3 或 5 words 的句子後再比較 noise_ratio。
2. 本次參數掃描使用固定 embeddings 與固定 UMAP 結果，比較重點集中在 HDBSCAN min_cluster_size。
3. 最佳參數建議再搭配 topic words 與代表句人工審查，避免只用 noise_ratio 選到語意過寬的主題。
4. 若 noise_ratio 仍偏高，可測試 HDBSCAN min_samples、UMAP n_neighbors，或 BERTopic reduce_outliers。
