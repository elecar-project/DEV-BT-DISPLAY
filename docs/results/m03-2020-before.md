---
title: 2020 前年份切分
description: M03 年份切分後的 2008-2019 BERTopic 結果。
---

# 2020 前｜年份切分

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料血緣

| 項目 | 設定 |
| --- | --- |
| 資料集 | 2008-2019，240 份資料 |
| 節點路徑 | 8New → M03 → T02 |
| 自訂停用詞 | 170 個 |

### 模型

| 項目 | 設定 |
| --- | --- |
| Embedding | `all-MiniLM-L6-v2` |
| UMAP | neighbors 5 / components 10 / cosine |
| HDBSCAN | min cluster 100 / min samples 5 / eom |
| Topic reduction | `nr_topics=auto` |

### LLM 命名

| 項目 | 設定 |
| --- | --- |
| Provider / model | OpenRouter / `openai/gpt-5.5` |
| 每個 topic 次數 | 50 |
| 代表句 | 6 句 / topic |
</aside>

<section markdown="1">
<div class="run-summary">
  <div class="run-stat"><strong>16</strong><span>主題群數</span></div>
  <div class="run-stat"><strong>25.93%</strong><span>noise ratio</span></div>
  <div class="run-stat"><strong>13 / 17</strong><span>穩定命名主題</span></div>
  <div class="run-stat"><strong>0.650</strong><span>balance score</span></div>
</div>

## 結果摘要

此節點用於與 2020 後資料比較，檢視年份切分後的主題結構是否產生可解釋的差異。

## 來源檔案

`Result/06.17_M03_split/06.17_M03-1(orig_08-19_tp-50)/`

</section>
</div>
