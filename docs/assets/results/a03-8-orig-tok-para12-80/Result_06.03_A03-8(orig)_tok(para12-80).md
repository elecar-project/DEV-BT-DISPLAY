# BERTopic min_cluster_size 檢測報告 - 06.03_A03-8(orig)_tok(para12-80)

- 建立時間：2026-06-03 03:02:22 UTC
- 資料來源：`Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset`
- 使用欄位：`sentence`
- 原始筆數：11136
- 可用 documents：11136
- 文本長度：min=4, avg=249.1, max=2044
- word_count：min=1, avg=43.4, max=389

## BERTopic 參數設定

| 參數 | 設定 | 統計/原因 |
| --- | --- | --- |
| Dataset | Result/06.03_A02/R06.03_A02-pre_LLM(orig)_tok(para12-80)_dataset | 11136 usable documents; text_col=sentence |
| Embedding Model | all-MiniLM-L6-v2 | 通用英文語意向量模型，與既有專案設定一致 |
| UMAP | n_neighbors=15, n_components=5, min_dist=0.0, metric=cosine, random_state=42 | 固定降維設定，讓不同 min_cluster_size 可比較 |
| HDBSCAN | metric=euclidean, cluster_selection_method=eom, prediction_data=True | 對固定 UMAP 結果測試 min_cluster_size |
| CountVectorizer | stop_words=english, ngram_range=(1, 2), min_df=2 | 最佳參數 BERTopic 訓練時使用，降低極低頻詞干擾 |
| min_cluster_size 測試範圍 | 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 500, 600, 700, 800, 900, 1000 | 依使用者指定完整測試 |
| 最佳 min_cluster_size | 200 | n_clusters=2, noise_ratio=0.0515, topic -1 count=574, topic 0 count=254, topic 1 count=10308 |

## min_cluster_size 不同參數測試結果

| min_cluster_size | n_clusters | noise_ratio | 主題 -1 count | 主題 0 count | 主題 1 count | 狀態 | 備註 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 41 | 0.4084 | 4548 | 254 | 204 | ok | 完成 |
| 75 | 27 | 0.4285 | 4772 | 254 | 204 | ok | 完成 |
| 100 | 18 | 0.3976 | 4428 | 254 | 204 | ok | 完成 |
| 125 | 14 | 0.4177 | 4652 | 254 | 204 | ok | 完成 |
| 150 | 3 | 0.0565 | 629 | 254 | 204 | ok | 完成 |
| 175 | 3 | 0.0578 | 644 | 254 | 204 | ok | 完成 |
| 200 | 2 | 0.0515 | 574 | 254 | 10308 | ok | 完成 |
| 225 | 2 | 0.0767 | 854 | 254 | 10028 | ok | 完成 |
| 250 | 2 | 0.1052 | 1171 | 254 | 9711 | ok | 完成 |
| 275 | 2 | 0.2923 | 3255 | 408 | 7473 | ok | 完成 |
| 300 | 2 | 0.3087 | 3438 | 393 | 7305 | ok | 完成 |
| 325 | 2 | 0.3284 | 3657 | 7107 | 372 | ok | 完成 |
| 350 | 2 | 0.3374 | 3757 | 393 | 6986 | ok | 完成 |
| 375 | 2 | 0.3380 | 3764 | 430 | 6942 | ok | 完成 |
| 400 | 2 | 0.3510 | 3909 | 406 | 6821 | ok | 完成 |
| 500 | 0 | 1.0000 | 11136 | 0 | 0 | ok | 完成 |
| 600 | 0 | 1.0000 | 11136 | 0 | 0 | ok | 完成 |
| 700 | 0 | 1.0000 | 11136 | 0 | 0 | ok | 完成 |
| 800 | 0 | 1.0000 | 11136 | 0 | 0 | ok | 完成 |
| 900 | 0 | 1.0000 | 11136 | 0 | 0 | ok | 完成 |
| 1000 | 0 | 1.0000 | 11136 | 0 | 0 | ok | 完成 |

## 測試結論

`min_cluster_size=200` 在本次掃描中離群值最低且保留有效主題。選擇規則為：優先選擇 n_clusters >= 2 且 noise_ratio 最低者；若並列，選 n_clusters 較多者，再選 min_cluster_size 較小者。
此設定的統計為 n_clusters=2、noise_ratio=0.0515、主題 -1 count=574、主題 0 count=254、主題 1 count=10308。

- 最佳參數 topic info CSV：`Result/06.03_A03_min-test/A03-8(orig)_tok(para12-80)/Result_06.03_A03-8(orig)_tok(para12-80)-best_topic_info.csv`
- 最佳參數 document-topic CSV：`Result/06.03_A03_min-test/A03-8(orig)_tok(para12-80)/Result_06.03_A03-8(orig)_tok(para12-80)-best_document_topics.csv`
- 完整 min_cluster_size CSV：`Result/06.03_A03_min-test/A03-8(orig)_tok(para12-80)/Result_06.03_A03-8(orig)_tok(para12-80)-min_cluster_size.csv`

## 錯誤輸出

### 檢測發現與建議
> 在運行過程中遇到的所有問題，用表格紀錄。

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 環境套件可載入，開始 BERTopic min_cluster_size 檢測。 |
| 前處理 | 有 14 筆少於 3 words 的短句保留在測試中，可能增加離群值。 |

### 整體錯誤輸出
> 最後嘗試還是失敗，需要更改的功能。

無。BERTopic min_cluster_size 掃描已完成。

### 可改進
> 不影響流程，但改了可以讓流程更順，或讓結果更好的建議。

1. 短句比例可能影響 HDBSCAN 密度判斷，可測試排除少於 3 或 5 words 的句子後再比較 noise_ratio。
2. 本次參數掃描使用固定 embeddings 與固定 UMAP 結果，比較重點集中在 HDBSCAN min_cluster_size。
3. 最佳參數建議再搭配 topic words 與代表句人工審查，避免只用 noise_ratio 選到語意過寬的主題。
4. 若 noise_ratio 仍偏高，可測試 HDBSCAN min_samples、UMAP n_neighbors，或 BERTopic reduce_outliers。
