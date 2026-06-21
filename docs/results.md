---
title: 結果
description: 以實驗路徑瀏覽 DEV-BT 的 BERTopic 結果與驗證分支。
---

# 結果

本頁依實驗的資料血緣與處理順序呈現。可點擊的節點已有完整結果與設定摘要；其他節點保留在地圖中，待後續整理後開放。

<div class="experiment-map-scroll" aria-label="DEV-BT 完整實驗地圖">
    <object class="experiment-map-full" type="image/svg+xml" data="{{ '/assets/img/experiment-map-full.svg?v=20260621-a04-year-v16' | relative_url }}">
    <img src="{{ '/assets/img/experiment-map-full.svg?v=20260621-a04-year-v16' | relative_url }}" alt="DEV-BT 完整實驗運行架構圖">
  </object>
</div>

## 如何閱讀

`A03-A05` 是資料版本、UMAP 與停用詞處理的探索階段；`M01-M03` 是選定設定後的主要模型運行；`T01-T04` 則用不同資料處理、年份切分與資料篩選條件檢驗結果是否穩定。

## 已整理結果

| 終點 | 實驗意義 | 目前狀態 |
| --- | --- | --- |
| [A03-2：del + tok min_cluster_size 掃描]({{ '/results/a03-2-del-tok.html' | relative_url }}) | 21 組 HDBSCAN 最小群集大小的敏感度分析 | 可檢視 |
| [8New-LLM30]({{ '/results/m02-llm30.html' | relative_url }}) | 最佳參數模型，LLM 命名 30 次驗證 | 可檢視 |
| [8New-LLM50]({{ '/results/m02-llm50.html' | relative_url }}) | 同一路徑以 50 次命名驗證，資料夾名稱歷史上誤標為 tp-30 | 可檢視 |
| [M01-8 三策略主程式]({{ '/results/m01-8-historical.html' | relative_url }}) | 歷史比較用途：A05-8.4 human 停用詞與三種候選策略的完整重跑 | 可檢視 |
| [2020 前]({{ '/results/m03-2020-before.html' | relative_url }}) | 年份切分後的 2008-2019 主題模型 | 可檢視 |
| [2020 後]({{ '/results/m03-2020-after.html' | relative_url }}) | 年份切分後的 2020-2025 主題模型 | 可檢視 |
| [T01 刪除／替換驗證]({{ '/results/t01-overview.html' | relative_url }}) | 比較刪除品牌／車款與替換為 Brand／Model 的主題結構 | 可檢視 |
| 其他 T01-T04 節點 | 驗證與敏感度分析 | 待整理 |

## A03 min_cluster_size 掃描

| 節點 | 資料處理版本 | 目前狀態 |
| --- | --- | --- |
| [A03 整體比較]({{ '/results/a03-min-cluster-overview.html' | relative_url }}) | A03-2、3、5、5.1、6、6.1、7、8 的中英文掃描圖比較 | 可檢視 |
| [A03-2]({{ '/results/a03-2-del-tok.html' | relative_url }}) | del + tok | 可檢視 |
| [A03-3]({{ '/results/a03-3-del-tok-para12-80.html' | relative_url }}) | del + tok + 段落 12-80 | 可檢視 |
| [A03-5]({{ '/results/a03-5-repl-tok.html' | relative_url }}) | repl + tok | 可檢視 |
| [A03-5.1]({{ '/results/a03-5-1-repl-y-tok.html' | relative_url }}) | repl-y + tok | 可檢視 |
| [A03-6]({{ '/results/a03-6-repl-tok-para12-80.html' | relative_url }}) | repl + tok + 段落 12-80 | 可檢視 |
| [A03-6.1]({{ '/results/a03-6-1-repl-y-tok-para12-80.html' | relative_url }}) | repl-y + tok + 段落 12-80 | 可檢視 |
| [A03-7]({{ '/results/a03-7-orig-tok.html' | relative_url }}) | orig + tok | 可檢視 |
| [A03-8]({{ '/results/a03-8-orig-tok-para12-80.html' | relative_url }}) | orig + tok + 段落 12-80 | 可檢視 |

## A04 UMAP 搜尋

可直接查看：[A04 整體比較]({{ '/results/a04-umap-overview.html' | relative_url }})、[A04-2]({{ '/results/a04-2-del-tok.html' | relative_url }})、[A04-3]({{ '/results/a04-3-del-tok-para12-80.html' | relative_url }})、[A04-5]({{ '/results/a04-5-repl-tok.html' | relative_url }})、[A04-6]({{ '/results/a04-6-repl-tok-para12-80.html' | relative_url }})、[A04-7]({{ '/results/a04-7-orig-tok.html' | relative_url }})、[A04-8]({{ '/results/a04-8-orig-tok-para12-80.html' | relative_url }})、[A04｜2020 前（2008-2019）]({{ '/results/a04-b01-08-19.html' | relative_url }})、[A04｜2020 後（2020-2025）]({{ '/results/a04-b01-20-25.html' | relative_url }})。

## A05 停用詞設計

[A05 停用詞總覽]({{ '/results/a05-stopwords-overview.html' | relative_url }})呈現正確的 A05-6 與 A05-8 orig REV 詞表迭代；流程圖的 6、8 節點可分別進入其分支頁，人工精選版為 [A05-8.4 human]({{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }})。

## 年份切分 min_cluster_size 掃描

| 資料集 | 實驗頁面 | 目前狀態 |
| --- | --- | --- |
| 2008-2019，240 份資料 | [B01 2008-2019]({{ '/results/b01-08-19-min-cluster.html' | relative_url }}) | 可檢視 |
| 2020-2025，194 份資料 | [B01 2020-2025]({{ '/results/b01-20-25-min-cluster.html' | relative_url }}) | 可檢視 |
