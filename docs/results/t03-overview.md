---
title: T03 資料篩選驗證
description: 檢查影片長度與廠商篩選對 BERTopic 主題結構的影響。
---

# T03｜資料篩選驗證

T03 固定使用主程式的 UMAP、HDBSCAN 與 A05-8.4 human 停用詞設定，分別以影片長度和廠商範圍篩選資料，檢查資料篩選本身是否改變主題數、離群比例與主題集中程度。

<aside class="table-note"><strong>閱讀方式：</strong>影長 1-35 分鐘資料集保留 103 部影片；去頭尾 5 廠資料集保留 237 部影片。兩個結果應與完整 orig 語料一併比較，避免將資料量差異直接解讀為模型品質差異。</aside>

## 結果比較

<div class="table-scroll"><table class="m01-strategy-table"><thead><tr><th>篩選方式</th><th>資料意義</th><th>句數</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>LLM 狀態</th></tr></thead><tbody><tr><td><a href="{{ '/results/t03-duration-1-35m.html' | relative_url }}">8New-影長1~35m</a></td><td>僅保留長度 1 至 35 分鐘的影片。</td><td>5,016</td><td>23</td><td>26.54%</td><td>11.86%</td><td>未設定／停用</td></tr><tr><td><a href="{{ '/results/t03-trimmed-manufacturers.html' | relative_url }}">8New-去頭尾5廠</a></td><td>刪除排序頭尾各 5 家廠商後的資料。</td><td>6,546</td><td>7</td><td>1.71%</td><td>85.32%</td><td>未執行：未提供 API Key</td></tr></tbody></table></div>

<aside class="table-note"><strong>LLM 驗證狀態：</strong>影長實驗依設定停用 LLM 主題命名；去頭尾 5 廠實驗雖保留 LLM50 設定，但因未提供 <code>OPENROUTER_API_KEY</code> 而跳過。因此兩者皆不應被解讀為已有 LLM 命名穩定性結果。</aside>

## 個別結果

可進入 [8New-影長1~35m]({{ '/results/t03-duration-1-35m.html' | relative_url }}) 與 [8New-去頭尾5廠]({{ '/results/t03-trimmed-manufacturers.html' | relative_url }}) 查看完整設定、主題摘要與原始輸出。
