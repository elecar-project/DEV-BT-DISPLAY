---
title: 結果
description: 以實驗路徑瀏覽 DEV-BT 的 BERTopic 結果與驗證分支。
---

# 結果

本頁依實驗的資料血緣與處理順序呈現。可點擊的節點已有完整結果與設定摘要；其他節點保留在地圖中，待後續整理後開放。

<div class="map-toolbar">
  <div><label for="map-zoom">地圖大小</label><select id="map-zoom"><option value="1440">標準檢視</option><option value="2000">放大檢視</option><option value="fit">符合頁面寬度</option></select><button id="map-fit" type="button">縮放至頁寬</button></div>
  <a href="#experiment-catalog">使用文字索引 →</a>
</div>
<div class="experiment-map-scroll" tabindex="0" role="region" aria-label="DEV-BT 完整實驗地圖，可使用方向鍵或觸控左右捲動">
    <object class="experiment-map-full" type="image/svg+xml" aria-label="完整實驗地圖，所有實驗亦可由下方文字索引開啟" data="{{ '/assets/img/experiment-map-full.svg?v=20261113' | relative_url }}">
    <img src="{{ '/assets/img/experiment-map-full.svg?v=20261113' | relative_url }}" alt="DEV-BT 完整實驗運行架構圖">
  </object>
</div>

<p class="map-caption">地圖可左右捲動。手機可使用下方文字索引，直接搜尋實驗名稱與處理版本。</p>

## 如何閱讀

`A03-A05` 是資料版本、UMAP 與停用詞處理的探索階段；`M01-M03` 是選定設定後的主要模型運行；`T01-T04` 則用不同資料處理、年份切分與資料篩選條件檢驗結果是否穩定。

## 已整理結果

| 終點 | 實驗意義 | 目前狀態 |
| --- | --- | --- |
| [A03-2：del + tok min_cluster_size 掃描]({{ '/results/a03-2-del-tok.html' | relative_url }}) | 21 組 HDBSCAN 最小群集大小的敏感度分析 | 可檢視 |
| [8New-LLM30]({{ '/results/m02-llm30.html' | relative_url }}) | 最佳參數模型，LLM 命名 30 次驗證 | 可檢視 |
| [8New-LLM50]({{ '/results/m02-llm50.html' | relative_url }}) | 另一次模型運行及 50 次命名驗證；分群為 34 主題，非 LLM30 的同一分群 | 可檢視 |
| [M01-8 三策略主程式]({{ '/results/m01-8-historical.html' | relative_url }}) | 歷史比較用途：A05-8.4 human 停用詞與三種候選策略的完整重跑 | 可檢視 |
| [2020 前]({{ '/results/m03-2020-before.html' | relative_url }}) | 年份切分後的 2008-2019 主題模型 | 可檢視 |
| [2020 後]({{ '/results/m03-2020-after.html' | relative_url }}) | 年份切分後的 2020-2025 主題模型 | 可檢視 |
| [T01 刪除／替換驗證]({{ '/results/t01-overview.html' | relative_url }}) | 比較刪除品牌／車款與替換為 Brand／Model 的主題結構 | 可檢視 |
| [T02 年份切分驗證]({{ '/results/t02-overview.html' | relative_url }}) | 以 2018、2019、2021 為界比較前後兩段資料 | 可檢視 |
| [T03 資料篩選驗證]({{ '/results/t03-overview.html' | relative_url }}) | 比較影長 600–2159 秒與去頭尾各 5 家廠商的資料篩選結果 | 可檢視 |
| 其他 T04 節點 | 驗證與敏感度分析 | 待整理 |

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

## 全部實驗文字索引 {#experiment-catalog}

<div class="catalog-search"><label for="result-search">搜尋實驗</label><input id="result-search" type="search" placeholder="例如 A05、年份、停用詞" aria-controls="result-catalog"><span id="result-search-count" role="status">顯示 64 / 64 頁</span></div>
<p id="result-search-empty" class="loading-text" hidden>沒有符合的實驗，請換個關鍵字。</p>
<div id="result-catalog" class="result-catalog" data-result-catalog>
<section class="catalog-group" data-result-group><h3>A03 · 群集大小探索</h3><ul><li data-result-item><a href="{{ '/results/a03-2-del-tok.html' | relative_url }}">A03-2 del tok min_cluster_size 掃描</a></li><li data-result-item><a href="{{ '/results/a03-3-del-tok-para12-80.html' | relative_url }}">A03-3｜del + tok + 段落 12-80</a></li><li data-result-item><a href="{{ '/results/a03-5-1-repl-y-tok.html' | relative_url }}">A03-5.1｜repl-y + tok</a></li><li data-result-item><a href="{{ '/results/a03-5-repl-tok.html' | relative_url }}">A03-5｜repl + tok</a></li><li data-result-item><a href="{{ '/results/a03-6-1-repl-y-tok-para12-80.html' | relative_url }}">A03-6.1｜repl-y + tok + 段落 12-80</a></li><li data-result-item><a href="{{ '/results/a03-6-repl-tok-para12-80.html' | relative_url }}">A03-6｜repl + tok + 段落 12-80</a></li><li data-result-item><a href="{{ '/results/a03-7-orig-tok.html' | relative_url }}">A03-7｜orig + tok</a></li><li data-result-item><a href="{{ '/results/a03-8-orig-tok-para12-80.html' | relative_url }}">A03-8｜orig + tok + 段落 12-80</a></li><li data-result-item><a href="{{ '/results/a03-min-cluster-overview.html' | relative_url }}">A03 min_cluster_size 整體比較</a></li></ul></section>
<section class="catalog-group" data-result-group><h3>A04 · UMAP 參數搜尋</h3><ul><li data-result-item><a href="{{ '/results/a04-2-del-tok.html' | relative_url }}">A04-2｜del + tok UMAP 搜尋</a></li><li data-result-item><a href="{{ '/results/a04-3-del-tok-para12-80.html' | relative_url }}">A04-3｜del + tok + 段落 12-80 UMAP 搜尋</a></li><li data-result-item><a href="{{ '/results/a04-5-repl-tok.html' | relative_url }}">A04-5｜repl + tok UMAP 搜尋</a></li><li data-result-item><a href="{{ '/results/a04-6-repl-tok-para12-80.html' | relative_url }}">A04-6｜repl + tok + 段落 12-80 UMAP 搜尋</a></li><li data-result-item><a href="{{ '/results/a04-7-orig-tok.html' | relative_url }}">A04-7｜orig + tok UMAP 搜尋</a></li><li data-result-item><a href="{{ '/results/a04-8-orig-tok-para12-80.html' | relative_url }}">A04-8｜orig + tok + 段落 12-80 UMAP 搜尋</a></li><li data-result-item><a href="{{ '/results/a04-b01-08-19.html' | relative_url }}">A04｜2020 前（2008-2019） UMAP 搜尋</a></li><li data-result-item><a href="{{ '/results/a04-b01-20-25.html' | relative_url }}">A04｜2020 後（2020-2025） UMAP 搜尋</a></li><li data-result-item><a href="{{ '/results/a04-umap-overview.html' | relative_url }}">A04 UMAP 整體比較</a></li></ul></section>
<section class="catalog-group" data-result-group><h3>A05 · 停用詞設計</h3><ul><li data-result-item><a href="{{ '/results/a05-6-1-stopwords.html' | relative_url }}">A05-6.1 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-6-2-stopwords.html' | relative_url }}">A05-6.2 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-6-3-stopwords.html' | relative_url }}">A05-6.3 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-6-overview.html' | relative_url }}">A05-6｜初步停用詞迭代</a></li><li data-result-item><a href="{{ '/results/a05-6-stopwords.html' | relative_url }}">A05-6 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-8-orig-rev-1-stopwords.html' | relative_url }}">A05-8.1 REV 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-8-orig-rev-2-stopwords.html' | relative_url }}">A05-8.2 REV 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-8-orig-rev-3-stopwords.html' | relative_url }}">A05-8.3 REV 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-8-orig-rev-all-stopwords.html' | relative_url }}">A05-8.4 all 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}">A05-8.4 human 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-8-orig-rev-overview.html' | relative_url }}">A05-8｜orig REV 詞表收斂</a></li><li data-result-item><a href="{{ '/results/a05-8-orig-rev-stopwords.html' | relative_url }}">A05-8 REV 停用詞設計</a></li><li data-result-item><a href="{{ '/results/a05-stopwords-overview.html' | relative_url }}">A05 停用詞設計</a></li></ul></section>
<section class="catalog-group" data-result-group><h3>M01–M03 · 主要模型</h3><ul><li data-result-item><a href="{{ '/results/m01-8-best-balance.html' | relative_url }}">M01-8 最佳平衡</a></li><li data-result-item><a href="{{ '/results/m01-8-historical.html' | relative_url }}">M01-8 三策略主程式</a></li><li data-result-item><a href="{{ '/results/m01-8-lowest-noise.html' | relative_url }}">M01-8 最低雜訊</a></li><li data-result-item><a href="{{ '/results/m01-8-most-topics.html' | relative_url }}">M01-8 最多主題</a></li><li data-result-item><a href="{{ '/results/m02-llm30.html' | relative_url }}">8New-LLM30</a></li><li data-result-item><a href="{{ '/results/m02-llm50.html' | relative_url }}">8New-LLM50</a></li><li data-result-item><a href="{{ '/results/m03-2020-after.html' | relative_url }}">2020 後｜年份切分</a></li><li data-result-item><a href="{{ '/results/m03-2020-before.html' | relative_url }}">2020 前｜年份切分</a></li></ul></section>
<section class="catalog-group" data-result-group><h3>T01–T03 · 驗證實驗</h3><ul><li data-result-item><a href="{{ '/results/t01-del.html' | relative_url }}">T01-3｜刪除品牌／車款</a></li><li data-result-item><a href="{{ '/results/t01-overview.html' | relative_url }}">T01 刪除與替換驗證</a></li><li data-result-item><a href="{{ '/results/t01-repl.html' | relative_url }}">T01-6｜替換品牌／車款</a></li><li data-result-item><a href="{{ '/results/t02-2018-after.html' | relative_url }}">T02 2018 後 年份切分</a></li><li data-result-item><a href="{{ '/results/t02-2018-before.html' | relative_url }}">T02 2018 前 年份切分</a></li><li data-result-item><a href="{{ '/results/t02-2019-after.html' | relative_url }}">T02 2019 後 年份切分</a></li><li data-result-item><a href="{{ '/results/t02-2019-before.html' | relative_url }}">T02 2019 前 年份切分</a></li><li data-result-item><a href="{{ '/results/t02-2021-after.html' | relative_url }}">T02 2021 後 年份切分</a></li><li data-result-item><a href="{{ '/results/t02-2021-before.html' | relative_url }}">T02 2021 前 年份切分</a></li><li data-result-item><a href="{{ '/results/t02-overview.html' | relative_url }}">T02 年份切分驗證</a></li><li data-result-item><a href="{{ '/results/t03-duration-1-35m.html' | relative_url }}">T03 影長 600–2159 秒驗證</a></li><li data-result-item><a href="{{ '/results/t03-overview.html' | relative_url }}">T03 資料篩選驗證</a></li><li data-result-item><a href="{{ '/results/t03-trimmed-manufacturers.html' | relative_url }}">T03 去頭尾五家廠商驗證</a></li></ul></section>
<section class="catalog-group" data-result-group><h3>資料檢核與早期結果</h3><ul><li data-result-item><a href="{{ '/results/a06-brand-removed.html' | relative_url }}">A06 有刪除廠商車款</a></li><li data-result-item><a href="{{ '/results/a06-no-brand-removal.html' | relative_url }}">A06 無刪除廠商車款</a></li><li data-result-item><a href="{{ '/results/a07-brand-removed.html' | relative_url }}">A07 有刪除廠商車款</a></li><li data-result-item><a href="{{ '/results/a07-no-brand-removal.html' | relative_url }}">A07 無刪除廠商車款</a></li><li data-result-item><a href="{{ '/results/a08-no-brand-removal.html' | relative_url }}">A08 無刪除廠商車款</a></li><li data-result-item><a href="{{ '/results/b01-08-19-min-cluster.html' | relative_url }}">B01｜2008-2019 min_cluster_size 掃描</a></li><li data-result-item><a href="{{ '/results/b01-20-25-min-cluster.html' | relative_url }}">B01｜2020-2025 min_cluster_size 掃描</a></li><li data-result-item><a href="{{ '/results/db-filter.html' | relative_url }}">DB Filter 篩選結果</a></li><li data-result-item><a href="{{ '/results/historical-index.html' | relative_url }}">歷史結果索引</a></li><li data-result-item><a href="{{ '/results/non-english-check.html' | relative_url }}">非英文與特殊符號檢查</a></li><li data-result-item><a href="{{ '/results/pre-llm-a02.html' | relative_url }}">06.03 A02 LLM 前處理</a></li><li data-result-item><a href="{{ '/results/year-match-a02.html' | relative_url }}">06.13 A02 年份比對</a></li></ul></section>
</div>
