# BERTopic min_cluster_size 檢測報告 - 06.03_A03-6(repl)_tok(para12-80)

- 建立時間：2026-06-03 02:29:04 UTC
- 資料來源：`Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok(para12-80)_dataset`
- 使用欄位：`sentence`
- 原始筆數：10978
- 可用 documents：10978
- 文本長度：min=8, avg=250.5, max=676
- word_count：min=2, avg=43.6, max=142

## BERTopic 參數設定

| 參數 | 設定 | 統計/原因 |
| --- | --- | --- |
| Dataset | Result/06.03_A02/R06.03_A02-pre_LLM(repl)_tok(para12-80)_dataset | 10978 usable documents; text_col=sentence |
| Embedding Model | all-MiniLM-L6-v2 | 通用英文語意向量模型，與既有專案設定一致 |
| UMAP | n_neighbors=15, n_components=5, min_dist=0.0, metric=cosine, random_state=42 | 固定降維設定，讓不同 min_cluster_size 可比較 |
| HDBSCAN | metric=euclidean, cluster_selection_method=eom, prediction_data=True | 對固定 UMAP 結果測試 min_cluster_size |
| CountVectorizer | stop_words=english, ngram_range=(1, 2), min_df=2 | 最佳參數 BERTopic 訓練時使用，降低極低頻詞干擾 |
| min_cluster_size 測試範圍 | 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 500, 600, 700, 800, 900, 1000 | 依使用者指定完整測試 |
| 最佳 min_cluster_size | 50 | n_clusters=2, noise_ratio=0.0007, topic -1 count=8, topic 0 count=67, topic 1 count=10903 |

## min_cluster_size 不同參數測試結果

| min_cluster_size | n_clusters | noise_ratio | 主題 -1 count | 主題 0 count | 主題 1 count | 狀態 | 備註 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 2 | 0.0007 | 8 | 67 | 10903 | ok | 完成 |
| 75 | 16 | 0.4005 | 4397 | 81 | 486 | ok | 完成 |
| 100 | 10 | 0.4095 | 4495 | 242 | 384 | ok | 完成 |
| 125 | 9 | 0.3893 | 4274 | 192 | 178 | ok | 完成 |
| 150 | 6 | 0.2993 | 3286 | 2009 | 153 | ok | 完成 |
| 175 | 5 | 0.4552 | 4997 | 1947 | 454 | ok | 完成 |
| 200 | 4 | 0.3768 | 4136 | 1939 | 3948 | ok | 完成 |
| 225 | 2 | 0.2720 | 2986 | 1927 | 6065 | ok | 完成 |
| 250 | 3 | 0.2835 | 3112 | 1423 | 1880 | ok | 完成 |
| 275 | 3 | 0.2978 | 3269 | 1402 | 1830 | ok | 完成 |
| 300 | 4 | 0.4157 | 4564 | 1387 | 1700 | ok | 完成 |
| 325 | 3 | 0.3477 | 3817 | 1351 | 4199 | ok | 完成 |
| 350 | 4 | 0.4598 | 5048 | 1599 | 1137 | ok | 完成 |
| 375 | 3 | 0.3772 | 4141 | 1493 | 4149 | ok | 完成 |
| 400 | 3 | 0.4059 | 4456 | 1160 | 4056 | ok | 完成 |
| 500 | 3 | 0.5120 | 5621 | 930 | 946 | ok | 完成 |
| 600 | 0 | 1.0000 | 10978 | 0 | 0 | ok | 完成 |
| 700 | 0 | 1.0000 | 10978 | 0 | 0 | ok | 完成 |
| 800 | 0 | 1.0000 | 10978 | 0 | 0 | ok | 完成 |
| 900 | 0 | 1.0000 | 10978 | 0 | 0 | ok | 完成 |
| 1000 | 0 | 1.0000 | 10978 | 0 | 0 | ok | 完成 |

## 測試結論

`min_cluster_size=50` 在本次掃描中離群值最低且保留有效主題。選擇規則為：優先選擇 n_clusters >= 2 且 noise_ratio 最低者；若並列，選 n_clusters 較多者，再選 min_cluster_size 較小者。
此設定的統計為 n_clusters=2、noise_ratio=0.0007、主題 -1 count=8、主題 0 count=67、主題 1 count=10903。

- 最佳參數 topic info CSV：`Result/06.03_A03_min-test/A03-6(repl)_tok(para12-80)/Result_06.03_A03-6(repl)_tok(para12-80)-best_topic_info.csv`
- 最佳參數 document-topic CSV：`Result/06.03_A03_min-test/A03-6(repl)_tok(para12-80)/Result_06.03_A03-6(repl)_tok(para12-80)-best_document_topics.csv`
- 完整 min_cluster_size CSV：`Result/06.03_A03_min-test/A03-6(repl)_tok(para12-80)/Result_06.03_A03-6(repl)_tok(para12-80)-min_cluster_size.csv`

## 錯誤輸出

### 檢測發現與建議
> 在運行過程中遇到的所有問題，用表格紀錄。

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 環境套件可載入，開始 BERTopic min_cluster_size 檢測。 |
| 前處理 | 有 9 筆少於 3 words 的短句保留在測試中，可能增加離群值。 |

### 整體錯誤輸出
> 最後嘗試還是失敗，需要更改的功能。

無。BERTopic min_cluster_size 掃描已完成。

### 可改進
> 不影響流程，但改了可以讓流程更順，或讓結果更好的建議。

1. 短句比例可能影響 HDBSCAN 密度判斷，可測試排除少於 3 或 5 words 的句子後再比較 noise_ratio。
2. 本次參數掃描使用固定 embeddings 與固定 UMAP 結果，比較重點集中在 HDBSCAN min_cluster_size。
3. 最佳參數建議再搭配 topic words 與代表句人工審查，避免只用 noise_ratio 選到語意過寬的主題。
4. 若 noise_ratio 仍偏高，可測試 HDBSCAN min_samples、UMAP n_neighbors，或 BERTopic reduce_outliers。
