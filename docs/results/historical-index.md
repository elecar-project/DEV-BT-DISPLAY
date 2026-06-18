---
title: 歷史結果索引
description: Historical result files from the mother repository.
---

# 歷史結果索引

<div class="results-layout" markdown="1">
<aside class="results-sidebar" markdown="1">
## 結果導覽

<div class="result-nav-group" markdown="1">
<a href="{{ '/results.html' | relative_url }}">結果總覽</a>
<a href="{{ '/results/a08-no-brand-removal.html' | relative_url }}">A08 無刪除廠商車款</a>
<a href="{{ '/results/a07-no-brand-removal.html' | relative_url }}">A07 無刪除廠商車款</a>
<a href="{{ '/results/a07-brand-removed.html' | relative_url }}">A07 有刪除廠商車款</a>
<a href="{{ '/results/a06-no-brand-removal.html' | relative_url }}">A06 無刪除廠商車款</a>
<a href="{{ '/results/a06-brand-removed.html' | relative_url }}">A06 有刪除廠商車款</a>
</div>

<div class="result-nav-group" markdown="1">
<a href="{{ '/results/pre-llm-a02.html' | relative_url }}">06.03 A02 LLM 前處理</a>
<a href="{{ '/results/year-match-a02.html' | relative_url }}">06.13 A02 年份比對</a>
<a href="{{ '/results/db-filter.html' | relative_url }}">DB Filter 篩選結果</a>
<a href="{{ '/results/non-english-check.html' | relative_url }}">非英文與特殊符號檢查</a>
</div>

<div class="result-nav-group" markdown="1">
<a class="active" href="{{ '/results/historical-index.html' | relative_url }}">歷史結果索引</a>
</div>
</aside>

<section class="results-content" markdown="1">

本頁先列出母倉庫 `Result/` 中已盤點的歷史結果檔，方便之後逐步搬成獨立頁面。

## BERTopic 歷史報告

| 檔案 | 備註 |
| --- | --- |
| `Result/Result_05.26_01(Y).md` | 早期試跑 |
| `Result/Result_05.27_A01-有刪除廠商車款.md` | A01 有刪除版本 |
| `Result/Result_05.27_A01-沒有刪除廠商車款.md` | A01 無刪除版本 |
| `Result/Result_05.27_A02-有刪除廠商車款.md` | A02 有刪除版本 |
| `Result/Result_05.27_A02-沒有刪除廠商車款.md` | A02 無刪除版本 |
| `Result/Result_05.27_A03(Y錯處)-有刪除廠商車款.md` | A03 有刪除版本，需注意標註 |
| `Result/Result_05.27_A03(Y錯處)-無刪除廠商車款.md` | A03 無刪除版本，需注意標註 |
| `Result/Result_05.27_old01-有刪除廠商車款.md` | 舊版有刪除 |
| `Result/Result_05.27_old01-無刪除廠商車款.md` | 舊版無刪除 |
| `Result/Result_05.28_A01(Y)-有刪除廠商車款.md` | A01 有刪除 |
| `Result/Result_05.28_A01(Y)-無刪除廠商車款.md` | A01 無刪除 |
| `Result/Result_05.29_A01-有刪除廠商車款.md` | A01 有刪除 |
| `Result/Result_05.29_A01-無刪除廠商車款.md` | A01 無刪除 |
| `Result/Result_05.29_A02-有刪除廠商車款.md` | A02 有刪除 |
| `Result/Result_05.29_A02-沒有刪除廠商車款.md` | A02 無刪除 |
| `Result/Result_05.29_A04-有刪除廠商車款.md` | A04 有刪除 |
| `Result/Result_05.29_A04-無刪除廠商車款.md` | A04 無刪除 |
| `Result/Result_06.02_A01-有刪除廠商車款.md` | A01 有刪除 |
| `Result/Result_06.02_A01-無刪除廠商車款.md` | A01 無刪除 |

## 建議整理順序

1. 先保留 A08 作為主要探索頁。
2. 把 A07/A06 作為參數與品牌詞對照。
3. 歷史報告只搬「有助於解釋參數選擇」的版本。
4. 其餘報告保留在母倉庫，以免內部展示站過度膨脹。

</section>
</div>
