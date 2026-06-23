---
title: T03 去頭尾五家廠商驗證
description: 刪除頭尾各五家廠商後的 BERTopic 驗證結果。
---

# T03｜去頭尾 5 家廠商

<div class="result-detail-layout" markdown="1">
<aside class="result-settings" markdown="1">
## 實驗設定

### 資料與模型

<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>資料集</td><td><code>#運行BERTopic整理/#2.1 清理後輸入資料集（dataset）/02.2-驗證集3 刪除頭尾各五家廠商_(237)/R06.03_A02-pre_LLM(orig)-(237)_tok(para12-80)_dataset</code></td></tr>
<tr><td>可用句子</td><td>6,546</td></tr>
<tr><td>Embedding</td><td><code>all-MiniLM-L6-v2</code></td></tr>
<tr><td>UMAP</td><td>neighbors 10 / components 15 / min dist 0.0 / cosine / random state 42</td></tr>
<tr><td>HDBSCAN</td><td>cluster 50 / samples 5 / eom / eps 0.2 / euclidean</td></tr>
<tr><td>Topic reduction</td><td><code>nr_topics=auto</code></td></tr>
</tbody></table>
<table class="settings-table"><thead><tr><th>項目</th><th>設定</th></tr></thead><tbody>
<tr><td>停用詞</td><td><a href="{{ '/results/a05-8-orig-rev-human-stopwords.html' | relative_url }}">A05-8.4 human</a>，客製 170 個</td></tr>
<tr><td>LLM 設計</td><td>OpenRouter / <code>openai/gpt-5.5</code>，每 topic 50 次；未執行</td></tr>
<tr><td>代表句</td><td>6 句 / topic</td></tr>
</tbody></table>

### 來源資料夾

<p><code>Result/T03_Validation/06.24_T03-2(orig-237-new-tp-X)</code></p>
<p><a href="{{ '/results/t03-overview.html' | relative_url }}">回到 T03 資料篩選驗證總覽</a></p>
</aside>

<section markdown="1">
<div class="run-summary">
<div class="run-stat"><strong>7</strong><span>有效主題數</span></div>
<div class="run-stat"><strong>1.71%</strong><span>noise ratio</span></div>
<div class="run-stat"><strong>85.32%</strong><span>最大主題比例</span></div>
<div class="run-stat"><strong>0.409</strong><span>balance score</span></div>
</div>

## 結果摘要

本實驗移除廠商排序頭尾各 5 家後，使用 237 部影片檢查廠商樣本分布是否主導主題結構。離群比例很低，但主題 0 占 85.32%，因此判讀時需同時注意低離群與高度主題集中的取捨。

<aside class="table-note"><strong>LLM50 未執行：</strong>設定原預計使用 OpenRouter <code>openai/gpt-5.5</code> 對每個 topic 做 50 次命名驗證，但因未提供 <code>OPENROUTER_API_KEY</code> 而跳過。這不是 0 個穩定主題，而是沒有可判定的 LLM 驗證結果。</aside>

## 預設主題語意摘要

<p class="section-intro">以下列出 7 個有效主題的 Default c-TF-IDF 代表詞。</p>

<div class="table-scroll"><table class="semantic-table"><thead><tr><th>Topic</th><th>句數</th><th>Default 代表詞（前 10）</th></tr></thead><tbody>
<tr><td>0</td><td>5,586</td><td>car, new, vehicle, bmw, electric, design, driving, drive, charging, battery</td></tr>
<tr><td>1</td><td>276</td><td>volvo, xc90, new, car, s60, xc40, safety, new xc90, cars, design</td></tr>
<tr><td>2</td><td>208</td><td>nissan, leaf, aria, nissan leaf, new nissan, new, ev, intelligent, technology</td></tr>
<tr><td>3</td><td>141</td><td>polestar, car, electric, brand, volvo, china, electric car, cars, performance</td></tr>
<tr><td>4</td><td>109</td><td>mustang, mach, mustang mach, vehicle, ford, drive, electric, car, customers</td></tr>
<tr><td>5</td><td>64</td><td>rogue, kix, saw, nissan, midnight, universe, wars, crossover, star, edition</td></tr>
<tr><td>6</td><td>51</td><td>pacifica, minivan, chrysler, standard, new, segment, safety, warning, 2017</td></tr>
</tbody></table></div>

## 原始輸出

<table class="output-table"><thead><tr><th>檔案</th><th>用途</th></tr></thead><tbody>
<tr><td><a href="{{ '/assets/results/t03-trimmed-manufacturers/06.24_T03-2(orig-237-new-tp-X).md' | relative_url }}">實驗報告</a></td><td>原始實驗設定、量化結果與表徵摘要</td></tr>
<tr><td><a href="{{ '/assets/results/t03-trimmed-manufacturers/06.24_T03-2(orig-237-new-tp-X)_combined_representations.md' | relative_url }}">表徵對照報告</a></td><td>Default、KeyBERT、POS、MMR 表徵對照</td></tr>
<tr><td><a href="{{ '/assets/results/t03-trimmed-manufacturers/06.24_T03-2(orig-237-new-tp-X)_LLM.md' | relative_url }}">LLM 命名紀錄</a></td><td>LLM50 設定與跳過原因</td></tr>
<tr><td><a href="{{ '/assets/results/t03-trimmed-manufacturers/06.24_T03-2(orig-237-new-tp-X)_custom_stopwords_used.txt' | relative_url }}">實際使用停用詞</a></td><td>本次使用的客製停用詞</td></tr>
<tr><td><a href="{{ '/assets/results/t03-trimmed-manufacturers/artifacts/final_config.json' | relative_url }}">final_config.json</a></td><td>最終模型設定與指標</td></tr>
<tr><td><a href="{{ '/assets/results/t03-trimmed-manufacturers/artifacts/topic_info_default.csv' | relative_url }}">topic_info_default.csv</a></td><td>Default 主題資訊與代表文本</td></tr>
<tr><td><a href="{{ '/assets/results/t03-trimmed-manufacturers/artifacts/representative_docs.csv' | relative_url }}">representative_docs.csv</a></td><td>各主題代表文本</td></tr>
<tr><td><a href="{{ '/assets/results/t03-trimmed-manufacturers/run_06_24_T03_2_orig_237_new_tp_X.py' | relative_url }}">執行程式</a></td><td>本次 BERTopic 執行腳本</td></tr>
</tbody></table>
</section>
</div>
