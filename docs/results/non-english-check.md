---
title: 非英文與特殊符號檢查
description: Non-English and special-character quality check for transcript data.
---

# 非英文與特殊符號檢查

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
<a class="active" href="{{ '/results/non-english-check.html' | relative_url }}">非英文與特殊符號檢查</a>
</div>
</aside>

<section class="results-content" markdown="1">

<div class="run-summary">
  <div class="run-stat"><strong>434</strong><span>檢查 TXT 檔案數</span></div>
  <div class="run-stat"><strong>33</strong><span>含非 ASCII / 特殊字元檔案</span></div>
  <div class="run-stat"><strong>1</strong><span>含外語 script 檔案</span></div>
  <div class="run-stat"><strong>0.0028%</strong><span>特殊字元占全部可見字元比例</span></div>
</div>

## 來源檔

| 項目 | 內容 |
| --- | --- |
| 母倉庫來源 | `Result/txt_non_english_analysis_05.24.md`、`Result/txt_non_english_analysis_05.24.csv` |
| 檢查資料夾 | `#TXT_DATA/05.24_txt-test_deleted(434)` |
| 總可見非空白字元 | 2,302,022 |

## 摘要

| 指標 | 數值 |
| --- | ---: |
| Files with any non-ASCII/special char | 33 / 434 |
| Non-ASCII/special chars in all visible text | 64 / 2,302,022 |
| Text volume of hit files | 348,658 / 2,302,022 |
| Files with foreign scripts only | 1 / 434 |
| Foreign-script chars in all visible text | 11 / 2,302,022 |

## 判讀

非英文與特殊符號比例很低，整體不太可能主導 BERTopic 結果。不過含外語 script 的檔案、
以及帶有特殊符號或歐洲語系字元的檔案，仍適合在正式模型前標記出來，避免後續解釋時誤判。

</section>
</div>
