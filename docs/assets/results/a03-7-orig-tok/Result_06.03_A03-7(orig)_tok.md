# BERTopic min_cluster_size 檢測報告 - 06.03_A03-7(orig)_tok

- 建立時間：2026-06-03 02:48:23 UTC
- 資料來源：`Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok_dataset`
- 使用欄位：`sentence`
- 原始筆數：31883
- 可用 documents：31883
- 文本長度：min=2, avg=86.4, max=2044
- word_count：min=1, avg=15.2, max=389

## BERTopic 參數設定

| 參數 | 設定 | 統計/原因 |
| --- | --- | --- |
| Dataset | Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok_dataset | 31883 usable documents; text_col=sentence |
| Embedding Model | all-MiniLM-L6-v2 | 通用英文語意向量模型，與既有專案設定一致 |
| UMAP | n_neighbors=15, n_components=5, min_dist=0.0, metric=cosine, random_state=42 | 固定降維設定，讓不同 min_cluster_size 可比較 |
| HDBSCAN | metric=euclidean, cluster_selection_method=eom, prediction_data=True | 對固定 UMAP 結果測試 min_cluster_size |
| CountVectorizer | stop_words=english, ngram_range=(1, 2), min_df=2 | 最佳參數 BERTopic 訓練時使用，降低極低頻詞干擾 |
| min_cluster_size 測試範圍 | 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 500, 600, 700, 800, 900, 1000 | 依使用者指定完整測試 |
| 最佳 min_cluster_size | 175 | n_clusters=2, noise_ratio=0.0143, topic -1 count=455, topic 0 count=374, topic 1 count=31054 |

## min_cluster_size 不同參數測試結果

| min_cluster_size | n_clusters | noise_ratio | 主題 -1 count | 主題 0 count | 主題 1 count | 狀態 | 備註 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 96 | 0.4677 | 14911 | 111 | 51 | ok | 完成 |
| 75 | 63 | 0.4747 | 15134 | 111 | 113 | ok | 完成 |
| 100 | 48 | 0.4580 | 14604 | 111 | 374 | ok | 完成 |
| 125 | 39 | 0.4999 | 15939 | 374 | 144 | ok | 完成 |
| 150 | 26 | 0.4597 | 14656 | 374 | 156 | ok | 完成 |
| 175 | 2 | 0.0143 | 455 | 374 | 31054 | ok | 完成 |
| 200 | 2 | 0.0158 | 505 | 374 | 31004 | ok | 完成 |
| 225 | 2 | 0.0167 | 534 | 374 | 30975 | ok | 完成 |
| 250 | 2 | 0.0168 | 535 | 374 | 30974 | ok | 完成 |
| 275 | 2 | 0.0168 | 535 | 374 | 30974 | ok | 完成 |
| 300 | 2 | 0.0173 | 550 | 374 | 30959 | ok | 完成 |
| 325 | 2 | 0.0173 | 552 | 374 | 30957 | ok | 完成 |
| 350 | 2 | 0.0189 | 603 | 374 | 30906 | ok | 完成 |
| 375 | 3 | 0.1453 | 4633 | 389 | 634 | ok | 完成 |
| 400 | 3 | 0.1715 | 5468 | 631 | 546 | ok | 完成 |
| 500 | 2 | 0.1928 | 6147 | 611 | 25125 | ok | 完成 |
| 600 | 4 | 0.6495 | 20707 | 2676 | 5309 | ok | 完成 |
| 700 | 4 | 0.6806 | 21700 | 2402 | 4951 | ok | 完成 |
| 800 | 3 | 0.6313 | 20128 | 1911 | 5765 | ok | 完成 |
| 900 | 3 | 0.6701 | 21365 | 5636 | 1029 | ok | 完成 |
| 1000 | 2 | 0.6949 | 22154 | 5159 | 4570 | ok | 完成 |

## 測試結論

`min_cluster_size=175` 在本次掃描中離群值最低且保留有效主題。選擇規則為：優先選擇 n_clusters >= 2 且 noise_ratio 最低者；若並列，選 n_clusters 較多者，再選 min_cluster_size 較小者。
此設定的統計為 n_clusters=2、noise_ratio=0.0143、主題 -1 count=455、主題 0 count=374、主題 1 count=31054。

- 最佳參數 topic info CSV：`Result/06.03_A03_min-test/A03-7(orig)_tok/Result_06.03_A03-7(orig)_tok-best_topic_info.csv`
- 最佳參數 document-topic CSV：`Result/06.03_A03_min-test/A03-7(orig)_tok/Result_06.03_A03-7(orig)_tok-best_document_topics.csv`
- 完整 min_cluster_size CSV：`Result/06.03_A03_min-test/A03-7(orig)_tok/Result_06.03_A03-7(orig)_tok-min_cluster_size.csv`

## 錯誤輸出

### 檢測發現與建議
> 在運行過程中遇到的所有問題，用表格紀錄。

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 環境套件可載入，開始 BERTopic min_cluster_size 檢測。 |
| 前處理 | 有 1471 筆少於 3 words 的短句保留在測試中，可能增加離群值。 |

### 整體錯誤輸出
> 最後嘗試還是失敗，需要更改的功能。

無。BERTopic min_cluster_size 掃描已完成。

### 可改進
> 不影響流程，但改了可以讓流程更順，或讓結果更好的建議。

1. 短句比例可能影響 HDBSCAN 密度判斷，可測試排除少於 3 或 5 words 的句子後再比較 noise_ratio。
2. 本次參數掃描使用固定 embeddings 與固定 UMAP 結果，比較重點集中在 HDBSCAN min_cluster_size。
3. 最佳參數建議再搭配 topic words 與代表句人工審查，避免只用 noise_ratio 選到語意過寬的主題。
4. 若 noise_ratio 仍偏高，可測試 HDBSCAN min_samples、UMAP n_neighbors，或 BERTopic reduce_outliers。
