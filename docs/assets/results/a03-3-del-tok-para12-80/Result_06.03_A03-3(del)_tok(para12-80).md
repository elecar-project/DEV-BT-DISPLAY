# BERTopic min_cluster_size 檢測報告 - 06.03_A03-3(del)_tok(para12-80)

- 建立時間：2026-06-03 02:02:19 UTC
- 資料來源：`Result/06.03_A02/R06.03_A02-pre_LLM(del)_tok(para12-80)_dataset`
- 使用欄位：`sentence`
- 原始筆數：10945
- 可用 documents：10945
- 文本長度：min=4, avg=246.0, max=664
- word_count：min=1, avg=42.9, max=142

## BERTopic 參數設定

| 參數 | 設定 | 統計/原因 |
| --- | --- | --- |
| Dataset | Result/06.03_A02/R06.03_A02-pre_LLM(del)_tok(para12-80)_dataset | 10945 usable documents; text_col=sentence |
| Embedding Model | all-MiniLM-L6-v2 | 通用英文語意向量模型，與既有專案設定一致 |
| UMAP | n_neighbors=15, n_components=5, min_dist=0.0, metric=cosine, random_state=42 | 固定降維設定，讓不同 min_cluster_size 可比較 |
| HDBSCAN | metric=euclidean, cluster_selection_method=eom, prediction_data=True | 對固定 UMAP 結果測試 min_cluster_size |
| CountVectorizer | stop_words=english, ngram_range=(1, 2), min_df=2 | 最佳參數 BERTopic 訓練時使用，降低極低頻詞干擾 |
| min_cluster_size 測試範圍 | 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 500, 600, 700, 800, 900, 1000 | 依使用者指定完整測試 |
| 最佳 min_cluster_size | 50 | n_clusters=3, noise_ratio=0.0112, topic -1 count=123, topic 0 count=71, topic 1 count=67 |

## min_cluster_size 不同參數測試結果

| min_cluster_size | n_clusters | noise_ratio | 主題 -1 count | 主題 0 count | 主題 1 count | 狀態 | 備註 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 3 | 0.0112 | 123 | 71 | 67 | ok | 完成 |
| 75 | 2 | 0.0726 | 795 | 91 | 10059 | ok | 完成 |
| 100 | 10 | 0.4321 | 4729 | 225 | 337 | ok | 完成 |
| 125 | 7 | 0.4111 | 4499 | 163 | 333 | ok | 完成 |
| 150 | 6 | 0.3759 | 4114 | 520 | 334 | ok | 完成 |
| 175 | 5 | 0.3423 | 3746 | 1391 | 4451 | ok | 完成 |
| 200 | 5 | 0.3545 | 3880 | 1375 | 4360 | ok | 完成 |
| 225 | 5 | 0.3885 | 4252 | 1340 | 4172 | ok | 完成 |
| 250 | 4 | 0.3783 | 4141 | 1325 | 3988 | ok | 完成 |
| 275 | 3 | 0.3825 | 4186 | 1324 | 1499 | ok | 完成 |
| 300 | 3 | 0.4057 | 4440 | 1291 | 3821 | ok | 完成 |
| 325 | 3 | 0.4309 | 4716 | 1177 | 1303 | ok | 完成 |
| 350 | 3 | 0.4659 | 5099 | 1096 | 3666 | ok | 完成 |
| 375 | 3 | 0.4688 | 5131 | 1060 | 3675 | ok | 完成 |
| 400 | 3 | 0.4594 | 5028 | 1169 | 3675 | ok | 完成 |
| 500 | 2 | 0.4048 | 4431 | 1030 | 5484 | ok | 完成 |
| 600 | 2 | 0.4122 | 4511 | 885 | 5549 | ok | 完成 |
| 700 | 0 | 1.0000 | 10945 | 0 | 0 | ok | 完成 |
| 800 | 0 | 1.0000 | 10945 | 0 | 0 | ok | 完成 |
| 900 | 0 | 1.0000 | 10945 | 0 | 0 | ok | 完成 |
| 1000 | 0 | 1.0000 | 10945 | 0 | 0 | ok | 完成 |

## 測試結論

`min_cluster_size=50` 在本次掃描中離群值最低且保留有效主題。選擇規則為：優先選擇 n_clusters >= 2 且 noise_ratio 最低者；若並列，選 n_clusters 較多者，再選 min_cluster_size 較小者。
此設定的統計為 n_clusters=3、noise_ratio=0.0112、主題 -1 count=123、主題 0 count=71、主題 1 count=67。

- 最佳參數 topic info CSV：`Result/06.03_A03_min-test/A03-3(del)_tok(para12-80)/Result_06.03_A03-3(del)_tok(para12-80)-best_topic_info.csv`
- 最佳參數 document-topic CSV：`Result/06.03_A03_min-test/A03-3(del)_tok(para12-80)/Result_06.03_A03-3(del)_tok(para12-80)-best_document_topics.csv`
- 完整 min_cluster_size CSV：`Result/06.03_A03_min-test/A03-3(del)_tok(para12-80)/Result_06.03_A03-3(del)_tok(para12-80)-min_cluster_size.csv`

## 錯誤輸出

### 檢測發現與建議
> 在運行過程中遇到的所有問題，用表格紀錄。

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 環境套件可載入，開始 BERTopic min_cluster_size 檢測。 |
| 前處理 | 有 16 筆少於 3 words 的短句保留在測試中，可能增加離群值。 |

### 整體錯誤輸出
> 最後嘗試還是失敗，需要更改的功能。

無。BERTopic min_cluster_size 掃描已完成。

### 可改進
> 不影響流程，但改了可以讓流程更順，或讓結果更好的建議。

1. 短句比例可能影響 HDBSCAN 密度判斷，可測試排除少於 3 或 5 words 的句子後再比較 noise_ratio。
2. 本次參數掃描使用固定 embeddings 與固定 UMAP 結果，比較重點集中在 HDBSCAN min_cluster_size。
3. 最佳參數建議再搭配 topic words 與代表句人工審查，避免只用 noise_ratio 選到語意過寬的主題。
4. 若 noise_ratio 仍偏高，可測試 HDBSCAN min_samples、UMAP n_neighbors，或 BERTopic reduce_outliers。
