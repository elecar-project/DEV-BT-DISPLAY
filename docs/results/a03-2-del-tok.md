---
title: A03-2 del tok min_cluster_size 掃描
description: del + tokenizer 資料集的 HDBSCAN min_cluster_size 敏感度分析。
---

# A03-2｜min_cluster_size 掃描

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 實驗目的

固定語意向量與降維設定，僅調整 HDBSCAN 的 `min_cluster_size`，比較主題群數、離群比例與主題分布。

### 資料血緣

| 項目 | 設定 |
| --- | --- |
| 資料集 | `pre_LLM(del)_tok_dataset` |
| 節點路徑 | A03-2 → A04 → A05 |
| 使用欄位 | `sentence` |
| 可用句子 | 31,474 |
| 短句 | 1,417 筆少於 3 words |

### 固定模型設定

| 項目 | 設定 |
| --- | --- |
| Embedding | `all-MiniLM-L6-v2` |
| UMAP | neighbors 15 / components 5 / min dist 0 / cosine |
| HDBSCAN | euclidean / eom / prediction data |
| Vectorizer | English stop words / ngram 1-2 / min df 2 |

### 掃描範圍

`50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 500, 600, 700, 800, 900, 1000`
</aside>

<section markdown="1">
<div class="run-summary">
  <div class="run-stat"><strong>21</strong><span>測試參數組數</span></div>
  <div class="run-stat"><strong>100</strong><span>自動選擇值</span></div>
  <div class="run-stat"><strong>2.18%</strong><span>該設定 noise ratio</span></div>
  <div class="run-stat"><strong>2</strong><span>非 noise 主題數</span></div>
</div>

## 結果摘要

本實驗以固定的 embedding 與 UMAP 結果，測試 21 組 `min_cluster_size`。程式的自動選擇規則為：先保留至少兩個非 noise 主題的結果，再選擇 noise ratio 最低者；若相同，再選擇主題較多、參數較小者。

> **判讀提醒：** `min_cluster_size=100` 雖有最低的 noise ratio（2.18%），但 97.42% 的句子被歸到同一個主題。它應視為「依既定規則選出的候選值」，尚不能當成語意區辨性最佳的最終模型。

## 參數掃描結果

| min cluster size | 非 noise 主題數 | noise ratio | 離群句數 | 主題 0 | 主題 1 |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 50 | 84 | 50.77% | 15,979 | 100 | 53 |
| 75 | 53 | 52.55% | 16,540 | 100 | 85 |
| **100** | **2** | **2.18%** | **687** | **30,663** | **124** |
| 125 | 28 | 54.50% | 17,153 | 214 | 146 |
| 150 | 16 | 48.59% | 15,293 | 219 | 4,429 |
| 175 | 15 | 51.08% | 16,076 | 218 | 4,454 |
| 200 | 14 | 53.80% | 16,933 | 205 | 4,453 |
| 225 | 2 | 11.70% | 3,683 | 4,743 | 23,048 |
| 250 | 11 | 55.19% | 17,369 | 4,178 | 738 |
| 275 | 2 | 13.15% | 4,138 | 4,676 | 22,660 |
| 300 | 2 | 13.82% | 4,350 | 4,622 | 22,502 |
| 325 | 2 | 14.39% | 4,530 | 4,584 | 22,360 |
| 350 | 2 | 14.74% | 4,639 | 4,582 | 22,253 |
| 375 | 2 | 15.15% | 4,768 | 4,562 | 22,144 |
| 400 | 2 | 15.40% | 4,848 | 4,551 | 22,075 |
| 500 | 2 | 17.79% | 5,600 | 4,430 | 21,444 |
| 600 | 2 | 22.08% | 6,949 | 4,233 | 20,292 |
| 700 | 2 | 22.34% | 7,031 | 4,149 | 20,294 |
| 800 | 2 | 22.49% | 7,077 | 4,103 | 20,294 |
| 900 | 2 | 24.72% | 7,781 | 3,911 | 19,782 |
| 1000 | 2 | 23.31% | 7,336 | 3,684 | 20,454 |

## 自動選擇值的主題分布

| Topic | 句數 | 比例 | 前幾個代表詞 |
| ---: | ---: | ---: | --- |
| -1（noise） | 687 | 2.18% | thank, absolutely, crown, aria, okay |
| 0 | 30,663 | 97.42% | car, new, like, just, vehicle, electric, design |
| 1 | 124 | 0.39% | warranty, mile, year, hybrid, maintenance |

Topic 0 的代表句同時涵蓋車輛設計、電動車、駕駛感受等多種內容，因此目前較接近「一般汽車產品敘述」的寬泛集合。後續應以代表詞、代表句與主題大小的平衡性，人工比較候選設定，而非只降低離群比例。

## 後續判讀方向

1. 優先人工比較 `50`、`75`、`125`、`150` 的代表詞與代表句，確認多群結果是否具有可解釋性。
2. 以「最大主題比例、主題數、noise ratio、代表句一致性」建立複合選擇規則。
3. 另測排除少於 3 或 5 words 的短句，檢查短句是否改變密度分群與離群比例。

## 來源檔案與下載

| 檔案 | 用途 |
| --- | --- |
| [參數掃描 CSV]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok-min_cluster_size.csv' | relative_url }}) | 21 組參數的完整統計 |
| [主題摘要 CSV]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok-best_topic_info.csv' | relative_url }}) | 自動選擇值的 topic 關鍵詞與代表句 |
| [句子－主題對照 CSV]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok-best_document_topics.csv' | relative_url }}) | 31,474 筆完整句子指派結果 |
| [實驗報告 Markdown]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok.md' | relative_url }}) | 原始執行報告 |
| [run log JSON]({{ '/assets/results/a03-2-del-tok/Result_06.03_A03-2(del)_tok-run_log.json' | relative_url }}) | 機器可讀的執行紀錄與選擇規則 |
| [執行程式 Python]({{ '/assets/results/a03-2-del-tok/run_06.03_A03_2_del_tok.py' | relative_url }}) | 可重現的實驗程式 |

</section>
</div>
