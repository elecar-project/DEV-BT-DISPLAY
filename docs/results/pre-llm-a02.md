---
title: 06.03 A02 LLM 前處理
description: OpenRouter LLM transcript cleaning run for 434 records.
---

# 06.03 A02 LLM 前處理

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
<a class="active" href="{{ '/results/pre-llm-a02.html' | relative_url }}">06.03 A02 LLM 前處理</a>
<a href="{{ '/results/year-match-a02.html' | relative_url }}">06.13 A02 年份比對</a>
<a href="{{ '/results/db-filter.html' | relative_url }}">DB Filter 篩選結果</a>
<a href="{{ '/results/non-english-check.html' | relative_url }}">非英文與特殊符號檢查</a>
</div>
</aside>

<section class="results-content" markdown="1">

<div class="run-summary">
  <div class="run-stat"><strong>434</strong><span>清理成功筆數</span></div>
  <div class="run-stat"><strong>0</strong><span>部分失敗筆數</span></div>
  <div class="run-stat"><strong>32.39s</strong><span>運行時長</span></div>
  <div class="run-stat"><strong>3.093731</strong><span>OpenRouter cost 加總</span></div>
</div>

## Run 資料

| 項目 | 內容 |
| --- | --- |
| 母倉庫來源 | `Result/06.03_A02/R06.03_A02-pre-LLM-result.md` |
| 輸入資料 | `#TXT_DATA/05.24_txt-test_deleted_dataset` |
| 資料型態 | Hugging Face Dataset / Arrow |
| 欄位 | `title`、`transcript` |
| 串接模型 | `openai/gpt-5.4-mini` |
| 開始時間 | 2026-06-02 20:24:11 UTC |
| 結束時間 | 2026-06-02 20:24:44 UTC |

## 處理統計摘要

| 項目 | 數值 |
| --- | ---: |
| Prompt tokens | 654,261 |
| Completion tokens | 578,721 |
| Total tokens | 1,232,982 |
| 標點增加或修正總數 | 30,543 |
| 重複句子處理總數 | 210 |
| 廠商/模型刪除總數 | 9,685 |
| 平均 LLM 刪修比例 | 0.0076 |

## 後續用途

這個 run 主要用於修補 Whisper ASR 逐字稿的標點、重複片段與明顯雜訊。
品牌與車款在 LLM 階段先保留，後續再用 deterministic 詞表產生刪除版或替換版，
方便比較 BERTopic embedding 是否受到品牌詞影響。

</section>
</div>
