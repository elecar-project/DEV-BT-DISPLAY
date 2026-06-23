---
title: T03 影長 1-35 分鐘驗證
description: 僅使用 1 至 35 分鐘影片的 BERTopic 驗證結果。
---

# T03｜影長 1-35 分鐘

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料與模型

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>#運行BERTopic整理/#2.1 清理後輸入資料集（dataset）/02.1-驗證集2 1-35 分鐘_(103)/R06.03_A02-pre_LLM(orig)-(103)_tok(para12-80)_dataset</code></td></tr>
<tr><td>可用句子</td><td>5,016</td></tr>
<tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code></td></tr>
<tr><td>UMAP</td><td>neighbors 10 / components 15 / min dist 0.0 / cosine</td></tr>
<tr><td>HDBSCAN</td><td>cluster 50 / samples 5 / eom / eps 0.2 / euclidean</td></tr>
<tr><td>Topic reduction</td><td><code>nr_topics=auto</code></td></tr>
</tbody></table>
<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>停用詞</td><td><a href="{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}">A05-8.4 human</a>，客製 170 個</td></tr>
<tr><td>LLM 設計</td><td>未設定／停用</td></tr>
<tr><td>代表句</td><td>6 句 / topic</td></tr>
</tbody></table>

### 來源資料夾

<p><code>Result/T03_Validation/06.24_T03-1(orig-103-new-tp-X)</code></p>
<p><a href="{{ '/results/t03-overview.html' | relative_url }}">回到 T03 資料篩選驗證總覽</a></p>
</aside>

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>23</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>26.54%</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>11.86%</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>1-35 分鐘</strong><span>影片長度篩選</span></div>
</div>

## 結果摘要

本實驗僅使用長度 1 至 35 分鐘的 103 部影片，檢查移除極短與極長影片後的主題結構。結果保留 23 個有效主題；最大主題占比為 11.86%，可用於和完整資料或其他篩選條件比較。

<aside class="table-note"><strong>LLM 狀態：</strong>本次設定明確停用 LLM 主題命名。<code>_LLM.md</code> 與 <code>_LLM.csv</code> 僅記錄該設定，並非 LLM 模型輸出。</aside>

## 預設主題語意摘要

<p class="section-intro">以下列出前 10 個有效主題的 Default c-TF-IDF 代表詞。</p>

<div class="table-scroll"><table class="semantic-table"><thead><tr><th>Topic</th><th>句數</th><th>Default 代表詞（前 10）</th></tr></thead><tbody>
<tr><td>0</td><td>595</td><td>kia, electric, ev, ev6, drive, range, power, battery</td></tr>
<tr><td>1</td><td>450</td><td>rear, interior, car, design, seats, also, seat, look</td></tr>
<tr><td>2</td><td>322</td><td>president, auto, vice, ladies, vice president, conference, press</td></tr>
<tr><td>3</td><td>309</td><td>bmw, class, mercedes, benz, new, series, car, design</td></tr>
<tr><td>4</td><td>211</td><td>toyota, corolla, pacifica, minivan, prius, new, car, rav4</td></tr>
<tr><td>5</td><td>170</td><td>karma, products, need, brand, designers, culture, future, change</td></tr>
<tr><td>6</td><td>157</td><td>assist, lane, parking, safety, collision, traffic, driver, road</td></tr>
<tr><td>7</td><td>134</td><td>mbux, display, screen, functions, center, navigation, control</td></tr>
<tr><td>8</td><td>133</td><td>charging, charge, route, mercedes, charger, home, stations, minutes</td></tr>
<tr><td>9</td><td>123</td><td>ioniq, hyundai, mobility, future, charging, xrt, new, vehicle</td></tr>
</tbody></table></div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody>
<tr><td><a href="{{ '/assets/results/t03-duration-1-35m/06.24_T03-1(orig-103-new-tp-X).md' | relative_url }}">實驗報告</a></td><td>原始實驗設定、量化結果與表徵摘要</td></tr>
<tr><td><a href="{{ '/assets/results/t03-duration-1-35m/06.24_T03-1(orig-103-new-tp-X)_combined_representations.md' | relative_url }}">表徵對照報告</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr>
<tr><td><a href="{{ '/assets/results/t03-duration-1-35m/06.24_T03-1(orig-103-new-tp-X)_custom_stopwords_used.txt' | relative_url }}">實際使用停用詞</a></td><td>本次使用的客製停用詞</td></tr>
<tr><td><a href="{{ '/assets/results/t03-duration-1-35m/artifacts/final_config.json' | relative_url }}">final_config.json</a></td><td>最終模型設定與指標</td></tr>
<tr><td><a href="{{ '/assets/results/t03-duration-1-35m/artifacts/topic_info_default.csv' | relative_url }}">topic_info_default.csv</a></td><td>Default 主題資訊與代表文本</td></tr>
<tr><td><a href="{{ '/assets/results/t03-duration-1-35m/artifacts/representative_docs.csv' | relative_url }}">representative_docs.csv</a></td><td>各主題代表文本</td></tr>
<tr><td><a href="{{ '/assets/results/t03-duration-1-35m/run_06_24_T03_1_orig_103_new_tp_X.py' | relative_url }}">執行程式</a></td><td>本次 BERTopic 執行腳本</td></tr>
</tbody></table>
</section>
</div>
