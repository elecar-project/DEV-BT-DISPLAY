# BERTopic min_cluster_size 檢測報告 - 06.03_A03-2(del)_tok

- 建立時間：2026-06-03 01:53:00 UTC
- 資料來源：`Result/06.03_A02/R06.03_A02-pre_LLM(del)_tok_dataset`
- 使用欄位：`sentence`
- 原始筆數：31474
- 可用 documents：31474
- 文本長度：min=2, avg=84.9, max=664
- word_count：min=1, avg=14.9, max=142

## BERTopic 參數設定

| 參數 | 設定 | 統計/原因 |
| --- | --- | --- |
| Dataset | Result/06.03_A02/R06.03_A02-pre_LLM(del)_tok_dataset | 31474 usable documents; text_col=sentence |
| Embedding Model | all-MiniLM-L6-v2 | 通用英文語意向量模型，與既有專案設定一致 |
| UMAP | n_neighbors=15, n_components=5, min_dist=0.0, metric=cosine, random_state=42 | 固定降維設定，讓不同 min_cluster_size 可比較 |
| HDBSCAN | metric=euclidean, cluster_selection_method=eom, prediction_data=True | 對固定 UMAP 結果測試 min_cluster_size |
| CountVectorizer | stop_words=english, ngram_range=(1, 2), min_df=2 | 最佳參數 BERTopic 訓練時使用，降低極低頻詞干擾 |
| min_cluster_size 測試範圍 | 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 500, 600, 700, 800, 900, 1000 | 依使用者指定完整測試 |
| 最佳 min_cluster_size | 100 | n_clusters=2, noise_ratio=0.0218, topic -1 count=687, topic 0 count=124, topic 1 count=30663 |

## min_cluster_size 不同參數測試結果

| min_cluster_size | n_clusters | noise_ratio | 主題 -1 count | 主題 0 count | 主題 1 count | 狀態 | 備註 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 84 | 0.5077 | 15979 | 100 | 53 | ok | 完成 |
| 75 | 53 | 0.5255 | 16540 | 100 | 85 | ok | 完成 |
| 100 | 2 | 0.0218 | 687 | 124 | 30663 | ok | 完成 |
| 125 | 28 | 0.5450 | 17153 | 214 | 146 | ok | 完成 |
| 150 | 16 | 0.4859 | 15293 | 219 | 4429 | ok | 完成 |
| 175 | 15 | 0.5108 | 16076 | 218 | 4454 | ok | 完成 |
| 200 | 14 | 0.5380 | 16933 | 205 | 4453 | ok | 完成 |
| 225 | 2 | 0.1170 | 3683 | 4743 | 23048 | ok | 完成 |
| 250 | 11 | 0.5519 | 17369 | 4178 | 738 | ok | 完成 |
| 275 | 2 | 0.1315 | 4138 | 4676 | 22660 | ok | 完成 |
| 300 | 2 | 0.1382 | 4350 | 4622 | 22502 | ok | 完成 |
| 325 | 2 | 0.1439 | 4530 | 4584 | 22360 | ok | 完成 |
| 350 | 2 | 0.1474 | 4639 | 4582 | 22253 | ok | 完成 |
| 375 | 2 | 0.1515 | 4768 | 4562 | 22144 | ok | 完成 |
| 400 | 2 | 0.1540 | 4848 | 4551 | 22075 | ok | 完成 |
| 500 | 2 | 0.1779 | 5600 | 4430 | 21444 | ok | 完成 |
| 600 | 2 | 0.2208 | 6949 | 4233 | 20292 | ok | 完成 |
| 700 | 2 | 0.2234 | 7031 | 4149 | 20294 | ok | 完成 |
| 800 | 2 | 0.2249 | 7077 | 4103 | 20294 | ok | 完成 |
| 900 | 2 | 0.2472 | 7781 | 3911 | 19782 | ok | 完成 |
| 1000 | 2 | 0.2331 | 7336 | 3684 | 20454 | ok | 完成 |

## 測試結論

`min_cluster_size=100` 在本次掃描中離群值最低且保留有效主題。選擇規則為：優先選擇 n_clusters >= 2 且 noise_ratio 最低者；若並列，選 n_clusters 較多者，再選 min_cluster_size 較小者。
此設定的統計為 n_clusters=2、noise_ratio=0.0218、主題 -1 count=687、主題 0 count=124、主題 1 count=30663。

- 最佳參數 topic info CSV：`Result/06.03_A03_min-test/A03-2(del)_tok/Result_06.03_A03-2(del)_tok-best_topic_info.csv`
- 最佳參數 document-topic CSV：`Result/06.03_A03_min-test/A03-2(del)_tok/Result_06.03_A03-2(del)_tok-best_document_topics.csv`
- 完整 min_cluster_size CSV：`Result/06.03_A03_min-test/A03-2(del)_tok/Result_06.03_A03-2(del)_tok-min_cluster_size.csv`

## 錯誤輸出

### 檢測發現與建議
> 在運行過程中遇到的所有問題，用表格紀錄。

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 環境套件可載入，開始 BERTopic min_cluster_size 檢測。 |
| 前處理 | 有 1417 筆少於 3 words 的短句保留在測試中，可能增加離群值。 |

### 整體錯誤輸出
> 最後嘗試還是失敗，需要更改的功能。

無。BERTopic min_cluster_size 掃描已完成。

### 可改進
> 不影響流程，但改了可以讓流程更順，或讓結果更好的建議。

1. 短句比例可能影響 HDBSCAN 密度判斷，可測試排除少於 3 或 5 words 的句子後再比較 noise_ratio。
2. 本次參數掃描使用固定 embeddings 與固定 UMAP 結果，比較重點集中在 HDBSCAN min_cluster_size。
3. 最佳參數建議再搭配 topic words 與代表句人工審查，避免只用 noise_ratio 選到語意過寬的主題。
4. 若 noise_ratio 仍偏高，可測試 HDBSCAN min_samples、UMAP n_neighbors，或 BERTopic reduce_outliers。
