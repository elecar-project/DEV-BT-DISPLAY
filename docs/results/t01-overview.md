---
title: T01 刪除與替換驗證
description: 比較刪除與替換品牌／車款名稱對 BERTopic 主題結構的影響。
---

# T01｜刪除與替換品牌／車款驗證

T01 固定 M02 類型的單一 UMAP／HDBSCAN 設定，將同一研究問題分別用刪除品牌／車款詞（del）與替換為 Brand／Model（repl）處理，檢查資料處理方法是否影響主題數、離群比例與主題集中度。

<div class="table-note" role="note"><strong>閱讀方式：</strong>del 直接移除專有名詞；repl 保留語句中的詞類位置，但以 Brand／Model 取代特定名稱。兩者都應和原始語料的結果一併判讀，而非只比較單一 balance score。</div>

## 結果比較

<div class="table-scroll"><table class="m01-strategy-table"><thead><tr><th>處理方式</th><th>資料處理意義</th><th>句數</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th><th>LLM50</th></tr></thead><tbody><tr><td><a href="{{ '/results/t01-del.html' | relative_url }}">del</a></td><td>將品牌與車款名稱從資料集中刪除，檢查移除專有名詞後主題結構的變化。</td><td>10,945</td><td>14</td><td>30.27%</td><td>23.03%</td><td>0.647</td><td>未執行</td></tr><tr><td><a href="{{ '/results/t01-repl.html' | relative_url }}">repl</a></td><td>將品牌與車款名稱分別替換為 Brand／Model，保留詞類位置但降低特定品牌名稱的主導性。</td><td>10,978</td><td>29</td><td>32.02%</td><td>8.07%</td><td>0.838</td><td>未執行</td></tr></tbody></table></div>

<div class="table-note" role="note"><strong>LLM 驗證狀態：</strong>兩份實驗均因缺少 <code>OPENROUTER_API_KEY</code> 而未執行 LLM50 命名與穩定性驗證；網站保留該錯誤與原始輸出，避免將未執行誤讀為驗證失敗。</div>

## 個別結果

可進入 [T01-3｜刪除品牌／車款]({{ '/results/t01-del.html' | relative_url }}) 與 [T01-6｜替換品牌／車款]({{ '/results/t01-repl.html' | relative_url }}) 查看完整模型設定、主題摘要與輸出檔。
