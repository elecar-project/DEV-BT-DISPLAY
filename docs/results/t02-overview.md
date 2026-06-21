---
title: T02 年份切分驗證
description: 以 2018、2019、2021 為界的年份切分 BERTopic 驗證。
---

# T02｜年份切分驗證

T02 分別以 2018、2019、2021 為切點，將同一資料脈絡分成前後兩段，檢查不同年份劃分下的主題結構是否穩定。各組使用原始輸出記錄的單一模型設定，因此比較時需同時閱讀切分期間與 UMAP／HDBSCAN 參數。

<aside class="table-note"><strong>LLM 狀態：</strong>這六份原始輸出未保留可用的 LLM 命名驗證結果。網站保留既有 BERTopic 與非 LLM 表徵結果，並一律標示為「未設定／未執行」。</aside>

## 六種年份分段比較

<div class="table-scroll"><table class="m01-strategy-table"><thead><tr><th>節點</th><th>資料期間</th><th>句數</th><th>主題數</th><th>noise ratio</th><th>最大主題比例</th><th>balance score</th></tr></thead><tbody><tr><td><a href="{{ '/results/t02-2018-before.html' | relative_url }}">2018 前</a></td><td>2008-2017</td><td>8,193</td><td>5</td><td>5.59%</td><td>85.10%</td><td>0.387</td></tr><tr><td><a href="{{ '/results/t02-2018-after.html' | relative_url }}">2018 後</a></td><td>2018-2025</td><td>13,647</td><td>20</td><td>28.53%</td><td>35.55%</td><td>0.671</td></tr><tr><td><a href="{{ '/results/t02-2019-before.html' | relative_url }}">2019 前</a></td><td>2008-2018</td><td>10,208</td><td>9</td><td>31.50%</td><td>40.46%</td><td>0.547</td></tr><tr><td><a href="{{ '/results/t02-2019-after.html' | relative_url }}">2019 後</a></td><td>2019-2025</td><td>11,632</td><td>31</td><td>29.88%</td><td>11.61%</td><td>0.832</td></tr><tr><td><a href="{{ '/results/t02-2021-before.html' | relative_url }}">2021 前</a></td><td>2008-2020</td><td>14,566</td><td>19</td><td>28.99%</td><td>27.86%</td><td>0.704</td></tr><tr><td><a href="{{ '/results/t02-2021-after.html' | relative_url }}">2021 後</a></td><td>2021-2025</td><td>7,274</td><td>17</td><td>26.79%</td><td>23.99%</td><td>0.709</td></tr></tbody></table></div>

## 個別結果

流程圖中的六個 T02 綠色節點可直接進入對應結果頁。
