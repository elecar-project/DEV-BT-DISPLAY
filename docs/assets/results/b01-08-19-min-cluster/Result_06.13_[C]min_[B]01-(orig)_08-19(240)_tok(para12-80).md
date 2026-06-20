# BERTopic min_cluster_size 檢測報告 - 06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)

- 建立時間：2026-06-16 20:35:01 UTC
- 資料來源：`Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_08-19(240)_tok(para12-80)_dataset`
- 使用欄位：`sentence`
- 原始筆數：11160
- 可用 documents：11160
- 文本長度：min=46, avg=123.6, max=523
- word_count：min=5, avg=21.9, max=80

## BERTopic 參數設定

| 參數 | 設定 | 統計/原因 |
| --- | --- | --- |
| Dataset | Result/06.13_[B]tok/06.13_[B]01-pre_LLM(orig)_08-19(240)_tok(para12-80)_dataset | 11160 usable documents; text_col=sentence |
| Embedding Model | all-MiniLM-L6-v2 | 通用英文語意向量模型，與既有專案設定一致 |
| UMAP | n_neighbors=15, n_components=5, min_dist=0.0, metric=cosine, random_state=42 | 固定降維設定，讓不同 min_cluster_size 可比較 |
| HDBSCAN | metric=euclidean, cluster_selection_method=eom, prediction_data=True | 對固定 UMAP 結果測試 min_cluster_size；測試表 topic 0/1 已按群集大小重編號 |
| CountVectorizer | stop_words=english, ngram_range=(1, 2), min_df=2 | 最佳參數 BERTopic 訓練時使用，降低極低頻詞干擾 |
| min_cluster_size 測試範圍 | 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 500, 600, 700, 800, 900, 1000 | 依使用者指定完整測試 |
| 最佳 min_cluster_size | 50 | n_clusters=5, noise_ratio=0.0041, topic -1 count=46, topic 0 count=10385, topic 1 count=281 |

## min_cluster_size 不同參數測試結果

> 註：測試表的 topic 0/1 count 依群集大小重編號，最大非離群群集為 topic 0；正式 BERTopic 輸出的 topic id 以 BERTopic model 為準。

| min_cluster_size | n_clusters | noise_ratio | 主題 -1 count | 主題 0 count | 主題 1 count | 狀態 | 備註 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 50 | 5 | 0.0041 | 46 | 10385 | 281 | ok | 完成 |
| 75 | 4 | 0.0236 | 263 | 10245 | 257 | ok | 完成 |
| 100 | 4 | 0.0254 | 283 | 10225 | 257 | ok | 完成 |
| 125 | 4 | 0.0317 | 354 | 10160 | 251 | ok | 完成 |
| 150 | 4 | 0.0366 | 409 | 10109 | 247 | ok | 完成 |
| 175 | 3 | 0.0676 | 754 | 9924 | 245 | ok | 完成 |
| 200 | 3 | 0.0938 | 1047 | 9630 | 246 | ok | 完成 |
| 225 | 3 | 0.0971 | 1084 | 9597 | 245 | ok | 完成 |
| 250 | 2 | 0.4336 | 4839 | 5190 | 1131 | ok | 完成 |
| 275 | 3 | 0.5378 | 6002 | 3396 | 1097 | ok | 完成 |
| 300 | 3 | 0.5375 | 5998 | 3486 | 1017 | ok | 完成 |
| 325 | 3 | 0.5737 | 6403 | 3275 | 946 | ok | 完成 |
| 350 | 3 | 0.5652 | 6308 | 3478 | 803 | ok | 完成 |
| 375 | 3 | 0.6053 | 6755 | 3168 | 669 | ok | 完成 |
| 400 | 3 | 0.6455 | 7204 | 2874 | 561 | ok | 完成 |
| 500 | 0 | 1.0000 | 11160 | 0 | 0 | ok | 完成 |
| 600 | 0 | 1.0000 | 11160 | 0 | 0 | ok | 完成 |
| 700 | 0 | 1.0000 | 11160 | 0 | 0 | ok | 完成 |
| 800 | 0 | 1.0000 | 11160 | 0 | 0 | ok | 完成 |
| 900 | 0 | 1.0000 | 11160 | 0 | 0 | ok | 完成 |
| 1000 | 0 | 1.0000 | 11160 | 0 | 0 | ok | 完成 |

## 測試結論

`min_cluster_size=50` 在本次掃描中離群值最低且保留有效主題。選擇規則為：優先選擇 n_clusters >= 2 且 noise_ratio 最低者；若並列，選 n_clusters 較多者，再選 min_cluster_size 較小者。
此設定的統計為 n_clusters=5、noise_ratio=0.0041、主題 -1 count=46、主題 0 count=10385、主題 1 count=281。

- 最佳參數 topic info CSV：`Result/06.13_[C]min/[B]01-(orig)_08-19(240)_tok(para12-80)/Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)-best_topic_info.csv`
- 最佳參數 document-topic CSV：`Result/06.13_[C]min/[B]01-(orig)_08-19(240)_tok(para12-80)/Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)-best_document_topics.csv`
- 完整 min_cluster_size CSV：`Result/06.13_[C]min/[B]01-(orig)_08-19(240)_tok(para12-80)/Result_06.13_[C]min_[B]01-(orig)_08-19(240)_tok(para12-80)-min_cluster_size.csv`
- 肘狀圖 PNG：`Result/06.13_[C]min/[B]01-(orig)_08-19(240)_tok(para12-80)/[B]01-(orig)_08-19(240)_tok(para12-80)_min_cluster_chart.png`

## 錯誤輸出

### 檢測發現與建議
> 在運行過程中遇到的所有問題，用表格紀錄。

| 流程 | 問題 |
| --- | --- |
| 環境開始運行 | 環境套件可載入，開始 BERTopic min_cluster_size 檢測。 |
| Embedding | 已完成 embeddings 並寫入快取：Result/06.13_[C]min/[B]01-(orig)_08-19(240)_tok(para12-80)/cache/embeddings_all-MiniLM-L6-v2.npy |
| UMAP | 已完成 UMAP 降維並寫入快取：Result/06.13_[C]min/[B]01-(orig)_08-19(240)_tok(para12-80)/cache/umap_nn15_nc5_md0p0_cosine_rs42.npy |

### 整體錯誤輸出
> 最後嘗試還是失敗，需要更改的功能。

無。BERTopic min_cluster_size 掃描已完成。

### 可改進
> 不影響流程，但改了可以讓流程更順，或讓結果更好的建議。

1. 本次參數掃描使用固定 embeddings 與固定 UMAP 結果，比較重點集中在 HDBSCAN min_cluster_size。
2. 最佳參數建議再搭配 topic words 與代表句人工審查，避免只用 noise_ratio 選到語意過寬的主題。
3. 若 noise_ratio 仍偏高，可測試 HDBSCAN min_samples、UMAP n_neighbors，或 BERTopic reduce_outliers。
